from fastapi import APIRouter, Depends
from ..core.oauth2 import get_current_user
from ..schemas.auth import TokenPayload


router = APIRouter()


@router.get("/me", response_model=TokenPayload)
def get_me(current_user: TokenPayload = Depends(get_current_user)):
    return current_user
