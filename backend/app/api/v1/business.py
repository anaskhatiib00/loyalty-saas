from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.business_repository import (
    get_business_by_owner_id,
    create_business,
    update_business,
)
from app.schemas.business import (
    BusinessCreate,
    BusinessUpdate,
    BusinessResponse,
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
    existing_business = get_business_by_owner_id(db, current_user.id)

    if existing_business:
        raise HTTPException(
            status_code=400,
            detail="Business already exists for this user",
        )

    return create_business(
        db=db,
        owner_id=current_user.id,
        business_data=business_data,
    )


@router.get("/me", response_model=BusinessResponse)
def get_my_business(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business profile not found",
        )

    return business


@router.patch("/me", response_model=BusinessResponse)
def update_my_business(
    business_data: BusinessUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business profile not found",
        )

    return update_business(
        db=db,
        business=business,
        business_data=business_data,
    )