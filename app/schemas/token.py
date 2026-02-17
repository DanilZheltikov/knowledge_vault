from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = 'bearer'


class RefreshToken(BaseModel):
    hashed_token: str
    user_id: int
    expires: datetime
