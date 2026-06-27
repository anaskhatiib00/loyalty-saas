from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class LoyaltyProgram(Base):
    __tablename__ = "loyalty_programs"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, unique=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    points_per_currency_unit = Column(Float, default=1.0)
    currency_unit = Column(String, default="USD")

    welcome_bonus_points = Column(Integer, default=0)
    birthday_bonus_points = Column(Integer, default=0)
    referral_bonus_points = Column(Integer, default=0)

    points_expire = Column(Boolean, default=False)
    expiration_months = Column(Integer, nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    business = relationship("Business", back_populates="loyalty_program")