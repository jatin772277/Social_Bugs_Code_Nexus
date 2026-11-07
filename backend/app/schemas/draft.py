from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime
from app.models.draft import DraftStatus,FindingSeverity,FindingStatus

class DraftCreate(BaseModel):
    title:str
    content:str
    channel:Optional[str]=None
    purpose:Optional[str]=None
    workspace_id:int

class DraftOut(BaseModel):
    id:int
    title:str
    content:str
    channel:Optional[str]
    purpose:Optional[str]
    status:DraftStatus
    creator_id:int
    workspace_id:int
    created_at:datetime
    updated_at:Optional[datetime]
    class Config:
        from_attributes=True

class FindingOut(BaseModel):
    id:int
    draft_id:int
    category:str
    severity:FindingSeverity
    location_start:Optional[int]
    location_end:Optional[int]
    quoted_content:str
    reason:str
    cited_clause_id:Optional[int]
    cited_clause_text:Optional[str]
    suggested_fix:Optional[str]
    status:FindingStatus
    dispute_reason:Optional[str]
    finding_source:str
    created_at:datetime
    class Config:
        from_attributes=True

class FindingAction(BaseModel):
    action:str
    dispute_reason:Optional[str]=None

class CommentCreate(BaseModel):
    text:str

class CommentOut(BaseModel):
    id:int
    draft_id:int
    author_id:int
    text:str
    created_at:datetime
    class Config:
        from_attributes=True

class ApprovalCreate(BaseModel):
    decision:str
    note:Optional[str]=None

class ApprovalOut(BaseModel):
    id:int
    draft_id:int
    approver_id:int
    decision:str
    note:Optional[str]
    created_at:datetime
    class Config:
        from_attributes=True

class RevisionOut(BaseModel):
    id:int
    draft_id:int
    revision_number:int
    content:str
    author_id:Optional[int]
    change_summary:Optional[str]
    created_at:datetime
    class Config:
        from_attributes=True

class AIDisclosureLogOut(BaseModel):
    id:int
    draft_id:int
    service_name:str
    masked_terms_count:int
    masked_preview:Optional[str]
    dispatched_at:datetime
    class Config:
        from_attributes=True

class DraftWithFindings(DraftOut):
    findings:List[FindingOut]=[]
    comments:List[CommentOut]=[]
    approvals:List[ApprovalOut]=[]
    revisions:List[RevisionOut]=[]
    disclosure_logs:List[AIDisclosureLogOut]=[]
