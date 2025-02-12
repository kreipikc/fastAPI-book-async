from fastapi import HTTPException, status
from ...users.responses.http_errors import ErrorDetail


class PasswdErrorCode:
    """Аll res_passwd error codes.

    Attributes:
        BAD_EMAIL: Bad email
        LACK_OF_EMAIL_IN_FORGOTTEN:
        BAD_RECOVERY_CODE:
    """
    BAD_EMAIL = "BAD_EMAIL"
    LACK_OF_EMAIL_IN_FORGOTTEN = "LACK_OF_EMAIL_IN_FORGOTTEN"
    BAD_RECOVERY_CODE = "BAD_RECOVERY_CODE"


class HTTTPError:
    """Аll res_passwd errors.

    Attributes:
        BAD_EMAIL_400: Bad email
        LACK_OF_EMAIL_IN_FORGOTTEN_400: Lack of email on the forgotten list
        BAD_RECOVERY_CODE_400: Bad recovery code for input email
    """
    BAD_EMAIL_400 = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ErrorDetail(
            code=PasswdErrorCode.BAD_EMAIL,
            reason="Non-existent email in the application"
        ).model_dump(),
    )

    LACK_OF_EMAIL_IN_FORGOTTEN_400 = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ErrorDetail(
            code=PasswdErrorCode.LACK_OF_EMAIL_IN_FORGOTTEN,
            reason="Lack of email on the forgotten list"
        ).model_dump(),
    )

    BAD_RECOVERY_CODE_400 = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ErrorDetail(
            code=PasswdErrorCode.BAD_RECOVERY_CODE,
            reason="Bad recovery code for input email"
        ).model_dump(),
    )