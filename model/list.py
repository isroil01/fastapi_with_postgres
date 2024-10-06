from pydantic import BaseModel
from config.database import Base
from sqlalchemy import Column,Integer,String

class Activity(BaseModel):
    title:str
    description:str
    time:str
    type:str
    state:str
    
class Activities(Base):
    __tablename__ = 'activity'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    state = Column(String, nullable=False)
    
