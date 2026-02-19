from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.user import User


class UserCRUD(CRUDBase):
    async def get_user_by_email(
        self,
        email: str,
        session: AsyncSession,
    ) -> Optional[User]:
        stmt = select(User).where(email == User.email)
        user = await session.execute(stmt)
        return user.scalars().first()


user_crud = UserCRUD(User)
