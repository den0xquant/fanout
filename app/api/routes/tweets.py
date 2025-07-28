from fastapi import APIRouter

from app.models import TweetPublic, TweetCreate
from app.api.deps import SessionDependency, CurrentUserDependency
from app.services import tweets


router = APIRouter(prefix="/tweets", tags=["tweets"])


@router.post("/", response_model=TweetPublic, summary="Create a new tweet")
def create_tweet(
    *,
    session: SessionDependency,
    current_user: CurrentUserDependency,
    tweet_data: TweetCreate
) -> TweetPublic:
    """Create a new tweet.

    Args:
        session (SessionDependency): The database session.
        current_user (CurrentUserDependency): The current user.
        tweet_data (TweetCreate): The data for the new tweet.

    Returns:
        TweetPublic: The created tweet.
    """
    return tweets.create_tweet(session=session, current_user=current_user, tweet_data=tweet_data)
