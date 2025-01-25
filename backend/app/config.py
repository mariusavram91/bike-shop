# app/config.py

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    ENV: str = Field(
        default="production",
        json_schema_extra={"env": "ENV"},
    )

    DATABASE_URL: str = Field(
        default="sqlite:///./database.db",
        json_schema_extra={"env": "DATABASE_URL"},
    )

    CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:5173",
        ],
        json_schema_extra={"env": "CORS_ORIGINS"},
    )
    ALLOW_CREDENTIALS: bool = Field(
        default=True,
        json_schema_extra={"env": "ALLOW_CREDENTIALS"},
    )
    ALLOW_METHODS: List[str] = Field(
        default=["*"],
        json_schema_extra={"env": "ALLOW_METHODS"},
    )
    ALLOW_HEADERS: List[str] = Field(
        default=["*"],
        json_schema_extra={"env": "ALLOW_HEADERS"},
    )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
