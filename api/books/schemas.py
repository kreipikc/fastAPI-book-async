from typing import Optional
from pydantic import BaseModel


# Схема для валидации данных с помощью pydantic
class Book(BaseModel):
    name: str
    description: Optional[str] = None