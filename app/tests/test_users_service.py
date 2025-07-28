import uuid
import pytest
from sqlmodel import SQLModel, create_engine, Session

from app.models import UserCreate
from app.services.users import create_user, get_user_by_id
from app.exceptions import UserAlreadyExistsError


def test_create_user_success(db: Session):
    user_data = UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="securepassword"
    )
    user_public = create_user(session=db, user_data=user_data)
    assert user_public.username == "testuser"
    assert user_public.email == "testuser@example.com"
    assert user_public.is_active


def test_create_user_duplicate_email(session):
    user_data = UserCreate(
        username="user1",
        email="duplicate@example.com",
        password="password123"
    )
    create_user(session=session, user_data=user_data)
    with pytest.raises(UserAlreadyExistsError):
        create_user(session=session, user_data=user_data)


def test_get_user_by_id_found(session):
    user_data = UserCreate(
        username="user2",
        email="user2@example.com",
        password="password456"
    )
    user_public = create_user(session=session, user_data=user_data)
    found_user = get_user_by_id(session, user_public.id)
    assert found_user is not None
    assert found_user.email == "user2@example.com"


def test_get_user_by_id_not_found(session):
    random_id = uuid.uuid4()
    user = get_user_by_id(session, random_id)
    assert user is None
