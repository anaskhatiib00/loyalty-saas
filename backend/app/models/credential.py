from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base

from sqlalchemy import UniqueConstraint

class Credential(Base):
    __tablename__ = "credentials"
    __table_args__ = (
    UniqueConstraint(
        "loyalty_card_id",
        "provider",
        name="uq_credential_card_provider",
    ),
    )   

    id = Column(Integer, primary_key=True, index=True)

    loyalty_card_id = Column(
        Integer,
        ForeignKey("loyalty_cards.id"),
        nullable=False,
    )

    provider = Column(String, nullable=False)

    provider_reference = Column(String, nullable=True)
    storage_path = Column(String, nullable=True)
    authentication_token = Column(String, nullable=True)

    status = Column(String, default="pending")

    last_synced_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    loyalty_card = relationship(
        "LoyaltyCard",
        back_populates="credentials",
    )

    registrations = relationship(
    "AppleWalletRegistration",
    back_populates="credential",
    )