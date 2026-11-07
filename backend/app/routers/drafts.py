from fastapi import APIRouter,Depends,HTTPException,BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User,UserRole
from app.models.draft import Draft,Finding,Comment,Approval,DraftStatus,FindingStatus
from app.schemas.draft import DraftCreate,DraftOut,DraftWithFindings,FindingOut,FindingAction,CommentCreate,CommentOut,ApprovalCreate,ApprovalOut
from app.services.review_service import run_full_review,get_insights

router=APIRouter(prefix="/api/drafts",tags=["drafts"])

@router.post("",response_model=DraftOut,status_code=201)
def create_draft(payload:DraftCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    draft=Draft(
        workspace_id=payload.workspace_id,
        creator_id=current_user.id,
        title=payload.title,
        content=payload.content,
        channel=payload.channel,
        purpose=payload.purpose,
        status=DraftStatus.draft,
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)
    return draft

@router.get("",response_model=List[DraftOut])
def list_drafts(workspace_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    q=db.query(Draft).filter(Draft.workspace_id==workspace_id)
    if current_user.role==UserRole.creator:
        q=q.filter(Draft.creator_id==current_user.id)
    return q.order_by(Draft.created_at.desc()).all()

@router.get("/{draft_id}",response_model=DraftWithFindings)
def get_draft(draft_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    draft=db.query(Draft).filter(Draft.id==draft_id).first()
    if not draft:
        raise HTTPException(404,"Draft not found")
    return draft

@router.post("/{draft_id}/review",response_model=List[FindingOut])
def trigger_review(draft_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    draft=db.query(Draft).filter(Draft.id==draft_id).first()
    if not draft:
        raise HTTPException(404,"Draft not found")
    draft.status=DraftStatus.under_review
    db.commit()
    findings=run_full_review(draft,db)
    draft.status=DraftStatus.pending_approval
    db.commit()
    return findings

@router.patch("/{draft_id}/findings/{finding_id}",response_model=FindingOut)
def act_on_finding(draft_id:int,finding_id:int,payload:FindingAction,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    finding=db.query(Finding).filter(Finding.id==finding_id,Finding.draft_id==draft_id).first()
    if not finding:
        raise HTTPException(404,"Finding not found")
    action=payload.action.lower()
    if action not in ('accept','dispute','dismiss'):
        raise HTTPException(400,"action must be accept, dispute, or dismiss")
    if action=='accept':
        finding.status=FindingStatus.accepted
    elif action=='dispute':
        finding.status=FindingStatus.disputed
        finding.dispute_reason=payload.dispute_reason
        if finding.cited_clause_id:
            from app.models.workspace import GuidelineClause
            cl=db.query(GuidelineClause).filter(GuidelineClause.id==finding.cited_clause_id).first()
            if cl:
                cl.dispute_count=(cl.dispute_count or 0)+1
    elif action=='dismiss':
        finding.status=FindingStatus.dismissed
        if finding.cited_clause_id:
            from app.models.workspace import GuidelineClause
            cl=db.query(GuidelineClause).filter(GuidelineClause.id==finding.cited_clause_id).first()
            if cl:
                cl.dismissed_count=(cl.dismissed_count or 0)+1
    db.commit()
    db.refresh(finding)
    return finding

@router.post("/{draft_id}/comments",response_model=CommentOut,status_code=201)
def add_comment(draft_id:int,payload:CommentCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    draft=db.query(Draft).filter(Draft.id==draft_id).first()
    if not draft:
        raise HTTPException(404,"Draft not found")
    c=Comment(draft_id=draft_id,author_id=current_user.id,text=payload.text)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.post("/{draft_id}/approve",response_model=ApprovalOut,status_code=201)
def approve_draft(draft_id:int,payload:ApprovalCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    if current_user.role not in (UserRole.manager,UserRole.reviewer,UserRole.admin):
        raise HTTPException(403,"Only managers, reviewers or admins can approve")
    draft=db.query(Draft).filter(Draft.id==draft_id).first()
    if not draft:
        raise HTTPException(404,"Draft not found")
    approval=Approval(draft_id=draft_id,approver_id=current_user.id,decision=payload.decision,note=payload.note)
    db.add(approval)
    if payload.decision=='approved':
        draft.status=DraftStatus.approved
    elif payload.decision=='rejected':
        draft.status=DraftStatus.rejected
    db.commit()
    db.refresh(approval)
    return approval

@router.delete("/{draft_id}",status_code=204)
def delete_draft(draft_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    draft=db.query(Draft).filter(Draft.id==draft_id).first()
    if not draft:
        raise HTTPException(404,"Draft not found")
    if draft.creator_id!=current_user.id and current_user.role not in (UserRole.admin,UserRole.manager):
        raise HTTPException(403,"Forbidden")
    db.delete(draft)
    db.commit()

