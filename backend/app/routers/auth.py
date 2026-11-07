from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password,create_access_token,hash_password,get_current_user
from app.models.user import User,UserRole
from app.schemas.user import UserCreate,UserOut,Token,LoginRequest

router=APIRouter(prefix="/api/auth",tags=["auth"])

@router.post("/register",response_model=UserOut,status_code=201)
def register(payload:UserCreate,db:Session=Depends(get_db)):
    existing=db.query(User).filter(User.email==payload.email).first()
    if existing:
        raise HTTPException(400,"Email already registered")
    user=User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        role=payload.role,
        workspace_id=payload.workspace_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login",response_model=Token)
def login(payload:LoginRequest,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==payload.email).first()
    if not user or not verify_password(payload.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    token=create_access_token({"sub":str(user.id)})
    return Token(access_token=token,token_type="bearer",user=UserOut.model_validate(user))

@router.get("/me",response_model=UserOut)
def me(current_user:User=Depends(get_current_user)):
    return current_user

