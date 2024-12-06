from typing import Optional
from app.database import Model
from sqlalchemy.orm import Mapped, mapped_column


class BookOrm(Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]