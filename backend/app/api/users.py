from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.user import User, UserUpdate
from ..services.user_service import UserService
from ..dependencies import get_current_active_user

router = APIRouter()

@router.get("/profile", response_model=User)
async def get_profile(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/profile", response_model=User)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    updated_user = user_service.update_user(current_user.id, user_update)
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return updated_user