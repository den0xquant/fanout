from sqlmodel import Session, select

from app.models import User
from app.core.security import verify_password


def authenticate(*, session: Session, username: str, password: str) -> User | None:
    """
    Authenticate user with username and password.
    
    Args:
        username (str): The username of the user.
        password (str): The password of the user.
    
    Returns:
        User | None: The authenticated user or None if authentication failed.
    """
    statement = select(User).where(User.username == username)
    db_user = session.exec(statement).first()
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
