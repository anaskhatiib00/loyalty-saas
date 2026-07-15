from dataclasses import dataclass

from app.core.international.countries import get_country_configuration
from app.core.international.currencies import get_currency_configuration
from app.core.international.locales import get_locale_configuration
from app.core.international.timezones import is_valid_timezone


@dataclass(frozen=True, slots=True)
class ResolvedRegionalConfiguration:
    country_code: str
    currency_code: str
    timezone: str
    locale: str


class InvalidRegionalConfigurationError(ValueError):
    pass


def resolve_regional_configuration(
    *,
    country_code: str,
    currency_override: str | None = None,
    timezone_override: str | None = None,
    locale_override: str | None = None,
) -> ResolvedRegionalConfiguration:
    country_configuration = get_country_configuration(country_code)

    if country_configuration is None:
        raise InvalidRegionalConfigurationError(
            f"Country code '{country_code}' is not configured."
        )

    currency_code = (
        currency_override.strip().upper()
        if currency_override
        else country_configuration.default_currency_code
    )

    timezone = (
        timezone_override.strip()
        if timezone_override
        else country_configuration.default_timezone
    )

    locale = (
        locale_override.strip().lower().replace("_", "-")
        if locale_override
        else country_configuration.default_locale
    )

    if get_currency_configuration(currency_code) is None:
        raise InvalidRegionalConfigurationError(
            f"Currency code '{currency_code}' is not configured."
        )

    if not is_valid_timezone(timezone):
        raise InvalidRegionalConfigurationError(
            f"Timezone '{timezone}' is invalid."
        )

    locale_configuration = get_locale_configuration(locale)

    if locale_configuration is None:
        raise InvalidRegionalConfigurationError(
            f"Locale '{locale}' is not configured."
        )

    if locale not in country_configuration.supported_locales:
        raise InvalidRegionalConfigurationError(
            f"Locale '{locale}' is not supported for country "
            f"'{country_configuration.code}'."
        )

    return ResolvedRegionalConfiguration(
        country_code=country_configuration.code,
        currency_code=currency_code,
        timezone=timezone,
        locale=locale,
    )