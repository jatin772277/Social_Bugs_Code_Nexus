from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime

class WorkspaceCreate(BaseModel):
    name:str
    description:Optional[str]=None

class WorkspaceOut(BaseModel):
    id:int
    name:str
    description:Optional[str]
    created_at:datetime
    class Config:
        from_attributes=True

class GuidelineClauseOut(BaseModel):
    id:int
    clause_number:str
    text:str
    category:Optional[str]
    dispute_count:int
    dismissed_count:int
    violation_count:int
    class Config:
        from_attributes=True

class GuidelineOut(BaseModel):
    id:int
    title:str
    source_filename:Optional[str]
    created_at:datetime
    clauses:List[GuidelineClauseOut]=[]
    class Config:
        from_attributes=True

class TerminologyCreate(BaseModel):
    term:str
    entry_type:str
    preferred_alternative:Optional[str]=None
    reason:Optional[str]=None

class TerminologyOut(BaseModel):
    id:int
    term:str
    entry_type:str
    preferred_alternative:Optional[str]
    reason:Optional[str]
    class Config:
        from_attributes=True

class FactCreate(BaseModel):
    claim:str
    source:Optional[str]=None
    expires_at:Optional[datetime]=None

class FactOut(BaseModel):
    id:int
    claim:str
    source:Optional[str]
    expires_at:Optional[datetime]
    created_at:datetime
    class Config:
        from_attributes=True

