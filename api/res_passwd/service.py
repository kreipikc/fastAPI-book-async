from sqlalchemy import select
from ..database import new_session
from ..users.auth import get_password_hash
from ..users.database import UsersOrm


class PasswdRepository:
    @classmethod
    async def update_password_by_email(cls, email: str, password: str) -> bool:
        """Updates the password for a user identified by email.

        Args:
            email (str): The email of the user whose password needs to be updated.
            password (str): The new password to set for the user.

        Returns:
            A bool, True if the password was successfully updated, False if the user was not found.
        """
        async with new_session() as session:
            result = await session.execute(select(UsersOrm).where(UsersOrm.email == email))
            user = result.scalar_one_or_none()

            if user:
                hashed_password = get_password_hash(password)
                user.password = hashed_password
                await session.commit()
                return True
            else:
                return False