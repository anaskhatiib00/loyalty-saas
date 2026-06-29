from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.customer_repository import get_customer_by_id
from app.repositories.loyalty_card_repository import (
    get_loyalty_card_by_public_id,
    get_loyalty_card_by_card_number,
)
from app.schemas.scan import ScanResolveRequest


def resolve_scan_service(
    db: Session,
    current_user: User,
    scan_data: ScanResolveRequest,
):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(status_code=404, detail="Business profile not found")

    card = get_loyalty_card_by_public_id(db, scan_data.identifier)

    if not card:
        card = get_loyalty_card_by_card_number(db, scan_data.identifier)

    if not card:
        raise HTTPException(status_code=404, detail="Loyalty card not found")

    customer = get_customer_by_id(db, card.customer_id)

    if not customer or customer.business_id != business.id:
        raise HTTPException(status_code=404, detail="Customer not found")

    if card.status != "active":
        raise HTTPException(status_code=400, detail="Loyalty card is not active")

    if not customer.is_active:
        raise HTTPException(status_code=400, detail="Customer is not active")

    return {
        "loyalty_card": card,
        "customer": customer,
    }