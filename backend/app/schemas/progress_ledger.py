from typing import Optional

from pydantic import BaseModel

from app.core.enums import LedgerEntryType


class ProgressLedgerCreate(BaseModel):
    customer_id: int
    change_amount: int
    entry_type: LedgerEntryType
    reference_type: Optional[str] = None
    reference_id: Optional[str] = None
    note: Optional[str] = None


class ProgressLedgerResponse(BaseModel):
    id: int
    business_id: int
    customer_id: int
    change_amount: int
    balance_after: int
    entry_type: LedgerEntryType
    reference_type: Optional[str]
    reference_id: Optional[str]
    note: Optional[str]

    class Config:
        from_attributes = True