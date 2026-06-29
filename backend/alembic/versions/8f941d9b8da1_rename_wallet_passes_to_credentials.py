"""Rename wallet passes to credentials

Revision ID: 8f941d9b8da1
Revises: f5f0ad754ba9
Create Date: 2026-06-29 14:54:09.260762

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "8f941d9b8da1"
down_revision: Union[str, Sequence[str], None] = "f5f0ad754ba9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table("wallet_passes", "credentials")


def downgrade() -> None:
    """Downgrade schema."""
    op.rename_table("credentials", "wallet_passes")