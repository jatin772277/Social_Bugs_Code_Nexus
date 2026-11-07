from fastapi import APIRouter,Depends,HTTPException,UploadFile,File,Form
from sqlalchemy.orm import Session
from typing import List,Optional
from app.core.database import get_db
from app.core.security import get_current_user,require_roles
from app.models.user import User,UserRole
from app.models.workspace import Workspace,Guideline,GuidelineClause,TerminologyEntry,ApprovedFact
from app.schemas.workspace import WorkspaceCreate,WorkspaceOut,GuidelineOut,TerminologyCreate,TerminologyOut,FactCreate,FactOut
from app.services.rules_engine import split_into_clauses,infer_category
import os,shutil

router=APIRouter(prefix="/api/workspaces",tags=["workspaces"])

@router.post("",response_model=WorkspaceOut,status_code=201)
def create_workspace(payload:WorkspaceCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    ws=Workspace(name=payload.name,description=payload.description)
    db.add(ws)
    db.commit()
    db.refresh(ws)
    current_user.workspace_id=ws.id
    db.commit()
    return ws

@router.get("",response_model=List[WorkspaceOut])
def list_workspaces(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return db.query(Workspace).all()

@router.get("/{workspace_id}",response_model=WorkspaceOut)
def get_workspace(workspace_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    ws=db.query(Workspace).filter(Workspace.id==workspace_id).first()
    if not ws:
        raise HTTPException(404,"Workspace not found")
    return ws

@router.post("/{workspace_id}/guidelines",response_model=GuidelineOut,status_code=201)
def import_guideline(
    workspace_id:int,
    title:str=Form(...),
    text_content:Optional[str]=Form(None),
    file:Optional[UploadFile]=File(None),
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    ws=db.query(Workspace).filter(Workspace.id==workspace_id).first()
    if not ws:
        raise HTTPException(404,"Workspace not found")
    raw=""
    fname=None
    if file:
        fname=file.filename
        content=file.file.read()
        if fname.endswith('.txt'):
            raw=content.decode('utf-8','ignore')
        else:
            raw=content.decode('utf-8','ignore')
    elif text_content:
        raw=text_content
    if not raw.strip():
        raise HTTPException(400,"No content provided")
    g=Guideline(workspace_id=workspace_id,title=title,source_filename=fname,raw_text=raw)
    db.add(g)
    db.commit()
    db.refresh(g)
    clauses=split_into_clauses(raw)
    for num,text in clauses:
        c=GuidelineClause(guideline_id=g.id,clause_number=num,text=text,category=infer_category(text))
        db.add(c)
    db.commit()
    db.refresh(g)
    return g

@router.get("/{workspace_id}/guidelines",response_model=List[GuidelineOut])
def list_guidelines(workspace_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return db.query(Guideline).filter(Guideline.workspace_id==workspace_id).all()

@router.delete("/{workspace_id}/guidelines/{guideline_id}",status_code=204)
def delete_guideline(workspace_id:int,guideline_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    g=db.query(Guideline).filter(Guideline.id==guideline_id,Guideline.workspace_id==workspace_id).first()
    if not g:
        raise HTTPException(404,"Guideline not found")
    db.delete(g)
    db.commit()

@router.post("/{workspace_id}/terminology",response_model=TerminologyOut,status_code=201)
def add_terminology(workspace_id:int,payload:TerminologyCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    ws=db.query(Workspace).filter(Workspace.id==workspace_id).first()
    if not ws:
        raise HTTPException(404,"Workspace not found")
    entry=TerminologyEntry(workspace_id=workspace_id,**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@router.get("/{workspace_id}/terminology",response_model=List[TerminologyOut])
def list_terminology(workspace_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return db.query(TerminologyEntry).filter(TerminologyEntry.workspace_id==workspace_id).all()

@router.delete("/{workspace_id}/terminology/{entry_id}",status_code=204)
def delete_terminology(workspace_id:int,entry_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    entry=db.query(TerminologyEntry).filter(TerminologyEntry.id==entry_id,TerminologyEntry.workspace_id==workspace_id).first()
    if not entry:
        raise HTTPException(404,"Not found")
    db.delete(entry)
    db.commit()

@router.post("/{workspace_id}/facts",response_model=FactOut,status_code=201)
def add_fact(workspace_id:int,payload:FactCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    ws=db.query(Workspace).filter(Workspace.id==workspace_id).first()
    if not ws:
        raise HTTPException(404,"Workspace not found")
    fact=ApprovedFact(workspace_id=workspace_id,**payload.model_dump())
    db.add(fact)
    db.commit()
    db.refresh(fact)
    return fact

@router.get("/{workspace_id}/facts",response_model=List[FactOut])
def list_facts(workspace_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return db.query(ApprovedFact).filter(ApprovedFact.workspace_id==workspace_id).all()

