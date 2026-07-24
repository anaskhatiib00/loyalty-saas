from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.application.use_cases.loyalty_scan.get_pos_recent_activity import (
    get_pos_recent_activity_use_case,
)
from app.application.use_cases.loyalty_scan.process_loyalty_scan import (
    process_loyalty_scan_use_case,
)
from app.application.use_cases.loyalty_scan.get_pos_workspace_context import (
    get_pos_workspace_context_use_case,
)
from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.pos import POSScanRequest, POSScanResponse
from app.schemas.pos_activity import POSRecentActivityResponse
from app.schemas.pos_context import POSWorkspaceContextResponse


router = APIRouter(
    prefix="/pos",
    tags=["Employee POS"],
)


@router.get(
    "/context",
    response_model=POSWorkspaceContextResponse,
)
def get_pos_workspace_context(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_pos_workspace_context_use_case(
        db=db,
        current_user=current_user,
    )


@router.post(
    "/scan",
    response_model=POSScanResponse,
)
def process_pos_scan(
    scan_data: POSScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return process_loyalty_scan_use_case(
        db=db,
        current_user=current_user,
        scan_data=scan_data,
    )


@router.get(
    "/activity",
    response_model=POSRecentActivityResponse,
)
def get_recent_activity(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_pos_recent_activity_use_case(
        db=db,
        current_user=current_user,
        limit=limit,
    )