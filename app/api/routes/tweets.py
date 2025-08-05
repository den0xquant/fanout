from fastapi import APIRouter, BackgroundTasks

from app.models import TweetPublic, TweetCreate
from app.api.deps import SessionDependency, CurrentUserDependency, PaginationDependency
from app.services import tweets, fanout


router = APIRouter(prefix="/tweets", tags=["tweets"])


@router.post("/", response_model=TweetPublic, summary="Create a new tweet")
def create_tweet(
    *,
    background_tasks: BackgroundTasks,
    session: SessionDependency,
    current_user: CurrentUserDependency,
    tweet_data: TweetCreate,
) -> TweetPublic:
    """Create a new tweet.

    Args:
        session (SessionDependency): The database session.
        current_user (CurrentUserDependency): The current user.
        tweet_data (TweetCreate): The data for the new tweet.

    Returns:
        TweetPublic: The created tweet.
    """
    tweet_public = tweets.create_tweet(
        session=session, current_user=current_user, tweet_data=tweet_data
    )
    background_tasks.add_task(
        fanout.fanout_to_followers, session=session, tweet=tweet_public
    )
    return tweet_public


@router.get(
    "/db/timeline",
    response_model=list[TweetPublic],
    summary="Get tweets of the user's followees",
)
def get_tweets_from_db(
    *,
    session: SessionDependency,
    current_user: CurrentUserDependency,
    pagination: PaginationDependency,
):
    """Gets tweets from db.

    Args:
        session (SessionDependency): The database session.
        current_user (CurrentUserDependency): The current user.
        pagination (PaginationDependency): Limit and offset for pagination.

    Returns:
        list[TweetPublic]: Timeline of tweets from db.
    """
    return tweets.get_followees_tweets_db(
        session=session, current_user=current_user, pagination=pagination
    )


@router.get(
    "/cache/timeline",
    response_model=list[TweetPublic],
    summary="Get tweets of the user's followees",
)
def get_tweets_from_cache(
    *, current_user: CurrentUserDependency
):
    """Gets tweets from cache

    Args:
        current_user (CurrentUserDependency): The current user.
        pagination (PaginationDependency): Limit and offset for pagination.

    Returns:
        list[TweetPublic]: Timeline of tweets from cache.
    """
    return tweets.get_followees_tweets_cache(
        current_user=current_user
    )
