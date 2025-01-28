from fastapi import APIRouter, Depends, status
from typing import List
from starlette.responses import Response
from .schemas import RoleRead, RoleCreate
from .service import RoleRepository
from ..admin.dependencies import get_current_admin_user


router = APIRouter(prefix="/roles", tags=["Role 📍"])


@router.get(
    path="/all_roles",
    summary="Information about all roles",
    description="Information about all roles",
    response_description="The all roles",
    status_code=status.HTTP_200_OK,
    response_model=List[RoleRead]
)
async def get_all_roles(user_data = Depends(get_current_admin_user)):
    return await RoleRepository.get_all_roles_db()


@router.post(
    path="/add_role",
    summary="Add a new role",
    description="Add a new role",
    response_description="Data from the database for the new role",
    status_code=status.HTTP_200_OK,
    response_model=RoleRead
)
async def add_role(data_role: RoleCreate, user_data = Depends(get_current_admin_user)):
    role_id = await RoleRepository.add_new_role_db(data_role)
    return RoleRead(id=role_id, role_type=data_role.role_type)


@router.put(
    path="/update_role",
    summary="Update role",
    description="Update role",
    response_description="Status response",
    status_code=status.HTTP_200_OK,
)
async def update_role(role_id: int, data_role: RoleCreate, user_data = Depends(get_current_admin_user)):
    await RoleRepository.update_role_db(role_id, data_role)
    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    path="/delete_role",
    summary="Delete role by ID",
    description="Delete role by ID",
    response_description="Status response",
    status_code=status.HTTP_200_OK
)
async def delete_role(role_id: int, user_data = Depends(get_current_admin_user)):
    await RoleRepository.delete_role_by_id(role_id)
    return Response(status_code=status.HTTP_200_OK)

