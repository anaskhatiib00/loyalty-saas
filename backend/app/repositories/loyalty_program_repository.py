from sqlalchemy.orm import Session

from app.models.loyalty_program import LoyaltyProgram
from app.schemas.loyalty_program import LoyaltyProgramCreate, LoyaltyProgramUpdate


def get_loyalty_program_by_business_id(db: Session, business_id: int):
    return (
        db.query(LoyaltyProgram)
        .filter(LoyaltyProgram.business_id == business_id)
        .first()
    )


def create_loyalty_program(
    db: Session,
    business_id: int,
    program_data: LoyaltyProgramCreate,
):
    program = LoyaltyProgram(
        business_id=business_id,
        **program_data.model_dump(),
    )

    db.add(program)
    db.commit()
    db.refresh(program)

    return program


def update_loyalty_program(
    db: Session,
    program: LoyaltyProgram,
    program_data: LoyaltyProgramUpdate,
):
    update_data = program_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(program, field, value)

    db.commit()
    db.refresh(program)

    return program