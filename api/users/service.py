from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from .auth import verify_password
from .database import UsersOrm
from .responses.http_errors import HTTTPError
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
            HTTTPError.EMAIL_ALREADY_EXISTS_409: If a user with the same email already exists.
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
                raise HTTTPError.EMAIL_ALREADY_EXISTS_409

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
