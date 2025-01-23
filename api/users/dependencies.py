from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt, ExpiredSignatureError
from .auth import SECRET_KEY_JWT, ALGORITHM, create_access_token
from .service import UserRepository


http_bearer = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    """Retrieves the current user based on the provided JWT token.

    Args:
        credentials: The HTTP authorization credentials containing the JWT token.

    Returns:
        A User, the user object corresponding to the valid JWT token.

    Raises:
        HTTPException: If the JWT token is expired, invalid, or if the user ID is not found or the user does not exist.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Access token expired')
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid access token!')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=401, detail='User ID not found')

    user = await UserRepository.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail='User not found')

    return user


async def refresh_access_token(refresh_token: str):
    """Refreshes the access token using a provided refresh token.

    Args:
        refresh_token (str): The refresh token used to generate a new access token.

    Returns:
        A str, new access token.

    Raises:
        HTTPException: If the refresh token is expired, invalid, or if the user ID is not found or the user does not exist.
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Refresh token expired')
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid refresh token')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=401, detail='User ID not found')

    user = await UserRepository.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail='User not found')

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
