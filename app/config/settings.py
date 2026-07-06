from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "TradeMind AI"

    DATA_DIR: Path = Path("data")
    REPORT_DIR: Path = Path("reports")
    LOG_DIR: Path = Path("logs")

    DEFAULT_PERIOD: ClassVar[str] = "5y"
    DEFAULT_INTERVAL: ClassVar[str] = "1d"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()

settings.DATA_DIR.mkdir(exist_ok=True)
settings.REPORT_DIR.mkdir(exist_ok=True)
settings.LOG_DIR.mkdir(exist_ok=True)