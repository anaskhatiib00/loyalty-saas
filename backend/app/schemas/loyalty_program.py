from typing import Optional

from pydantic import BaseModel


class LoyaltyProgramCreate(BaseModel):
    name: str
    description: Optional[str] = None
    points_per_currency_unit: float = 1.0
    currency_unit: str = "USD"
    welcome_bonus_points: int = 0
    birthday_bonus_points: int = 0
    referral_bonus_points: int = 0
    points_expire: bool = False
    expiration_months: Optional[int] = None
    is_active: bool = True


class LoyaltyProgramUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    points_per_currency_unit: Optional[float] = None
    currency_unit: Optional[str] = None
    welcome_bonus_points: Optional[int] = None
    birthday_bonus_points: Optional[int] = None
    referral_bonus_points: Optional[int] = None
    points_expire: Optional[bool] = None
    expiration_months: Optional[int] = None
    is_active: Optional[bool] = None


class LoyaltyProgramResponse(BaseModel):
    id: int
    business_id: int
    name: str
    description: Optional[str]
    points_per_currency_unit: float
    currency_unit: str
    welcome_bonus_points: int
    birthday_bonus_points: int
    referral_bonus_points: int
    points_expire: bool
    expiration_months: Optional[int]
    is_active: bool

    class Config:
        from_attributes = True