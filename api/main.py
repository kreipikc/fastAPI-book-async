from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from .books.router import router as books_router
from .res_passwd.redis import RedisDB
from .res_passwd.smtp import SmtpTools
from .roles.service import RoleRepository
from .users.router import router as auth_router
from .admin.router import router as admin_router
from .roles.router import router as role_router
from .res_passwd.router import router as res_passwd_router
from .config import (
    REDIS_URL,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_EMAIL,
    SMTP_PASSWORD
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await RoleRepository.create_default_roles()
    print("Table 'roles' ready")

    app.redis = RedisDB(url=REDIS_URL)
    print("Redis ready")

    app.smtp = SmtpTools(SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD)
    print("Smtp ready")

    try:
        yield
    finally:
        await app.redis.close()
        app.smtp.__del__()


app = FastAPI(lifespan=lifespan)
app.include_router(books_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(role_router)
app.include_router(res_passwd_router)


@app.get("/")
async def go_to_docs():
    return RedirectResponse(url="/docs", status_code=status.HTTP_308_PERMANENT_REDIRECT)