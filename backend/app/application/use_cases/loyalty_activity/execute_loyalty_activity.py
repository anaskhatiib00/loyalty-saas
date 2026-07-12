from sqlalchemy.orm import Session

from app.core.enums import LedgerEntryType, ProgramType
from app.loyalty.engine import calculate_loyalty_progress
from app.models.business import Business
from app.models.customer import Customer
from app.models.employee import Employee
from app.models.location import Location
from app.models.loyalty_card import LoyaltyCard
from app.models.loyalty_program import LoyaltyProgram
from app.repositories.loyalty_activity_repository import create_loyalty_activity
from app.repositories.progress_ledger_repository import create_ledger_entry
from app.repositories.reward_repository import get_rewards_by_business_id


def _build_customer_name(customer: Customer) -> str:
    return " ".join(
        part
        for part in [
            customer.first_name,
            customer.last_name,
        ]
        if part
    ).strip()


def _get_primary_unlocked_reward(
    unlocked_rewards: list[dict],
) -> dict | None:
    if not unlocked_rewards:
        return None

    return unlocked_rewards[0]


def execute_loyalty_activity(
    db: Session,
    *,
    business: Business,
    location: Location,
    employee: Employee | None,
    customer: Customer,
    loyalty_card: LoyaltyCard,
    program: LoyaltyProgram,
    activity_type: str,
    purchase_amount: float = 0,
    qualifying_quantity: int = 1,
    source: str = "manager_dashboard",
    idempotency_key: str | None = None,
    note: str | None = None,
):
    """
    Execute an authorized loyalty transaction as one database transaction.

    Authentication, authorization, tenant validation, and context resolution
    must happen before this function is called.

    This function owns:

    - loyalty calculation
    - customer balance updates
    - immutable activity persistence
    - progress-ledger persistence
    - reward lifecycle persistence
    - transaction commit or rollback
    """

    balance_before = customer.current_progress

    try:
        rewards = get_rewards_by_business_id(
            db,
            business.id,
        )

        engine_result = calculate_loyalty_progress(
            program=program,
            current_progress=balance_before,
            rewards=rewards,
            amount_spent=purchase_amount,
            quantity=qualifying_quantity,
        )

        calculated_progress = engine_result["new_progress"]
        earned_progress = engine_result["earned_progress"]
        unlocked_rewards = engine_result["unlocked_rewards"]

        primary_reward = _get_primary_unlocked_reward(
            unlocked_rewards,
        )

        program_type = (
            program.program_type.value
            if hasattr(program.program_type, "value")
            else program.program_type
        )

        reward_was_collected = (
            program_type == ProgramType.STAMPS.value
            and program.target_count is not None
            and calculated_progress >= program.target_count
        )

        if reward_was_collected:
            balance_after = 0
            progress_change = (
                program.target_count - balance_before
            )
            event_type = "reward_collected"
        else:
            balance_after = calculated_progress
            progress_change = earned_progress
            event_type = "progress_added"

        customer.current_progress = balance_after

        reward_id = (
            primary_reward.get("id")
            if primary_reward
            else None
        )
        reward_name_snapshot = (
            primary_reward.get("name")
            if primary_reward
            else None
        )

        activity = create_loyalty_activity(
            db=db,
            business_id=business.id,
            location_id=location.id,
            employee_id=employee.id if employee else None,
            customer_id=customer.id,
            loyalty_card_id=loyalty_card.id,
            loyalty_program_id=program.id,
            reward_id=reward_id,
            event_type=event_type,
            activity_type=activity_type,
            source=source,
            status="completed",
            purchase_amount=purchase_amount,
            qualifying_quantity=qualifying_quantity,
            progress_change=progress_change,
            balance_before=balance_before,
            balance_after=balance_after,
            customer_name_snapshot=_build_customer_name(customer),
            employee_name_snapshot=(
                employee.full_name
                if employee
                else None
            ),
            location_name_snapshot=location.name,
            program_name_snapshot=program.name,
            reward_name_snapshot=reward_name_snapshot,
            idempotency_key=idempotency_key,
            note=note,
        )

        if reward_was_collected:
            create_ledger_entry(
                db=db,
                business_id=business.id,
                customer_id=customer.id,
                change_amount=progress_change,
                balance_after=program.target_count,
                entry_type=LedgerEntryType.PURCHASE,
                reference_type="loyalty_activity",
                reference_id=str(activity.id),
                note=note,
            )

            create_ledger_entry(
                db=db,
                business_id=business.id,
                customer_id=customer.id,
                change_amount=-program.target_count,
                balance_after=balance_after,
                entry_type=LedgerEntryType.REDEMPTION,
                reference_type="reward_collected",
                reference_id=str(activity.id),
                note=(
                    reward_name_snapshot
                    or "Reward collected"
                ),
            )
        else:
            create_ledger_entry(
                db=db,
                business_id=business.id,
                customer_id=customer.id,
                change_amount=progress_change,
                balance_after=balance_after,
                entry_type=LedgerEntryType.PURCHASE,
                reference_type="loyalty_activity",
                reference_id=str(activity.id),
                note=note,
            )

        db.add(customer)
        db.commit()

        db.refresh(customer)
        db.refresh(activity)

        return {
            "activity": activity,
            "unlocked_rewards": unlocked_rewards,
            "reward_collected": reward_was_collected,
        }

    except Exception:
        db.rollback()
        raise