from sqlalchemy.orm import Session

from app.models.business import Business
from app.schemas.business import BusinessCreate, BusinessUpdate


def get_business_by_owner_id(db: Session, owner_id: int):
    return db.query(Business).filter(Business.owner_id == owner_id).first()


def create_business(db: Session, owner_id: int, business_data: BusinessCreate):
    business = Business(
        owner_id=owner_id,
        **business_data.model_dump(),
    )

    db.add(business)
    db.commit()
    db.refresh(business)

    return business


def update_business(db: Session, business: Business, business_data: BusinessUpdate):
    update_data = business_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(business, field, value)

    db.commit()
    db.refresh(business)

    return business