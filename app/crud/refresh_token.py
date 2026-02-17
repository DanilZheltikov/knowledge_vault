from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import RefreshToken


class RefreshTokenCRUD(CRUDBase):
    pass


refresh_token_crud = RefreshTokenCRUD(RefreshToken)
