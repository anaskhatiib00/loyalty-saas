from typing import Optional

from pydantic import BaseModel


class RewardCreate(BaseModel):
    name: str
    description: Optional[str] = None
    points_required: int
    reward_type: str = "discount"
    reward_value: Optional[str] = None
    is_active: bool = True


class RewardUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    points_required: Optional[int] = None
    reward_type: Optional[str] = None
    reward_value: Optional[str] = None
    is_active: Optional[bool] = None


class RewardResponse(BaseModel):
    id: int
    business_id: int
    name: str
    description: Optional[str]
    points_required: int
    reward_type: str
    reward_value: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True