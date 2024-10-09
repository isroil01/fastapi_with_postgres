from jose import JWTError,jwt
from datetime import datetime,timedelta
from model.user import TokenData,Token,User,UserType
from config.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# secret key
SECRET_KEY = 'user_activity'
ALGORITHM = 'HS256'
ACCESS_TOKEN_MINUTES = 30

def create_access_token(data:dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_MINUTES)
    to_encode.update({'exp': expire})
    
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_access_token (token:str,credentials_exceiptions):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithm=[ALGORITHM])
        id:str = payload.get('user_id')
    
        if id is None:
           raise credentials_exceiptions
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exceiptions
    return token_data
    
def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='not validate credential',headers={'WWW-Authenticate': 'Bearer'})        
    tokens = verify_access_token(token,credential_exception)
    user = db.query(User).filter(User.id == tokens.id).first()
    return user