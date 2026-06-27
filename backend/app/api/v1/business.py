from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.business import (
    BusinessCreate,
    BusinessUpdate,
    BusinessResponse,
)
from app.services.business_service import (
    create_my_business_service,
    get_my_business_service,
    update_my_business_service,
)


router = APIRouter(
    prefix="/business",
    tags=["Business"],
)


@router.post("", response_model=BusinessResponse)
def create_my_business(
    business_data: BusinessCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_my_business_service(db, current_user, business_data)


@router.get("/me", response_model=BusinessResponse)
def get_my_business(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_business_service(db, current_user)


@router.patch("/me", response_model=BusinessResponse)
def update_my_business(
    business_data: BusinessUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_my_business_service(db, current_user, business_data)