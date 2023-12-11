from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    env_name: str = 'Local'
    base_url: str = 'http://localhost:8000'
    db_url: str = 'sqlite:///.shortner.db'

    class Config:
        env_file = '.env'


# para fazer cache das informações
@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Carergando configurações para: {settings.env_name}")
    return settings