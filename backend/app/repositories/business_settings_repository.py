from sqlalchemy.orm import Session

from app.models.business_settings import BusinessSettings
from app.schemas.business_settings import BusinessSettingsUpdate


def get_business_settings_by_business_id(
    db: Session,
    business_id: int,
) -> BusinessSettings | None:
    return (
        db.query(BusinessSettings)
        .filter(BusinessSettings.business_id == business_id)
        .first()
    )


def update_business_settings(
    db: Session,
    business_settings: BusinessSettings,
    settings_data: BusinessSettingsUpdate,
) -> BusinessSettings:
    update_values = settings_data.model_dump(
        exclude_unset=True,
    )

    try:
        for field, value in update_values.items():
            setattr(business_settings, field, value)

        db.commit()
        db.refresh(business_settings)

        return business_settings

    except Exception:
        db.rollback()
        raise
    