from fastapi import HTTPException, status
from ...users.responses.http_errors import ErrorDetail


class RoleErrorCode:
    """Аll error codes for roles.

    Attributes:
        ROLE_NOT_FOUND: Role not found on database.
    """
    ROLE_NOT_FOUND = "ROLE_NOT_FOUND"


class HTTTPError:
    """Аll error codes for roles.

    Attributes:
        ROLE_NOT_FOUND_404: Role not found on database.
    """
    ROLE_NOT_FOUND_404 = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=ErrorDetail(
            code=RoleErrorCode.ROLE_NOT_FOUND,
            reason="Role not found"
        ).model_dump(),
    )