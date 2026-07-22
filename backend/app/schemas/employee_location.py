from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EmployeeLocationAssign(BaseModel):
    location_id: int = Field(gt=0)
    is_primary: bool = False


class EmployeeCurrentLocationSelect(BaseModel):
    location_id: int = Field(gt=0)


class EmployeeLocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int
    location_id: int
    assigned_by_user_id: int | None
    assigned_at: datetime
    is_primary: bool
    is_current: bool
    is_active: bool