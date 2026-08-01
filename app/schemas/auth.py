from pydantic import BaseModel
from ..models.user import Role


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    user_id: int
    role: Role

