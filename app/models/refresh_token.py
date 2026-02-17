from datetime import datetime, timezone

from sqlalchemy import String, ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class RefreshToken(Base):
    hashed_token: Mapped[str] = mapped_column(String, unique=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(ondelete='CASCADE')
    )
    expires: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    