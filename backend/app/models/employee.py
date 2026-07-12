from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, unique=True)

    full_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    role = Column(String, default="cashier")
    status = Column(String, default="active")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    business = relationship("Business")
    location = relationship("Location")
    