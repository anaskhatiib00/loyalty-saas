"""Add user account link to employees

Revision ID: 5517c5134105
Revises: 863824adce01
Create Date: 2026-07-09
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5517c5134105"
down_revision: Union[str, Sequence[str], None] = "863824adce01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column(
        "employees",
        sa.Column("user_id", sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        "fk_employees_user_id_users",
        "employees",
        "users",
        ["user_id"],
        ["id"],
    )

    op.create_index(
        "ix_employees_user_id",
        "employees",
        ["user_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_employees_user_id", table_name="employees")
    op.drop_constraint(
        "fk_employees_user_id_users",
        "employees",
        type_="foreignkey",
    )
    op.drop_column("employees", "user_id")