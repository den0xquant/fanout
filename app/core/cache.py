from redis import Redis

from app.core.config import settings


redis_instance = Redis.from_url(str(settings.REDIS_URI), decode_responses=True)
