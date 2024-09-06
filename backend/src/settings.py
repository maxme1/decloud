from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    slack: Path | None = None
    telegram_export: Path | None = None
    telegram_sdk: Path | None = None
    base_url: str


settings = Settings(_env_file=Path(__file__).resolve().parent.parent / '.env')
