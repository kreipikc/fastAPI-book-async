from typing import List
from fastapi import APIRouter, status
from fastapi.responses import Response
from .schemas import BookCreate, BookRead
from .service import BookRepository


router = APIRouter(prefix="/books", tags=["Books 📚"])


@router.get(
    path="/",
    summary="Get all books",
    description="Get all books",
    response_description="A list of all books in the database",
    status_code=status.HTTP_200_OK,
    response_model=List[BookRead]
)
async def get_all():
    books = await BookRepository.db_get_all()
    return [BookRead.model_validate(row) for row in books]


@router.post(
    path="/",
    summary="Add new book",
    description="Add new book",
    response_description="The book object with the ID from the database",
    status_code=status.HTTP_201_CREATED,
    response_model=BookRead
)
async def add_book(book: BookCreate):
    book_id = await BookRepository.db_add_one(book)
    return BookRead(id=book_id, name=book.name, description=book.description)


@router.get(
    path="/{id_book}",
    summary="Get a book by id",
    description="Get a book by id",
    response_description="The details of the book with the specified ID",
    status_code=status.HTTP_200_OK,
    response_model=BookRead
)
async def get_one(id_book: int):
    book = await BookRepository.db_get_one(id_book)
    return BookRead.model_validate(book)


@router.put(
    path="/{id_book}",
    summary="Update a specific book",
    description="Update a specific book",
    response_description="A message indicating whether the update was successful",
    status_code=status.HTTP_200_OK
)
async def update_book(book: BookCreate, id_book: int, response: Response):
    result = await BookRepository.db_update(book, id_book)
    if result:
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.delete(
    path="/{id_book}",
    summary="Delete a specific book",
    description="Delete a specific book",
    response_description="No content is returned if the deletion was successful",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(id_book: int):
    result = await BookRepository.db_delete(id_book)
    if result:
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_404_NOT_FOUND)