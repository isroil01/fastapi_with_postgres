from fastapi import FastAPI
from routes.activity import router 

app = FastAPI()

# activity
app.include_router(router)
# users
