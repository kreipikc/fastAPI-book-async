from pydantic import BaseModel, Field


class RoleRead(BaseModel):
    id: int = Field(description="ID роли для изменения")
    role_type: str = Field(description="Новое роли")


class RoleCreate(BaseModel):
    role_type: str = Field(description="Название новой роли")