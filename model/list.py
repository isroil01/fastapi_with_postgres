from pydantic import BaseModel

class Activity(BaseModel):
    title:str
    description:str
    id:int
    time:str
    type:str
    state:str