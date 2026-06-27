from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.location import (
    LocationCreate,
    LocationUpdate,
    LocationResponse,
)
from app.services.location_service import (
    create_location_service,
    list_locations_service,
    get_location_service,
    update_location_service,
    delete_location_service,
)


router = APIRouter(
    prefix="/locations",
    tags=["Locations"],
)


@router.post("", response_model=LocationResponse)
def create_location(
    location_data: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_location_service(db, current_user, location_data)


@router.get("", response_model=list[LocationResponse])
def list_locations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_locations_service(db, current_user)


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_location_service(db, current_user, location_id)


@router.patch("/{location_id}", response_model=LocationResponse)
def update_location(
    location_id: int,
    location_data: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_location_service(db, current_user, location_id, location_data)


@router.delete("/{location_id}")
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_location_service(db, current_user, location_id)