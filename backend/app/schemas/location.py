from typing import Optional

from pydantic import BaseModel


class LocationCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    address: str
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    is_default: bool = False


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    is_default: Optional[bool] = None


class LocationResponse(BaseModel):
    id: int
    business_id: int
    name: str
    phone: Optional[str]
    address: str
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    is_default: bool

    class Config:
        from_attributes = True