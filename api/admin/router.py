from fastapi import APIRouter, status, Response, Depends
from typing import List
from .responses.responses import base_admin_response, AdminResponses
from ..users.schemas import UserInfo
from .service import AdminRepository
from .dependencies import get_current_admin_user


router = APIRouter(prefix="/admin", tags=["Admin 👔"])


@router.get(
    path="/all_users",
    summary="Information about all users",
    description="Information about all users",
    response_description="The all users",
    status_code=status.HTTP_200_OK,
    response_model=List[UserInfo],
    responses=base_admin_response,
)
async def get_all_users(user_data: UserInfo = Depends(get_current_admin_user)):
    return await AdminRepository.find_all_user()


@router.put(
    path="/update_user_role",
    summary="Update role for user",
    description="Update role for user",
    response_description="HTTP 200 STATUS",
    status_code=status.HTTP_200_OK,
    responses=AdminResponses.update_user_role_put,
)
async def update_user_role(id_user: int, role_id: int, user_data: UserInfo = Depends(get_current_admin_user)):
    await AdminRepository.change_role(id_user, role_id)
    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    path="/delete_user",
    summary="Delete user",
    description="Delete user",
    response_description="HTTP 204 STATUS",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=AdminResponses.delete_user,
)
async def delete_user(id_user: int, user_data: UserInfo = Depends(get_current_admin_user)):
    await AdminRepository.delete_user_by_id(id_user)
    return Response(status_code=status.HTTP_200_OK)