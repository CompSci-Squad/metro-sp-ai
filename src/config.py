from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PORT: int
    HOST: str

    model_config = SettingsConfigDict(env_file=".env")