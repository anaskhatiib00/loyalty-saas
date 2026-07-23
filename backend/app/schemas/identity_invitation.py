from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.enums import EmployeeRole, IdentityInvitationStatus
from app.schemas.user import UserResponse


class IdentityInvitationCreate(BaseModel):
    location_id: int | None = None
    full_name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=50)
    role: EmployeeRole = EmployeeRole.CASHIER

    @field_validator("full_name")
    @classmethod
    def normalize_full_name(cls, value: str) -> str:
        normalized = " ".join(value.strip().split())

        if not normalized:
            raise ValueError("Full name cannot be empty")

        return normalized

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip()

        return normalized or None

    @field_validator("role")
    @classmethod
    def reject_owner_role(cls, value: EmployeeRole) -> EmployeeRole:
        if value == EmployeeRole.OWNER:
            raise ValueError(
                "Business owner accounts cannot be created through employee invitations"
            )

        return value


class IdentityInvitationAccept(BaseModel):
    token: str = Field(min_length=32, max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("token")
    @classmethod
    def normalize_token(cls, value: str) -> str:
        normalized = value.strip()

        if not normalized:
            raise ValueError("Invitation token cannot be empty")

        return normalized


class IdentityInvitationResponse(BaseModel):
    id: int
    business_id: int
    employee_id: int | None
    email: EmailStr
    role: EmployeeRole
    status: IdentityInvitationStatus
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class IdentityInvitationCreatedResponse(BaseModel):
    invitation: IdentityInvitationResponse
    employee_id: int
    delivery_status: str = "pending"
    development_invitation_token: str | None = None
    development_accept_url: str | None = None


class IdentityInvitationAcceptedResponse(BaseModel):
    message: str
    employee_id: int
    user: UserResponse
