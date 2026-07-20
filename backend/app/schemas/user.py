from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class BusinessSummary(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CurrentEmployeeSummary(BaseModel):
    id: int
    business_id: int
    location_id: Optional[int] = None
    role: str
    status: str

    class Config:
        from_attributes = True


class CurrentUserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    # General account identity:
    # business_owner or employee
    role: str
    account_type: str

    business: BusinessSummary | None = None
    employee: CurrentEmployeeSummary | None = None

    class Config:
        from_attributes = True
