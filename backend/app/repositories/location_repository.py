from sqlalchemy.orm import Session

from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate


def create_location(db: Session, business_id: int, location_data: LocationCreate):
    location = Location(
        business_id=business_id,
        **location_data.model_dump(),
    )

    db.add(location)
    db.commit()
    db.refresh(location)

    return location


def get_locations_by_business_id(db: Session, business_id: int):
    return db.query(Location).filter(Location.business_id == business_id).all()


def get_location_by_id(db: Session, location_id: int):
    return db.query(Location).filter(Location.id == location_id).first()


def update_location(db: Session, location: Location, location_data: LocationUpdate):
    update_data = location_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(location, field, value)

    db.commit()
    db.refresh(location)

    return location


def delete_location(db: Session, location: Location):
    db.delete(location)
    db.commit()