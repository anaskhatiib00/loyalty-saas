from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class LoyaltyCard(Base):
    __tablename__ = "loyalty_cards"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, unique=True)

    card_number = Column(String, unique=True, index=True, nullable=False)
    public_id = Column(String, unique=True, index=True, nullable=False)

    status = Column(String, default="active")  # active, suspended, replaced

    apple_pass_url = Column(String, nullable=True)
    google_pass_url = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer", back_populates="loyalty_card")
    transactions = relationship("Transaction", back_populates="loyalty_card")