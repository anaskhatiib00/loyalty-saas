"""Rename external id to provider reference

Revision ID: 0234050789cf
Revises: 8f941d9b8da1
Create Date: 2026-06-30 22:25:32.023155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0234050789cf'
down_revision: Union[str, Sequence[str], None] = '8f941d9b8da1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "credentials",
        "external_id",
        new_column_name="provider_reference",
    )
    op.drop_index("ix_wallet_passes_id", table_name="credentials")
    op.create_index("ix_credentials_id", "credentials", ["id"])


def downgrade() -> None:
    op.drop_index("ix_credentials_id", table_name="credentials")
    op.create_index("ix_wallet_passes_id", "credentials", ["id"])
    op.alter_column(
        "credentials",
        "provider_reference",
        new_column_name="external_id",
    )