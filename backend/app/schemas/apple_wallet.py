from pydantic import BaseModel


class AppleWalletRegistrationRequest(BaseModel):
    pushToken: str