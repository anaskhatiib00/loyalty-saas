from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def create_employee(db: Session, business_id: int, employee_data: EmployeeCreate):
    employee = Employee(
        business_id=business_id,
        **employee_data.model_dump(),
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


def get_employees_by_business_id(db: Session, business_id: int):
    return db.query(Employee).filter(Employee.business_id == business_id).all()


def get_employee_by_id(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()


def update_employee(db: Session, employee: Employee, employee_data: EmployeeUpdate):
    update_data = employee_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)

    return employee


def delete_employee(db: Session, employee: Employee):
    db.delete(employee)
    db.commit()


def get_employee_by_user_id(db: Session, user_id: int):
    return db.query(Employee).filter(Employee.user_id == user_id).first()