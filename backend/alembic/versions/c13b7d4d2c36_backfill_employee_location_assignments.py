"""backfill employee location assignments

Revision ID: c13b7d4d2c36
Revises: c175dc5cc7dd
Create Date: 2026-07-24 04:17:50.263811
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "c13b7d4d2c36"
down_revision: Union[str, Sequence[str], None] = "c175dc5cc7dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Backfill current location assignments for legacy employees.

    Employees created before the assignment architecture may have a valid
    employees.location_id but no current employee_locations assignment.
    """

    # Repair an existing assignment that matches the legacy location when
    # the employee does not already have an active current assignment.
    op.execute(
        """
        UPDATE employee_locations
        SET
            is_primary = true,
            is_current = true,
            is_active = true
        WHERE id IN (
            SELECT MIN(matching_assignment.id)
            FROM employee_locations AS matching_assignment
            JOIN employees
                ON employees.id = matching_assignment.employee_id
            WHERE employees.location_id IS NOT NULL
              AND matching_assignment.location_id = employees.location_id
              AND NOT EXISTS (
                  SELECT 1
                  FROM employee_locations AS current_assignment
                  WHERE current_assignment.employee_id = employees.id
                    AND current_assignment.is_current = true
                    AND current_assignment.is_active = true
              )
            GROUP BY matching_assignment.employee_id
        )
        """
    )

    # Create a new assignment only when no matching assignment exists and the
    # employee still does not have an active current operating location.
    op.execute(
        """
        INSERT INTO employee_locations (
            employee_id,
            location_id,
            assigned_by_user_id,
            is_primary,
            is_current,
            is_active
        )
        SELECT
            employees.id,
            employees.location_id,
            businesses.owner_id,
            true,
            true,
            true
        FROM employees
        JOIN businesses
            ON businesses.id = employees.business_id
        WHERE employees.location_id IS NOT NULL
          AND NOT EXISTS (
              SELECT 1
              FROM employee_locations AS matching_assignment
              WHERE matching_assignment.employee_id = employees.id
                AND matching_assignment.location_id = employees.location_id
          )
          AND NOT EXISTS (
              SELECT 1
              FROM employee_locations AS current_assignment
              WHERE current_assignment.employee_id = employees.id
                AND current_assignment.is_current = true
                AND current_assignment.is_active = true
          )
        """
    )


def downgrade() -> None:
    """
    Preserve assignment data because backfilled records cannot safely be
    distinguished from assignments created during normal operation.
    """
    pass