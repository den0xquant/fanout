import json
from typing import Sequence
from sqlmodel import Session, select

from app.core.cache import redis_instance
from app.models import (
    Tweet,
    TweetCreate,
    TweetPublic,
    User,
    Follows,
    Pagination,
)


def create_tweet(
    *, session: Session, current_user: User, tweet_data: TweetCreate
) -> TweetPublic:
    """
    Create a new tweet.

    Args:
        session (SessionDependency): The database session.
        current_user (CurrentUserDependency): The current user.
        tweet_data (TweetCreate): The data for the new tweet.

    Returns:
        TweetPublic: The created tweet.
    """
    tweet = Tweet.model_validate(tweet_data, update={"owner_id": current_user.id})
    session.add(tweet)
    session.commit()
    session.refresh(tweet)
    return TweetPublic.model_validate(tweet)


def get_followees_tweets_db(
    *, session: Session, current_user: User, pagination: Pagination
) -> Sequence[Tweet]:
    """Fetches tweets from users that the current user is following.

    Args:
        session (Session): The database session used to execute queries.
        current_user (User): The user whose followed users' tweets are to be retrieved.
        pagination (Pagination): The limit and offset values.

    Returns:
        Sequence[Tweet]: A list of tweets posted by users followed by the current user.
    """
    statement = (
        select(Tweet)
        .join(User, Tweet.owner_id == User.id)  # pyright: ignore[reportArgumentType]
        .join(Follows, Follows.followee_id == User.id)  # pyright: ignore[reportArgumentType]
        .where(Follows.follower_id == current_user.id)
        .limit(pagination.limit)
        .offset(pagination.offset)
    )
    return session.exec(statement).all()


def get_followees_tweets_cache(*, current_user: User, pagination: Pagination) -> list[TweetPublic]:
    """Fetches tweets from users that the current user is following.

    Args:
        current_user (User): The user for which to fetch the tweets timeline.
        pagination (Pagination): The limit and offset values.

    Returns:
        Sequence[TweetPublic]: Serializer tweets from Redis cache.
    """
    tweets = redis_instance.lrange(
        name=f"tweets:{current_user.id}",
        start=pagination.offset,
        end=pagination.offset + pagination.limit - 1,
    )
    return [TweetPublic(**json.loads(tweet)) for tweet in tweets] if tweets else []  # type: ignore
