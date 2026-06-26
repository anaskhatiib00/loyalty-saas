from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    loyalty_card_id = Column(Integer, ForeignKey("loyalty_cards.id"), nullable=False)

    transaction_type = Column(String, nullable=False)  # earn, redeem, adjust
    points = Column(Integer, nullable=False)
    description = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    loyalty_card = relationship("LoyaltyCard", back_populates="transactions")