from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from fastapi import Depends
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.db import engine
from app.core.security import ALGORITHM
from app.models import User, TokenPayload


def get_session():
    """
    Create a new SQLAlchemy session.

    Returns:
        Session: A new SQLAlchemy session.
    """
    with Session(engine) as session:
        yield session



reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token"
)

SessionDependency = Annotated[Session, Depends(get_session)]
TokenDependency = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDependency, token: TokenDependency) -> User:
    """
    Dependency to get the current user from the session.

    Args:
        session (Session): The SQLAlchemy session.

    Returns:
        User: The current user.
    """
    # Logic to retrieve the current user from the session
    # This is a placeholder and should be replaced with actual logic
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user


CurrentUserDependency = Annotated[User, Depends(get_current_user)]
