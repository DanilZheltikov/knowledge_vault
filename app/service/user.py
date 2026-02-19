from sqlalchemy.ext.asyncio import AsyncSession

from app.core import exceptions
from app.core.utils import get_password_hash
from app.crud.user import user_crud
from app.models import User
from app.schemas.user import UserCreate


async def user_create_service(
    user_in: UserCreate,
    session: AsyncSession
) -> User:
    if await user_crud.get_user_by_email(user_in.email, session=session):
        raise exceptions.UserExistsException
    hashed_password = get_password_hash(password=user_in.password)
    new_user_data = user_in.model_dump(exclude={'password'})
    new_user_data['password'] = hashed_password
    new_user_schema = UserCreate(**new_user_data)
    return await user_crud.create(obj_in=new_user_schema, session=session)
