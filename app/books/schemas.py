from typing import Optional
from pydantic import BaseModel


# Схема для валидации данных с помощью pydantic
class SBook(BaseModel):
    name: str
    description: Optional[str] = None