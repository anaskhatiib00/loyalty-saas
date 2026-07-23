from sqlalchemy.orm import Session

from app.application.identity.invitations.acceptance import (
    accept_identity_invitation,
)
from app.application.identity.invitations.creation import (
    create_identity_invitation,
)
from app.application.identity.invitations.preview import (
    preview_identity_invitation,
)
from app.application.identity.invitations.types import (
    CreatedIdentityInvitation,
)
from app.schemas.identity_invitation import IdentityInvitationCreate


def create_identity_invitation_service(
    db: Session,
    *,
    business_id: int,
    created_by_user_id: int,
    invitation_data: IdentityInvitationCreate,
) -> CreatedIdentityInvitation:
    return create_identity_invitation(
        db,
        business_id=business_id,
        created_by_user_id=created_by_user_id,
        invitation_data=invitation_data,
    )


def preview_identity_invitation_service(
    db: Session,
    *,
    token: str,
):
    return preview_identity_invitation(
        db,
        token=token,
    )


def accept_identity_invitation_service(
    db: Session,
    *,
    token: str,
    password: str,
):
    return accept_identity_invitation(
        db,
        token=token,
        password=password,
    )