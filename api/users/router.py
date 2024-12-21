from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import Response
from .auth import get_password_hash, create_access_token, create_refresh_token
from .dependencies import get_current_user, refresh_access_token
from .schemas import UserCreate, UserRead
from .service import UserRepository
from .dependencies import get_current_admin_user


router = APIRouter(prefix="/auth", tags=["Auth 🙎🏻‍♂️"])


@router.post(
    path="/register",
    summary="UserCreate registration",
    description="UserCreate registration",
    response_description="HTTP 201 STATUS",
    status_code=status.HTTP_201_CREATED
)
async def register_user(user_data: UserCreate):
    user = await UserRepository.find_one_or_none(user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пользователь уже существует')
    user_data.password = get_password_hash(user_data.password)
    await UserRepository.add_user(user_data)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post(
    path="/login",
    summary="Login for user",
    description="Login for user",
    response_description="HTTP 200 STATUS",
    status_code=status.HTTP_200_OK
)
async def auth_user(response: Response, user_data: UserRead):
    check = await UserRepository.authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверная почта или пароль')

    access_token = create_access_token({"sub": str(check.id)})
    refresh_token = create_refresh_token({"sub": str(check.id)})

    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    response.set_cookie(key="users_refresh_token", value=refresh_token, httponly=True)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post(
    path="/refresh",
    summary="Refresh access token",
    description="Refresh access token",
    response_description="A JSON object containing the new access token and its type",
    status_code=status.HTTP_200_OK
)
async def refresh_token_endpoint(response: Response, new_token: dict = Depends(refresh_access_token)):
    response.set_cookie(key="users_access_token", value=new_token["access_token"], httponly=True)
    return new_token


@router.post(
    path="/logout",
    summary="Logout account",
    description="Logout account",
    response_description="HTTP 204 STATUS",
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    response.delete_cookie(key="users_refresh_token")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    path="/me",
    summary="Information about you",
    description="Information about you",
    response_description="UserCreate info",
    status_code=status.HTTP_200_OK
)
async def get_me(user_data: UserCreate = Depends(get_current_user)):
    return user_data


# Ниже приведены endpoints для role: Admin
@router.get(
    path="/all_users",
    summary="Information about all users",
    description="Information about all users",
    response_description="The all users",
    status_code=status.HTTP_200_OK
)
async def get_all_users(user_data: UserCreate = Depends(get_current_admin_user)):
    return await UserRepository.find_all_user()


@router.put(
    path="/update_user_role",
    summary="Update role for user",
    description="Update role for user",
    response_description="HTTP 200 STATUS",
    status_code=status.HTTP_200_OK
)
async def update_user_role(id_user: int, role: str, user_data: UserCreate = Depends(get_current_admin_user)):
    await UserRepository.change_role(id_user, role)
    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    path="/delete_user",
    summary="Delete user",
    description="Delete user",
    response_description="HTTP 204 STATUS",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(id_user: int, user_data: UserCreate = Depends(get_current_admin_user)):
    await UserRepository.delete_user_by_id(id_user)
    return Response(status_code=status.HTTP_200_OK)