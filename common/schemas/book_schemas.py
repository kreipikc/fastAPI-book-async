from typing import Optional
from pydantic import BaseModel, ConfigDict

class SBookAdd(BaseModel):
    name: str
    description: Optional[str] = None

class SBook(SBookAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)