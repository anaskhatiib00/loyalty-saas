from urllib.parse import urlencode

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.application.authorization.dependencies import require_permission
from app.application.authorization.permissions import Permission
from app.application.identity.current_business_context import (
    CurrentBusinessContext,
)
from app.core.settings import settings
from app.db.database import get_db
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
)
from app.schemas.identity_invitation import (
    IdentityInvitationAccept,
    IdentityInvitationAcceptedResponse,
    IdentityInvitationCreate,
    IdentityInvitationCreatedResponse,
)
from app.services.employee_service import (
    create_employee_service,
    delete_employee_service,
    get_employee_service,
    list_employees_service,
    update_employee_service,
)
from app.services.identity_invitation_service import (
    accept_identity_invitation_service,
    create_identity_invitation_service,
    preview_identity_invitation_service,

)
from app.schemas.identity_invitation_preview import (
    IdentityInvitationPreviewResponse,
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.post("", response_model=EmployeeResponse)
def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    context: CurrentBusinessContext = Depends(
        require_permission(Permission.EMPLOYEES_CREATE)
    ),
):
    return create_employee_service(
        db,
        context.business.id,
        employee_data,
    )


@router.post(
    "/invitations",
    response_model=IdentityInvitationCreatedResponse,
    status_code=status.HTTP_201_CREATED,
)
def invite_employee(
    invitation_data: IdentityInvitationCreate,
    db: Session = Depends(get_db),
    context: CurrentBusinessContext = Depends(
        require_permission(Permission.EMPLOYEES_INVITE)
    ),
):
    result = create_identity_invitation_service(
        db,
        business_id=context.business.id,
        created_by_user_id=context.user.id,
        invitation_data=invitation_data,
    )

    response = {
        "invitation": result.invitation,
        "employee_id": result.invitation.employee_id,
        "delivery_status": "pending",
        "development_invitation_token": None,
        "development_accept_url": None,
    }

    if settings.DEBUG:
        query = urlencode(
            {
                "token": result.raw_token,
            }
        )

        response["development_invitation_token"] = result.raw_token
        response["development_accept_url"] = (
            f"{settings.FRONTEND_URL.rstrip('/')}"
            f"/employee/accept?{query}"
        )

    return response


@router.get(
    "/invitations/preview",
    response_model=IdentityInvitationPreviewResponse,
)
def preview_employee_invitation(
    token: str,
    db: Session = Depends(get_db),
):
    return preview_identity_invitation_service(
        db,
        token=token,
    )


@router.post(
    "/invitations/accept",
    response_model=IdentityInvitationAcceptedResponse,
)
def accept_employee_invitation(
    acceptance_data: IdentityInvitationAccept,
    db: Session = Depends(get_db),
):
    return accept_identity_invitation_service(
        db,
        token=acceptance_data.token,
        password=acceptance_data.password,
    )


@router.get("", response_model=list[EmployeeResponse])
def list_employees(
    db: Session = Depends(get_db),
    context: CurrentBusinessContext = Depends(
        require_permission(Permission.EMPLOYEES_READ)
    ),
):
    return list_employees_service(
        db,
        context.business.id,
    )


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    context: CurrentBusinessContext = Depends(
        require_permission(Permission.EMPLOYEES_READ)
    ),
):
    return get_employee_service(
        db,
        context.business.id,
        employee_id,
    )


@router.patch("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    context: CurrentBusinessContext = Depends(
        require_permission(Permission.EMPLOYEES_UPDATE)
    ),
):
    return update_employee_service(
        db,
        context.business.id,
        employee_id,
        employee_data,
    )


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    context: CurrentBusinessContext = Depends(
        require_permission(Permission.EMPLOYEES_DELETE)
    ),
):
    return delete_employee_service(
        db,
        context.business.id,
        employee_id,
    )
