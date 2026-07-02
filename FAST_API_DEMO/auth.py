from jose import jwt, JWSError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer

SCREATE_KEY = "myscreat"
ALGORITHEM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 60

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

# token create
def create_token(data:dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode,SCREATE_KEY,algorithm=ALGORITHEM)


def verify_token(token:str= Depends(oauth2_schema)):
    try: 
        payload = jwt.decode(token,SCREATE_KEY,algorithms=ALGORITHEM)
        return payload
    except JWSError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )
    


