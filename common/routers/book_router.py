from fastapi import APIRouter
from common.schemas.book_schemas import SBookAdd
from common.service.repository import BookRepository

router = APIRouter(prefix="/book", tags=["book"])

@router.get("")
async def get_all():
    books = await BookRepository.db_get_all()
    return {"books": books}

@router.post("")
async def add_book(book: SBookAdd):
    book_id = await BookRepository.db_add_one(book)
    return {"book_id": book_id}

@router.get("/{id_book}")
async def get_one(id_book: int):
    book = await BookRepository.db_get_one(id_book)
    return {"book": book}

@router.put("/{id_book}")
async def update_book(book: SBookAdd, id_book: int):
    result = await BookRepository.db_update(book, id_book)
    return {"Success": result}

@router.delete("/{id_book}")
async def delete_book(id_book: int):
    result = await BookRepository.db_delete(id_book)
    return {"Success": result}