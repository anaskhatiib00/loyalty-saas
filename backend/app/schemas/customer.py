from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    location_id: int
    first_name: str
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None


class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None
    is_active: Optional[bool] = None


class CustomerResponse(BaseModel):
    id: int
    business_id: int
    location_id: int
    first_name: str
    last_name: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    date_of_birth: Optional[date]
    current_progress: int
    total_rewards_redeemed: int
    is_active: bool

    class Config:
        from_attributes = True