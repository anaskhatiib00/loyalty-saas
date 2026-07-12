from sqlalchemy.orm import Session

from app.application.use_cases.loyalty_scan.resolve_employee_context import (
    resolve_employee_context,
)
from app.models.loyalty_activity import LoyaltyActivity
from app.models.user import User
from app.repositories.loyalty_activity_repository import (
    get_recent_activities_by_employee_id,
)
from app.schemas.pos_activity import (
    POSActivityItem,
    POSRecentActivityResponse,
)


def _resolve_program_type(activity: LoyaltyActivity) -> str:
    if activity.loyalty_program is not None:
        program_type = activity.loyalty_program.program_type

        if hasattr(program_type, "value"):
            return program_type.value

        return str(program_type)

    return activity.activity_type


def _build_activity_item(
    activity: LoyaltyActivity,
) -> POSActivityItem:
    return POSActivityItem(
        id=activity.id,
        customer_id=activity.customer_id,
        customer_name=(
            activity.customer_name_snapshot
            or "Unknown customer"
        ),
        employee_id=activity.employee_id,
        employee_name=(
            activity.employee_name_snapshot
            or "Unknown employee"
        ),
        location_id=activity.location_id,
        location_name=(
            activity.location_name_snapshot
            or "Unknown location"
        ),
        program_type=_resolve_program_type(activity),
        event_type=activity.event_type,
        activity_type=activity.activity_type,
        source=activity.source,
        progress_change=activity.progress_change,
        balance_before=activity.balance_before,
        balance_after=activity.balance_after,
        reward_id=activity.reward_id,
        reward_name=activity.reward_name_snapshot,
        created_at=activity.created_at,
    )


def get_pos_recent_activity_use_case(
    db: Session,
    current_user: User,
    limit: int = 20,
) -> POSRecentActivityResponse:
    employee_context = resolve_employee_context(
        db=db,
        current_user=current_user,
    )

    activities = get_recent_activities_by_employee_id(
        db=db,
        business_id=employee_context.business.id,
        employee_id=employee_context.employee.id,
        location_id=employee_context.location.id,
        limit=limit,
    )

    activity_items = [
        _build_activity_item(activity)
        for activity in activities
    ]

    return POSRecentActivityResponse(
        employee_id=employee_context.employee.id,
        employee_name=employee_context.employee.full_name,
        location_id=employee_context.location.id,
        location_name=employee_context.location.name,
        total_activities=len(activity_items),
        activities=activity_items,
    )