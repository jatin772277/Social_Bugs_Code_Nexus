from sqlalchemy import Column,Integer,String,DateTime,Text,ForeignKey,Enum as SAEnum,JSON,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class DraftStatus(str,enum.Enum):
    draft="draft"
    under_review="under_review"
    pending_approval="pending_approval"
    approved="approved"
    rejected="rejected"

class FindingSeverity(str,enum.Enum):
    critical="critical"
    major="major"
    minor="minor"
    info="info"

class FindingStatus(str,enum.Enum):
    open="open"
    accepted="accepted"
    disputed="disputed"
    dismissed="dismissed"

class Draft(Base):
    __tablename__="drafts"
    id=Column(Integer,primary_key=True,index=True)
    workspace_id=Column(Integer,ForeignKey("workspaces.id"),nullable=False)
    creator_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    title=Column(String,nullable=False)
    content=Column(Text,nullable=False)
    channel=Column(String,nullable=True)
    purpose=Column(Text,nullable=True)
    status=Column(SAEnum(DraftStatus),default=DraftStatus.draft)
    file_path=Column(String,nullable=True)
    file_type=Column(String,nullable=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    updated_at=Column(DateTime(timezone=True),onupdate=func.now())
    workspace=relationship("Workspace",back_populates="drafts")
    creator=relationship("User",back_populates="drafts",foreign_keys=[creator_id])
    findings=relationship("Finding",back_populates="draft",cascade="all,delete-orphan")
    comments=relationship("Comment",back_populates="draft",cascade="all,delete-orphan")
    approvals=relationship("Approval",back_populates="draft",cascade="all,delete-orphan")
    revisions=relationship("Revision",back_populates="draft",cascade="all,delete-orphan")
    disclosure_logs=relationship("AIDisclosureLog",back_populates="draft",cascade="all,delete-orphan")

class Finding(Base):
    __tablename__="findings"
    id=Column(Integer,primary_key=True,index=True)
    draft_id=Column(Integer,ForeignKey("drafts.id"),nullable=False)
    category=Column(String,nullable=False)
    severity=Column(SAEnum(FindingSeverity),nullable=False)
    location_start=Column(Integer,nullable=True)
    location_end=Column(Integer,nullable=True)
    quoted_content=Column(Text,nullable=False)
    reason=Column(Text,nullable=False)
    cited_clause_id=Column(Integer,ForeignKey("guideline_clauses.id"),nullable=True)
    cited_clause_text=Column(Text,nullable=True)
    cited_fact_id=Column(Integer,ForeignKey("approved_facts.id"),nullable=True)
    suggested_fix=Column(Text,nullable=True)
    status=Column(SAEnum(FindingStatus),default=FindingStatus.open)
    dispute_reason=Column(Text,nullable=True)
    finding_source=Column(String,default="ai")
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    draft=relationship("Draft",back_populates="findings")
    cited_clause=relationship("GuidelineClause")

class Comment(Base):
    __tablename__="comments"
    id=Column(Integer,primary_key=True,index=True)
    draft_id=Column(Integer,ForeignKey("drafts.id"),nullable=False)
    author_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    text=Column(Text,nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    draft=relationship("Draft",back_populates="comments")
    author=relationship("User",back_populates="comments")

class Approval(Base):
    __tablename__="approvals"
    id=Column(Integer,primary_key=True,index=True)
    draft_id=Column(Integer,ForeignKey("drafts.id"),nullable=False)
    approver_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    decision=Column(String,nullable=False)
    note=Column(Text,nullable=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    draft=relationship("Draft",back_populates="approvals")
    approver=relationship("User")

class Revision(Base):
    __tablename__="revisions"
    id=Column(Integer,primary_key=True,index=True)
    draft_id=Column(Integer,ForeignKey("drafts.id"),nullable=False)
    revision_number=Column(Integer,default=1,nullable=False)
    content=Column(Text,nullable=False)
    author_id=Column(Integer,ForeignKey("users.id"),nullable=True)
    change_summary=Column(String,nullable=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    draft=relationship("Draft",back_populates="revisions")
    author=relationship("User")

class AIDisclosureLog(Base):
    __tablename__="ai_disclosure_logs"
    id=Column(Integer,primary_key=True,index=True)
    draft_id=Column(Integer,ForeignKey("drafts.id"),nullable=False)
    service_name=Column(String,nullable=False)
    masked_terms_count=Column(Integer,default=0)
    masked_preview=Column(Text,nullable=True)
    dispatched_at=Column(DateTime(timezone=True),server_default=func.now())
    draft=relationship("Draft",back_populates="disclosure_logs")
