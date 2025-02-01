from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt, ExpiredSignatureError
from .auth import SECRET_KEY_JWT, ALGORITHM, create_access_token
from .database import UsersOrm
from .responses.http_errors import HTTTPError
from .schemas import UserInfo
from .service import UserRepository


http_bearer = HTTPBearer()


async def descript_and_check_token(token: str) -> UsersOrm:
    """Decodes and validates a JWT token, retrieves the corresponding user, and checks the user's status.

    Args:
        token (str): The JWT token to be decoded and validated.

    Returns:
        A UsersOrm, the user object corresponding to the validated token.

    Raises:
        HTTTPError.BAD_CREDENTIALS_403: If the token has expired.
        HTTTPError.INVALID_TOKEN_401: If the token is invalid or does not contain a user ID.
        HTTTPError.DATA_OUT_OF_DATE_403: If the user corresponding to the token does not exist.
        HTTTPError.USER_NOT_ACTIVE_403: If the user corresponding to the token is not active.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTTPError.BAD_CREDENTIALS_403
    except JWTError:
        raise HTTTPError.INVALID_TOKEN_401

    user_id = payload.get('sub')
    if not user_id:
        raise HTTTPError.INVALID_TOKEN_401

    user = await UserRepository.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTTPError.DATA_OUT_OF_DATE_403

    if not user.is_active:
        raise HTTTPError.USER_NOT_ACTIVE_403

    return user


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> UserInfo:
    """Retrieves the current user based on the provided JWT token.

    Args:
        credentials (HTTPAuthorizationCredentials): The HTTP authorization credentials containing the JWT token.

    Returns:
        UserInfo: The user object corresponding to the valid JWT token.
    """
    token = credentials.credentials

    user = await descript_and_check_token(token)

    return UserInfo.model_validate(user.__dict__)


async def refresh_access_token(refresh_token: str) -> str:
    """Refreshes the access token using a provided refresh token.

    Args:
        refresh_token (str): The refresh token used to generate a new access token.

    Returns:
        A str, new access token.
    """
    user = await descript_and_check_token(refresh_token)

    new_access_token = create_access_token({"sub": str(user.id)})
    return new_access_token


# # Проверка на роль студента
# async def get_current_student(current_user: UserCreate = Depends(get_current_user)):
#     """Checks if the current user has the role of a student.
#
#     Args:
#         current_user: The current user object retrieved from the dependency.
#
#     Returns:
#         A UserCreate, the current user object if they have the role of a student.
#
#     Raises:
#         HTTPException: If the current user does not have the role of a student, raises a 403 Forbidden exception.
#     """
#     if current_user.is_student:
#         return current_user
#     raise HTTPException(status_code=403, detail='Недостаточно прав!')
#
#
# # Проверка на роль учителя
# async def get_current_teacher(current_user: UserCreate = Depends(get_current_user)):
#     """Checks if the current user has the role of a teacher.
#
#     Args:
#         current_user (UserCreate): The current user object retrieved from the dependency.
#
#     Returns:
#         A UserCreate, the current user object if they have the role of a teacher.
#
#     Raises:
#         HTTPException: If the current user does not have the role of a teacher, raises a 403 Forbidden exception.
#     """
#     if current_user.is_teacher:
#         return current_user
#     raise HTTPException(status_code=403, detail='Недостаточно прав!')
