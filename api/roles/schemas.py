from pydantic import BaseModel, Field


class RoleRead(BaseModel):
    id: int = Field(description="ID роли")
    role_type: str = Field(description="Название роли")


class RoleCreate(BaseModel):
    role_type: str = Field(description="Название роли")