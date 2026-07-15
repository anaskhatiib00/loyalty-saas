from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class BusinessSettings(Base):
    __tablename__ = "business_settings"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    business_id: Mapped[int] = mapped_column(
        ForeignKey(
            "businesses.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    default_country_code: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
    )

    currency_override: Mapped[str | None] = mapped_column(
        String(3),
        nullable=True,
    )

    timezone_override: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    locale_override: Mapped[str | None] = mapped_column(
        String(16),
        nullable=True,
    )

    business = relationship(
        "Business",
        back_populates="settings",
    )