from datetime import datetime

from sqlalchemy.orm import Session

from app.core.enums import IdentityInvitationStatus
from app.models.identity_invitation import IdentityInvitation


def create_identity_invitation(
    db: Session,
    *,
    business_id: int,
    employee_id: int | None,
    email: str,
    role: str,
    token_hash: str,
    expires_at: datetime,
    created_by_user_id: int | None,
) -> IdentityInvitation:
    invitation = IdentityInvitation(
        business_id=business_id,
        employee_id=employee_id,
        email=email.strip().lower(),
        role=role,
        token_hash=token_hash,
        status=IdentityInvitationStatus.PENDING.value,
        expires_at=expires_at,
        created_by_user_id=created_by_user_id,
    )

    db.add(invitation)
    db.flush()

    return invitation


def get_identity_invitation_by_id(
    db: Session,
    invitation_id: int,
) -> IdentityInvitation | None:
    return (
        db.query(IdentityInvitation)
        .filter(IdentityInvitation.id == invitation_id)
        .first()
    )


def get_identity_invitation_by_token_hash(
    db: Session,
    token_hash: str,
) -> IdentityInvitation | None:
    return (
        db.query(IdentityInvitation)
        .filter(IdentityInvitation.token_hash == token_hash)
        .first()
    )


def get_pending_identity_invitation_by_business_email(
    db: Session,
    business_id: int,
    email: str,
) -> IdentityInvitation | None:
    normalized_email = email.strip().lower()

    return (
        db.query(IdentityInvitation)
        .filter(
            IdentityInvitation.business_id == business_id,
            IdentityInvitation.email == normalized_email,
            IdentityInvitation.status
            == IdentityInvitationStatus.PENDING.value,
        )
        .order_by(IdentityInvitation.created_at.desc())
        .first()
    )


def get_pending_identity_invitation_by_employee_id(
    db: Session,
    employee_id: int,
) -> IdentityInvitation | None:
    return (
        db.query(IdentityInvitation)
        .filter(
            IdentityInvitation.employee_id == employee_id,
            IdentityInvitation.status
            == IdentityInvitationStatus.PENDING.value,
        )
        .order_by(IdentityInvitation.created_at.desc())
        .first()
    )


def mark_identity_invitation_accepted(
    db: Session,
    invitation: IdentityInvitation,
    *,
    accepted_user_id: int,
    accepted_at: datetime,
) -> IdentityInvitation:
    invitation.status = IdentityInvitationStatus.ACCEPTED.value
    invitation.accepted_user_id = accepted_user_id
    invitation.accepted_at = accepted_at

    db.flush()

    return invitation


def mark_identity_invitation_revoked(
    db: Session,
    invitation: IdentityInvitation,
    *,
    revoked_at: datetime,
) -> IdentityInvitation:
    invitation.status = IdentityInvitationStatus.REVOKED.value
    invitation.revoked_at = revoked_at

    db.flush()

    return invitation


def mark_identity_invitation_expired(
    db: Session,
    invitation: IdentityInvitation,
) -> IdentityInvitation:
    invitation.status = IdentityInvitationStatus.EXPIRED.value

    db.flush()

    return invitation
