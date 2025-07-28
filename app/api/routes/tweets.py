from fastapi import APIRouter

from app.models import TweetPublic, TweetCreate
from app.api.deps import SessionDependency, CurrentUserDependency, PaginationDependency
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


@router.post("/explore", response_model=list[TweetPublic], summary="Get tweets of the user's followees")
def get_tweets_from_db(*, session: SessionDependency, current_user: CurrentUserDependency, pagination: PaginationDependency):
    """Gets tweets from db using the following query:
    
    SELECT tweets, users, FROM tweets
    JOIN users ON tweets.owner_id = users.id
    JOIN follows ON follows.followee_id = users.id
    WHERE follows.follower_id = current_user 

    Args:
        session (SessionDependency): The database session.
        current_user (CurrentUserDependency): The current user.

    Returns:
        _type_: _description_
    """
    tweets.get_followees_tweets_cache(session=session, current_user=current_user, pagination=pagination)
    return tweets.get_followees_tweets_db(session=session, current_user=current_user, pagination=pagination)
