from sqlalchemy.orm import Session

from app.core.enums import EmployeeRole, EmployeeStatus
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def create_employee(
    db: Session,
    business_id: int,
    employee_data: EmployeeCreate,
):
    employee = Employee(
        business_id=business_id,
        **employee_data.model_dump(),
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


def create_employee_in_transaction(
    db: Session,
    *,
    business_id: int,
    location_id: int | None,
    full_name: str,
    email: str,
    phone: str | None,
    role: EmployeeRole,
) -> Employee:
    """
    Create an invited employee without committing the transaction.

    The employee remains unable to authenticate until an invitation is
    accepted and a User account is linked.
    """
    employee = Employee(
        business_id=business_id,
        location_id=location_id,
        user_id=None,
        full_name=full_name.strip(),
        email=email.strip().lower(),
        phone=phone,
        role=role.value,
        status=EmployeeStatus.INVITED.value,
    )

    db.add(employee)
    db.flush()

    return employee


def get_employees_by_business_id(db: Session, business_id: int):
    return (
        db.query(Employee)
        .filter(Employee.business_id == business_id)
        .all()
    )


def get_employee_by_id(db: Session, employee_id: int):
    return (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )


def get_employee_by_user_id(db: Session, user_id: int):
    return (
        db.query(Employee)
        .filter(Employee.user_id == user_id)
        .first()
    )


def get_employee_by_business_email(
    db: Session,
    business_id: int,
    email: str,
) -> Employee | None:
    normalized_email = email.strip().lower()

    return (
        db.query(Employee)
        .filter(
            Employee.business_id == business_id,
            Employee.email == normalized_email,
        )
        .first()
    )


def link_employee_to_user(
    db: Session,
    employee: Employee,
    *,
    user_id: int,
) -> Employee:
    employee.user_id = user_id
    employee.status = EmployeeStatus.ACTIVE.value

    db.flush()

    return employee


def update_employee(
    db: Session,
    employee: Employee,
    employee_data: EmployeeUpdate,
):
    update_data = employee_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)

    return employee


def delete_employee(db: Session, employee: Employee):
    db.delete(employee)
    db.commit()
