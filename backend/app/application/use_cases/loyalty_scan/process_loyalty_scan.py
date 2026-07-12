from sqlalchemy.orm import Session

from app.application.use_cases.loyalty_activity.execute_loyalty_activity import (
    execute_loyalty_activity,
)
from app.application.use_cases.loyalty_scan.resolve_customer_context import (
    resolve_customer_context,
)
from app.application.use_cases.loyalty_scan.resolve_employee_context import (
    resolve_employee_context,
)
from app.application.use_cases.loyalty_scan.resolve_program_activity import (
    resolve_program_activity,
)
from app.models.user import User
from app.schemas.pos import POSScanRequest


def process_loyalty_scan_use_case(
    db: Session,
    current_user: User,
    scan_data: POSScanRequest,
):
    employee_context = resolve_employee_context(
        db=db,
        current_user=current_user,
    )

    customer_context = resolve_customer_context(
        db=db,
        business_id=employee_context.business.id,
        loyalty_card_identifier=scan_data.loyalty_card_identifier,
    )

    program_context = resolve_program_activity(
        db=db,
        business_id=employee_context.business.id,
    )

    activity_result = execute_loyalty_activity(
        db=db,
        business=employee_context.business,
        location=employee_context.location,
        employee=employee_context.employee,
        customer=customer_context.customer,
        loyalty_card=customer_context.loyalty_card,
        program=program_context.program,
        activity_type=program_context.activity_type,
        purchase_amount=program_context.purchase_amount,
        qualifying_quantity=program_context.qualifying_quantity,
        source="employee_pos",
        note="Employee POS automatic scan",
    )

    return {
        "customer_id": customer_context.customer.id,
        "loyalty_card_id": customer_context.loyalty_card.id,
        "program_type": program_context.program.program_type,
        "current_progress": customer_context.customer.current_progress,
        "reward_available": len(activity_result["unlocked_rewards"]) > 0,
        "reward_collected": activity_result["reward_collected"],
        "unlocked_rewards": activity_result["unlocked_rewards"],
    }