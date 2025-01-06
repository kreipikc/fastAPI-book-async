from fastapi import Request, HTTPException, Depends
from jose import JWTError, jwt, ExpiredSignatureError
from .auth import SECRET_KEY_JWT, ALGORITHM, create_access_token
from .schemas import UserCreate
from .service import UserRepository, is_token_invalidated


def get_token(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        raise HTTPException(status_code=401, detail='Authorization header not found')

    token_type, token = auth_header.split()
    if token_type.lower() != 'bearer':
        raise HTTPException(status_code=401, detail='Invalid token type')

    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Access token expired')
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid access token!')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=401, detail='UserCreate ID not found')

    user = await UserRepository.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail='UserCreate not found')

    return user


async def refresh_access_token(refresh_token: str = Depends(get_token)):
    if await is_token_invalidated(refresh_token):
        raise HTTPException(status_code=401, detail='Refresh token is invalidated')

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Refresh token expired')
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid refresh token')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=401, detail='UserCreate ID not found')

    user = await UserRepository.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail='UserCreate not found')

    new_access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": new_access_token}



# Проверка на роль студента
async def get_current_student(current_user: UserCreate = Depends(get_current_user)):
    if current_user.is_student:
        return current_user
    raise HTTPException(status_code=403, detail='Недостаточно прав!')


# Проверка на роль учителя
async def get_current_teacher(current_user: UserCreate = Depends(get_current_user)):
    if current_user.is_teacher:
        return current_user
    raise HTTPException(status_code=403, detail='Недостаточно прав!')


# Проверка на роль админа
async def get_current_admin_user(current_user: UserCreate = Depends(get_current_user)):
    if current_user.is_admin:
        return current_user
    raise HTTPException(status_code=403, detail='Недостаточно прав!')
