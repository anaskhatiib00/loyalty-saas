"""add loyalty activity audit fields

Revision ID: d8ec706ce94e
Revises: 5517c5134105
Create Date: 2026-07-11 19:14:52.131114
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision: str = "d8ec706ce94e"
down_revision: Union[str, Sequence[str], None] = "5517c5134105"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------
    # Rename the existing progress field without losing historical data.
    # ------------------------------------------------------------------

    op.alter_column(
        "loyalty_activities",
        "earned_progress",
        new_column_name="progress_change",
        existing_type=sa.Integer(),
    )

    # ------------------------------------------------------------------
    # Add loyalty and reward context.
    # ------------------------------------------------------------------

    op.add_column(
        "loyalty_activities",
        sa.Column(
            "loyalty_program_id",
            sa.Integer(),
            nullable=True,
        ),
    )
    op.add_column(
        "loyalty_activities",
        sa.Column(
            "reward_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # ------------------------------------------------------------------
    # Add event classification and source fields.
    # The status column already exists in this database.
    # ------------------------------------------------------------------

    op.add_column(
        "loyalty_activities",
        sa.Column(
            "event_type",
            sa.String(),
            nullable=False,
            server_default="progress_added",
        ),
    )
    op.add_column(
        "loyalty_activities",
        sa.Column(
            "source",
            sa.String(),
            nullable=False,
            server_default="manager_dashboard",
        ),
    )

    # ------------------------------------------------------------------
    # Add progress audit values.
    # ------------------------------------------------------------------

    op.add_column(
        "loyalty_activities",
        sa.Column(
            "balance_before",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    # ------------------------------------------------------------------
    # Add immutable historical snapshots.
    # ------------------------------------------------------------------

    op.add_column(
        "loyalty_activities",
        sa.Column(
            "customer_name_snapshot",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "loyalty_activities",
        sa.Column(
            "employee_name_snapshot",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "loyalty_activities",
        sa.Column(
            "location_name_snapshot",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "loyalty_activities",
        sa.Column(
            "program_name_snapshot",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "loyalty_activities",
        sa.Column(
            "reward_name_snapshot",
            sa.String(),
            nullable=True,
        ),
    )

    # ------------------------------------------------------------------
    # Add reliability metadata.
    # ------------------------------------------------------------------

    op.add_column(
        "loyalty_activities",
        sa.Column(
            "idempotency_key",
            sa.String(),
            nullable=True,
        ),
    )

    # ------------------------------------------------------------------
    # Add foreign-key constraints.
    # ------------------------------------------------------------------

    op.create_foreign_key(
        "fk_loyalty_activities_loyalty_program_id",
        "loyalty_activities",
        "loyalty_programs",
        ["loyalty_program_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_loyalty_activities_reward_id",
        "loyalty_activities",
        "rewards",
        ["reward_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # ------------------------------------------------------------------
    # Backfill existing records.
    # ------------------------------------------------------------------

    op.execute(
        """
        UPDATE loyalty_activities AS activity
        SET loyalty_program_id = program.id
        FROM loyalty_programs AS program
        WHERE program.business_id = activity.business_id
          AND activity.loyalty_program_id IS NULL
        """
    )

    op.execute(
        """
        UPDATE loyalty_activities
        SET balance_before = GREATEST(
            balance_after - progress_change,
            0
        )
        """
    )

    op.execute(
        """
        UPDATE loyalty_activities AS activity
        SET customer_name_snapshot = TRIM(
            CONCAT_WS(
                ' ',
                customer.first_name,
                customer.last_name
            )
        )
        FROM customers AS customer
        WHERE customer.id = activity.customer_id
          AND activity.customer_name_snapshot IS NULL
        """
    )

    op.execute(
        """
        UPDATE loyalty_activities AS activity
        SET employee_name_snapshot = employee.full_name
        FROM employees AS employee
        WHERE employee.id = activity.employee_id
          AND activity.employee_name_snapshot IS NULL
        """
    )

    op.execute(
        """
        UPDATE loyalty_activities AS activity
        SET location_name_snapshot = location.name
        FROM locations AS location
        WHERE location.id = activity.location_id
          AND activity.location_name_snapshot IS NULL
        """
    )

    op.execute(
        """
        UPDATE loyalty_activities AS activity
        SET program_name_snapshot = program.name
        FROM loyalty_programs AS program
        WHERE program.id = activity.loyalty_program_id
          AND activity.program_name_snapshot IS NULL
        """
    )

    # ------------------------------------------------------------------
    # Add uniqueness and query-performance indexes.
    # ------------------------------------------------------------------

    op.create_unique_constraint(
        "uq_loyalty_activities_business_id_idempotency_key",
        "loyalty_activities",
        ["business_id", "idempotency_key"],
    )

    op.create_index(
        "ix_loyalty_activities_business_created_at",
        "loyalty_activities",
        ["business_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_loyalty_activities_employee_created_at",
        "loyalty_activities",
        ["employee_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_loyalty_activities_location_created_at",
        "loyalty_activities",
        ["location_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_loyalty_activities_customer_created_at",
        "loyalty_activities",
        ["customer_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    # ------------------------------------------------------------------
    # Remove indexes and constraints in reverse order.
    # ------------------------------------------------------------------

    op.drop_index(
        "ix_loyalty_activities_customer_created_at",
        table_name="loyalty_activities",
    )
    op.drop_index(
        "ix_loyalty_activities_location_created_at",
        table_name="loyalty_activities",
    )
    op.drop_index(
        "ix_loyalty_activities_employee_created_at",
        table_name="loyalty_activities",
    )
    op.drop_index(
        "ix_loyalty_activities_business_created_at",
        table_name="loyalty_activities",
    )

    op.drop_constraint(
        "uq_loyalty_activities_business_id_idempotency_key",
        "loyalty_activities",
        type_="unique",
    )
    op.drop_constraint(
        "fk_loyalty_activities_reward_id",
        "loyalty_activities",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_loyalty_activities_loyalty_program_id",
        "loyalty_activities",
        type_="foreignkey",
    )

    # ------------------------------------------------------------------
    # Remove fields introduced by this migration.
    # The pre-existing status column must remain untouched.
    # ------------------------------------------------------------------

    op.drop_column("loyalty_activities", "idempotency_key")
    op.drop_column("loyalty_activities", "reward_name_snapshot")
    op.drop_column("loyalty_activities", "program_name_snapshot")
    op.drop_column("loyalty_activities", "location_name_snapshot")
    op.drop_column("loyalty_activities", "employee_name_snapshot")
    op.drop_column("loyalty_activities", "customer_name_snapshot")
    op.drop_column("loyalty_activities", "balance_before")
    op.drop_column("loyalty_activities", "source")
    op.drop_column("loyalty_activities", "event_type")
    op.drop_column("loyalty_activities", "reward_id")
    op.drop_column("loyalty_activities", "loyalty_program_id")

    # ------------------------------------------------------------------
    # Restore the original progress column name.
    # ------------------------------------------------------------------

    op.alter_column(
        "loyalty_activities",
        "progress_change",
        new_column_name="earned_progress",
        existing_type=sa.Integer(),
    )