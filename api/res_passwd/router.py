from fastapi import APIRouter, status, Request, Response
from .responses.http_errors import HTTTPError
from .responses.responses import PasswdResponse
from .schemas import ForgotPassword, ResetPassword
from .service import PasswdRepository
from .utils import create_recovery_code
from ..users.service import UserRepository


router = APIRouter(prefix="/auth", tags=["Auth 🙎🏻‍♂️"])


@router.post(
    path="/forgot_password",
    summary="Request a reset password procedure",
    description="Sends a password recovery code by email",
    response_description="HTTP 204 STATUS",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=PasswdResponse.forgot_password_post,
)
async def forgot_password(request: Request, forgot: ForgotPassword):
    user = await UserRepository.find_one_or_none(str(forgot.email))
    if user is None:
        raise HTTTPError.BAD_EMAIL_400

    recovery_code = create_recovery_code()

    await request.app.smtp.send_email(forgot.email, recovery_code)
    await request.app.redis.add_email_code(forgot.email, recovery_code)

    return Response(status_code=status.HTTP_200_OK)


@router.post(
    path="/reset_password",
    summary="Reset a password",
    description="Reset a password by recovery code in email",
    response_description="HTTP 204 STATUS",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=PasswdResponse.reset_password_post,
)
async def reset_password(request: Request, reset: ResetPassword):
    recovery_code = await request.app.redis.get_email_code(reset.email)
    if not recovery_code:
        raise HTTTPError.LACK_OF_EMAIL_IN_FORGOTTEN_400

    if recovery_code != reset.code:
        raise HTTTPError.BAD_RECOVERY_CODE_400

    check = await PasswdRepository.update_password_by_email(email=str(reset.email), password=reset.password)
    if not check:
        raise HTTTPError.BAD_EMAIL_400

    await request.app.redis.del_email_code(reset.email)

    return Response(status_code=status.HTTP_200_OK)
