from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class LocaleConfiguration:
    code: str
    name: str
    language_code: str
    text_direction: str


_LOCALE_CONFIGURATIONS: dict[str, LocaleConfiguration] = {
    "en": LocaleConfiguration(
        code="en",
        name="English",
        language_code="en",
        text_direction="ltr",
    ),
    "ar": LocaleConfiguration(
        code="ar",
        name="Arabic",
        language_code="ar",
        text_direction="rtl",
    ),
}


LOCALE_CONFIGURATIONS: Mapping[str, LocaleConfiguration] = MappingProxyType(
    _LOCALE_CONFIGURATIONS
)


def normalize_locale_code(locale_code: str) -> str:
    return locale_code.strip().lower().replace("_", "-")


def get_locale_configuration(
    locale_code: str,
) -> LocaleConfiguration | None:
    normalized_locale_code = normalize_locale_code(locale_code)
    return LOCALE_CONFIGURATIONS.get(normalized_locale_code)


def is_configured_locale(locale_code: str) -> bool:
    return get_locale_configuration(locale_code) is not None