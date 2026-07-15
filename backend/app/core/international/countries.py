from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class CountryConfiguration:
    code: str
    name: str
    default_currency_code: str
    default_timezone: str
    default_locale: str
    supported_locales: tuple[str, ...]
    signup_enabled: bool = False


_COUNTRY_CONFIGURATIONS: dict[str, CountryConfiguration] = {
    "JO": CountryConfiguration(
        code="JO",
        name="Jordan",
        default_currency_code="JOD",
        default_timezone="Asia/Amman",
        default_locale="en",
        supported_locales=("en", "ar"),
        signup_enabled=True,
    ),
    "AE": CountryConfiguration(
        code="AE",
        name="United Arab Emirates",
        default_currency_code="AED",
        default_timezone="Asia/Dubai",
        default_locale="en",
        supported_locales=("en", "ar"),
    ),
    "SA": CountryConfiguration(
        code="SA",
        name="Saudi Arabia",
        default_currency_code="SAR",
        default_timezone="Asia/Riyadh",
        default_locale="ar",
        supported_locales=("ar", "en"),
    ),
    "QA": CountryConfiguration(
        code="QA",
        name="Qatar",
        default_currency_code="QAR",
        default_timezone="Asia/Qatar",
        default_locale="ar",
        supported_locales=("ar", "en"),
    ),
    "KW": CountryConfiguration(
        code="KW",
        name="Kuwait",
        default_currency_code="KWD",
        default_timezone="Asia/Kuwait",
        default_locale="ar",
        supported_locales=("ar", "en"),
    ),
    "US": CountryConfiguration(
        code="US",
        name="United States",
        default_currency_code="USD",
        default_timezone="America/New_York",
        default_locale="en",
        supported_locales=("en",),
    ),
}


COUNTRY_CONFIGURATIONS: Mapping[str, CountryConfiguration] = MappingProxyType(
    _COUNTRY_CONFIGURATIONS
)


def normalize_country_code(country_code: str) -> str:
    return country_code.strip().upper()


def get_country_configuration(
    country_code: str,
) -> CountryConfiguration | None:
    normalized_country_code = normalize_country_code(country_code)
    return COUNTRY_CONFIGURATIONS.get(normalized_country_code)


def is_configured_country(country_code: str) -> bool:
    return get_country_configuration(country_code) is not None


def is_signup_enabled_country(country_code: str) -> bool:
    configuration = get_country_configuration(country_code)

    return bool(configuration and configuration.signup_enabled)


def get_signup_enabled_countries() -> tuple[CountryConfiguration, ...]:
    return tuple(
        configuration
        for configuration in COUNTRY_CONFIGURATIONS.values()
        if configuration.signup_enabled
    )