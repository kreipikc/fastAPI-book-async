import os
from typing import Optional
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv(dotenv_path="common/database/.env")

engine = create_async_engine(os.getenv("URL_DATABASE"))
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class BookOrm(Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]

async def create_tables():
    async with engine.begin() as conn:
        print("Создание таблиц")
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        print("Удаление таблиц")
        await conn.run_sync(Model.metadata.drop_all)