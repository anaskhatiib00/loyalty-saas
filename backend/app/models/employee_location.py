from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class EmployeeLocation(Base):
    __tablename__ = "employee_locations"

    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "location_id",
            name="uq_employee_locations_employee_location",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey(
            "employees.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    location_id = Column(
        Integer,
        ForeignKey(
            "locations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    assigned_by_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    assigned_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    is_primary = Column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        server_default="true",
        nullable=False,
    )

    employee = relationship(
        "Employee",
        back_populates="location_assignments",
    )

    location = relationship(
        "Location",
        back_populates="employee_assignments",
    )

    assigned_by_user = relationship("User")