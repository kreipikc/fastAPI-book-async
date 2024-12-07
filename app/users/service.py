from pydantic import EmailStr
from fastapi import HTTPException
from sqlalchemy import select, update, delete
from app.database import new_session
from app.users.auth import verify_password
from app.users.base import UsersOrm
from app.users.schemas import SUser


class UserRepository:
    @classmethod
    async def find_one_or_none(cls, email: str):
        async with new_session() as session:
            result = await session.execute(select(UsersOrm).where(UsersOrm.email == email))
            user = result.scalar_one_or_none()
            return user

    @classmethod
    async def add_user(cls, data: SUser) -> int:
        async with new_session() as session:
            user_dict = data.model_dump()
            user = UsersOrm(**user_dict)
            session.add(user)  # Добавить изменения
            await session.flush()  # Отправит изменение, не завершая транзакцию
            await session.commit()  # Сохранит все изменения в БД, завершит транзакцию
            return user.id

    @classmethod
    async def authenticate_user(cls, email: EmailStr, password: str):
        user = await cls.find_one_or_none(email)
        if not user or verify_password(default_password=password, hashed_password=user.password) is False:
            return None
        return user

    @classmethod
    async def find_one_or_none_by_id(cls, id_user: int):
        async with new_session() as session:
            user = await session.get(UsersOrm, id_user)
            if user:
                return user
            return None

    @classmethod
    async def find_all_user(cls):
        async with new_session() as session:
            result = await session.execute(select(UsersOrm))
            user_models = result.scalars().all()
            return user_models

    @classmethod
    async def change_role(cls, id_user: int, new_role: str):
        async with new_session() as session:
            user = await session.get(UsersOrm, id_user)
            if user is None:
                raise HTTPException(status_code=404, detail='Пользователь не найден')

            stmt = (
                update(UsersOrm)
                .where(UsersOrm.id == id_user)
                .values(
                    is_user=False,
                    is_student=False,
                    is_teacher=False,
                    is_admin=False,
                )
            )
            await session.execute(stmt)

            if new_role == "user":
                stmt = update(UsersOrm).where(UsersOrm.id == id_user).values(is_user=True)
            elif new_role == "student":
                stmt = update(UsersOrm).where(UsersOrm.id == id_user).values(is_student=True)
            elif new_role == "teacher":
                stmt = update(UsersOrm).where(UsersOrm.id == id_user).values(is_teacher=True)
            elif new_role == "admin":
                stmt = update(UsersOrm).where(UsersOrm.id == id_user).values(is_admin=True)
            else:
                raise HTTPException(status_code=400, detail='Не валидная роль')

            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete_user_by_id(cls, id_user: int):
        async with new_session() as session:
            user = await session.get(UsersOrm, id_user)
            if user is None:
                raise HTTPException(status_code=404, detail='Пользователь не найден')

            await session.execute(delete(UsersOrm).where(UsersOrm.id == id_user))
            await session.commit()