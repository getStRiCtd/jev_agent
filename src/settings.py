from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class JevClientSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    api_key: SecretStr = Field(validation_alias="JEV_API_KEY")
