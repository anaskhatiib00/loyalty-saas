from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.loyalty_activity import (
    LoyaltyActivityCreate,
    LoyaltyActivityResponse,
)
from app.application.loyalty_activity_application import (
    process_loyalty_activity_application,
)
from app.services.loyalty_activity_service import list_customer_activities_service


router = APIRouter(
    prefix="/loyalty-activities",
    tags=["Loyalty Activities"],
)


@router.post("")
def process_loyalty_activity(
    activity_data: LoyaltyActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return process_loyalty_activity_application(db, current_user, activity_data)


@router.get("/customer/{customer_id}", response_model=list[LoyaltyActivityResponse])
def list_customer_activities(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_customer_activities_service(db, current_user, customer_id)