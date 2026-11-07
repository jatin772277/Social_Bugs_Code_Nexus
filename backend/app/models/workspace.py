from sqlalchemy import Column,Integer,String,DateTime,Text,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Workspace(Base):
    __tablename__="workspaces"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    description=Column(Text,nullable=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    members=relationship("User",back_populates="workspace")
    guidelines=relationship("Guideline",back_populates="workspace")
    terminology=relationship("TerminologyEntry",back_populates="workspace")
    approved_facts=relationship("ApprovedFact",back_populates="workspace")
    drafts=relationship("Draft",back_populates="workspace")

class Guideline(Base):
    __tablename__="guidelines"
    id=Column(Integer,primary_key=True,index=True)
    workspace_id=Column(Integer,ForeignKey("workspaces.id"),nullable=False)
    title=Column(String,nullable=False)
    source_filename=Column(String,nullable=True)
    raw_text=Column(Text,nullable=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    workspace=relationship("Workspace",back_populates="guidelines")
    clauses=relationship("GuidelineClause",back_populates="guideline",cascade="all,delete-orphan")

class GuidelineClause(Base):
    __tablename__="guideline_clauses"
    id=Column(Integer,primary_key=True,index=True)
    guideline_id=Column(Integer,ForeignKey("guidelines.id"),nullable=False)
    clause_number=Column(String,nullable=False)
    text=Column(Text,nullable=False)
    category=Column(String,nullable=True)
    dispute_count=Column(Integer,default=0)
    dismissed_count=Column(Integer,default=0)
    violation_count=Column(Integer,default=0)
    guideline=relationship("Guideline",back_populates="clauses")

class TerminologyEntry(Base):
    __tablename__="terminology"
    id=Column(Integer,primary_key=True,index=True)
    workspace_id=Column(Integer,ForeignKey("workspaces.id"),nullable=False)
    term=Column(String,nullable=False)
    entry_type=Column(String,nullable=False)
    preferred_alternative=Column(String,nullable=True)
    reason=Column(Text,nullable=True)
    workspace=relationship("Workspace",back_populates="terminology")

class ApprovedFact(Base):
    __tablename__="approved_facts"
    id=Column(Integer,primary_key=True,index=True)
    workspace_id=Column(Integer,ForeignKey("workspaces.id"),nullable=False)
    claim=Column(Text,nullable=False)
    source=Column(String,nullable=True)
    expires_at=Column(DateTime(timezone=True),nullable=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    workspace=relationship("Workspace",back_populates="approved_facts")

