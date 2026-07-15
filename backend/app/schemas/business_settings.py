from typing import Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from app.core.international import (
    normalize_country_code,
    normalize_currency_code,
    normalize_locale_code,
    normalize_timezone_name,
    resolve_regional_configuration,
)


class BusinessSettingsCreate(BaseModel):
    default_country_code: str = Field(
        min_length=2,
        max_length=2,
    )
    currency_override: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )
    timezone_override: str | None = Field(
        default=None,
        max_length=64,
    )
    locale_override: str | None = Field(
        default=None,
        max_length=16,
    )

    @field_validator("default_country_code")
    @classmethod
    def normalize_default_country_code(cls, value: str) -> str:
        return normalize_country_code(value)

    @field_validator("currency_override")
    @classmethod
    def normalize_currency_override(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return normalize_currency_code(value)

    @field_validator("timezone_override")
    @classmethod
    def normalize_timezone_override(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return normalize_timezone_name(value)

    @field_validator("locale_override")
    @classmethod
    def normalize_locale_override(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return normalize_locale_code(value)

    @model_validator(mode="after")
    def validate_regional_configuration(self) -> Self:
        resolve_regional_configuration(
            country_code=self.default_country_code,
            currency_override=self.currency_override,
            timezone_override=self.timezone_override,
            locale_override=self.locale_override,
        )

        return self


class BusinessSettingsUpdate(BaseModel):
    default_country_code: str | None = Field(
        default=None,
        min_length=2,
        max_length=2,
    )
    currency_override: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )
    timezone_override: str | None = Field(
        default=None,
        max_length=64,
    )
    locale_override: str | None = Field(
        default=None,
        max_length=16,
    )

    @field_validator("default_country_code")
    @classmethod
    def normalize_default_country_code(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return normalize_country_code(value)

    @field_validator("currency_override")
    @classmethod
    def normalize_currency_override(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return normalize_currency_code(value)

    @field_validator("timezone_override")
    @classmethod
    def normalize_timezone_override(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return normalize_timezone_name(value)

    @field_validator("locale_override")
    @classmethod
    def normalize_locale_override(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return normalize_locale_code(value)


class BusinessSettingsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    default_country_code: str
    currency_override: str | None
    timezone_override: str | None
    locale_override: str | None


class ResolvedRegionalConfigurationResponse(BaseModel):
    country_code: str
    currency_code: str
    timezone: str
    locale: str


class BusinessSettingsDetailsResponse(BaseModel):
    settings: BusinessSettingsResponse
    resolved: ResolvedRegionalConfigurationResponse