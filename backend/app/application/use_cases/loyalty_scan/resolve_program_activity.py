from dataclasses import dataclass

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import LoyaltyActivityType, ProgramType
from app.models.loyalty_program import LoyaltyProgram
from app.repositories.loyalty_program_repository import (
    get_loyalty_program_by_business_id,
)


@dataclass
class ProgramActivityContext:
    program: LoyaltyProgram
    activity_type: LoyaltyActivityType
    purchase_amount: float
    qualifying_quantity: int


def resolve_program_activity(
    db: Session,
    business_id: int,
) -> ProgramActivityContext:
    program = get_loyalty_program_by_business_id(db, business_id)

    if not program:
        raise HTTPException(status_code=404, detail="Loyalty program not found")

    if not program.is_active:
        raise HTTPException(status_code=400, detail="Loyalty program is not active")

    activity_context = _build_activity_context(program)

    return ProgramActivityContext(
        program=program,
        activity_type=activity_context.activity_type,
        purchase_amount=activity_context.purchase_amount,
        qualifying_quantity=activity_context.qualifying_quantity,
    )


def _build_activity_context(program: LoyaltyProgram) -> ProgramActivityContext:
    if program.program_type == ProgramType.POINTS.value:
        return ProgramActivityContext(
            program=program,
            activity_type=LoyaltyActivityType.PURCHASE,
            purchase_amount=0,
            qualifying_quantity=1,
        )

    if program.program_type == ProgramType.STAMPS.value:
        return ProgramActivityContext(
            program=program,
            activity_type=LoyaltyActivityType.STAMP_SCAN,
            purchase_amount=0,
            qualifying_quantity=1,
        )

    if program.program_type == ProgramType.VISITS.value:
        return ProgramActivityContext(
            program=program,
            activity_type=LoyaltyActivityType.VISIT,
            purchase_amount=0,
            qualifying_quantity=1,
        )

    if program.program_type == ProgramType.SPEND.value:
        return ProgramActivityContext(
            program=program,
            activity_type=LoyaltyActivityType.PURCHASE,
            purchase_amount=0,
            qualifying_quantity=1,
        )

    if program.program_type == ProgramType.PRODUCT.value:
        return ProgramActivityContext(
            program=program,
            activity_type=LoyaltyActivityType.PRODUCT_PURCHASE,
            purchase_amount=0,
            qualifying_quantity=1,
        )

    raise HTTPException(
        status_code=400,
        detail=f"Unsupported loyalty program type: {program.program_type}",
    )