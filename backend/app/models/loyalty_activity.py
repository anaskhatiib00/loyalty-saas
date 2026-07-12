from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class LoyaltyActivity(Base):
    __tablename__ = "loyalty_activities"

    # ------------------------------------------------------------------
    # Database constraints and query indexes
    # ------------------------------------------------------------------

    __table_args__ = (
        UniqueConstraint(
            "business_id",
            "idempotency_key",
            name="uq_loyalty_activities_business_id_idempotency_key",
        ),
        Index(
            "ix_loyalty_activities_business_created_at",
            "business_id",
            "created_at",
        ),
        Index(
            "ix_loyalty_activities_employee_created_at",
            "employee_id",
            "created_at",
        ),
        Index(
            "ix_loyalty_activities_location_created_at",
            "location_id",
            "created_at",
        ),
        Index(
            "ix_loyalty_activities_customer_created_at",
            "customer_id",
            "created_at",
        ),
    )

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ------------------------------------------------------------------
    # Tenant and operational context
    # ------------------------------------------------------------------

    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False,
    )
    location_id = Column(
        Integer,
        ForeignKey("locations.id"),
        nullable=False,
    )
    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Customer and loyalty context
    # ------------------------------------------------------------------

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
    )
    loyalty_card_id = Column(
        Integer,
        ForeignKey("loyalty_cards.id"),
        nullable=False,
    )
    loyalty_program_id = Column(
        Integer,
        ForeignKey("loyalty_programs.id"),
        nullable=True,
    )
    reward_id = Column(
        Integer,
        ForeignKey("rewards.id"),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Event classification
    # ------------------------------------------------------------------

    event_type = Column(
        String,
        nullable=False,
        default="progress_added",
        server_default="progress_added",
    )
    activity_type = Column(
        String,
        nullable=False,
    )
    source = Column(
        String,
        nullable=False,
        default="manager_dashboard",
        server_default="manager_dashboard",
    )
    status = Column(
        String,
        nullable=False,
        default="completed",
        server_default="completed",
    )

    # ------------------------------------------------------------------
    # Transaction inputs
    # ------------------------------------------------------------------

    purchase_amount = Column(
        Float,
        nullable=False,
        default=0,
        server_default="0",
    )
    qualifying_quantity = Column(
        Integer,
        nullable=False,
        default=1,
        server_default="1",
    )

    # ------------------------------------------------------------------
    # Progress result
    # ------------------------------------------------------------------

    progress_change = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    balance_before = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    balance_after = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    # ------------------------------------------------------------------
    # Immutable historical snapshots
    # ------------------------------------------------------------------

    customer_name_snapshot = Column(
        String,
        nullable=True,
    )
    employee_name_snapshot = Column(
        String,
        nullable=True,
    )
    location_name_snapshot = Column(
        String,
        nullable=True,
    )
    program_name_snapshot = Column(
        String,
        nullable=True,
    )
    reward_name_snapshot = Column(
        String,
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Reliability and audit metadata
    # ------------------------------------------------------------------

    idempotency_key = Column(
        String,
        nullable=True,
    )
    note = Column(
        String,
        nullable=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # ------------------------------------------------------------------
    # ORM relationships
    # ------------------------------------------------------------------

    customer = relationship("Customer")
    employee = relationship("Employee")
    location = relationship("Location")
    loyalty_program = relationship("LoyaltyProgram")
    reward = relationship("Reward")

    loyalty_card = relationship(
        "LoyaltyCard",
        back_populates="activities",
    )