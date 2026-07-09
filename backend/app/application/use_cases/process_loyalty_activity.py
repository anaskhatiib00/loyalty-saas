from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import LedgerEntryType, ProgramType
from app.loyalty.engine import calculate_loyalty_progress
from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.customer_repository import get_customer_by_id
from app.repositories.employee_repository import get_employee_by_id
from app.repositories.location_repository import get_location_by_id
from app.repositories.loyalty_activity_repository import create_loyalty_activity
from app.repositories.loyalty_card_repository import (
    get_loyalty_card_by_card_number,
    get_loyalty_card_by_public_id,
)
from app.repositories.loyalty_program_repository import get_loyalty_program_by_business_id
from app.repositories.progress_ledger_repository import create_ledger_entry
from app.repositories.reward_repository import get_rewards_by_business_id
from app.schemas.loyalty_activity import LoyaltyActivityCreate


def process_loyalty_activity_use_case(
    db: Session,
    current_user: User,
    activity_data: LoyaltyActivityCreate,
):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(status_code=404, detail="Business profile not found")

    location = get_location_by_id(db, activity_data.location_id)

    if not location or location.business_id != business.id:
        raise HTTPException(status_code=404, detail="Location not found")

    if activity_data.employee_id:
        employee = get_employee_by_id(db, activity_data.employee_id)

        if not employee or employee.business_id != business.id:
            raise HTTPException(status_code=404, detail="Employee not found")

    card = get_loyalty_card_by_public_id(db, activity_data.loyalty_card_identifier)

    if not card:
        card = get_loyalty_card_by_card_number(db, activity_data.loyalty_card_identifier)

    if not card:
        raise HTTPException(status_code=404, detail="Loyalty card not found")

    customer = get_customer_by_id(db, card.customer_id)

    if not customer or customer.business_id != business.id:
        raise HTTPException(status_code=404, detail="Customer not found")

    program = get_loyalty_program_by_business_id(db, business.id)

    if not program:
        raise HTTPException(status_code=404, detail="Loyalty program not found")

    rewards = get_rewards_by_business_id(db, business.id)

    engine_result = calculate_loyalty_progress(
        program=program,
        current_progress=customer.current_progress,
        rewards=rewards,
        amount_spent=activity_data.purchase_amount,
        quantity=activity_data.qualifying_quantity,
    )

    earned_progress = engine_result["earned_progress"]
    calculated_progress = engine_result["new_progress"]
    unlocked_rewards = engine_result["unlocked_rewards"]

    reward_was_collected = (
        program.program_type == ProgramType.STAMPS
        and program.target_count is not None
        and calculated_progress >= program.target_count
    )

    if reward_was_collected:
        final_progress = 0
        actual_change = program.target_count - customer.current_progress
    else:
        final_progress = calculated_progress
        actual_change = earned_progress

    customer.current_progress = final_progress

    activity = create_loyalty_activity(
        db=db,
        business_id=business.id,
        location_id=location.id,
        employee_id=activity_data.employee_id,
        customer_id=customer.id,
        loyalty_card_id=card.id,
        activity_type=activity_data.activity_type,
        purchase_amount=activity_data.purchase_amount,
        qualifying_quantity=activity_data.qualifying_quantity,
        earned_progress=actual_change,
        balance_after=final_progress,
        note=activity_data.note,
    )

    if reward_was_collected:
        create_ledger_entry(
            db=db,
            business_id=business.id,
            customer_id=customer.id,
            change_amount=actual_change,
            balance_after=program.target_count,
            entry_type=LedgerEntryType.PURCHASE,
            reference_type="loyalty_activity",
            reference_id=str(activity.id),
            note=activity_data.note,
        )

        create_ledger_entry(
            db=db,
            business_id=business.id,
            customer_id=customer.id,
            change_amount=-program.target_count,
            balance_after=final_progress,
            entry_type=LedgerEntryType.REDEMPTION,
            reference_type="reward_collected",
            reference_id=str(activity.id),
            note=(
                unlocked_rewards[0].get("name", "Reward collected")
                if unlocked_rewards
                else "Reward collected"
            ),
        )
    else:
        create_ledger_entry(
            db=db,
            business_id=business.id,
            customer_id=customer.id,
            change_amount=actual_change,
            balance_after=final_progress,
            entry_type=LedgerEntryType.PURCHASE,
            reference_type="loyalty_activity",
            reference_id=str(activity.id),
            note=activity_data.note,
        )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return {
        "activity": activity,
        "unlocked_rewards": unlocked_rewards,
        "reward_collected": reward_was_collected,
    }