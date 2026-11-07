from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole

class UserCreate(BaseModel):
    email:EmailStr
    full_name:str
    password:str
    role:UserRole=UserRole.creator
    workspace_id:Optional[int]=None

class UserOut(BaseModel):
    id:int
    email:str
    full_name:str
    role:UserRole
    workspace_id:Optional[int]
    is_active:bool
    created_at:datetime
    class Config:
        from_attributes=True

class Token(BaseModel):
    access_token:str
    token_type:str
    user:UserOut

class LoginRequest(BaseModel):
    email:str
    password:str

