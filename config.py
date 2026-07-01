"""
Configuration module for Secure Password Vault.
Handles environment variables and application settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration settings."""

    # Database settings
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "password_vault")

    # Security settings
    PBKDF2_ITERATIONS = 260000
    SALT_LENGTH = 32
    LOGIN_ATTEMPT_LIMIT = 5
    LOGIN_LOCK_DURATION = 10  # minutes

    # Application settings
    APP_NAME = "Secure Password Vault"
    APP_VERSION = "0.1.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Paths
    BASE_DIR = Path(__file__).parent
    LOG_DIR = BASE_DIR / "logs"
    DATA_DIR = BASE_DIR / "data"

    @classmethod
    def get_database_url(cls) -> str:
        """Get PostgreSQL connection URL."""
        return (
            f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@"
            f"{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        )

    @classmethod
    def ensure_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        cls.LOG_DIR.mkdir(exist_ok=True)
        cls.DATA_DIR.mkdir(exist_ok=True)
