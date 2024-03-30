from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Validation Check
    secret_key: str
    database_url: str

    model_config = SettingsConfigDict(env_file=".env")


# Enhancing performance by cache setting
@lru_cache()
def get_settings():
    return Settings()
