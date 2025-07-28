from uuid import UUID

from sqlmodel import Session, select

from app.models import TweetPublic, Follows
from app.core.cache import redis_instance


def fanout_to_followers(*, session: Session, tweet: TweetPublic) -> None:
    statement = select(Follows.follower_id).where(Follows.followee_id == tweet.owner_id)
    follower_ids = session.exec(statement).all()

    for follower_id in follower_ids:
        redis_instance.lpush(f"tweets:{follower_id}", tweet.model_dump_json())
        redis_instance.ltrim(f"tweets:{follower_id}", 0, 999)
