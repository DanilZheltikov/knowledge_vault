from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.refresh_token import RefreshToken


class User(Base):
    email: Mapped[str] = mapped_column(String(150), unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_stuff: Mapped[bool] = mapped_column(Boolean, default=False)
    refresh_token: Mapped['RefreshToken'] = relationship(
        back_populates='user',
        cascade='delete'
    )
