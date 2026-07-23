from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.application.identity.invitations.validation import (
    get_invited_employee,
    get_valid_pending_invitation,
)
from app.repositories.business_repository import get_business_by_id


def preview_identity_invitation(
    db: Session,
    *,
    token: str,
):
    invitation = get_valid_pending_invitation(
        db,
        token=token,
    )

    employee = get_invited_employee(
        db,
        invitation=invitation,
    )

    business = get_business_by_id(
        db,
        invitation.business_id,
    )

    if business is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invited business no longer exists",
        )

    return {
        "business_name": business.name,
        "employee_name": employee.full_name,
        "role": invitation.role,
        "expires_at": invitation.expires_at,
    }
