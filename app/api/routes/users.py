from fastapi import APIRouter

from app.models import UserCreate, UserPublic
from app.api.deps import SessionDependency
from app.services import users


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", summary="Create a new user")
def create_user(*, session: SessionDependency, user_data: UserCreate) -> UserPublic:
    """
    Create a new user.

    Args:
        session (SessionDependency): The database session.
        user_data (UserCreate): The data for the new user.

    Returns:
        UserPublic: The created user.
    """
    
    return users.create_user(session=session, user_data=user_data)
