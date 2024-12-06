import os
import aioredis
from dotenv import load_dotenv

load_dotenv()
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_post = os.getenv("REDIS_PORT", 6379)

redis_client = aioredis.from_url(f"redis://{redis_host}:{redis_post}")