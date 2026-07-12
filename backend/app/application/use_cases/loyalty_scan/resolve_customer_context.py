from dataclasses import dataclass

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.loyalty_card import LoyaltyCard
from app.repositories.customer_repository import get_customer_by_id
from app.repositories.loyalty_card_repository import (
    get_loyalty_card_by_card_number,
    get_loyalty_card_by_public_id,
)


@dataclass
class CustomerScanContext:
    customer: Customer
    loyalty_card: LoyaltyCard


def resolve_customer_context(
    db: Session,
    business_id: int,
    loyalty_card_identifier: str,
) -> CustomerScanContext:
    loyalty_card = get_loyalty_card_by_public_id(
        db,
        loyalty_card_identifier,
    )

    if not loyalty_card:
        loyalty_card = get_loyalty_card_by_card_number(
            db,
            loyalty_card_identifier,
        )

    if not loyalty_card:
        raise HTTPException(status_code=404, detail="Loyalty card not found")

    if loyalty_card.status != "active":
        raise HTTPException(status_code=400, detail="Loyalty card is not active")

    customer = get_customer_by_id(db, loyalty_card.customer_id)

    if not customer or customer.business_id != business_id:
        raise HTTPException(status_code=404, detail="Customer not found")

    if not customer.is_active:
        raise HTTPException(status_code=400, detail="Customer is not active")

    return CustomerScanContext(
        customer=customer,
        loyalty_card=loyalty_card,
    )