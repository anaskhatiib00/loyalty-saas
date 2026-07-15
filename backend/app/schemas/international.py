from pydantic import BaseModel


class CountryOptionResponse(BaseModel):
    code: str
    name: str
    default_currency_code: str
    default_timezone: str
    default_locale: str
    supported_locales: tuple[str, ...]
    signup_enabled: bool


class CurrencyOptionResponse(BaseModel):
    code: str
    name: str
    decimal_places: int
    symbol: str


class LocaleOptionResponse(BaseModel):
    code: str
    name: str
    language_code: str
    text_direction: str


class InternationalOptionsResponse(BaseModel):
    countries: list[CountryOptionResponse]
    currencies: list[CurrencyOptionResponse]
    locales: list[LocaleOptionResponse]