from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.application.authorization.dependencies import require_permission
from app.application.authorization.permissions import Permission
from app.application.identity.current_business_context import (
    CurrentBusinessContext,
)
from app.db.database import get_db
from app.schemas.employee_location import (
    EmployeeLocationAssign,
    EmployeeLocationResponse,
)
from app.services.employee_location_service import (
    assign_employee_location_service,
    deactivate_employee_location_service,
    list_employee_locations_service,
    set_primary_employee_location_service,
)


router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.get(
    "/{employee_id}/locations",
    response_model=list[EmployeeLocationResponse],
)
def list_employee_locations(
    employee_id: int,
    db: Session = Depends(get_db),
    context: CurrentBusinessContext = Depends(
        require_permission(Permission.EMPLOYEES_READ)
    ),
):
    return list_employee_locations_service(
        db,
        business_id=context.business.id,
        employee_id=employee_id,
    )


@router.post(
    "/{employee_id}/locations",
    response_model=EmployeeLocationResponse,
    status_code=status.HTTP_201_CREATED,
)
def assign_employee_location(
    employee_id: int,
    assignment_data: EmployeeLocationAssign,
    db: Session = Depends(get_db),
    context: CurrentBusinessContext = Depends(
        require_permission(Permission.EMPLOYEES_UPDATE)
    ),
):
    return assign_employee_location_service(
        db,
        business_id=context.business.id,
        employee_id=employee_id,
        location_id=assignment_data.location_id,
        assigned_by_user_id=context.user.id,
        make_primary=assignment_data.is_primary,
    )


@router.patch(
    "/{employee_id}/locations/{location_id}/primary",
    response_model=EmployeeLocationResponse,
)
def set_primary_employee_location(
    employee_id: int,
    location_id: int,
    db: Session = Depends(get_db),
    context: CurrentBusinessContext = Depends(
        require_permission(Permission.EMPLOYEES_UPDATE)
    ),
):
    return set_primary_employee_location_service(
        db,
        business_id=context.business.id,
        employee_id=employee_id,
        location_id=location_id,
    )


@router.delete(
    "/{employee_id}/locations/{location_id}",
    response_model=EmployeeLocationResponse,
)
def deactivate_employee_location(
    employee_id: int,
    location_id: int,
    db: Session = Depends(get_db),
    context: CurrentBusinessContext = Depends(
        require_permission(Permission.EMPLOYEES_UPDATE)
    ),
):
    return deactivate_employee_location_service(
        db,
        business_id=context.business.id,
        employee_id=employee_id,
        location_id=location_id,
    )
