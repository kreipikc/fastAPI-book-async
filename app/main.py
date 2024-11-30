from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.common.database.database import create_tables, delete_tables
from app.common.routers.books_router import router as books_router
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
app.include_router(books_router)

@app.get("/")
async def go_to_docs():
    return RedirectResponse(url="/docs", status_code=308)