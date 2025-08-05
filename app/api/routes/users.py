from typing import Annotated
from uuid import UUID
from fastapi import APIRouter

from app.models import UserRegister, UserPublic, UserId
from app.api.deps import SessionDependency, CurrentUserDependency
from app.services import users


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", summary="Create a new user")
def create_user(*, session: SessionDependency, user_data: UserRegister) -> UserPublic:
    """
    Create a new user.

    Args:
        session (SessionDependency): The database session.
        user_data (UserRegister): The data for the new user.

    Returns:
        UserPublic: The created user.
    """

    return users.create_user(session=session, user_data=user_data)


@router.get("/{user_id}", summary="Get an user by id")
def get_user(*, session: SessionDependency, user_id) -> UserPublic:
    return users.get_user_by_id(session=session, user_id=user_id)


@router.post("/follow", summary="Follows on target user")
def follow_user(*, session: SessionDependency, user: UserId, current_user: CurrentUserDependency) -> str:
    return users.follow(session=session, followee_id=user.id, follower_id=current_user.id)
