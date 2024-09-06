from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    slack_root: Path | None = None
    telegram_root: Path | None = None
    telegram_api_root: Path | None = None
    base_url: str


settings = Settings(_env_file=Path(__file__).resolve().parent.parent / '.env')
