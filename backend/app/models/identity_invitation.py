from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import IdentityInvitationStatus
from app.db.database import Base


class IdentityInvitation(Base):
    __tablename__ = "identity_invitations"

    __table_args__ = (
        UniqueConstraint(
            "token_hash",
            name="uq_identity_invitations_token_hash",
        ),
        CheckConstraint(
            "status IN ('pending', 'accepted', 'revoked', 'expired')",
            name="ck_identity_invitations_status",
        ),
        Index(
            "ix_identity_invitations_business_email",
            "business_id",
            "email",
        ),
        Index(
            "ix_identity_invitations_business_status",
            "business_id",
            "status",
        ),
        Index(
            "ix_identity_invitations_employee_id",
            "employee_id",
        ),
        Index(
            "ix_identity_invitations_expires_at",
            "expires_at",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    business_id = Column(
        Integer,
        ForeignKey(
            "businesses.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    employee_id = Column(
        Integer,
        ForeignKey(
            "employees.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    email = Column(
        String(320),
        nullable=False,
    )

    role = Column(
        String(32),
        nullable=False,
    )

    token_hash = Column(
        String(64),
        nullable=False,
    )

    status = Column(
        String(32),
        nullable=False,
        default=IdentityInvitationStatus.PENDING.value,
        server_default=IdentityInvitationStatus.PENDING.value,
    )

    expires_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_by_user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    accepted_user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    accepted_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    revoked_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    business = relationship(
        "Business",
        foreign_keys=[business_id],
    )

    employee = relationship(
        "Employee",
        foreign_keys=[employee_id],
    )

    created_by_user = relationship(
        "User",
        foreign_keys=[created_by_user_id],
    )

    accepted_user = relationship(
        "User",
        foreign_keys=[accepted_user_id],
    )
