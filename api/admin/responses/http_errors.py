from fastapi import HTTPException, status
from ...users.responses.http_errors import ErrorDetail


class AdminErrorCode:
    """Аll error codes for admins.

    Attributes:
        USER_NOT_FOUND: User not found on database.
    """
    USER_NOT_FOUND = "USER_NOT_FOUND"


class HTTTPError:
    """Аll error codes for admins.

    Attributes:
        USER_NOT_FOUND_404: User not found on database.
    """
    USER_NOT_FOUND_404 = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=ErrorDetail(
            code=AdminErrorCode.USER_NOT_FOUND,
            reason="User not found"
        ).model_dump(),
    )