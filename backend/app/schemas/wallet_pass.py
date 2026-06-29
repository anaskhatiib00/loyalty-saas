from pydantic import BaseModel

from app.core.enums import WalletProvider, WalletPassStatus


class WalletPassResponse(BaseModel):
    id: int
    loyalty_card_id: int
    provider: WalletProvider
    status: WalletPassStatus

    class Config:
        from_attributes = True