"""
Logging and monitoring module for Secure Password Vault.
Handles application logging and error tracking.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from config import Config


class LogManager:
    """Manages application logging."""

    _logger = None

    @classmethod
    def setup_logging(cls, level=logging.INFO):
        """Initialize logging configuration."""
        Config.ensure_directories()

        # Create logger
        logger = logging.getLogger("vault")
        logger.setLevel(level)

        # Create logs directory
        log_file = Config.LOG_DIR / f"vault_{datetime.now().strftime('%Y%m%d')}.log"

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        cls._logger = logger
        return logger

    @classmethod
    def get_logger(cls):
        """Get or create logger instance."""
        if cls._logger is None:
            cls.setup_logging()
        return cls._logger

    @classmethod
    def log_security_event(cls, event_type: str, user_id: int, details: str):
        """Log security-relevant events."""
        logger = cls.get_logger()
        logger.warning(f"SECURITY[{event_type}] User ID: {user_id} - {details}")

    @classmethod
    def log_error(cls, error_msg: str, exception: Exception = None):
        """Log error events."""
        logger = cls.get_logger()
        if exception:
            logger.error(f"{error_msg}: {str(exception)}")
        else:
            logger.error(error_msg)
