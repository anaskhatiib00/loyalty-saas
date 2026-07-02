from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class AppleWalletRegistration(Base):
    __tablename__ = "apple_wallet_registrations"

    id = Column(Integer, primary_key=True, index=True)

    credential_id = Column(Integer, ForeignKey("credentials.id"), nullable=False)

    device_library_identifier = Column(String, nullable=False)
    push_token = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    last_updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    credential = relationship(
        "Credential",
        back_populates="registrations",
    )