from ..database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship


class RolesOrm(Model):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    role_type: Mapped[str] = mapped_column(unique=True)

    users = relationship(argument="UsersOrm", back_populates="roles")