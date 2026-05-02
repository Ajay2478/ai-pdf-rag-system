"""
Centralized application configuration using Pydantic Settings (v2)

- Loads environment variables from .env
- Provides typed access to config across the app
- Ensures required values (like DATABASE_URL) are present
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ==============================
    # Application Settings
    # ==============================
    APP_NAME: str = "AI PDF Reader"
    ENV: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    # ==============================
    # Database Settings (Required)
    # ==============================
    DATABASE_URL: str

    # ==============================
    # Pydantic Settings Config (v2)
    # ==============================
    model_config = SettingsConfigDict(
        env_file=".env",          # Load from .env
        env_file_encoding="utf-8",
        extra="ignore"           # Ignore unknown env variables
    )


# Global settings instance (singleton)
settings = Settings()