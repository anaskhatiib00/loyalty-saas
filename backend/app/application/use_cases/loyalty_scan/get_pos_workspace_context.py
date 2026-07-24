from sqlalchemy.orm import Session

from app.application.use_cases.loyalty_scan.resolve_employee_context import (
    resolve_employee_context,
)
from app.models.user import User
from app.schemas.pos_context import (
    POSBusinessContext,
    POSEmployeeContext,
    POSLocationContext,
    POSWorkspaceContextResponse,
)


def get_pos_workspace_context_use_case(
    db: Session,
    current_user: User,
) -> POSWorkspaceContextResponse:
    """
    Return the authenticated employee's POS workspace context.

    The employee and assigned operating location are resolved from the
    authenticated user. The client cannot select or override either value.
    """
    employee_context = resolve_employee_context(
        db=db,
        current_user=current_user,
    )

    business = employee_context.business
    employee = employee_context.employee
    location = employee_context.location

    return POSWorkspaceContextResponse(
        business=POSBusinessContext(
            id=business.id,
            name=business.name,
        ),
        employee=POSEmployeeContext(
            id=employee.id,
            full_name=employee.full_name,
            role=employee.role,
        ),
        location=POSLocationContext(
            id=location.id,
            name=location.name,
            address=location.address,
            city=location.city,
            state=location.state,
            country=location.country,
        ),
    )