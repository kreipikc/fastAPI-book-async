from fastapi import HTTPException, status
from sqlalchemy import select
from typing import List
from .database import RolesOrm
from .schemas import RoleRead, RoleCreate
from ..database import new_session


class RoleRepository:
    @classmethod
    async def create_default_roles(cls) -> None:
        """Creates default roles if they do not already exist.

        This method checks for the existence of default roles ('user' and 'admin') in the database.
        If these roles do not exist, it creates them.

        Returns:
            None
        """
        async with new_session() as session:
            user_role_exists = await session.execute(select(RolesOrm).where(RolesOrm.role_type == "user"))
            user_role_exists = user_role_exists.scalars().one_or_none()

            admin_role_exists = await session.execute(select(RolesOrm).where(RolesOrm.role_type == "admin"))
            admin_role_exists = admin_role_exists.scalars().one_or_none()

            if not user_role_exists:
                user_role = RolesOrm(role_type="user")
                session.add(user_role)

            if not admin_role_exists:
                admin_role = RolesOrm(role_type="admin")
                session.add(admin_role)

            await session.commit()

    @classmethod
    async def get_role_by_id(cls, role_id: int) -> RoleRead:
        """Retrieves a role by its ID.

        Args:
            role_id (int): The ID of the role to retrieve.

        Returns:
            A RoleRead, the role object corresponding to the provided role ID.

        Raises:
            HTTPException: If the role with the given ID is not found.
        """
        async with new_session() as session:
            role_exists = await session.get(RolesOrm, role_id)
            if not role_exists:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

            return RoleRead.model_validate(role_exists.__dict__)

    @classmethod
    async def get_all_roles_db(cls) -> List[RoleRead]:
        """Retrieves all roles from the database.

        Returns:
            A List[RoleRead], the list of RoleRead objects representing all roles in the database.
        """
        async with new_session() as session:
            role_model = await session.execute(select(RolesOrm))
            role_model = role_model.scalars().all()
            return [RoleRead.model_validate(role.__dict__) for role in role_model]

    @classmethod
    async def add_new_role_db(cls, role_data: RoleCreate):
        """Adds a new role to the database.

        Args:
            role_data (RoleCreate): The data for the new role to be added.

        Returns:
            A int, the ID of the newly created role.
        """
        async with new_session() as session:
            role_dict = role_data.model_dump()
            role = RolesOrm(**role_dict)
            session.add(role)
            await session.flush()
            await session.commit()
            return role.id

    @classmethod
    async def update_role_db(cls, role_id: int, role_data: RoleCreate) -> None:
        """Updates the role information for a given role ID.

        Args:
            role_id (int): The ID of the role to be updated.
            role_data (RoleCreate): The new data for the role.

        Returns:
            None

        Raises:
            HTTPException: If the role with the given ID is not found.
        """
        async with new_session() as session:
            result = await session.execute(select(RolesOrm).where(RolesOrm.id == role_id))
            role_old = result.scalars().one_or_none()
            if role_old is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

            role_old.role_type = role_data.role_type
            await session.commit()

    @classmethod
    async def delete_role_by_id(cls, role_id: int) -> None:
        """Deletes a role by its ID.

        Args:
            role_id (int): The ID of the role to be deleted.

        Returns:
            None

        Raises:
            HTTPException: If the role with the given ID is not found.
        """
        async with new_session() as session:
            role = await session.get(RolesOrm, role_id)
            if role:
                await session.delete(role)
                await session.commit()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")