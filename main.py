from fastapi import FastAPI
from common.database.database import create_tables, delete_tables
from common.routers.book_router import router as book_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("Таблицы очищены")
    await create_tables()
    print("Таблицы готовы к работе")
    yield
    print("Выключение")

app = FastAPI(lifespan=lifespan)
app.include_router(book_router)