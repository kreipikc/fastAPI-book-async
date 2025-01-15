from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    Request,
    Response,
)
from .auth import get_password_hash, create_access_token, create_refresh_token
from .dependencies import get_current_user, refresh_access_token
from .schemas import UserCreate, UserRead, Token
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
    description="Authorization in the application",
    response_description="Access token (Bearer) and refresh token (Cookie)",
    status_code=status.HTTP_200_OK,
    response_model=Token,
)
async def auth_user(response: Response, user_data: UserRead):
    check = await UserRepository.authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверная почта или пароль')

    access_token = create_access_token(data={"sub": str(check.id)})
    create_refresh_token(response=response, data={"sub": str(check.id)})

    return Token(access_token=access_token, token_type="Bearer")


@router.post(
    path="/refresh",
    summary="Refresh access token",
    description="Refresh access token",
    response_description="Bearer Token (Access)",
    status_code=status.HTTP_200_OK,
    response_model=Token,
)
async def refresh_token_endpoint(request: Request):
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise ValueError("Refresh token not found")

        access_token = await refresh_access_token(refresh_token=refresh_token)
        return Token(access_token=access_token, token_type="Bearer")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.__str__())


@router.post(
    path="/logout",
    summary="Logout account",
    description="Logout account",
    response_description="HTTP 204 STATUS",
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout_user(response: Response):
    response.delete_cookie(
        key="refresh_token",
        secure=False,
        httponly=True,
    )
    response.status_code = status.HTTP_200_OK
    return response


@router.get(
    path="/me",
    summary="Information about you",
    description="Information about you",
    response_description="User info",
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