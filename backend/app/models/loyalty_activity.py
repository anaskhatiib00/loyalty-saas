from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class LoyaltyActivity(Base):
    __tablename__ = "loyalty_activities"

    id = Column(Integer, primary_key=True, index=True)

    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    loyalty_card_id = Column(Integer, ForeignKey("loyalty_cards.id"), nullable=False)

    activity_type = Column(String, nullable=False)
    status = Column(String, default="completed")

    purchase_amount = Column(Float, default=0)
    qualifying_quantity = Column(Integer, default=1)

    earned_progress = Column(Integer, default=0)
    balance_after = Column(Integer, default=0)

    note = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer")
    loyalty_card = relationship(
    "LoyaltyCard",
    back_populates="activities",
    )
    employee = relationship("Employee")