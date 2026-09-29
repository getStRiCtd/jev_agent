from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class JevClientSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    api_key: SecretStr = Field(..., validate_default="JEV_API_KEY")

class AppSettings:
    jev_settings: JevClientSettings = JevClientSettings()

settings: AppSettings = AppSettings()