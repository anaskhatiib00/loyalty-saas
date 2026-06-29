from pydantic import BaseModel

from app.core.enums import CredentialProvider, CredentialStatus


class CredentialResponse(BaseModel):
    id: int
    loyalty_card_id: int
    provider: CredentialProvider
    status: CredentialStatus

    class Config:
        from_attributes = True