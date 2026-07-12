from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.application.use_cases.get_manager_activity_feed import (
    get_manager_activity_feed_use_case,
)
from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.manager_activity import (
    ManagerActivityFeedResponse,
)

router = APIRouter(
    prefix="/manager",
    tags=["Manager Dashboard"],
)


@router.get(
    "/activity",
    response_model=ManagerActivityFeedResponse,
)
def get_manager_activity(
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
    ),
    location_id: int | None = Query(default=None),
    employee_id: int | None = Query(default=None),
    event_type: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_manager_activity_feed_use_case(
        db=db,
        current_user=current_user,
        location_id=location_id,
        employee_id=employee_id,
        event_type=event_type,
        limit=limit,
    )