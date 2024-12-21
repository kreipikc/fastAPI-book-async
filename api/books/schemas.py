from typing import Optional
from pydantic import BaseModel


class BookCreate(BaseModel):
    name: str
    description: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Example1",
                    "description": "Example2",
                }
            ]
        }
    }


class BookRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "Example1",
                    "description": "Example2",
                }
            ]
        }
    }