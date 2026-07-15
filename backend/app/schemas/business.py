from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.business_settings import (
    BusinessSettingsCreate,
    BusinessSettingsResponse,
)


class BusinessCreate(BaseModel):
    name: str
    business_type: str
    phone: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    brand_color: str = "#000000"
    settings: BusinessSettingsCreate


class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    business_type: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    brand_color: Optional[str] = None


class BusinessResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    name: str
    business_type: str
    phone: Optional[str]
    address: Optional[str]
    logo_url: Optional[str]
    brand_color: str
    settings: BusinessSettingsResponse