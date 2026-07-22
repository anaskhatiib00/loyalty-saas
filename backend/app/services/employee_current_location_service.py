from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.employee_location import EmployeeLocation
from app.models.location import Location
from app.repositories.employee_location_repository import (
    clear_current_employee_location_assignments,
    get_active_employee_location_assignment,
    get_current_employee_location_assignment,
    set_employee_location_assignment_current,
)
from app.repositories.employee_repository import get_employee_by_id
from app.repositories.location_repository import get_location_by_id


def _get_business_employee(
    db: Session,
    *,
    business_id: int,
    employee_id: int,
) -> Employee:
    """
    Return an employee only when it belongs to the requested business.
    """
    employee = get_employee_by_id(
        db,
        employee_id,
    )

    if employee is None or employee.business_id != business_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return employee


def _get_business_location(
    db: Session,
    *,
    business_id: int,
    location_id: int,
) -> Location:
    """
    Return a location only when it belongs to the requested business.
    """
    location = get_location_by_id(
        db,
        location_id,
    )

    if location is None or location.business_id != business_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )

    return location


def get_employee_current_location_service(
    db: Session,
    *,
    business_id: int,
    employee_id: int,
) -> EmployeeLocation | None:
    """
    Return the employee's current active operating location.

    The employee is validated against the current business to prevent
    cross-business access.
    """
    _get_business_employee(
        db,
        business_id=business_id,
        employee_id=employee_id,
    )

    return get_current_employee_location_assignment(
        db,
        employee_id=employee_id,
    )


def set_employee_current_location_service(
    db: Session,
    *,
    business_id: int,
    employee_id: int,
    location_id: int,
) -> EmployeeLocation:
    """
    Select the employee's current operating location.

    Business rules:
    - Employee must belong to the current business.
    - Location must belong to the current business.
    - Employee must have an active assignment to the location.
    - Only one assignment may be current.
    - Employee.location_id remains synchronized temporarily for legacy POS
      compatibility.
    """
    employee = _get_business_employee(
        db,
        business_id=business_id,
        employee_id=employee_id,
    )

    _get_business_location(
        db,
        business_id=business_id,
        location_id=location_id,
    )

    assignment = get_active_employee_location_assignment(
        db,
        employee_id=employee_id,
        location_id=location_id,
    )

    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active employee location assignment not found",
        )

    if assignment.is_current:
        return assignment

    try:
        clear_current_employee_location_assignments(
            db,
            employee_id=employee_id,
            exclude_location_id=location_id,
        )

        set_employee_location_assignment_current(
            db,
            assignment=assignment,
        )

        employee.location_id = location_id

        db.commit()

        db.refresh(assignment)
        db.refresh(employee)

        return assignment

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee current location conflicts with existing data",
        ) from exc

    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to set employee current location",
        ) from exc


def clear_employee_current_location_service(
    db: Session,
    *,
    business_id: int,
    employee_id: int,
) -> None:
    """
    Clear the employee's current operating location.

    Employee.location_id falls back to the active primary assignment when one
    exists. Otherwise it is cleared.
    """
    employee = _get_business_employee(
        db,
        business_id=business_id,
        employee_id=employee_id,
    )

    current_assignment = get_current_employee_location_assignment(
        db,
        employee_id=employee_id,
    )

    if current_assignment is None:
        return

    try:
        current_assignment.is_current = False

        primary_assignment = next(
            (
                assignment
                for assignment in employee.location_assignments
                if assignment.is_active and assignment.is_primary
            ),
            None,
        )

        employee.location_id = (
            primary_assignment.location_id
            if primary_assignment is not None
            else None
        )

        db.flush()
        db.commit()

        db.refresh(employee)

    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to clear employee current location",
        ) from exc