from fastapi import status
from .http_errors import HTTTPError
from ...users.responses.utils import convert_to_example


class PasswdResponse:
    """res_passwd responses.

    Attributes:
        forgot_password_post: Responses for forgot_password_post
        reset_password_post: Responses for reset_password_post
    """
    forgot_password_post = {
        status.HTTP_400_BAD_REQUEST: convert_to_example([
            HTTTPError.BAD_EMAIL_400,
        ]),
    }

    reset_password_post = {
        status.HTTP_400_BAD_REQUEST: convert_to_example([
            HTTTPError.BAD_EMAIL_400,
            HTTTPError.BAD_RECOVERY_CODE_400,
            HTTTPError.LACK_OF_EMAIL_IN_FORGOTTEN_400,
        ]),
    }