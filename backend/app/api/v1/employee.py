from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.services.employee_service import (
    create_employee_service,
    list_employees_service,
    get_employee_service,
    update_employee_service,
    delete_employee_service,
)


router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.post("", response_model=EmployeeResponse)
def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_employee_service(db, current_user, employee_data)


@router.get("", response_model=list[EmployeeResponse])
def list_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_employees_service(db, current_user)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_employee_service(db, current_user, employee_id)


@router.patch("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_employee_service(db, current_user, employee_id, employee_data)


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_employee_service(db, current_user, employee_id)