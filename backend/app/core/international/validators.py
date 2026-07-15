from app.core.international.countries import is_configured_country
from app.core.international.currencies import is_configured_currency
from app.core.international.locales import is_configured_locale
from app.core.international.timezones import is_valid_timezone


def validate_country_code(country_code: str) -> bool:
    return is_configured_country(country_code)


def validate_currency_code(currency_code: str) -> bool:
    return is_configured_currency(currency_code)


def validate_locale(locale_code: str) -> bool:
    return is_configured_locale(locale_code)


def validate_timezone(timezone_name: str) -> bool:
    return is_valid_timezone(timezone_name)