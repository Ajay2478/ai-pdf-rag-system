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
    # Security
    # ==============================
    SECRET_KEY: str

    # ==============================
    # AI / LLM
    # ==============================
    GROQ_API_KEY: str

    # ==============================
    # Pydantic Settings Config (v2)
    # ==============================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Global settings instance (singleton)
settings = Settings()  # type: ignore  # runtime loads from .env