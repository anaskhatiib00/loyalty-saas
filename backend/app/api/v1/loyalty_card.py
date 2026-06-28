from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.loyalty_card import LoyaltyCardCreate, LoyaltyCardResponse
from app.services.loyalty_card_service import (
    create_loyalty_card_service,
    get_loyalty_card_by_customer_service,
    lookup_loyalty_card_service,
)


router = APIRouter(
    prefix="/loyalty-cards",
    tags=["Loyalty Cards"],
)


@router.post("", response_model=LoyaltyCardResponse)
def create_loyalty_card(
    card_data: LoyaltyCardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_loyalty_card_service(db, current_user, card_data)


@router.get("/customer/{customer_id}", response_model=LoyaltyCardResponse)
def get_loyalty_card_by_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_loyalty_card_by_customer_service(db, current_user, customer_id)


@router.get("/lookup/{identifier}", response_model=LoyaltyCardResponse)
def lookup_loyalty_card(
    identifier: str,
    db: Session = Depends(get_db),
):
    return lookup_loyalty_card_service(db, identifier)