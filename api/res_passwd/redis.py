from typing import Optional
import redis.asyncio as redis


class RedisDB:
    """
    Class for working with Redis
    """
    def __init__(self, url: str) -> None:
        self.__redis_connect = redis.from_url(url=url)

    async def add_email_code(self, email: str, code: str) -> None:
        await self.__redis_connect.setex(email, 900, code)

    async def get_email_code(self, email: str) -> Optional[str]:
        code = await self.__redis_connect.get(email)

        if code:
            return code.decode('utf-8')

        return None

    async def del_email_code(self, email: str) -> None:
        await self.__redis_connect.delete(email)

    async def close(self) -> None:
        await self.__redis_connect.close()