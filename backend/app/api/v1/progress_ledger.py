from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.progress_ledger import (
    ProgressLedgerCreate,
    ProgressLedgerResponse,
)
from app.services.progress_ledger_service import (
    create_progress_ledger_entry_service,
    list_customer_ledger_service,
)


router = APIRouter(
    prefix="/progress-ledger",
    tags=["Progress Ledger"],
)


@router.post("", response_model=ProgressLedgerResponse)
def create_progress_ledger_entry(
    ledger_data: ProgressLedgerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_progress_ledger_entry_service(db, current_user, ledger_data)


@router.get("/customer/{customer_id}", response_model=list[ProgressLedgerResponse])
def list_customer_ledger(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_customer_ledger_service(db, current_user, customer_id)