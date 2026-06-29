from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class WalletPass(Base):
    __tablename__ = "wallet_passes"

    id = Column(Integer, primary_key=True, index=True)

    loyalty_card_id = Column(
        Integer,
        ForeignKey("loyalty_cards.id"),
        nullable=False,
    )

    provider = Column(String, nullable=False)

    external_id = Column(String, nullable=True)
    authentication_token = Column(String, nullable=True)

    status = Column(String, default="pending")

    last_synced_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    loyalty_card = relationship(
        "LoyaltyCard",
        back_populates="wallet_passes",
    )