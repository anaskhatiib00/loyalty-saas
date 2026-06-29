from typing import Optional

from pydantic import BaseModel


class ScanResolveRequest(BaseModel):
    identifier: str


class ScanCustomerResponse(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    current_progress: int
    is_active: bool

    class Config:
        from_attributes = True


class ScanLoyaltyCardResponse(BaseModel):
    id: int
    card_number: str
    public_id: str
    status: str

    class Config:
        from_attributes = True


class ScanResolveResponse(BaseModel):
    loyalty_card: ScanLoyaltyCardResponse
    customer: ScanCustomerResponse