from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from .database import BookOrm
from .schemas import Book
from ..database import new_session
from ..redis import redis_client
import json


async def set_data_redis_books(book: BookOrm):
    book_dict = {
        "id": book.id,
        "name": book.name,
        "description": book.description,
    }
    json_book = json.dumps(book_dict)
    await redis_client.set(book.id, json_book, 30)

async def get_data_redis_books(id_book: int):
    book = await redis_client.get(id_book)
    if book:
        return json.loads(book)
    return None


class BookRepository:
    @classmethod
    async def db_add_one(cls, data: Book) -> int:
        async with new_session() as session:
            book_dict = data.model_dump()
            # Можно указывать явно -> BookOrm(name=book_dict["name"], и т.д.)
            book = BookOrm(**book_dict)
            session.add(book)       # Добавить изменения
            await session.flush()   # Отправит изменение, не завершая транзакцию
            await session.commit()  # Сохранит все изменения в БД, завершит транзакцию
            return book.id

    @classmethod
    async def db_get_all(cls):
        async with new_session() as session:
            query = select(BookOrm)
            result = await session.execute(query)
            book_models = result.scalars().all()
            return book_models

    @classmethod
    async def db_get_one(cls, id_book: int):
        result = await get_data_redis_books(id_book)
        if result:
            return result

        async with new_session() as session:
            book = await session.get(BookOrm, id_book)
            await set_data_redis_books(book)
            return book

    @classmethod
    async def db_update(cls, data: Book, id_book: int) -> bool:
        async with new_session() as session:
            stmt = update(BookOrm).where(BookOrm.id == id_book).values(**data.model_dump(exclude_unset=True))
            await session.execute(stmt)
            await session.commit()
            return True

    @classmethod
    async def db_delete(cls, id_book: int):
        async with new_session() as session:
            try:
                book = await session.get(BookOrm, id_book)
                if book:
                    await session.delete(book)
                    await session.commit()
                    return True
                else:
                    return False
            except NoResultFound:
                return NoResultFound