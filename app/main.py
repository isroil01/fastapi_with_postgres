from fastapi import FastAPI
from routes.activity import router 
from routes.user import router as userRouter
from model import list 
from config.database import engine 

list.Base.metadata.create_all(bind=engine)

app = FastAPI()

# activity
app.include_router(router)
app.include_router(userRouter)
# users
