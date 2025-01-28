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
from .schemas import UserCreate, UserRead, Token, UserInfo
from .service import UserRepository


router = APIRouter(prefix="/auth", tags=["Auth 🙎🏻‍♂️"])


@router.post(
    path="/register",
    summary="UserCreate registration",
    description="UserCreate registration",
    response_description="HTTP 201 STATUS",
    status_code=status.HTTP_201_CREATED
)
async def register_user(user_data: UserCreate):
    try:
        user_data.password = get_password_hash(user_data.password)
        await UserRepository.add_user(user_data)
        return Response(status_code=status.HTTP_201_CREATED)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверная почта или пароль")

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
    status_code=status.HTTP_200_OK,
    response_model=UserInfo
)
async def get_me(user_data: UserInfo = Depends(get_current_user)):
    return user_data
