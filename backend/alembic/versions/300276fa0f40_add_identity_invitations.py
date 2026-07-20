"""add identity invitations

Revision ID: 300276fa0f40
Revises: 8f481a443f63
Create Date: 2026-07-20 04:57:37.809743
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "300276fa0f40"
down_revision: Union[str, Sequence[str], None] = "8f481a443f63"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "identity_invitations",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "business_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "employee_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "email",
            sa.String(length=320),
            nullable=False,
        ),
        sa.Column(
            "role",
            sa.String(length=32),
            nullable=False,
        ),
        sa.Column(
            "token_hash",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=32),
            server_default="pending",
            nullable=False,
        ),
        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "created_by_user_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "accepted_user_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "accepted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "revoked_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'accepted', 'revoked', 'expired')",
            name="ck_identity_invitations_status",
        ),
        sa.ForeignKeyConstraint(
            ["accepted_user_id"],
            ["users.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["business_id"],
            ["businesses.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["created_by_user_id"],
            ["users.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["employee_id"],
            ["employees.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "token_hash",
            name="uq_identity_invitations_token_hash",
        ),
    )

    op.create_index(
        "ix_identity_invitations_business_email",
        "identity_invitations",
        ["business_id", "email"],
        unique=False,
    )

    op.create_index(
        "ix_identity_invitations_business_status",
        "identity_invitations",
        ["business_id", "status"],
        unique=False,
    )

    op.create_index(
        "ix_identity_invitations_employee_id",
        "identity_invitations",
        ["employee_id"],
        unique=False,
    )

    op.create_index(
        "ix_identity_invitations_expires_at",
        "identity_invitations",
        ["expires_at"],
        unique=False,
    )

    op.create_index(
        "ix_identity_invitations_id",
        "identity_invitations",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_identity_invitations_id",
        table_name="identity_invitations",
    )

    op.drop_index(
        "ix_identity_invitations_expires_at",
        table_name="identity_invitations",
    )

    op.drop_index(
        "ix_identity_invitations_employee_id",
        table_name="identity_invitations",
    )

    op.drop_index(
        "ix_identity_invitations_business_status",
        table_name="identity_invitations",
    )

    op.drop_index(
        "ix_identity_invitations_business_email",
        table_name="identity_invitations",
    )

    op.drop_table("identity_invitations")