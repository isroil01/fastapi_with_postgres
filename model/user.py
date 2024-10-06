from pydantic import BaseModel,EmailStr
from config.database import Base
from datetime import datetime
from sqlalchemy import Column,Integer,String,TIMESTAMP


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String,nullable=False,unique = True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    
class UserType(BaseModel):
    email:EmailStr    
    password:str
    
class UserResponse(BaseModel):
    email:EmailStr
    id:int 
    created_at:datetime
    class Config:
        orm_mode=True
       