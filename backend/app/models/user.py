from sqlalchemy import Column,Integer,String,DateTime,Boolean,Text,Enum as SAEnum,ForeignKey,JSON,Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class UserRole(str,enum.Enum):
    creator="creator"
    manager="manager"
    reviewer="reviewer"
    admin="admin"

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True,index=True,nullable=False)
    full_name=Column(String,nullable=False)
    hashed_password=Column(String,nullable=False)
    role=Column(SAEnum(UserRole),default=UserRole.creator,nullable=False)
    workspace_id=Column(Integer,ForeignKey("workspaces.id"),nullable=True)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    workspace=relationship("Workspace",back_populates="members")
    drafts=relationship("Draft",back_populates="creator",foreign_keys="Draft.creator_id")
    comments=relationship("Comment",back_populates="author")

