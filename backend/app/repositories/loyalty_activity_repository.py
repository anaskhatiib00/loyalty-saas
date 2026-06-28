from sqlalchemy.orm import Session

from app.models.loyalty_activity import LoyaltyActivity


def create_loyalty_activity(
    db: Session,
    business_id: int,
    location_id: int,
    employee_id: int | None,
    customer_id: int,
    loyalty_card_id: int,
    activity_type: str,
    purchase_amount: float,
    qualifying_quantity: int,
    earned_progress: int,
    balance_after: int,
    note: str | None = None,
):
    activity = LoyaltyActivity(
        business_id=business_id,
        location_id=location_id,
        employee_id=employee_id,
        customer_id=customer_id,
        loyalty_card_id=loyalty_card_id,
        activity_type=activity_type,
        purchase_amount=purchase_amount,
        qualifying_quantity=qualifying_quantity,
        earned_progress=earned_progress,
        balance_after=balance_after,
        note=note,
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


def get_activities_by_customer_id(db: Session, customer_id: int):
    return (
        db.query(LoyaltyActivity)
        .filter(LoyaltyActivity.customer_id == customer_id)
        .order_by(LoyaltyActivity.created_at.desc())
        .all()
    )