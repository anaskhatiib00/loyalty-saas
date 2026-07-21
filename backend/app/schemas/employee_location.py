from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EmployeeLocationAssign(BaseModel):
    location_id: int
    is_primary: bool = False


class EmployeeLocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int
    location_id: int
    assigned_by_user_id: int
    assigned_at: datetime
    is_primary: bool
    is_active: bool