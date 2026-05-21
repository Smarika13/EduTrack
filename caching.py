import redis.asyncio as redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

caching = redis.from_url(REDIS_URL)


def get_redis():
    return caching
