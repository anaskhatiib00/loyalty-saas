from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.application.identity.invitations.validation import (
    get_invited_employee,
    get_valid_pending_invitation,
)
from app.core.enums import EmployeeStatus, UserRole
from app.core.security import hash_password
from app.repositories.employee_repository import link_employee_to_user
from app.repositories.identity_invitation_repository import (
    mark_identity_invitation_accepted,
)
from app.repositories.user_repository import (
    create_user_in_transaction,
    get_user_by_email,
)


def accept_identity_invitation(
    db: Session,
    *,
    token: str,
    password: str,
):
    invitation = get_valid_pending_invitation(
        db,
        token=token,
    )

    employee = get_invited_employee(
        db,
        invitation=invitation,
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

    now = datetime.now(timezone.utc)

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
            detail=(
                "Unable to create the employee user account "
                "because identity data already exists"
            ),
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
