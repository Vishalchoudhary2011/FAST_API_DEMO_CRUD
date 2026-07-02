from fastapi import FastAPI,HTTPException, Depends
from jose import jwt 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

app = FastAPI()

#JWT config
SECREAT_KEY = "myscreat"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 30

#Password hashing set up 
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# Oauth set up
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

#Dummy fake user DB 
fake_user_db = {
    "admin":{
        "username":"admin",
        "hashed_password" : pwd_context.hash("12345")
    }
}

# Hash password 
def hash_password (password:str):
    return pwd_context.hash(password)

# Verify password 
def verify_password(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)

#Create token
def create_token (data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(to_encode,SECREAT_KEY,algorithm=ALGORITHM)
    return token



# Login API (Token OAuth2 + JWT Form)
@app.post("/login")
def login(formData:OAuth2PasswordRequestForm = Depends()):
    user = fake_user_db.get(formData.username)
    if not user or not verify_password(formData.password, user["hashed_password"]):
        raise HTTPException(
            status_code=400,
            detail="Invalid user and password"
        )
    access_token =  create_token({"sub": formData.username})
    return {
         "access_token": access_token,
         "token_type": "bearer"
    }

# Verify token with OAuth2 + jwt 
def verify_token(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, SECREAT_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="invalid token"
            )
        return username
    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="invalid token"
        )
    
#Protected route
@app.get("/protected")
def protected_route(username:str = Depends(verify_token)):
    return {
        "message": f"Hello {username}, you have access to this protected route!",
         "user": username
    }





# # Login API (Token JWT genration)
# @app.post("/login")
# def login(username:str,password:str):
#     if username != "admin" or password != "12345":
#         raise HTTPException(
#             status_code=401,
#             detail="invalid user and password"
#         )
#     token = create_token({
#         "sub":username
#     })

#     return{
#         "access_token" : token
#     }

# #JWT Token verify
# def verify_token(token:str = Header(None)):
#     try:
#         payload = jwt.decode(token,SECREAT_KEY,algorithms=[ALGORITHM])
#         return payload
#     except: 
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid  or expire token"
#         )
    
#protected Route api
# @app.get("/secure")
# def secure_data(user = Depends(verify_token)):
#     return {
#          "message" : "Secure date accessed",
#          "user" : user
#     }

    


