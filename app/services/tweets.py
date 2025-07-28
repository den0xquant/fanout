from sqlmodel import Session

from app.models import Tweet, TweetCreate, TweetPublic, User


def create_tweet(
    *,
    session: Session,
    current_user: User,
    tweet_data: TweetCreate
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
