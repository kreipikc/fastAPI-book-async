from fastapi import HTTPException, Depends
from ..users.schemas import UserCreate
from ..users.dependencies import get_current_user


async def get_current_admin_user(current_user: UserCreate = Depends(get_current_user)):
    """Checks if the current user has the role of an admin.

    Args:
        current_user (UserCreate): The current user object retrieved from the dependency.

    Returns:
        A UserCreate, the current user object if they have the role of an admin.

    Raises:
        HTTPException: If the current user does not have the role of an admin, raises a 403 Forbidden exception.
    """
    if current_user.is_admin:
        return current_user
    raise HTTPException(status_code=403, detail='Недостаточно прав!')