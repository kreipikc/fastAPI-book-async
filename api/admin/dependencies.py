from fastapi import Depends
from ..roles.service import RoleRepository
from ..users.responses.http_errors import HTTTPError
from ..users.schemas import UserInfo
from ..users.dependencies import get_current_user


async def get_current_admin_user(current_user: UserInfo = Depends(get_current_user)):
    """Checks if the current user has the role of an admin.

    Args:
        current_user (UserInfo): The current user object retrieved from the dependency.

    Returns:
        A UserCreate, the current user object if they have the role of an admin.

    Raises:
        HTTTPError.NO_ACCESS_RIGHTS_403: If the current user does not have the role of an admin
    """
    role_db = await RoleRepository.get_role_by_id(current_user.role_id)

    if role_db.role_type == "admin":
        return current_user
    raise HTTTPError.NO_ACCESS_RIGHTS_403