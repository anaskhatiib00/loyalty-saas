"""add employee location assignments

Revision ID: e3f3b0186e2a
Revises: 300276fa0f40
Create Date: 2026-07-21 01:33:22.044587
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e3f3b0186e2a"
down_revision: Union[str, Sequence[str], None] = "300276fa0f40"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "employee_locations",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "employee_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "location_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "assigned_by_user_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "assigned_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "is_primary",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["assigned_by_user_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["employee_id"],
            ["employees.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["location_id"],
            ["locations.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "employee_id",
            "location_id",
            name="uq_employee_locations_employee_location",
        ),
    )

    op.create_index(
        "ix_employee_locations_assigned_by_user_id",
        "employee_locations",
        ["assigned_by_user_id"],
        unique=False,
    )

    op.create_index(
        "ix_employee_locations_employee_id",
        "employee_locations",
        ["employee_id"],
        unique=False,
    )

    op.create_index(
        "ix_employee_locations_id",
        "employee_locations",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_employee_locations_location_id",
        "employee_locations",
        ["location_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_employee_locations_location_id",
        table_name="employee_locations",
    )

    op.drop_index(
        "ix_employee_locations_id",
        table_name="employee_locations",
    )

    op.drop_index(
        "ix_employee_locations_employee_id",
        table_name="employee_locations",
    )

    op.drop_index(
        "ix_employee_locations_assigned_by_user_id",
        table_name="employee_locations",
    )

    op.drop_table("employee_locations")