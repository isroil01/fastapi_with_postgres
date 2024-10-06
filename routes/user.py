from fastapi import APIRouter,status,HTTPException,Response,Depends
from typing import Optional
from config.database import get_db
from sqlalchemy.orm import Session
from model.user import User,UserType,UserResponse


router  = APIRouter()

# signup
@router.post('/signup',status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def register_user(user:UserType,db:Session = Depends(get_db)):
    created_user = User(**user.dict())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user