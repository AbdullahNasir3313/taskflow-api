from pydantic import BaseModel, EmailStr
from datetime import datetime
from ..models.user import Role


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserLogin):
    username: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: Role
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True





