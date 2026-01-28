from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.security import create_access_token, authenticate_user
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
    token = create_access_token(user.email)
    token = Token(access_token=token)

    return token
