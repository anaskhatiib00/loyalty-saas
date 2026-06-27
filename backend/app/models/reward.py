from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    required_value = Column(Integer, nullable=False)

    reward_type = Column(String, default="discount")  # discount, free_item, cashback, custom
    reward_value = Column(String, nullable=True)
    redemption_behavior = Column(String, default="deduct")
    redemption_mode = Column(String, default="manual")
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    business = relationship("Business", back_populates="rewards")