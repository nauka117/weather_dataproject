from abc import ABC
from pathlib import Path

from pydantic import (
    Field,
    field_validator
)

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

import re

class CommonSettings(BaseSettings, ABC):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

class OpenWeatherMapSettings(CommonSettings):
    key: str = Field(alias="OWM_API_KEY")

    @field_validator('key')
    def validate_owm_api_key(cls, value):
        pattern = re.compile(r"^[a-f0-9]{32}$")
        if not pattern.match(value):
            raise ValueError("OWM_API_KEY must be a 32-character hexadecimal string.")
        return value

class VisualCrossingSettings(CommonSettings):
    key: str = Field(alias="VC_API_KEY")

    @field_validator('key')
    def validate_vc_api_key(cls, value):
        pattern = re.compile(r"^[A-Z0-9]{25}$")
        if not pattern.match(value):
            raise ValueError("VC_API_KEY must be a 25-character alphanumeric string.")
        return value

class MeteostatSettings(CommonSettings):
    key: str = Field(alias="METEOSTAT_API_KEY")

    @field_validator('key')
    def validate_meteostat_api_key(cls, value):
        pattern = re.compile(r"^[a-z0-9]{50}$")
        if not pattern.match(value):
            raise ValueError("METEOSTAT_API_KEY must be a 50-character alphanumeric string.")
        return value

class WeatherapiSettings(CommonSettings):
    key: str = Field(alias="WEATHERAPI_API_KEY")

    @field_validator('key')
    def validate_weatherapi_api_key(cls, value):
        pattern = re.compile(r"^[a-z0-9]{50}$")
        if not pattern.match(value):
            raise ValueError("WEATHERAPI_API_KEY must be a 50-character alphanumeric string.")
        return value

class WeatherbitSettings(CommonSettings):
    key: str = Field(alias="WEATHERBIT_API_KEY")

    @field_validator('key')
    def validate_weatherbit_api_key(cls, value):
        pattern = re.compile(r"^[a-z0-9]{50}$")
        if not pattern.match(value):
            raise ValueError("WEATHERBIT_API_KEY must be a 50-character alphanumeric string.")
        return value


class NominatimSettings(CommonSettings):
    user_agent: str = Field(alias="GC_USER_AGENT")

class Settings(CommonSettings):
    OWM_API: OpenWeatherMapSettings = Field(default_factory=OpenWeatherMapSettings)
    VC_API: VisualCrossingSettings = Field(default_factory=VisualCrossingSettings)
    METEOSTAT_API: MeteostatSettings = Field(default_factory=MeteostatSettings)
    WEATHERAPI_API: WeatherapiSettings = Field(default_factory=WeatherapiSettings)
    WEATHERBIT_API: WeatherbitSettings = Field(default_factory=WeatherbitSettings)
    GC_API: NominatimSettings = Field(default_factory=NominatimSettings)

