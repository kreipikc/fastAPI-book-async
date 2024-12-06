from datetime import datetime, timezone
from fastapi import Request, HTTPException, Depends
from jose import JWTError, jwt
from app.users.auth import SECRET_KEY_JWT, ALGORITHM
from app.users.schemas import SUser
from app.users.service import UserRepository


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=401, detail='Token not found')
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail='Токен не валидный!')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)

    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=401, detail='Токен истек')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=401, detail='Не найден ID пользователя')

    user = await UserRepository.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail='User not found')

    return user


# Проверка на роль студента
async def get_current_student(current_user: SUser = Depends(get_current_user)):
    if current_user.is_student:
        return current_user
    raise HTTPException(status_code=403, detail='Недостаточно прав!')


# Проверка на роль учителя
async def get_current_teacher(current_user: SUser = Depends(get_current_user)):
    if current_user.is_teacher:
        return current_user
    raise HTTPException(status_code=403, detail='Недостаточно прав!')


# Проверка на роль админа
async def get_current_admin_user(current_user: SUser = Depends(get_current_user)):
    if current_user.is_admin:
        return current_user
    raise HTTPException(status_code=403, detail='Недостаточно прав!')
