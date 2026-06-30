from pydantic import BaseModel

from app.core.enums import CredentialProvider, CredentialStatus


class CredentialCreate(BaseModel):
    loyalty_card_id: int
    provider: CredentialProvider


class CredentialResponse(BaseModel):
    id: int
    loyalty_card_id: int
    provider: CredentialProvider
    provider_reference: str | None
    authentication_token: str | None
    status: CredentialStatus

    class Config:
        from_attributes = True