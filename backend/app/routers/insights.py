from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.review_service import get_insights

router=APIRouter(prefix="/api/insights",tags=["insights"])

@router.get("/{workspace_id}")
def workspace_insights(workspace_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return get_insights(workspace_id,db)

