from datetime import datetime,timedelta,timezone
from typing import Optional
from jose import JWTError,jwt
import bcrypt
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.database import get_db

settings=get_settings()
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def verify_password(plain:str,hashed:str)->bool:
    try:
        return bcrypt.checkpw(plain.encode('utf-8')[:72],hashed.encode('utf-8'))
    except Exception:
        return False

def hash_password(password:str)->str:
    salt=bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8')[:72],salt).decode('utf-8')

def create_access_token(data:dict,expires_delta:Optional[timedelta]=None):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+(expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.secret_key,algorithm=settings.algorithm)

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    from app.models.user import User
    creds_exc=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    try:
        payload=jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        user_id:str=payload.get("sub")
        if user_id is None:
            raise creds_exc
    except JWTError:
        raise creds_exc
    user=db.query(User).filter(User.id==int(user_id)).first()
    if user is None:
        raise creds_exc
    return user

def require_roles(*roles):
    def checker(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403,detail="Insufficient permissions")
        return current_user
    return checker
