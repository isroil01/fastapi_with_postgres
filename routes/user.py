from fastapi import APIRouter,status,HTTPException,Response,Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Optional
from config.database import get_db
from sqlalchemy.orm import Session
from model.user import User,UserType,UserResponse
from utils import hash_password,verify
from oauth import create_access_token

router  = APIRouter(tags=['User'])

# login
@router.post('/login')
def login(user:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    
    user_data = db.query(User).filter(User.email == user.username).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='given email is not registered')
    if not verify(user.password, user_data.password) :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Credantial')
    access_token = create_access_token(data={'user_id':user_data.id})
    return {'message':access_token,"token_type": 'bearer'}

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