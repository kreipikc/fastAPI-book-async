from fastapi import HTTPException
from ..database import new_session
from ..users.database import UsersOrm
from sqlalchemy import select, update, delete


class AdminRepository:
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