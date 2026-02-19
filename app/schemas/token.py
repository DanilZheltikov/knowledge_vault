from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class Token(AccessToken):
    refresh_token: Optional[str] = None


class RefreshTokenCreate(BaseModel):
    hashed_token: str
    user_id: int
    expires: datetime
