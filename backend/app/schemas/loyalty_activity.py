from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.core.enums import LoyaltyActivityStatus, LoyaltyActivityType


class LoyaltyActivityCreate(BaseModel):
    loyalty_card_identifier: str
    location_id: int
    employee_id: int | None = None

    activity_type: LoyaltyActivityType

    purchase_amount: float = 0
    qualifying_quantity: int = 1

    note: str | None = None


class LoyaltyActivityResponse(BaseModel):
    id: int

    business_id: int
    location_id: int
    employee_id: int | None = None

    customer_id: int
    loyalty_card_id: int
    loyalty_program_id: int | None = None
    reward_id: int | None = None

    event_type: str
    activity_type: LoyaltyActivityType
    source: str
    status: LoyaltyActivityStatus

    purchase_amount: float
    qualifying_quantity: int

    progress_change: int
    balance_before: int
    balance_after: int

    customer_name_snapshot: str | None = None
    employee_name_snapshot: str | None = None
    location_name_snapshot: str | None = None
    program_name_snapshot: str | None = None
    reward_name_snapshot: str | None = None

    note: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class LoyaltyActivityResult(BaseModel):
    activity: LoyaltyActivityResponse
    unlocked_rewards: list[dict[str, Any]]
    reward_collected: bool = False