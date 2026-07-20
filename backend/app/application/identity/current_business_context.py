from dataclasses import dataclass

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.enums import EmployeeStatus
from app.models.business import Business
from app.models.employee import Employee
from app.models.user import User
from app.repositories.business_repository import (
    get_business_by_id,
    get_business_by_owner_id,
)
from app.repositories.employee_repository import get_employee_by_user_id


@dataclass(frozen=True)
class CurrentBusinessContext:
    user: User
    business: Business
    employee: Employee | None
    is_owner: bool

    @property
    def is_employee(self) -> bool:
        return self.employee is not None

    @property
    def employee_role(self) -> str | None:
        if self.employee is None:
            return None

        return self.employee.role


def resolve_current_business_context(
    db: Session,
    current_user: User,
) -> CurrentBusinessContext:
    """
    Resolve the authenticated user's business relationship.

    A user may access a business through one of two identity paths:

    1. Business owner:
       User -> Business.owner_id

    2. Employee:
       User -> Employee.user_id -> Business

    Employee identities must be active before they can receive a valid
    business context.
    """
    owned_business = get_business_by_owner_id(
        db,
        current_user.id,
    )

    if owned_business is not None:
        return CurrentBusinessContext(
            user=current_user,
            business=owned_business,
            employee=None,
            is_owner=True,
        )

    employee = get_employee_by_user_id(
        db,
        current_user.id,
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not associated with a business",
        )

    if employee.status != EmployeeStatus.ACTIVE.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Employee account is inactive",
        )

    business = get_business_by_id(
        db,
        employee.business_id,
    )

    if business is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee business not found",
        )

    return CurrentBusinessContext(
        user=current_user,
        business=business,
        employee=employee,
        is_owner=False,
    )
