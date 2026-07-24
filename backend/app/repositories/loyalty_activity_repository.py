from sqlalchemy.orm import Session

from app.models.loyalty_activity import LoyaltyActivity

from datetime import datetime


def create_loyalty_activity(
    db: Session,
    *,
    business_id: int,
    location_id: int,
    employee_id: int | None,
    customer_id: int,
    loyalty_card_id: int,
    loyalty_program_id: int | None,
    reward_id: int | None,
    event_type: str,
    activity_type: str,
    source: str,
    status: str,
    purchase_amount: float,
    qualifying_quantity: int,
    progress_change: int,
    balance_before: int,
    balance_after: int,
    customer_name_snapshot: str | None,
    employee_name_snapshot: str | None,
    location_name_snapshot: str | None,
    program_name_snapshot: str | None,
    reward_name_snapshot: str | None,
    idempotency_key: str | None = None,
    note: str | None = None,
) -> LoyaltyActivity:
    activity = LoyaltyActivity(
        business_id=business_id,
        location_id=location_id,
        employee_id=employee_id,
        customer_id=customer_id,
        loyalty_card_id=loyalty_card_id,
        loyalty_program_id=loyalty_program_id,
        reward_id=reward_id,
        event_type=event_type,
        activity_type=activity_type,
        source=source,
        status=status,
        purchase_amount=purchase_amount,
        qualifying_quantity=qualifying_quantity,
        progress_change=progress_change,
        balance_before=balance_before,
        balance_after=balance_after,
        customer_name_snapshot=customer_name_snapshot,
        employee_name_snapshot=employee_name_snapshot,
        location_name_snapshot=location_name_snapshot,
        program_name_snapshot=program_name_snapshot,
        reward_name_snapshot=reward_name_snapshot,
        idempotency_key=idempotency_key,
        note=note,
    )

    db.add(activity)
    db.flush()

    return activity


def get_activities_by_customer_id(
    db: Session,
    customer_id: int,
) -> list[LoyaltyActivity]:
    return (
        db.query(LoyaltyActivity)
        .filter(LoyaltyActivity.customer_id == customer_id)
        .order_by(
            LoyaltyActivity.created_at.desc(),
            LoyaltyActivity.id.desc(),
        )
        .all()
    )


def get_recent_activities_by_employee_id(
    db: Session,
    *,
    business_id: int,
    employee_id: int,
    location_id: int,
    start_at: datetime,
    end_at: datetime,
    limit: int = 20,
) -> list[LoyaltyActivity]:
    safe_limit = max(1, min(limit, 100))

    return (
        db.query(LoyaltyActivity)
        .filter(
            LoyaltyActivity.business_id == business_id,
            LoyaltyActivity.employee_id == employee_id,
            LoyaltyActivity.location_id == location_id,
            LoyaltyActivity.source == "employee_pos",
            LoyaltyActivity.status == "completed",
            LoyaltyActivity.created_at >= start_at,
            LoyaltyActivity.created_at < end_at,
        )
        .order_by(
            LoyaltyActivity.created_at.desc(),
            LoyaltyActivity.id.desc(),
        )
        .limit(safe_limit)
        .all()
    )


def get_recent_activities_by_business_id(
    db: Session,
    *,
    business_id: int,
    location_id: int | None = None,
    employee_id: int | None = None,
    event_type: str | None = None,
    limit: int = 50,
) -> list[LoyaltyActivity]:
    safe_limit = max(1, min(limit, 100))

    query = db.query(LoyaltyActivity).filter(
        LoyaltyActivity.business_id == business_id,
        LoyaltyActivity.status == "completed",
    )

    if location_id is not None:
        query = query.filter(
            LoyaltyActivity.location_id == location_id,
        )

    if employee_id is not None:
        query = query.filter(
            LoyaltyActivity.employee_id == employee_id,
        )

    if event_type:
        query = query.filter(
            LoyaltyActivity.event_type == event_type,
        )

    return (
        query.order_by(
            LoyaltyActivity.created_at.desc(),
            LoyaltyActivity.id.desc(),
        )
        .limit(safe_limit)
        .all()
    )