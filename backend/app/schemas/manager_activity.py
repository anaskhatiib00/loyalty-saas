from datetime import datetime

from pydantic import BaseModel


class ManagerActivityItem(BaseModel):
    id: int

    customer_id: int
    customer_name: str

    employee_id: int | None = None
    employee_name: str | None = None

    location_id: int
    location_name: str

    loyalty_program_id: int | None = None
    program_name: str | None = None
    program_type: str

    event_type: str
    activity_type: str
    source: str
    status: str

    progress_change: int
    balance_before: int
    balance_after: int

    reward_id: int | None = None
    reward_name: str | None = None

    created_at: datetime


class ManagerActivityFeedResponse(BaseModel):
    total_activities: int
    activities: list[ManagerActivityItem]