from datetime import datetime

from pydantic import BaseModel


class POSActivityItem(BaseModel):
    id: int

    customer_id: int
    customer_name: str

    employee_id: int
    employee_name: str

    location_id: int
    location_name: str

    program_type: str
    event_type: str
    activity_type: str
    source: str

    progress_change: int
    balance_before: int
    balance_after: int

    reward_id: int | None = None
    reward_name: str | None = None

    created_at: datetime


class POSRecentActivityResponse(BaseModel):
    employee_id: int
    employee_name: str

    location_id: int
    location_name: str

    total_activities: int
    activities: list[POSActivityItem]