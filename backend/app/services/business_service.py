from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.business_repository import (
    get_business_by_owner_id,
    create_business,
    update_business,
)
from app.schemas.business import BusinessCreate, BusinessUpdate


def create_my_business_service(
    db: Session,
    current_user: User,
    business_data: BusinessCreate,
):
    existing_business = get_business_by_owner_id(db, current_user.id)

    if existing_business:
        raise HTTPException(
            status_code=400,
            detail="Business already exists for this user",
        )

    return create_business(db, current_user.id, business_data)


def get_my_business_service(db: Session, current_user: User):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business profile not found",
        )

    return business


def update_my_business_service(
    db: Session,
    current_user: User,
    business_data: BusinessUpdate,
):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business profile not found",
        )

    return update_business(db, business, business_data)