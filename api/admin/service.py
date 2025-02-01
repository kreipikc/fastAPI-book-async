from typing import List
from ..database import new_session
from ..roles.database import RolesOrm
from ..roles.responses.http_errors import HTTTPError as HTTTPErrorRoles
from .responses.http_errors import HTTTPError as HTTTPErrorAdmin
from ..users.database import UsersOrm
from sqlalchemy import select, update, delete
from ..users.schemas import UserInfo


class AdminRepository:
    @classmethod
    async def find_all_user(cls) -> List[UserInfo]:
        """Finds all users in the database.

       Returns:
           A List[UserInfo], list of all user objects.
       """
        async with new_session() as session:
            result = await session.execute(select(UsersOrm))
            user_models = result.scalars().all()
            return [UserInfo.model_validate(user.__dict__) for user in user_models]

    @classmethod
    async def change_role(cls, id_user: int, new_role_id: int) -> None:
        """Change the role of a user.

        Args:
            id_user (int): The ID of the user whose role needs to be changed.
            new_role_id (int): The ID of the new role to be assigned to the user.

        Returns:
            None

        Raises:
            HTTTPErrorAdmin.USER_NOT_FOUND_404: If the user not found
            HTTTPErrorRoles.ROLE_NOT_FOUND_404: If the role not found
        """
        async with new_session() as session:
            user = await session.get(UsersOrm, id_user)
            if user is None:
                raise HTTTPErrorAdmin.USER_NOT_FOUND_404

            role = await session.get(RolesOrm, new_role_id)
            if role is None:
                raise HTTTPErrorRoles.ROLE_NOT_FOUND_404

            await session.execute(update(UsersOrm).where(UsersOrm.id == id_user).values(role_id=role.id))
            await session.commit()


    @classmethod
    async def delete_user_by_id(cls, id_user: int) -> None:
        """Deletes a user by ID.

        This method deletes a user from the database based on the provided ID.

        Args:
            id_user (int): The ID of the user to delete.

        Raises:
            HTTTPErrorAdmin.USER_NOT_FOUND_404: If the user is not found.
        """
        async with new_session() as session:
            user = await session.get(UsersOrm, id_user)
            if user is None:
                raise HTTTPErrorAdmin.USER_NOT_FOUND_404

            await session.execute(delete(UsersOrm).where(UsersOrm.id == id_user))
            await session.commit()