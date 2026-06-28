from typing import Optional

from pydantic import BaseModel, EmailStr

from app.core.enums import EmployeeRole, EmployeeStatus


class EmployeeCreate(BaseModel):
    location_id: Optional[int] = None
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: EmployeeRole = EmployeeRole.CASHIER
    status: EmployeeStatus = EmployeeStatus.ACTIVE


class EmployeeUpdate(BaseModel):
    location_id: Optional[int] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[EmployeeRole] = None
    status: Optional[EmployeeStatus] = None


class EmployeeResponse(BaseModel):
    id: int
    business_id: int
    location_id: Optional[int]
    full_name: str
    email: Optional[EmailStr]
    phone: Optional[str]
    role: EmployeeRole
    status: EmployeeStatus

    class Config:
        from_attributes = True