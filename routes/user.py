from fastapi import APIRouter,status,HTTPException,Response,Depends
from typing import Optional
from config.database import get_db
from sqlalchemy.orm import Session
from model.user import User,UserType,UserResponse
from utils import hash_password,verify


router  = APIRouter()

# login
@router.post('/login')
def login(user:UserType,db:Session = Depends(get_db)):
    user_data = db.query(User).filter(User.email == user.email).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='given email is not registered')
    if not verify(user.password, user_data.password) :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalid Credantial')
    return {'message':''}

# signup
@router.post('/signup',status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def register_user(user:UserType,db:Session = Depends(get_db)):
    
    # hash password
    hashed_pwd = hash_password(user.password)
    user.password = hashed_pwd
    
    created_user = User(**user.dict())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user

@router.get('/users/{id}',response_model= UserResponse)
def get_users (id:int,db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='for the gicen id user not found')
    return user