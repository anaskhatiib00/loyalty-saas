from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)

    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False,
    )

    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=False)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)

    is_default = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    business = relationship(
        "Business",
        back_populates="locations",
    )

    employee_assignments = relationship(
        "EmployeeLocation",
        back_populates="location",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
