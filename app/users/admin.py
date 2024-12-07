from fastapi import APIRouter, Depends
from app.users.dependencies import get_current_admin_user
from app.users.schemas import SUser
from app.users.service import UserRepository


router = APIRouter(prefix="/admin", tags=["Admin 🛠️"])


@router.get("/all_users", summary="Information about all users")
async def get_all_users(user_data: SUser = Depends(get_current_admin_user)):
    return await UserRepository.find_all_user()


@router.put("/update_user_role", summary="Update role for user")
async def update_user_role(id_user: int, role: str , user_data: SUser = Depends(get_current_admin_user)):
    await UserRepository.change_role(id_user, role)
    return {"message": "Роль у пользователя успешно изменена"}


@router.delete("/delete_user", summary="Delete user")
async def delete_user(id_user: int, user_data: SUser = Depends(get_current_admin_user)):
    await UserRepository.delete_user_by_id(id_user)
    return {"message": "Пользователь успешно удален"}