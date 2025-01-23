from pydantic import EmailStr
from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from .auth import verify_password
from .database import UsersOrm
from .schemas import UserCreate
from ..database import new_session


class UserRepository:
    @classmethod
    async def find_one_or_none(cls, email: str):
        """Finds a user by email.

        Args:
            email: The email of the user to find.

        Returns:
            A Optional[UsersOrm], the user object if found, otherwise None.
        """
        async with new_session() as session:
            result = await session.execute(select(UsersOrm).where(UsersOrm.email == email))
            user = result.scalar_one_or_none()
            return user

    @classmethod
    async def add_user(cls, data: UserCreate) -> int:
        """Adds a new user to the database.

        This method adds a new user to the database and returns the ID of the created user.

        Args:
            data: The data for the new user.

        Returns:
            A int, the ID of the newly created user.

        Raises:
            ValueError: If a user with the same email already exists.
        """
        async with new_session() as session:
            try:
                user_dict = data.model_dump()
                user = UsersOrm(**user_dict)
                session.add(user)
                await session.flush()
                await session.commit()
                return user.id
            except IntegrityError:
                await session.rollback()
                raise ValueError("User with this email already exists")

    @classmethod
    async def authenticate_user(cls, email: EmailStr, password: str):
        """Authenticates a user by email and password.

        Args:
            email: The email of the user to authenticate.
            password: The password of the user to authenticate.

        Returns:
            A Optional[UsersOrm], the user object if authentication is successful, otherwise None.
        """
        user = await cls.find_one_or_none(email)
        if not user or verify_password(default_password=password, hashed_password=user.password) is False:
            return None
        return user

    @classmethod
    async def find_one_or_none_by_id(cls, id_user: int):
        """Finds a user by ID.

        Args:
            id_user (int): The ID of the user to find.

        Returns:
            A Optional[UsersOrm], the user object if found, otherwise None.
        """
        async with new_session() as session:
            user = await session.get(UsersOrm, id_user)
            if user:
                return user
            return None

    @classmethod
    async def find_all_user(cls):
        """Finds all users in the database.

       Returns:
           A List[UsersOrm], list of all user objects.
       """
        async with new_session() as session:
            result = await session.execute(select(UsersOrm))
            user_models = result.scalars().all()
            return user_models

    @classmethod
    async def change_role(cls, id_user: int, new_role: str):
        """Changes the role of a user.

        This method changes the role of a user in the database.

        Args:
            id_user (int): The ID of the user whose role is to be changed.
            new_role (str): The new role to assign to the user.

        Returns:
            None

        Raises:
            HTTPException: If the user is not found or the role is invalid.
        """
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
        """Deletes a user by ID.

        This method deletes a user from the database based on the provided ID.

        Args:
            id_user (int): The ID of the user to delete.

        Raises:
            HTTPException: If the user is not found.
        """
        async with new_session() as session:
            user = await session.get(UsersOrm, id_user)
            if user is None:
                raise HTTPException(status_code=404, detail='Пользователь не найден')

            await session.execute(delete(UsersOrm).where(UsersOrm.id == id_user))
            await session.commit()