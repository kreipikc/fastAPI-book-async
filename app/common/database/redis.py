import os
import aioredis
import json
from dotenv import load_dotenv
from app.common.database.database import BookOrm

load_dotenv()
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_post = os.getenv("REDIS_PORT", 6379)

redis_client = aioredis.from_url(f"redis://{redis_host}:{redis_post}")

async def set_data_redis(book: BookOrm):
    book_dict = {
        "id": book.id,
        "name": book.name,
        "description": book.description,
    }
    json_book = json.dumps(book_dict)
    await redis_client.set(book.id, json_book, 30)

async def get_data_redis(id_book: int):
    book = await redis_client.get(id_book)
    if book:
        return json.loads(book)
    return None