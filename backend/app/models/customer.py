from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)

    current_progress = Column(Integer, default=0)
    total_rewards_redeemed = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    business = relationship("Business", back_populates="customers")
    loyalty_card = relationship("LoyaltyCard", back_populates="customer", uselist=False)