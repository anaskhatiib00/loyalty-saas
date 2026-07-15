"""add business regional settings

Revision ID: 8f481a443f63
Revises: d8ec706ce94e
Create Date: 2026-07-15 06:04:04.819834
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8f481a443f63"
down_revision: Union[str, Sequence[str], None] = "d8ec706ce94e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "business_settings",
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
            "default_country_code",
            sa.String(length=2),
            nullable=False,
        ),
        sa.Column(
            "currency_override",
            sa.String(length=3),
            nullable=True,
        ),
        sa.Column(
            "timezone_override",
            sa.String(length=64),
            nullable=True,
        ),
        sa.Column(
            "locale_override",
            sa.String(length=16),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["business_id"],
            ["businesses.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "business_id",
            name="uq_business_settings_business_id",
        ),
    )

    op.create_index(
        "ix_business_settings_business_id",
        "business_settings",
        ["business_id"],
        unique=True,
    )

    op.create_index(
        "ix_business_settings_id",
        "business_settings",
        ["id"],
        unique=False,
    )

    op.execute(
        sa.text(
            """
            INSERT INTO business_settings (
                business_id,
                default_country_code,
                currency_override,
                timezone_override,
                locale_override
            )
            SELECT
                businesses.id,
                'JO',
                NULL,
                NULL,
                NULL
            FROM businesses
            WHERE NOT EXISTS (
                SELECT 1
                FROM business_settings
                WHERE business_settings.business_id = businesses.id
            )
            """
        )
    )


def downgrade() -> None:
    op.drop_index(
        "ix_business_settings_id",
        table_name="business_settings",
    )

    op.drop_index(
        "ix_business_settings_business_id",
        table_name="business_settings",
    )

    op.drop_table("business_settings")