from fastapi import status, HTTPException
from ...users.responses.http_errors import ErrorDetail


class BookErrorCode:
    """Аll error codes for books.

    Attributes:
        BOOK_NOT_FOUND: Book not found on database.
    """
    BOOK_NOT_FOUND = "BOOK_NOT_FOUND"


class HTTTPError:
    """Аll error codes for books.

    Attributes:
        BOOK_NOT_FOUNT_404: Book not found on database.
    """
    BOOK_NOT_FOUNT_404 = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=ErrorDetail(
            code=BookErrorCode.BOOK_NOT_FOUND,
            reason="Book not found"
        ).model_dump(),
    )