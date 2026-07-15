from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.international import (
    InvalidRegionalConfigurationError,
    resolve_regional_configuration,
)
from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.business_settings_repository import (
    get_business_settings_by_business_id,
    update_business_settings,
)
from app.schemas.business_settings import (
    BusinessSettingsDetailsResponse,
    BusinessSettingsResponse,
    BusinessSettingsUpdate,
    ResolvedRegionalConfigurationResponse,
)


def _get_owned_business_settings(
    db: Session,
    current_user: User,
):
    business = get_business_by_owner_id(
        db,
        current_user.id,
    )

    if business is None:
        raise HTTPException(
            status_code=404,
            detail="Business profile not found",
        )

    settings = get_business_settings_by_business_id(
        db,
        business.id,
    )

    if settings is None:
        raise HTTPException(
            status_code=404,
            detail="Business regional settings not found",
        )

    return settings


def _build_settings_details_response(
    settings,
) -> BusinessSettingsDetailsResponse:
    resolved = resolve_regional_configuration(
        country_code=settings.default_country_code,
        currency_override=settings.currency_override,
        timezone_override=settings.timezone_override,
        locale_override=settings.locale_override,
    )

    return BusinessSettingsDetailsResponse(
        settings=BusinessSettingsResponse.model_validate(settings),
        resolved=ResolvedRegionalConfigurationResponse(
            country_code=resolved.country_code,
            currency_code=resolved.currency_code,
            timezone=resolved.timezone,
            locale=resolved.locale,
        ),
    )


def get_my_business_settings_service(
    db: Session,
    current_user: User,
) -> BusinessSettingsDetailsResponse:
    settings = _get_owned_business_settings(
        db,
        current_user,
    )

    return _build_settings_details_response(settings)


def update_my_business_settings_service(
    db: Session,
    current_user: User,
    settings_data: BusinessSettingsUpdate,
) -> BusinessSettingsDetailsResponse:
    settings = _get_owned_business_settings(
        db,
        current_user,
    )

    update_values = settings_data.model_dump(
        exclude_unset=True,
    )

    final_country_code = update_values.get(
        "default_country_code",
        settings.default_country_code,
    )
    final_currency_override = update_values.get(
        "currency_override",
        settings.currency_override,
    )
    final_timezone_override = update_values.get(
        "timezone_override",
        settings.timezone_override,
    )
    final_locale_override = update_values.get(
        "locale_override",
        settings.locale_override,
    )

    try:
        resolve_regional_configuration(
            country_code=final_country_code,
            currency_override=final_currency_override,
            timezone_override=final_timezone_override,
            locale_override=final_locale_override,
        )
    except InvalidRegionalConfigurationError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    updated_settings = update_business_settings(
        db,
        settings,
        settings_data,
    )

    return _build_settings_details_response(
        updated_settings,
    )