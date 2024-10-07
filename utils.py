from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

# hash password
def hash_password(pwd:str):
    return pwd_context.hash(pwd)

# verify hash
def verify(pwd:str,hashed_pwd:str):
    return pwd_context.verify(pwd,hashed_pwd)