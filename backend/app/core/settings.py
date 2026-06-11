import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_name: str = "TaskForge"
    version: str = "0.1.0"

    database_url: str = os.getenv("DATABASE_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = AppSettings()