from dataclasses import dataclass

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.employee import Employee
from app.models.location import Location
from app.models.user import User
from app.repositories.business_repository import get_business_by_id
from app.repositories.employee_repository import get_employee_by_user_id
from app.repositories.location_repository import get_location_by_id


@dataclass
class EmployeeScanContext:
    business: Business
    employee: Employee
    location: Location


def resolve_employee_context(
    db: Session,
    current_user: User,
) -> EmployeeScanContext:
    employee = get_employee_by_user_id(db, current_user.id)

    if not employee:
        raise HTTPException(
            status_code=403,
            detail="Employee profile not linked",
        )

    if employee.status != "active":
        raise HTTPException(
            status_code=403,
            detail="Employee account is inactive",
        )

    business = get_business_by_id(db, employee.business_id)

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Employee business not found",
        )

    if employee.location_id is None:
        raise HTTPException(
            status_code=400,
            detail="Employee has no assigned location",
        )

    location = get_location_by_id(db, employee.location_id)

    if not location:
        raise HTTPException(
            status_code=404,
            detail="Employee location not found",
        )

    if location.business_id != business.id:
        raise HTTPException(
            status_code=403,
            detail="Employee location does not belong to employee business",
        )

    return EmployeeScanContext(
        business=business,
        employee=employee,
        location=location,
    )