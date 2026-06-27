from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.location_repository import (
    create_location,
    get_locations_by_business_id,
    get_location_by_id,
    update_location,
    delete_location,
)
from app.schemas.location import LocationCreate, LocationUpdate


def get_current_user_business(db: Session, current_user: User):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business profile not found",
        )

    return business


def create_location_service(
    db: Session,
    current_user: User,
    location_data: LocationCreate,
):
    business = get_current_user_business(db, current_user)

    return create_location(
        db=db,
        business_id=business.id,
        location_data=location_data,
    )


def list_locations_service(db: Session, current_user: User):
    business = get_current_user_business(db, current_user)

    return get_locations_by_business_id(db, business.id)


def get_location_service(db: Session, current_user: User, location_id: int):
    business = get_current_user_business(db, current_user)

    location = get_location_by_id(db, location_id)

    if not location or location.business_id != business.id:
        raise HTTPException(
            status_code=404,
            detail="Location not found",
        )

    return location


def update_location_service(
    db: Session,
    current_user: User,
    location_id: int,
    location_data: LocationUpdate,
):
    location = get_location_service(db, current_user, location_id)

    return update_location(db, location, location_data)


def delete_location_service(db: Session, current_user: User, location_id: int):
    location = get_location_service(db, current_user, location_id)

    delete_location(db, location)

    return {"message": "Location deleted successfully"}