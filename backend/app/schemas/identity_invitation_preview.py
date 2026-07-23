from datetime import datetime

from pydantic import BaseModel

from app.core.enums import EmployeeRole


class IdentityInvitationPreviewResponse(BaseModel):
    business_name: str
    employee_name: str
    role: EmployeeRole
    expires_at: datetime