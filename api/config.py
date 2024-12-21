import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")
ALGORITHM = os.getenv("ALGORITHM", "HS256")