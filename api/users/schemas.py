from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr = Field(description="Электронная почта")
    password: str = Field(min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    phone_number: str = Field(description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "example@example.com",
                    "password": "example_password",
                    "phone_number": "+79999999999",
                    "first_name": "Example1",
                    "last_name": "Example2",
                }
            ]
        }
    }


class UserRead(BaseModel):
    email: EmailStr = Field(description="Электронная почта")
    password: str = Field(min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "example@example.com",
                    "password": "example_password",
                }
            ]
        }
    }