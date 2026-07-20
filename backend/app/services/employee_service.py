from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.employee_repository import (
    create_employee,
    get_employees_by_business_id,
    get_employee_by_id,
    update_employee,
    delete_employee,
)
from app.repositories.location_repository import get_location_by_id
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def get_current_user_business(db: Session, current_user: User):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(status_code=404, detail="Business profile not found")

    return business


def validate_location(db: Session, business_id: int, location_id: int | None):
    if location_id is None:
        return

    location = get_location_by_id(db, location_id)

    if not location or location.business_id != business_id:
        raise HTTPException(status_code=404, detail="Location not found")


def create_employee_service(
    db: Session,
    business_id: int,
    employee_data: EmployeeCreate,
):
    validate_location(
        db,
        business_id,
        employee_data.location_id,
    )

    return create_employee(
        db,
        business_id,
        employee_data,
    )


def list_employees_service(
    db: Session,
    business_id: int,
):
    return get_employees_by_business_id(
        db,
        business_id,
    )


def get_employee_service(
    db: Session,
    business_id: int,
    employee_id: int,
):
    employee = get_employee_by_id(
        db,
        employee_id,
    )

    if not employee or employee.business_id != business_id:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return employee


def update_employee_service(
    db: Session,
    business_id: int,
    employee_id: int,
    employee_data: EmployeeUpdate,
):
    validate_location(
        db,
        business_id,
        employee_data.location_id,
    )

    employee = get_employee_service(
        db,
        business_id,
        employee_id,
    )

    return update_employee(
        db,
        employee,
        employee_data,
    )


def delete_employee_service(
    db: Session,
    business_id: int,
    employee_id: int,
):
    employee = get_employee_service(
        db,
        business_id,
        employee_id,
    )

    delete_employee(
        db,
        employee,
    )

    return {
        "message": "Employee deleted successfully",
    }
