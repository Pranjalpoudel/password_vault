"""
Utilities module for Secure Password Vault.
Provides helper functions for encryption, validation, and data formatting.
"""

import string
import re
from typing import Tuple
from datetime import datetime


class ValidationUtils:
    """Utility functions for input validation."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """Validate username format and length."""
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters."
        if len(username) > 50:
            return False, "Username must be at most 50 characters."
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return False, "Username can only contain letters, numbers, underscore, and hyphen."
        return True, "Valid"

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Validate master password requirements."""
        if not password or len(password) < 8:
            return False, "Password must be at least 8 characters."
        if len(password) > 256:
            return False, "Password must be at most 256 characters."
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        if not (has_upper and has_lower and has_digit):
            return False, "Password must contain uppercase, lowercase, and digit."
        return True, "Valid"

    @staticmethod
    def validate_service_name(service_name: str) -> Tuple[bool, str]:
        """Validate service name."""
        if not service_name or len(service_name) < 2:
            return False, "Service name must be at least 2 characters."
        if len(service_name) > 100:
            return False, "Service name must be at most 100 characters."
        return True, "Valid"


class FormatUtils:
    """Utility functions for data formatting."""

    @staticmethod
    def format_timestamp(timestamp: datetime) -> str:
        """Format timestamp for display."""
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def mask_password(password: str, visible_chars: int = 3) -> str:
        """Mask password for safe display."""
        if len(password) <= visible_chars:
            return "*" * len(password)
        return password[:visible_chars] + "*" * (len(password) - visible_chars)

    @staticmethod
    def truncate_text(text: str, max_length: int = 50) -> str:
        """Truncate text with ellipsis."""
        if len(text) > max_length:
            return text[:max_length - 3] + "..."
        return text

    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format bytes to human-readable size."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
