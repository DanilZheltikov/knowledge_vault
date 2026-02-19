from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.security import authenticate_user, get_refresh_token_from_cookie
from app.core.utils import set_refresh_cookie
from app.schemas.token import AccessToken
from app.schemas.user import UserCreate, UserRead
from app.service.user import user_create_service
from app.service.token import rotate_refresh_token_service

router = APIRouter()

FormDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]
RefreshTokenDep = Annotated[str, Depends(get_refresh_token_from_cookie)]
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post('/register', response_model=UserRead)
async def register_user(user: UserCreate, session: SessionDep):
    new_user = await user_create_service(user_in=user, session=session)
    return new_user


@router.post('/login', response_model=AccessToken)
async def login(
    form_data: FormDataDep,
    session: SessionDep,
    response: Response
):
    token = await authenticate_user(
        email=form_data.username,
        password=form_data.password,
        session=session
    )
    set_refresh_cookie(response, token.refresh_token)
    return token


@router.post('/refresh', response_model=AccessToken)
async def rotate_refresh_token(
    token: RefreshTokenDep,
    session: SessionDep,
    response: Response
):
    tokens = await rotate_refresh_token_service(token=token, session=session)
    set_refresh_cookie(response, tokens.refresh_token)
    return tokens
