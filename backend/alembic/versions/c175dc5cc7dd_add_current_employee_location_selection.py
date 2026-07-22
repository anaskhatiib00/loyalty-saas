"""add current employee location selection

Revision ID: c175dc5cc7dd
Revises: e3f3b0186e2a
Create Date: 2026-07-22 02:28:33.831077
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c175dc5cc7dd"
down_revision: Union[str, Sequence[str], None] = "e3f3b0186e2a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add employee current location selection."""

    op.add_column(
        "employee_locations",
        sa.Column(
            "is_current",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
    )

    op.create_check_constraint(
        "ck_employee_locations_current_requires_active",
        "employee_locations",
        "(NOT is_current) OR is_active",
    )

    op.create_index(
        "uq_employee_locations_current_employee",
        "employee_locations",
        ["employee_id"],
        unique=True,
        postgresql_where=sa.text("is_current = true"),
    )


def downgrade() -> None:
    """Remove employee current location selection."""

    op.drop_index(
        "uq_employee_locations_current_employee",
        table_name="employee_locations",
        postgresql_where=sa.text("is_current = true"),
    )

    op.drop_constraint(
        "ck_employee_locations_current_requires_active",
        "employee_locations",
        type_="check",
    )

    op.drop_column(
        "employee_locations",
        "is_current",
    )