from app.core.international import (
    COUNTRY_CONFIGURATIONS,
    CURRENCY_CONFIGURATIONS,
    LOCALE_CONFIGURATIONS,
)
from app.schemas.international import (
    CountryOptionResponse,
    CurrencyOptionResponse,
    InternationalOptionsResponse,
    LocaleOptionResponse,
)


def get_international_options_service() -> InternationalOptionsResponse:
    countries = [
        CountryOptionResponse(
            code=configuration.code,
            name=configuration.name,
            default_currency_code=configuration.default_currency_code,
            default_timezone=configuration.default_timezone,
            default_locale=configuration.default_locale,
            supported_locales=configuration.supported_locales,
            signup_enabled=configuration.signup_enabled,
        )
        for configuration in COUNTRY_CONFIGURATIONS.values()
    ]

    currencies = [
        CurrencyOptionResponse(
            code=configuration.code,
            name=configuration.name,
            decimal_places=configuration.decimal_places,
            symbol=configuration.symbol,
        )
        for configuration in CURRENCY_CONFIGURATIONS.values()
    ]

    locales = [
        LocaleOptionResponse(
            code=configuration.code,
            name=configuration.name,
            language_code=configuration.language_code,
            text_direction=configuration.text_direction,
        )
        for configuration in LOCALE_CONFIGURATIONS.values()
    ]

    return InternationalOptionsResponse(
        countries=sorted(
            countries,
            key=lambda country: country.name,
        ),
        currencies=sorted(
            currencies,
            key=lambda currency: currency.code,
        ),
        locales=sorted(
            locales,
            key=lambda locale: locale.code,
        ),
    )