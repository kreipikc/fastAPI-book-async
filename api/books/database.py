from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Model


class BookOrm(Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]