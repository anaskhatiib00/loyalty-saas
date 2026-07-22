from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.application.authorization.dependencies import require_permission
from app.application.authorization.permissions import Permission
from app.application.identity.current_business_context import (
    CurrentBusinessContext,
)
from app.db.database import get_db
from app.schemas.employee_location import (
    EmployeeCurrentLocationSelect,
    EmployeeLocationAssign,
    EmployeeLocationResponse,
)
from app.services.employee_current_location_service import (
    clear_employee_current_location_service,
    get_employee_current_location_service,
    set_employee_current_location_service,
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


@router.get(
    "/{employee_id}/locations/current",
    response_model=EmployeeLocationResponse | None,
)
def get_employee_current_location(
    employee_id: int,
    db: Session = Depends(get_db),
    context: CurrentBusinessContext = Depends(
        require_permission(Permission.EMPLOYEES_READ)
    ),
):
    return get_employee_current_location_service(
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
    "/{employee_id}/locations/current",
    response_model=EmployeeLocationResponse,
)
def set_employee_current_location(
    employee_id: int,
    selection_data: EmployeeCurrentLocationSelect,
    db: Session = Depends(get_db),
    context: CurrentBusinessContext = Depends(
        require_permission(Permission.EMPLOYEES_UPDATE)
    ),
):
    return set_employee_current_location_service(
        db,
        business_id=context.business.id,
        employee_id=employee_id,
        location_id=selection_data.location_id,
    )


@router.delete(
    "/{employee_id}/locations/current",
    status_code=status.HTTP_204_NO_CONTENT,
)
def clear_employee_current_location(
    employee_id: int,
    db: Session = Depends(get_db),
    context: CurrentBusinessContext = Depends(
        require_permission(Permission.EMPLOYEES_UPDATE)
    ),
) -> Response:
    clear_employee_current_location_service(
        db,
        business_id=context.business.id,
        employee_id=employee_id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


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
