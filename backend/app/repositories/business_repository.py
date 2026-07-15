from sqlalchemy.orm import Session, joinedload

from app.models.business import Business
from app.models.business_settings import BusinessSettings
from app.schemas.business import BusinessCreate, BusinessUpdate



def get_business_by_owner_id(
    db: Session,
    owner_id: int,
) -> Business | None:
    return (
        db.query(Business)
        .options(joinedload(Business.settings))
        .filter(Business.owner_id == owner_id)
        .first()
    )


def get_business_by_id(
    db: Session,
    business_id: int,
) -> Business | None:
    return (
        db.query(Business)
        .options(joinedload(Business.settings))
        .filter(Business.id == business_id)
        .first()
    )


def create_business(
    db: Session,
    owner_id: int,
    business_data: BusinessCreate,
) -> Business:
    business_values = business_data.model_dump(
        exclude={"settings"},
    )
    settings_values = business_data.settings.model_dump()

    business = Business(
        owner_id=owner_id,
        **business_values,
    )

    try:
        db.add(business)
        db.flush()

        business_settings = BusinessSettings(
            business_id=business.id,
            **settings_values,
        )

        db.add(business_settings)
        db.commit()
        db.refresh(business)

        return get_business_by_id(db, business.id)

    except Exception:
        db.rollback()
        raise


def update_business(
    db: Session,
    business: Business,
    business_data: BusinessUpdate,
) -> Business:
    update_data = business_data.model_dump(
        exclude_unset=True,
    )

    try:
        for field, value in update_data.items():
            setattr(business, field, value)

        db.commit()
        db.refresh(business)

        return get_business_by_id(db, business.id)

    except Exception:
        db.rollback()
        raise