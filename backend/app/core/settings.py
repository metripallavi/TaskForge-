from pydantic import BaseModel


class AppSettings(BaseModel):
    app_name: str = "TaskForge"
    version: str = "0.1.0"


settings = AppSettings()
