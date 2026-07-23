from dataclasses import dataclass

from app.models.identity_invitation import IdentityInvitation


@dataclass(frozen=True)
class CreatedIdentityInvitation:
    invitation: IdentityInvitation
    raw_token: str
