from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from .books.router import router as books_router
from .roles.service import RoleRepository
from .users.router import router as auth_router
from .admin.router import router as admin_router
from .roles.router import router as role_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Запуск")
    await RoleRepository.create_default_roles()
    print("Таблица roles - готова")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(books_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(role_router)


@app.get("/")
async def go_to_docs():
    return RedirectResponse(url="/docs", status_code=status.HTTP_308_PERMANENT_REDIRECT)