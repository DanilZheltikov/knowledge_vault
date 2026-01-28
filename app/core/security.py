from datetime import datetime, timedelta, timezone

import jwt

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.utils import verify_password
from app.crud.user import user_crud
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


def create_access_token(
        subject: str,
        expires_minutes: int = settings.access_token_expire_minutes
) -> str:
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode = {'exp': expire, 'sub': str(subject)}
    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


async def authenticate_user_from_token(
    token: str,
    session: AsyncSession
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось проверить учетные данные',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=settings.algorithm,
        )
        email = payload.get('sub')

        if email is None:
            raise credentials_exception

    except jwt.InvalidTokenError:
        raise credentials_exception

    user = await user_crud.get_user_by_email(email=email, session=session)
    if not user:
        raise credentials_exception

    return user


async def authenticate_user(
    email: str,
    password: str,
    session: AsyncSession
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Неверный email или пароль',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    user = await user_crud.get_user_by_email(email=email, session=session)

    if not user:
        raise credentials_exception

    if not verify_password(password, user.hashed_password):
        raise credentials_exception

    return user
