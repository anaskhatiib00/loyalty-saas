from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import LoyaltyActivityType, ProgramType
from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.customer_repository import get_customer_by_id
from app.repositories.location_repository import get_location_by_id
from app.repositories.loyalty_card_repository import (
    get_loyalty_card_by_card_number,
    get_loyalty_card_by_public_id,
)
from app.repositories.loyalty_program_repository import (
    get_loyalty_program_by_business_id,
)
from app.schemas.loyalty_activity import LoyaltyActivityCreate
from app.schemas.pos import POSScanRequest
from app.application.use_cases.process_loyalty_activity import (
    process_loyalty_activity_use_case,
)


def get_activity_type_for_program(program_type: str) -> LoyaltyActivityType:
    program_activity_map = {
        ProgramType.POINTS.value: LoyaltyActivityType.PURCHASE,
        ProgramType.STAMPS.value: LoyaltyActivityType.STAMP_SCAN,
        ProgramType.VISITS.value: LoyaltyActivityType.VISIT,
        ProgramType.SPEND.value: LoyaltyActivityType.PURCHASE,
        ProgramType.PRODUCT.value: LoyaltyActivityType.PRODUCT_PURCHASE,
    }

    activity_type = program_activity_map.get(program_type)

    if not activity_type:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported loyalty program type: {program_type}",
        )

    return activity_type


def process_loyalty_scan_use_case(
    db: Session,
    current_user: User,
    scan_data: POSScanRequest,
):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(status_code=404, detail="Business profile not found")

    location = get_location_by_id(db, scan_data.location_id)

    if not location or location.business_id != business.id:
        raise HTTPException(status_code=404, detail="Location not found")

    card = get_loyalty_card_by_public_id(
        db,
        scan_data.loyalty_card_identifier,
    )

    if not card:
        card = get_loyalty_card_by_card_number(
            db,
            scan_data.loyalty_card_identifier,
        )

    if not card:
        raise HTTPException(status_code=404, detail="Loyalty card not found")

    if card.status != "active":
        raise HTTPException(status_code=400, detail="Loyalty card is not active")

    customer = get_customer_by_id(db, card.customer_id)

    if not customer or customer.business_id != business.id:
        raise HTTPException(status_code=404, detail="Customer not found")

    if not customer.is_active:
        raise HTTPException(status_code=400, detail="Customer is not active")

    program = get_loyalty_program_by_business_id(db, business.id)

    if not program:
        raise HTTPException(status_code=404, detail="Loyalty program not found")

    if not program.is_active:
        raise HTTPException(status_code=400, detail="Loyalty program is not active")

    activity_type = get_activity_type_for_program(program.program_type)

    activity_data = LoyaltyActivityCreate(
        loyalty_card_identifier=scan_data.loyalty_card_identifier,
        location_id=location.id,
        activity_type=activity_type,
        purchase_amount=0,
        qualifying_quantity=1,
        note="Employee POS automatic scan",
    )

    activity_result = process_loyalty_activity_use_case(
        db=db,
        current_user=current_user,
        activity_data=activity_data,
    )

    db.refresh(customer)

    return {
        "customer_id": customer.id,
        "loyalty_card_id": card.id,
        "program_type": program.program_type,
        "current_progress": customer.current_progress,
        "reward_available": len(activity_result["unlocked_rewards"]) > 0,
        "reward_collected": activity_result["reward_collected"],
        "unlocked_rewards": activity_result["unlocked_rewards"],
    }