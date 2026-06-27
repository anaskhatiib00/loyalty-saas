from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.loyalty_program import (
    LoyaltyProgramCreate,
    LoyaltyProgramUpdate,
    LoyaltyProgramResponse,
)
from app.services.loyalty_program_service import (
    create_loyalty_program_service,
    get_my_loyalty_program_service,
    update_loyalty_program_service,
)

from app.loyalty.engine import calculate_loyalty_progress


router = APIRouter(
    prefix="/loyalty-program",
    tags=["Loyalty Program"],
)


@router.post("", response_model=LoyaltyProgramResponse)
def create_loyalty_program(
    program_data: LoyaltyProgramCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_loyalty_program_service(db, current_user, program_data)


@router.get("/me", response_model=LoyaltyProgramResponse)
def get_my_loyalty_program(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_loyalty_program_service(db, current_user)


@router.patch("/me", response_model=LoyaltyProgramResponse)
def update_my_loyalty_program(
    program_data: LoyaltyProgramUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_loyalty_program_service(db, current_user, program_data)


@router.get("/test-engine")
def test_loyalty_engine(
    amount_spent: float = 10,
    quantity: int = 1,
    current_progress: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    program = get_my_loyalty_program_service(db, current_user)

    return calculate_loyalty_progress(
        program=program,
        current_progress=current_progress,
        amount_spent=amount_spent,
        quantity=quantity,
    )