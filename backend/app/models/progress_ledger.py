from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class ProgressLedger(Base):
    __tablename__ = "progress_ledger"

    id = Column(Integer, primary_key=True, index=True)

    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    change_amount = Column(Integer, nullable=False)
    balance_after = Column(Integer, nullable=False)

    entry_type = Column(String, nullable=False)
    reference_type = Column(String, nullable=True)
    reference_id = Column(String, nullable=True)
    note = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer")