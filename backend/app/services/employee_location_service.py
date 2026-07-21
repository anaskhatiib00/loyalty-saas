from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.employee_location import EmployeeLocation
from app.models.location import Location
from app.repositories.employee_location_repository import (
    clear_primary_employee_location_assignments,
    count_active_employee_location_assignments,
    create_employee_location_assignment,
    deactivate_employee_location_assignment,
    get_active_employee_location_assignment,
    get_employee_location_assignment,
    get_employee_location_assignments,
    reactivate_employee_location_assignment,
    set_employee_location_assignment_primary,
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


def list_employee_locations_service(
    db: Session,
    *,
    business_id: int,
    employee_id: int,
    include_inactive: bool = False,
) -> list[EmployeeLocation]:
    """
    List the location assignments belonging to an employee.

    The employee is validated against the current business to prevent
    cross-business access.
    """
    _get_business_employee(
        db,
        business_id=business_id,
        employee_id=employee_id,
    )

    return get_employee_location_assignments(
        db,
        employee_id=employee_id,
        include_inactive=include_inactive,
    )


def assign_employee_location_service(
    db: Session,
    *,
    business_id: int,
    employee_id: int,
    location_id: int,
    assigned_by_user_id: int | None,
    make_primary: bool = False,
) -> EmployeeLocation:
    """
    Assign an employee to a location.

    Business rules:
    - Employee and location must belong to the same business.
    - Duplicate active assignments are rejected.
    - Inactive assignments are reactivated.
    - The employee's first active assignment becomes primary.
    - Only one active assignment may be primary.
    - Employee.location_id remains synchronized as a compatibility bridge.
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

    existing_assignment = get_employee_location_assignment(
        db,
        employee_id=employee_id,
        location_id=location_id,
    )

    if existing_assignment is not None and existing_assignment.is_active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee is already assigned to this location",
        )

    active_assignment_count = (
        count_active_employee_location_assignments(
            db,
            employee_id=employee_id,
        )
    )

    should_be_primary = (
        make_primary or active_assignment_count == 0
    )

    try:
        if should_be_primary:
            clear_primary_employee_location_assignments(
                db,
                employee_id=employee_id,
            )

        if existing_assignment is not None:
            assignment = reactivate_employee_location_assignment(
                db,
                assignment=existing_assignment,
                assigned_by_user_id=assigned_by_user_id,
                is_primary=should_be_primary,
            )
        else:
            assignment = create_employee_location_assignment(
                db,
                employee_id=employee_id,
                location_id=location_id,
                assigned_by_user_id=assigned_by_user_id,
                is_primary=should_be_primary,
            )

        if should_be_primary:
            employee.location_id = location_id

        db.commit()

        db.refresh(assignment)
        db.refresh(employee)

        return assignment

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "The employee location assignment conflicts "
                "with existing assignment data"
            ),
        ) from exc

    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to assign employee to location",
        ) from exc


def set_primary_employee_location_service(
    db: Session,
    *,
    business_id: int,
    employee_id: int,
    location_id: int,
) -> EmployeeLocation:
    """
    Set one active employee-location assignment as primary.

    Employee.location_id is also updated while the legacy compatibility
    field remains in use.
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

    try:
        clear_primary_employee_location_assignments(
            db,
            employee_id=employee_id,
            exclude_location_id=location_id,
        )

        set_employee_location_assignment_primary(
            db,
            assignment=assignment,
        )

        employee.location_id = location_id

        db.commit()

        db.refresh(assignment)
        db.refresh(employee)

        return assignment

    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to set primary employee location",
        ) from exc


def deactivate_employee_location_service(
    db: Session,
    *,
    business_id: int,
    employee_id: int,
    location_id: int,
) -> EmployeeLocation:
    """
    Deactivate an employee-location assignment.

    If the removed assignment was primary, another active assignment is
    promoted. If no active assignments remain, Employee.location_id is
    cleared.
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

    was_primary = assignment.is_primary

    try:
        deactivate_employee_location_assignment(
            db,
            assignment=assignment,
        )

        if was_primary:
            remaining_assignments = (
                get_employee_location_assignments(
                    db,
                    employee_id=employee_id,
                    include_inactive=False,
                )
            )

            if remaining_assignments:
                replacement = remaining_assignments[0]

                clear_primary_employee_location_assignments(
                    db,
                    employee_id=employee_id,
                )

                set_employee_location_assignment_primary(
                    db,
                    assignment=replacement,
                )

                employee.location_id = replacement.location_id
            else:
                employee.location_id = None

        elif employee.location_id == location_id:
            primary_assignment = next(
                (
                    item
                    for item in get_employee_location_assignments(
                        db,
                        employee_id=employee_id,
                        include_inactive=False,
                    )
                    if item.is_primary
                ),
                None,
            )

            employee.location_id = (
                primary_assignment.location_id
                if primary_assignment is not None
                else None
            )

        db.commit()

        db.refresh(assignment)
        db.refresh(employee)

        return assignment

    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to deactivate employee location assignment",
        ) from exc