from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.application.identity.invitations.types import (
    CreatedIdentityInvitation,
)
from app.core.identity_tokens import (
    generate_invitation_token,
    hash_invitation_token,
)
from app.core.settings import settings
from app.repositories.employee_repository import (
    create_employee_in_transaction,
    get_employee_by_business_email,
)
from app.repositories.identity_invitation_repository import (
    create_identity_invitation as create_identity_invitation_record,
    get_pending_identity_invitation_by_business_email,
)
from app.repositories.location_repository import get_location_by_id
from app.repositories.user_repository import get_user_by_email
from app.schemas.identity_invitation import IdentityInvitationCreate


def validate_invitation_location(
    db: Session,
    *,
    business_id: int,
    location_id: int | None,
) -> None:
    if location_id is None:
        return

    location = get_location_by_id(
        db,
        location_id,
    )

    if not location or location.business_id != business_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )


def validate_email_availability(
    db: Session,
    *,
    business_id: int,
    email: str,
) -> None:
    existing_user = get_user_by_email(
        db,
        email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user account already exists with this email",
        )

    existing_employee = get_employee_by_business_email(
        db,
        business_id,
        email,
    )

    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An employee already exists with this email",
        )

    pending_invitation = (
        get_pending_identity_invitation_by_business_email(
            db,
            business_id,
            email,
        )
    )

    if pending_invitation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A pending invitation already exists for this email",
        )


def create_identity_invitation(
    db: Session,
    *,
    business_id: int,
    created_by_user_id: int,
    invitation_data: IdentityInvitationCreate,
) -> CreatedIdentityInvitation:
    validate_invitation_location(
        db,
        business_id=business_id,
        location_id=invitation_data.location_id,
    )

    normalized_email = str(
        invitation_data.email,
    ).strip().lower()

    validate_email_availability(
        db,
        business_id=business_id,
        email=normalized_email,
    )

    raw_token = generate_invitation_token()
    token_hash = hash_invitation_token(raw_token)

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(
        hours=settings.IDENTITY_INVITATION_EXPIRE_HOURS,
    )

    try:
        employee = create_employee_in_transaction(
            db,
            business_id=business_id,
            location_id=invitation_data.location_id,
            full_name=invitation_data.full_name,
            email=normalized_email,
            phone=invitation_data.phone,
            role=invitation_data.role,
        )

        invitation = create_identity_invitation_record(
            db,
            business_id=business_id,
            employee_id=employee.id,
            email=normalized_email,
            role=invitation_data.role.value,
            token_hash=token_hash,
            expires_at=expires_at,
            created_by_user_id=created_by_user_id,
        )

        db.commit()

        db.refresh(employee)
        db.refresh(invitation)

        return CreatedIdentityInvitation(
            invitation=invitation,
            raw_token=raw_token,
        )

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "The employee invitation conflicts with "
                "existing identity data"
            ),
        ) from exc

    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create employee invitation",
        ) from exc