from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.customer_repository import get_customer_by_id
from app.repositories.loyalty_activity_repository import get_activities_by_customer_id


def list_customer_activities_service(
    db: Session,
    current_user: User,
    customer_id: int,
):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(status_code=404, detail="Business profile not found")

    customer = get_customer_by_id(db, customer_id)

    if not customer or customer.business_id != business.id:
        raise HTTPException(status_code=404, detail="Customer not found")

    return get_activities_by_customer_id(db, customer.id)