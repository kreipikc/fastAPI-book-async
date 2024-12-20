from fastapi import APIRouter, status
from .schemas import Book
from .service import BookRepository


router = APIRouter(prefix="/books", tags=["Books 📚"])


@router.get(
    path="/",
    summary="Get all books",
    description="Get all books",
    status_code=status.HTTP_200_OK
)
async def get_all():
    books = await BookRepository.db_get_all()
    return {"books": books}


@router.post(
    path="/",
    summary="Add new book",
    description="Add new book",
    status_code=status.HTTP_201_CREATED
)
async def add_book(book: Book):
    book_id = await BookRepository.db_add_one(book)
    return {"book_id": book_id}


@router.get(
    path="/{id_book}",
    summary="Get a book by id",
    description="Get a book by id",
    status_code=status.HTTP_200_OK
)
async def get_one(id_book: int):
    book = await BookRepository.db_get_one(id_book)
    return {"book": book}


@router.put(
    path="/{id_book}",
    summary="Update a specific book",
    description="Update a specific book",
    status_code=status.HTTP_200_OK
)
async def update_book(book: Book, id_book: int):
    result = await BookRepository.db_update(book, id_book)
    return {"Success": result}


@router.delete(
    path="/{id_book}",
    summary="Delete a specific book",
    description="Delete a specific book",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(id_book: int):
    result = await BookRepository.db_delete(id_book)
    return {"Success": result}