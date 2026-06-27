from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.loyalty_program_repository import (
    get_loyalty_program_by_business_id,
    create_loyalty_program,
    update_loyalty_program,
)
from app.schemas.loyalty_program import LoyaltyProgramCreate, LoyaltyProgramUpdate


def get_current_user_business(db: Session, current_user: User):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business profile not found",
        )

    return business


def create_loyalty_program_service(
    db: Session,
    current_user: User,
    program_data: LoyaltyProgramCreate,
):
    business = get_current_user_business(db, current_user)

    existing_program = get_loyalty_program_by_business_id(db, business.id)

    if existing_program:
        raise HTTPException(
            status_code=400,
            detail="Loyalty program already exists for this business",
        )

    return create_loyalty_program(db, business.id, program_data)


def get_my_loyalty_program_service(db: Session, current_user: User):
    business = get_current_user_business(db, current_user)

    program = get_loyalty_program_by_business_id(db, business.id)

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Loyalty program not found",
        )

    return program


def update_loyalty_program_service(
    db: Session,
    current_user: User,
    program_data: LoyaltyProgramUpdate,
):
    business = get_current_user_business(db, current_user)

    program = get_loyalty_program_by_business_id(db, business.id)

    if not program:
        raise HTTPException(
            status_code=404,
            detail="Loyalty program not found",
        )

    return update_loyalty_program(db, program, program_data)