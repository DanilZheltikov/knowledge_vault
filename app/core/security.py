from datetime import datetime, timedelta, timezone
from hashlib import sha256

import jwt

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.utils import verify_password
from app.crud.refresh_token import refresh_token_crud
from app.crud.user import user_crud
from app.models import User
from app.schemas.token import RefreshToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


def create_jwt(token_type: str, token_data: dict) -> str:
    jwt_payload = {
        'token_type': token_type,
        'iat': datetime.now(tz=timezone.utc)
    }
    jwt_payload.update(token_data)
    return jwt.encode(
        payload=jwt_payload,
        key=settings.secret_key,
        algorithm=settings.algorithm
    )


def create_access_token(
    subject: str,
    expires_minutes: int = settings.access_token_expire_minutes
) -> str:
    expire = (
        datetime.now(tz=timezone.utc)
        + timedelta(minutes=expires_minutes)
    )
    jwt_payload = {
        'exp': expire,
        'sub': subject
    }

    return create_jwt(token_type='access', token_data=jwt_payload)


async def create_refresh_token(
    subject: str,
    session: AsyncSession,
    expires_minutes: int = settings.refresh_token_expire_minutes
) -> str:
    expire = (
        datetime.now(tz=timezone.utc)
        + timedelta(minutes=expires_minutes)
    )
    jwt_payload = {
        'exp': expire,
        'sub': subject
    }
    refresh_token = create_jwt(token_type='refresh', token_data=jwt_payload)
    user = await user_crud.get_user_by_email(email=subject, session=session)

    await refresh_token_crud.create(
        obj_in=RefreshToken(
            user_id=user.id,
            hashed_token=sha256(refresh_token.encode()).hexdigest(),
            expires=expire
        ),
        session=session
    )
    return refresh_token


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
