from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(override=True)


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str

    model_config = SettingsConfigDict(
        extra="ignore",
    )


CONFIG = Settings()  # type: ignore
