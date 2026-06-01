from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_name: str = "TaskForge"
    version: str = "0.1.0"
    database_url: str = "sqlite:///./taskforge.db"

    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = AppSettings()
