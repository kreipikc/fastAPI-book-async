from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from .database import BookOrm
from .schemas import BookCreate, BookRead
from ..database import new_session
from ..redis import redis_client
import json


async def set_data_redis_books(book: BookOrm):
    """Sets book data in Redis cache.

    This function converts the book object to a dictionary, serializes it to JSON, and stores it in Redis with an expiration time of 30 seconds.

    Args:
        book (BookOrm): The book object to be cached.
    """
    book_dict = {
        "id": book.id,
        "name": book.name,
        "description": book.description,
    }
    json_book = json.dumps(book_dict)
    await redis_client.set(book.id, json_book, 30)

async def get_data_redis_books(id_book: int) -> Optional[BookRead]:
    """Retrieves book data from Redis cache.

    This function retrieves the book data from Redis, deserializes it from JSON, and returns it as a BookRead object.

    Args:
        id_book (int): The ID of the book to retrieve.

    Returns:
        A Optional[BookRead], the book data as a BookRead object if found in Redis, otherwise None.
    """
    book = await redis_client.get(id_book)
    if book:
        return BookRead(**json.loads(book))
    return None


class BookRepository:
    @classmethod
    async def db_add_one(cls, data: BookCreate) -> int:
        """Adds a new book to the database.

        This method adds a new book to the database and returns the ID of the created book.

        Args:
            data (BookCreate): The data for the new book.

        Returns:
            A int, the ID of the newly created book.
        """
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
        """Retrieves all books from the database.

        Returns:
            A List[BookRead], list of all book objects.
        """
        async with new_session() as session:
            query = select(BookOrm)
            result = await session.execute(query)
            book_models = result.scalars().all()
            return [BookRead(id=book.id, name=book.name, description=book.description) for book in book_models]

    @classmethod
    async def db_get_one(cls, id_book: int):
        """Retrieves a single book by ID from Redis or the database.

        Args:
            id_book (int): The ID of the book to retrieve.

        Returns:
            A BookRead, the book object if found.
        """
        result = await get_data_redis_books(id_book)
        if result:
            return BookRead.model_validate(result)

        async with new_session() as session:
            book = await session.get(BookOrm, id_book)
            await set_data_redis_books(book)
            return BookRead(id=book.id, name=book.name, description=book.description)

    @classmethod
    async def db_update(cls, data: BookCreate, id_book: int) -> bool:
        """Updates an existing book in the database.

        Args:
            data (BookCreate): The updated data for the book.
            id_book (int): The ID of the book to update.

        Returns:
            A bool, true if the update is successful.
        """
        async with new_session() as session:
            stmt = update(BookOrm).where(BookOrm.id == id_book).values(**data.model_dump(exclude_unset=True))
            await session.execute(stmt)
            await session.commit()
            return True

    @classmethod
    async def db_delete(cls, id_book: int):
        """Deletes a book from the database by ID.

        Args:
            id_book (int): The ID of the book to delete.

        Returns:
            A bool, true if the book is successfully deleted, False if the book is not found.

        Raises:
            NoResultFound: If the book is not found in the database.
        """
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