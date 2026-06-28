from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.customer_repository import get_customer_by_id
from app.repositories.loyalty_card_repository import (
    create_loyalty_card,
    get_loyalty_card_by_customer_id,
    get_loyalty_card_by_public_id,
    get_loyalty_card_by_card_number,
)
from app.schemas.loyalty_card import LoyaltyCardCreate
from app.utils.card_number import generate_card_number, generate_public_id


def create_loyalty_card_service(
    db: Session,
    current_user: User,
    card_data: LoyaltyCardCreate,
):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(status_code=404, detail="Business profile not found")

    customer = get_customer_by_id(db, card_data.customer_id)

    if not customer or customer.business_id != business.id:
        raise HTTPException(status_code=404, detail="Customer not found")

    existing_card = get_loyalty_card_by_customer_id(db, customer.id)

    if existing_card:
        raise HTTPException(
            status_code=400,
            detail="Customer already has a loyalty card",
        )

    card_number = generate_card_number(business.name)
    public_id = generate_public_id()

    return create_loyalty_card(
        db=db,
        customer_id=customer.id,
        card_number=card_number,
        public_id=public_id,
    )


def get_loyalty_card_by_customer_service(
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

    card = get_loyalty_card_by_customer_id(db, customer.id)

    if not card:
        raise HTTPException(status_code=404, detail="Loyalty card not found")

    return card


def lookup_loyalty_card_service(
    db: Session,
    identifier: str,
):
    card = get_loyalty_card_by_public_id(db, identifier)

    if not card:
        card = get_loyalty_card_by_card_number(db, identifier)

    if not card:
        raise HTTPException(status_code=404, detail="Loyalty card not found")

    return card