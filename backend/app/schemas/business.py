from pydantic import BaseModel
from typing import Optional


class BusinessCreate(BaseModel):
    name: str
    business_type: str
    phone: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    brand_color: str = "#000000"


class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    business_type: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    brand_color: Optional[str] = None


class BusinessResponse(BaseModel):
    id: int
    owner_id: int
    name: str
    business_type: str
    phone: Optional[str]
    address: Optional[str]
    logo_url: Optional[str]
    brand_color: str

    class Config:
        from_attributes = True