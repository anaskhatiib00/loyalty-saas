from pydantic import BaseModel


class LoyaltyCardCreate(BaseModel):
    customer_id: int


class LoyaltyCardResponse(BaseModel):
    id: int
    customer_id: int
    card_number: str
    public_id: str
    status: str

    class Config:
        from_attributes = True