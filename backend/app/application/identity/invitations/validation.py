from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.enums import IdentityInvitationStatus
from app.core.identity_tokens import hash_invitation_token
from app.models.identity_invitation import IdentityInvitation
from app.repositories.employee_repository import get_employee_by_id
from app.repositories.identity_invitation_repository import (
    get_identity_invitation_by_token_hash,
    mark_identity_invitation_expired,
)


def normalize_datetime_to_utc(
    value: datetime,
) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc)


def mark_expired_invitation(
    db: Session,
    invitation: IdentityInvitation,
) -> None:
    try:
        mark_identity_invitation_expired(
            db,
            invitation,
        )
        db.commit()

    except SQLAlchemyError:
        db.rollback()


def get_valid_pending_invitation(
    db: Session,
    *,
    token: str,
) -> IdentityInvitation:
    token_hash = hash_invitation_token(token)

    invitation = get_identity_invitation_by_token_hash(
        db,
        token_hash,
    )

    if invitation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

    if invitation.status != IdentityInvitationStatus.PENDING.value:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invitation is no longer pending",
        )

    expires_at = normalize_datetime_to_utc(
        invitation.expires_at,
    )

    if expires_at <= datetime.now(timezone.utc):
        mark_expired_invitation(
            db,
            invitation,
        )

        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Invitation has expired",
        )

    return invitation


def get_invited_employee(
    db: Session,
    *,
    invitation: IdentityInvitation,
):
    if invitation.employee_id is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invitation is not linked to an employee",
        )

    employee = get_employee_by_id(
        db,
        invitation.employee_id,
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invited employee no longer exists",
        )

    if employee.business_id != invitation.business_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Invitation employee does not belong to "
                "the invitation business"
            ),
        )

    if employee.email is None or (
        employee.email.strip().lower()
        != invitation.email.strip().lower()
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invitation email does not match the employee",
        )

    return employee
