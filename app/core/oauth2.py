from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from .config import settings
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from ..schemas.auth import TokenPayload


oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")



ALGORITHM = settings.algorithm
SECRET_KEY = settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes



def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    jwt_encode = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return jwt_encode


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        role: str = payload.get("role")

        if id is None:
            raise credentials_exception

        token_data = TokenPayload(user_id=id, role=role)
        return token_data

    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate the credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
    
    
    