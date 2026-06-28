from typing import Optional

from pydantic import BaseModel

from app.core.enums import LoyaltyActivityType, LoyaltyActivityStatus


class LoyaltyActivityCreate(BaseModel):
    loyalty_card_identifier: str
    location_id: int
    employee_id: Optional[int] = None
    activity_type: LoyaltyActivityType
    purchase_amount: float = 0
    qualifying_quantity: int = 1
    note: Optional[str] = None


class LoyaltyActivityResponse(BaseModel):
    id: int
    business_id: int
    location_id: int
    employee_id: Optional[int]
    customer_id: int
    loyalty_card_id: int
    activity_type: LoyaltyActivityType
    status: LoyaltyActivityStatus
    purchase_amount: float
    qualifying_quantity: int
    earned_progress: int
    balance_after: int
    note: Optional[str]

    class Config:
        from_attributes = True


class LoyaltyActivityResult(BaseModel):
    activity: LoyaltyActivityResponse
    unlocked_rewards: list