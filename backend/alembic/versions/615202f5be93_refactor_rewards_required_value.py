"""Refactor rewards required value

Revision ID: 615202f5be93
Revises: 871d8ee98af0
Create Date: 2026-06-27 13:51:26.591436

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '615202f5be93'
down_revision: Union[str, Sequence[str], None] = '871d8ee98af0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "rewards",
        "points_required",
        new_column_name="required_value",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "rewards",
        "required_value",
        new_column_name="points_required",
    )