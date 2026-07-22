from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.employee_location import EmployeeLocation


def get_employee_location_assignment(
    db: Session,
    *,
    employee_id: int,
    location_id: int,
) -> EmployeeLocation | None:
    """
    Return an employee-location assignment regardless of whether it is active.
    """
    return (
        db.query(EmployeeLocation)
        .filter(
            EmployeeLocation.employee_id == employee_id,
            EmployeeLocation.location_id == location_id,
        )
        .first()
    )


def get_active_employee_location_assignment(
    db: Session,
    *,
    employee_id: int,
    location_id: int,
) -> EmployeeLocation | None:
    """
    Return an active employee-location assignment.
    """
    return (
        db.query(EmployeeLocation)
        .filter(
            EmployeeLocation.employee_id == employee_id,
            EmployeeLocation.location_id == location_id,
            EmployeeLocation.is_active.is_(True),
        )
        .first()
    )


def get_primary_employee_location_assignment(
    db: Session,
    *,
    employee_id: int,
) -> EmployeeLocation | None:
    """
    Return the employee's active primary location assignment.
    """
    return (
        db.query(EmployeeLocation)
        .filter(
            EmployeeLocation.employee_id == employee_id,
            EmployeeLocation.is_active.is_(True),
            EmployeeLocation.is_primary.is_(True),
        )
        .first()
    )


def get_current_employee_location_assignment(
    db: Session,
    *,
    employee_id: int,
) -> EmployeeLocation | None:
    """
    Return the employee's current active operating location.
    """
    return (
        db.query(EmployeeLocation)
        .filter(
            EmployeeLocation.employee_id == employee_id,
            EmployeeLocation.is_active.is_(True),
            EmployeeLocation.is_current.is_(True),
        )
        .first()
    )


def get_employee_location_assignments(
    db: Session,
    *,
    employee_id: int,
    include_inactive: bool = False,
) -> list[EmployeeLocation]:
    """
    Return all assignments for an employee.

    Active assignments are returned by default. Inactive assignments can be
    included for administrative or audit purposes.
    """
    query = db.query(EmployeeLocation).filter(
        EmployeeLocation.employee_id == employee_id,
    )

    if not include_inactive:
        query = query.filter(
            EmployeeLocation.is_active.is_(True),
        )

    return (
        query.order_by(
            EmployeeLocation.is_current.desc(),
            EmployeeLocation.is_primary.desc(),
            EmployeeLocation.assigned_at.asc(),
            EmployeeLocation.id.asc(),
        )
        .all()
    )


def count_active_employee_location_assignments(
    db: Session,
    *,
    employee_id: int,
) -> int:
    """
    Count the employee's active location assignments.
    """
    return (
        db.query(EmployeeLocation)
        .filter(
            EmployeeLocation.employee_id == employee_id,
            EmployeeLocation.is_active.is_(True),
        )
        .count()
    )


def create_employee_location_assignment(
    db: Session,
    *,
    employee_id: int,
    location_id: int,
    assigned_by_user_id: int | None,
    is_primary: bool = False,
) -> EmployeeLocation:
    """
    Create an assignment without committing the surrounding transaction.
    """
    assignment = EmployeeLocation(
        employee_id=employee_id,
        location_id=location_id,
        assigned_by_user_id=assigned_by_user_id,
        is_primary=is_primary,
        is_current=False,
        is_active=True,
    )

    db.add(assignment)
    db.flush()

    return assignment


def reactivate_employee_location_assignment(
    db: Session,
    *,
    assignment: EmployeeLocation,
    assigned_by_user_id: int | None,
    is_primary: bool = False,
) -> EmployeeLocation:
    """
    Reactivate a previously deactivated assignment.
    """
    assignment.assigned_by_user_id = assigned_by_user_id
    assignment.assigned_at = datetime.now(timezone.utc)
    assignment.is_primary = is_primary
    assignment.is_current = False
    assignment.is_active = True

    db.flush()

    return assignment


def clear_primary_employee_location_assignments(
    db: Session,
    *,
    employee_id: int,
    exclude_location_id: int | None = None,
) -> None:
    """
    Remove the primary flag from active assignments for one employee.
    """
    query = db.query(EmployeeLocation).filter(
        EmployeeLocation.employee_id == employee_id,
        EmployeeLocation.is_active.is_(True),
        EmployeeLocation.is_primary.is_(True),
    )

    if exclude_location_id is not None:
        query = query.filter(
            EmployeeLocation.location_id != exclude_location_id,
        )

    query.update(
        {
            EmployeeLocation.is_primary: False,
        },
        synchronize_session="fetch",
    )

    db.flush()


def clear_current_employee_location_assignments(
    db: Session,
    *,
    employee_id: int,
    exclude_location_id: int | None = None,
) -> None:
    """
    Remove the current operating location flag from active assignments.
    """
    query = db.query(EmployeeLocation).filter(
        EmployeeLocation.employee_id == employee_id,
        EmployeeLocation.is_active.is_(True),
        EmployeeLocation.is_current.is_(True),
    )

    if exclude_location_id is not None:
        query = query.filter(
            EmployeeLocation.location_id != exclude_location_id,
        )

    query.update(
        {
            EmployeeLocation.is_current: False,
        },
        synchronize_session="fetch",
    )

    db.flush()


def set_employee_location_assignment_primary(
    db: Session,
    *,
    assignment: EmployeeLocation,
) -> EmployeeLocation:
    """
    Mark an active assignment as primary.

    The service layer must clear any existing primary assignment first.
    """
    assignment.is_primary = True

    db.flush()

    return assignment


def set_employee_location_assignment_current(
    db: Session,
    *,
    assignment: EmployeeLocation,
) -> EmployeeLocation:
    """
    Mark an assignment as the employee's current operating location.

    The service layer must clear any previous current assignment first.
    """
    assignment.is_current = True

    db.flush()

    return assignment


def deactivate_employee_location_assignment(
    db: Session,
    *,
    assignment: EmployeeLocation,
) -> EmployeeLocation:
    """
    Deactivate an assignment without deleting its historical record.
    """
    assignment.is_active = False
    assignment.is_primary = False
    assignment.is_current = False

    db.flush()

    return assignment