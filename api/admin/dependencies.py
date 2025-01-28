from fastapi import HTTPException, Depends, status
from ..roles.service import RoleRepository
from ..users.schemas import UserCreate, UserInfo
from ..users.dependencies import get_current_user


async def get_current_admin_user(current_user: UserInfo = Depends(get_current_user)):
    """Checks if the current user has the role of an admin.

    Args:
        current_user (UserCreate): The current user object retrieved from the dependency.

    Returns:
        A UserCreate, the current user object if they have the role of an admin.

    Raises:
        HTTPException: If the current user does not have the role of an admin, raises a 403 Forbidden exception.
    """
    role_db = await RoleRepository.get_role_by_id(current_user.role_id)

    if role_db.role_type == "admin":
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав!")