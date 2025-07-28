import uuid

from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.core.security import get_password_hash
from app.models import User, UserCreate, UserPublic
from app.exceptions import UserAlreadyExistsError


def create_user(*, session: Session, user_data: UserCreate) -> UserPublic:
    """
    Create a new user in the database.

    Args:
        session (Session): The database session.
        user (UserCreate): The user data to create.

    Returns:
        UserPublic: The created user.
    """
    statement = select(User).where(User.email == user_data.email)
    if session.exec(statement).first():
        raise UserAlreadyExistsError()

    db_user = User.model_validate(
        user_data, update={"hashed_password": get_password_hash(user_data.password)}
    )
    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    except IntegrityError:
        raise UserAlreadyExistsError
    return UserPublic.model_validate(db_user)


def get_user_by_id(session: Session, user_id: uuid.UUID) -> UserPublic | None:
    """
    Get a user by their ID.

    Args:
        session (Session): The database session.
        user_id (uuid.UUID): The ID of the user to retrieve.

    Returns:
        UserPublic | None: The user if found, otherwise None.
    """
    statement = select(User).where(User.id == user_id)
    db_user = session.exec(statement).first()
    if not db_user:
        return None
    return UserPublic.model_validate(db_user)
