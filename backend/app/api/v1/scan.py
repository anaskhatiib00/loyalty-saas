from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.scan import ScanResolveRequest, ScanResolveResponse
from app.services.scan_service import resolve_scan_service


router = APIRouter(
    prefix="/scan",
    tags=["Scan"],
)


@router.post("/resolve", response_model=ScanResolveResponse)
def resolve_scan(
    scan_data: ScanResolveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return resolve_scan_service(db, current_user, scan_data)