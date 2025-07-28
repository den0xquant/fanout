from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models import Token
from app.api.deps import SessionDependency
from app.core.config import settings
from app.core.security import create_access_token
from app.services.auth import authenticate


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login/access-token", summary="Login and get access token")
def login_access_token(*, session: SessionDependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    Login endpoint to authenticate user and return access token.
    This endpoint requires a valid username and password.
    """
    user = authenticate(session=session, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            subject=user.id,
            expires_delta=expires_delta
        )
    )
