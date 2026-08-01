from fastapi import HTTPException, status, Depends, APIRouter
from ..schemas.user import UserCreate, UserResponse, UserLogin
from ..schemas.auth import Token
from ..db.database import get_db
from sqlalchemy.orm import Session
from ..models.user import User
from ..utils import hash, verify
from ..core.oauth2 import create_access_token



router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)



@router.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    email = db.query(User).filter(User.email == user.email).first()
    if email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This Email is already taken")
    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = create_access_token({'user_id': user.id, 'role': user.role.value})
    return {"access_token": access_token, "token_type": "bearer"}