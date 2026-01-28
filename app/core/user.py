from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import oauth2_scheme, authenticate_user_from_token


async def get_current_user(
    token: Annotated[str, oauth2_scheme],
    session: AsyncSession
):
    user = await authenticate_user_from_token(token, session)
    return user
