from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.security import (
    authenticate_user,
    create_access_token,
    create_refresh_token
)
from app.crud.user import user_crud
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserRead

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
FormDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/register', response_model=UserRead)
async def register_user(user: UserCreate, session: SessionDep):
    new_user = await user_crud.create(user, session)
    return new_user


@router.post('/token', response_model=Token)
async def user_login(form_data: FormDataDep, session: SessionDep):
    user = await authenticate_user(
        form_data.username,
        form_data.password,
        session
    )
    access_token = create_access_token(user.email)
    refresh_token = await create_refresh_token(
        subject=user.email,
        session=session
    )
    token = Token(
        access_token=access_token,
        refresh_token=refresh_token
    )
    return token


@router.post('/refresh', response_model=Token)
async def rotate_refresh_token(token: str, session: SessionDep):
    pass
