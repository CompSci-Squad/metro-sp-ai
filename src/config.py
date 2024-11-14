from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    port: int = 8080

    model_config = SettingsConfigDict(env_file=".env")