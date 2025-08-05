import logging
import random
import string
from uuid import UUID

from app.core.db import engine, Session
from app.services.fanout import fanout_to_followers
from app.models import TweetPublic, User, UserCreate, Follows, Tweet, TweetCreate


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_random_string(n: int) -> str:
    return "".join(random.choices(string.ascii_letters, k=n))


def random_email():
    return f"{get_random_string(5)}@{get_random_string(5)}.com"


def create_user(session: Session, data: UserCreate) -> User:
    db_user = User.model_validate(data, update={"hashed_password": data.password})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def create_tweet(session: Session, data: TweetCreate, owner_id: UUID):
    db_tweet = Tweet.model_validate(data, update={"owner_id": owner_id})
    session.add(db_tweet)
    session.commit()
    session.refresh(db_tweet)
    tweet = TweetPublic.model_validate(db_tweet)
    fanout_to_followers(session=session, tweet=tweet)


def generate_data(session: Session):
    CREDENTIALS = [
        (f"user-test-{i}", "qwerty123") for i in range(10)
    ]
    created_users_ids = []
    for username, password in CREDENTIALS:
        data = UserCreate(
            username=username,
            email=random_email(),
            password=password
        )
        user_db = create_user(session=session, data=data)
        created_users_ids.append(user_db.id)

    followers = []
    for _ in range(100):
        user_data = UserCreate(
            username=get_random_string(10),
            email=random_email(),
            password=get_random_string(10)
        )
        follower = create_user(session=session, data=user_data)
        for followee_id in created_users_ids:
            followers.append(Follows(followee_id=followee_id, follower_id=follower.id))
    
    session.bulk_save_objects(followers)

    for owner_id in created_users_ids:
        data = TweetCreate(title=get_random_string(10), content=get_random_string(20))
        create_tweet(session=session, data=data, owner_id=owner_id)


def main():
    with Session(engine) as session:
        generate_data(session)


if __name__ == "__main__":
    main()
