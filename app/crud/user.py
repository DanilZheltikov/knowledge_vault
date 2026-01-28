from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import get_password_hash
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate


class UserCRUD(CRUDBase):
    async def create(self, obj_in: UserCreate, session: AsyncSession) -> User:
        hashed_password = get_password_hash(obj_in.password)
        new_user = User(email=obj_in.email, hashed_password=hashed_password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    async def get_user_by_email(
        self,
        email: str,
        session: AsyncSession,
    ) -> Optional[User]:
        stmt = select(User).where(email == User.email)
        user = await session.execute(stmt)
        return user.scalars().first()


user_crud = UserCRUD(User)
