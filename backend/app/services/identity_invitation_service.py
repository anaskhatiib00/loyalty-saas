from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.identity_tokens import (
    generate_invitation_token,
    hash_invitation_token,
)
from app.core.settings import settings
from app.models.identity_invitation import IdentityInvitation
from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.employee_repository import (
    create_employee_in_transaction,
    get_employee_by_business_email,
)
from app.repositories.identity_invitation_repository import (
    create_identity_invitation,
    get_pending_identity_invitation_by_business_email,
)
from app.repositories.user_repository import get_user_by_email
from app.repositories.location_repository import get_location_by_id
from app.schemas.identity_invitation import IdentityInvitationCreate


@dataclass(frozen=True)
class CreatedIdentityInvitation:
    invitation: IdentityInvitation
    raw_token: str


def _get_owned_business(db: Session, current_user: User):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only a business owner can invite employees",
        )

    return business


def _validate_invitation_location(
    db: Session,
    *,
    business_id: int,
    location_id: int | None,
) -> None:
    if location_id is None:
        return

    location = get_location_by_id(db, location_id)

    if not location or location.business_id != business_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )


def _validate_email_availability(
    db: Session,
    *,
    business_id: int,
    email: str,
) -> None:
    existing_user = get_user_by_email(db, email)

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


def create_identity_invitation_service(
    db: Session,
    *,
    current_user: User,
    invitation_data: IdentityInvitationCreate,
) -> CreatedIdentityInvitation:
    business = _get_owned_business(db, current_user)

    _validate_invitation_location(
        db,
        business_id=business.id,
        location_id=invitation_data.location_id,
    )

    normalized_email = str(invitation_data.email).strip().lower()

    _validate_email_availability(
        db,
        business_id=business.id,
        email=normalized_email,
    )

    raw_token = generate_invitation_token()
    token_hash = hash_invitation_token(raw_token)

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(
        hours=settings.IDENTITY_INVITATION_EXPIRE_HOURS
    )

    try:
        employee = create_employee_in_transaction(
            db,
            business_id=business.id,
            location_id=invitation_data.location_id,
            full_name=invitation_data.full_name,
            email=normalized_email,
            phone=invitation_data.phone,
            role=invitation_data.role,
        )

        invitation = create_identity_invitation(
            db,
            business_id=business.id,
            employee_id=employee.id,
            email=normalized_email,
            role=invitation_data.role.value,
            token_hash=token_hash,
            expires_at=expires_at,
            created_by_user_id=current_user.id,
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
            detail="The employee invitation conflicts with existing identity data",
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


def accept_identity_invitation_service(
    db: Session,
    *,
    token: str,
    password: str,
):
    from app.core.enums import (
        EmployeeStatus,
        IdentityInvitationStatus,
        UserRole,
    )
    from app.core.security import hash_password
    from app.repositories.employee_repository import (
        get_employee_by_id,
        link_employee_to_user,
    )
    from app.repositories.identity_invitation_repository import (
        get_identity_invitation_by_token_hash,
        mark_identity_invitation_accepted,
        mark_identity_invitation_expired,
    )
    from app.repositories.user_repository import (
        create_user_in_transaction,
    )

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

    now = datetime.now(timezone.utc)

    expires_at = invitation.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= now:
        try:
            mark_identity_invitation_expired(
                db,
                invitation,
            )
            db.commit()
        except SQLAlchemyError:
            db.rollback()

        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Invitation has expired",
        )

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
            detail="Invitation employee does not belong to the invitation business",
        )

    if employee.email is None or (
        employee.email.strip().lower()
        != invitation.email.strip().lower()
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invitation email does not match the employee",
        )

    if employee.user_id is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee already has a user account",
        )

    if employee.status != EmployeeStatus.INVITED.value:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee is not awaiting invitation acceptance",
        )

    existing_user = get_user_by_email(
        db,
        invitation.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user account already exists with this email",
        )

    try:
        user = create_user_in_transaction(
            db,
            full_name=employee.full_name,
            email=invitation.email,
            hashed_password=hash_password(password),
            role=UserRole.EMPLOYEE.value,
        )

        link_employee_to_user(
            db,
            employee,
            user_id=user.id,
        )

        mark_identity_invitation_accepted(
            db,
            invitation,
            accepted_user_id=user.id,
            accepted_at=now,
        )

        db.commit()

        db.refresh(user)
        db.refresh(employee)
        db.refresh(invitation)

        return {
            "message": "Invitation accepted successfully",
            "employee_id": employee.id,
            "user": user,
        }

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unable to create the employee user account because identity data already exists",
        ) from exc

    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to accept employee invitation",
        ) from exc
