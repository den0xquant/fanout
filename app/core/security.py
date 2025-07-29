from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # type: ignore


ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    # return pwd_context.verify(plain_password, hashed_password)
    return plain_password == hashed_password


def get_password_hash(password: str) -> str:
    """
    Generate a hashed password.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    # return pwd_context.hash(password)  # Uncomment this line when you want to use bcrypt
    return password


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    """
    Create a JWT access token with an expiration time.

    Args:
        subject (str | Any): The subject of the token (usually the user ID).
        expires_delta (timedelta): The duration for which the token is valid.

    Returns:
        str: The encoded JWT token.
    """
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
