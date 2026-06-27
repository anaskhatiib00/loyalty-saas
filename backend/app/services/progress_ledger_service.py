from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.customer_repository import get_customer_by_id
from app.repositories.progress_ledger_repository import (
    create_ledger_entry,
    get_ledger_by_customer_id,
)
from app.schemas.progress_ledger import ProgressLedgerCreate


def create_progress_ledger_entry_service(
    db: Session,
    current_user: User,
    ledger_data: ProgressLedgerCreate,
):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(status_code=404, detail="Business profile not found")

    customer = get_customer_by_id(db, ledger_data.customer_id)

    if not customer or customer.business_id != business.id:
        raise HTTPException(status_code=404, detail="Customer not found")

    new_balance = customer.current_progress + ledger_data.change_amount

    if new_balance < 0:
        raise HTTPException(
            status_code=400,
            detail="Progress balance cannot be negative",
        )

    customer.current_progress = new_balance

    entry = create_ledger_entry(
        db=db,
        business_id=business.id,
        customer_id=customer.id,
        change_amount=ledger_data.change_amount,
        balance_after=new_balance,
        entry_type=ledger_data.entry_type,
        reference_type=ledger_data.reference_type,
        reference_id=ledger_data.reference_id,
        note=ledger_data.note,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return entry


def list_customer_ledger_service(
    db: Session,
    current_user: User,
    customer_id: int,
):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(status_code=404, detail="Business profile not found")

    customer = get_customer_by_id(db, customer_id)

    if not customer or customer.business_id != business.id:
        raise HTTPException(status_code=404, detail="Customer not found")

    return get_ledger_by_customer_id(db, customer.id)