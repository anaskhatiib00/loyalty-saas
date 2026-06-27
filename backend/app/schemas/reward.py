from typing import Optional

from pydantic import BaseModel

from app.core.enums import RewardType

from app.core.enums import RewardType, RedemptionBehavior, RedemptionMode

class RewardCreate(BaseModel):
    name: str
    description: Optional[str] = None
    required_value: int
    reward_type: RewardType = RewardType.DISCOUNT
    reward_value: Optional[str] = None
    is_active: bool = True
    redemption_behavior: RedemptionBehavior = RedemptionBehavior.DEDUCT
    redemption_mode: RedemptionMode = RedemptionMode.MANUAL


class RewardUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    required_value: Optional[int] = None
    reward_type: Optional[RewardType] = None
    reward_value: Optional[str] = None
    is_active: Optional[bool] = None
    redemption_behavior: Optional[RedemptionBehavior] = None
    redemption_mode: Optional[RedemptionMode] = None


class RewardResponse(BaseModel):
    id: int
    business_id: int
    name: str
    description: Optional[str]
    required_value: int
    reward_type: RewardType
    reward_value: Optional[str]
    is_active: bool
    redemption_behavior: RedemptionBehavior
    redemption_mode: RedemptionMode

    class Config:
        from_attributes = True