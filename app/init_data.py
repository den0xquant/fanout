import logging
import random
import string
from typing import Sequence

from sqlmodel import Session, select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.core.db import engine
from app.models import UserCreate, User, Follows, Tweet


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NUM_USERS = 1_000_000
NUM_TWEETS = 5_000_000
NUM_FOLLOWS = 10_000_000


def get_random_string(n: int) -> str:
    return "".join(random.choices(string.ascii_letters, k=n))


def random_email():
    return f"{get_random_string(10)}@{get_random_string(5)}.com"


def generate_users(session: Session) -> None:
    users = []
    for _ in range(NUM_USERS):
        user_data = UserCreate(
            username=get_random_string(20),
            email=random_email(),
            password=get_random_string(8),
        )
        user_obj = User.model_validate(
            user_data, update={"hashed_password": user_data.password}
        )
        users.append(user_obj)

        if len(users) % 1_000 == 0:
            session.bulk_save_objects(users)
            session.commit()
            print(f"→ {len(users)} users inserted...")
            users = []
    if len(users) != 0:
        session.bulk_save_objects(users)
        session.commit()
    print(f"✅ {NUM_USERS} users created.")


def get_users(session: Session, count: int = 5000) -> Sequence[User]:
    total = session.exec(select(func.count("*")).select_from(User)).one()
    offset = random.randint(0, max(0, total - count))
    statement = select(User).offset(offset).limit(count)
    return session.exec(statement).all()


def generate_follows(session: Session):
    user_ids = session.exec(select(User.id)).all()
    saved_objects_count = 0
    follows = set()

    while saved_objects_count < NUM_FOLLOWS:
        followee_id = random.choice(user_ids)
        for follower_id in user_ids:
            if followee_id == follower_id:
                continue

            follows.add((follower_id, followee_id))

            if len(follows) % 10_000 == 0:
                saved_objects_count += 10_000
                try:
                    session.bulk_save_objects([
                        Follows(follower_id=fr, followee_id=fe)
                        for fr, fe in follows
                    ])
                    session.commit()
                except IntegrityError:
                    continue

                print(f"→ {len(follows)} follows inserted...")
                follows = set()

    if len(follows) != 0:
        try:
            session.bulk_save_objects([
                Follows(follower_id=fr, followee_id=fe)
                for fr, fe in follows
            ])
            session.commit()
        except IntegrityError:
            pass
    
    print(f"✅ {NUM_FOLLOWS} follows created.")


def generate_tweets(session: Session):
    user_id = '9f99b6f9-0287-4d44-b21b-a83a4f66050a'
    statement = select(User).options(selectinload(User.followers)).where(User.id == user_id) # pyright: ignore[reportArgumentType]
    user_obj = session.exec(statement).first()
    print('✅ Count followers', len(user_obj.followers)) # pyright: ignore[reportOptionalMemberAccess]

    tweets = []
    saved_tweets = 0

    while saved_tweets < NUM_TWEETS:
        for follower in user_obj.followers: # pyright: ignore[reportOptionalMemberAccess]
            amount_tweets = random.randint(50, 200)
            follower_tweets = [
                Tweet(
                    title=get_random_string(20),
                    content=get_random_string(100),
                    owner_id=follower.id
                )
                for _ in range(amount_tweets)
            ]
            tweets.extend(follower_tweets)
            
            if len(tweets) % 10_0000 == 0:
                session.bulk_save_objects(tweets)
                session.commit()
                print(f"→ {len(tweets)} tweets inserted...")
                saved_tweets += 10_000
                tweets = []
    print(f"✅ {NUM_TWEETS} tweets created.")


def follow_to_users(session: Session):
    user_ids = session.exec(select(User.id)).all()
    saved_objects_count = 0
    follows = set()

    while saved_objects_count < NUM_FOLLOWS:
        follower_id = random.choice(user_ids)
        for followee_id in user_ids:
            if followee_id == follower_id:
                continue

            follows.add((follower_id, followee_id))

            if len(follows) % 10_000 == 0:
                saved_objects_count += 10_000
                try:
                    session.bulk_save_objects([
                        Follows(follower_id=fr, followee_id=fe)
                        for fr, fe in follows
                    ])
                    session.commit()
                except IntegrityError:
                    continue

                print(f"→ {len(follows)} follows inserted...")
                follows = set()

    if len(follows) != 0:
        try:
            session.bulk_save_objects([
                Follows(follower_id=fr, followee_id=fe)
                for fr, fe in follows
            ])
            session.commit()
        except IntegrityError:
            pass
    
    print(f"✅ {NUM_FOLLOWS} follows created.")


def main():
    logger.info("Initializing service")
    with Session(engine) as session:
        print("🚀 Starting data generation...")
        # generate_users(session)
        # generate_follows(session)
        # generate_tweets(session)
        follow_to_users(session)
        print("🎉 Done.")
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
