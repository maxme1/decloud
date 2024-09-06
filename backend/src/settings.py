from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    slack_root: Path
    telegram_root: Path
    base_url: str


settings = Settings(_env_file=Path(__file__).resolve().parent.parent / '.env')
