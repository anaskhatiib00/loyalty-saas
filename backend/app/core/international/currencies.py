from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class CurrencyConfiguration:
    code: str
    name: str
    decimal_places: int
    symbol: str


_CURRENCY_CONFIGURATIONS: dict[str, CurrencyConfiguration] = {
    "JOD": CurrencyConfiguration(
        code="JOD",
        name="Jordanian Dinar",
        decimal_places=3,
        symbol="د.ا",
    ),
    "AED": CurrencyConfiguration(
        code="AED",
        name="United Arab Emirates Dirham",
        decimal_places=2,
        symbol="د.إ",
    ),
    "SAR": CurrencyConfiguration(
        code="SAR",
        name="Saudi Riyal",
        decimal_places=2,
        symbol="ر.س",
    ),
    "QAR": CurrencyConfiguration(
        code="QAR",
        name="Qatari Riyal",
        decimal_places=2,
        symbol="ر.ق",
    ),
    "KWD": CurrencyConfiguration(
        code="KWD",
        name="Kuwaiti Dinar",
        decimal_places=3,
        symbol="د.ك",
    ),
    "USD": CurrencyConfiguration(
        code="USD",
        name="United States Dollar",
        decimal_places=2,
        symbol="$",
    ),
}


CURRENCY_CONFIGURATIONS: Mapping[str, CurrencyConfiguration] = MappingProxyType(
    _CURRENCY_CONFIGURATIONS
)


def normalize_currency_code(currency_code: str) -> str:
    return currency_code.strip().upper()


def get_currency_configuration(
    currency_code: str,
) -> CurrencyConfiguration | None:
    normalized_currency_code = normalize_currency_code(currency_code)
    return CURRENCY_CONFIGURATIONS.get(normalized_currency_code)


def is_configured_currency(currency_code: str) -> bool:
    return get_currency_configuration(currency_code) is not None