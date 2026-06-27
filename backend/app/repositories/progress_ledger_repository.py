from sqlalchemy.orm import Session

from app.models.progress_ledger import ProgressLedger


def create_ledger_entry(
    db: Session,
    business_id: int,
    customer_id: int,
    change_amount: int,
    balance_after: int,
    entry_type: str,
    reference_type: str | None = None,
    reference_id: str | None = None,
    note: str | None = None,
):
    entry = ProgressLedger(
        business_id=business_id,
        customer_id=customer_id,
        change_amount=change_amount,
        balance_after=balance_after,
        entry_type=entry_type,
        reference_type=reference_type,
        reference_id=reference_id,
        note=note,
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry


def get_ledger_by_customer_id(db: Session, customer_id: int):
    return (
        db.query(ProgressLedger)
        .filter(ProgressLedger.customer_id == customer_id)
        .order_by(ProgressLedger.created_at.desc())
        .all()
    )