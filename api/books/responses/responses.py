from fastapi import status
from .http_errors import HTTTPError
from ...users.responses.utils import convert_to_example


class BookResponses:
    """Users responses.

    Attributes:
        get_book: Responses for get_book
        update_book_put: Responses for update_book_put
        delete_book: Responses for delete_book
    """
    get_book = {
        status.HTTP_404_NOT_FOUND: convert_to_example([
            HTTTPError.BOOK_NOT_FOUNT_404,
        ]),
    }

    update_book_put = {
        status.HTTP_404_NOT_FOUND: convert_to_example([
            HTTTPError.BOOK_NOT_FOUNT_404,
        ]),
    }

    delete_book = {
        status.HTTP_404_NOT_FOUND: convert_to_example([
            HTTTPError.BOOK_NOT_FOUNT_404,
        ]),
    }