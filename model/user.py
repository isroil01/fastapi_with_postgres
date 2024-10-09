from pydantic import BaseModel,EmailStr
from config.database import Base
from datetime import datetime
from sqlalchemy import Column,Integer,String,TIMESTAMP,func
from typing import Optional


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String,nullable=False,unique = True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    
class UserType(BaseModel):
    id:int
    email:EmailStr    
    password:str
    
class UserResponse(BaseModel):
    email:EmailStr
    id:int 
    created_at:datetime
    class Config:
        orm_mode=True
        
        
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id:Optional[str] = None
       