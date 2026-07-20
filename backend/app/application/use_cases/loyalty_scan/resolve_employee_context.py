from dataclasses import dataclass

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.application.identity.current_business_context import (
    resolve_current_business_context,
)
from app.models.business import Business
from app.models.employee import Employee
from app.models.location import Location
from app.models.user import User
from app.repositories.location_repository import get_location_by_id


@dataclass(frozen=True)
class EmployeeScanContext:
    business: Business
    employee: Employee
    location: Location


def resolve_employee_context(
    db: Session,
    current_user: User,
) -> EmployeeScanContext:
    """
    Resolve the authenticated employee context required for POS scanning.

    General identity and business resolution is delegated to the centralized
    business-context resolver. This use case adds the POS-specific requirement
    that the employee must have a valid assigned location.
    """
    business_context = resolve_current_business_context(
        db,
        current_user,
    )

    employee = business_context.employee

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Employee access is required",
        )

    if employee.location_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee has no assigned location",
        )

    location = get_location_by_id(
        db,
        employee.location_id,
    )

    if location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee location not found",
        )

    if location.business_id != business_context.business.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Employee location does not belong to employee business",
        )

    return EmployeeScanContext(
        business=business_context.business,
        employee=employee,
        location=location,
    )
