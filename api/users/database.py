from ..database import Model
from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..roles.database import RolesOrm # Для того чтобы alembic нашел таблицу roles для связи


class UsersOrm(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), default=1)
    roles = relationship(argument="RolesOrm", back_populates="users")

    extend_existing = True