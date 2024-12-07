import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt


load_dotenv()
SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")
ALGORITHM = os.getenv("ALGORITHM")
if SECRET_KEY_JWT is None:
    raise ValueError("SECRET_KEY_JWT environment variable not set")
if ALGORITHM is None:
    raise ValueError("ALGORITHM environment variable not set")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(default_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(default_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY_JWT, algorithm=ALGORITHM)
    return encode_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY_JWT, algorithm=ALGORITHM)
    return encode_jwt