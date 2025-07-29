from fastapi import APIRouter

from app.models import UserRegister, UserPublic
from app.api.deps import SessionDependency
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
