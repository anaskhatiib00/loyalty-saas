from sqlalchemy.orm import Session

from app.models.loyalty_activity import LoyaltyActivity
from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.loyalty_activity_repository import (
    get_recent_activities_by_business_id,
)
from app.schemas.manager_activity import (
    ManagerActivityFeedResponse,
    ManagerActivityItem,
)


def _resolve_program_type(activity: LoyaltyActivity) -> str:
    if activity.loyalty_program is not None:
        program_type = activity.loyalty_program.program_type

        if hasattr(program_type, "value"):
            return program_type.value

        return str(program_type)

    return activity.activity_type


def _build_manager_activity_item(
    activity: LoyaltyActivity,
) -> ManagerActivityItem:
    return ManagerActivityItem(
        id=activity.id,
        customer_id=activity.customer_id,
        customer_name=(
            activity.customer_name_snapshot
            or "Unknown customer"
        ),
        employee_id=activity.employee_id,
        employee_name=activity.employee_name_snapshot,
        location_id=activity.location_id,
        location_name=(
            activity.location_name_snapshot
            or "Unknown location"
        ),
        loyalty_program_id=activity.loyalty_program_id,
        program_name=activity.program_name_snapshot,
        program_type=_resolve_program_type(activity),
        event_type=activity.event_type,
        activity_type=activity.activity_type,
        source=activity.source,
        status=activity.status,
        progress_change=activity.progress_change,
        balance_before=activity.balance_before,
        balance_after=activity.balance_after,
        reward_id=activity.reward_id,
        reward_name=activity.reward_name_snapshot,
        created_at=activity.created_at,
    )


def get_manager_activity_feed_use_case(
    db: Session,
    current_user: User,
    *,
    location_id: int | None = None,
    employee_id: int | None = None,
    event_type: str | None = None,
    limit: int = 50,
) -> ManagerActivityFeedResponse:
    business = get_business_by_owner_id(
        db,
        current_user.id,
    )

    if not business:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Business profile not found",
        )

    activities = get_recent_activities_by_business_id(
        db=db,
        business_id=business.id,
        location_id=location_id,
        employee_id=employee_id,
        event_type=event_type,
        limit=limit,
    )

    activity_items = [
        _build_manager_activity_item(activity)
        for activity in activities
    ]

    return ManagerActivityFeedResponse(
        total_activities=len(activity_items),
        activities=activity_items,
    )