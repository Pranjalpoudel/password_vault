"""
Password Generator and Strength Checker module for Secure Password Vault.
Generates secure passwords and evaluates password strength using Shannon entropy.
"""

import secrets
import string
import math
import re
from typing import Tuple


class PasswordGenerator:
    """Generates cryptographically secure passwords."""

    def __init__(self):
        """Initialize character sets."""
        self.uppercase = string.ascii_uppercase
        self.lowercase = string.ascii_lowercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def generate(self, length: int = 16, 
                 use_uppercase: bool = True,
                 use_lowercase: bool = True,
                 use_digits: bool = True,
                 use_symbols: bool = True) -> str:
        """
        Generate a secure random password.
        
        Args:
            length: Password length (minimum 8, default 16)
            use_uppercase: Include uppercase letters
            use_lowercase: Include lowercase letters
            use_digits: Include digits
            use_symbols: Include special symbols
            
        Returns:
            Generated password string
        """
        if length < 8:
            length = 8

        # Build character pool
        char_pool = ""
        required_chars = []

        if use_uppercase:
            char_pool += self.uppercase
            required_chars.append(secrets.choice(self.uppercase))
        if use_lowercase:
            char_pool += self.lowercase
            required_chars.append(secrets.choice(self.lowercase))
        if use_digits:
            char_pool += self.digits
            required_chars.append(secrets.choice(self.digits))
        if use_symbols:
            char_pool += self.symbols
            required_chars.append(secrets.choice(self.symbols))

        # Ensure at least one character from each enabled set
        remaining_length = length - len(required_chars)
        password_list = required_chars + [
            secrets.choice(char_pool) for _ in range(remaining_length)
        ]

        # Shuffle to avoid predictable pattern
        rng = secrets.SystemRandom()
        rng.shuffle(password_list)

        return "".join(password_list)


class PasswordStrengthChecker:
    """Evaluates password strength using Shannon entropy and pattern analysis."""

    # Strength levels
    STRENGTH_VERY_WEAK = 0
    STRENGTH_WEAK = 1
    STRENGTH_FAIR = 2
    STRENGTH_GOOD = 3
    STRENGTH_VERY_STRONG = 4

    STRENGTH_LABELS = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Good",
        4: "Very Strong"
    }

    STRENGTH_COLORS = {
        0: "#FF4444",  # Red
        1: "#FF8844",  # Orange
        2: "#FFCC44",  # Yellow
        3: "#88CC44",  # Light Green
        4: "#44CC44"   # Green
    }

    # Common passwords and patterns to detect
    COMMON_PATTERNS = [
        r"123", r"456", r"789", r"abc", r"qwerty", r"password",
        r"admin", r"letmein", r"welcome", r"monkey", r"dragon"
    ]

    def check(self, password: str) -> Tuple[int, str, str, dict]:
        """
        Evaluate password strength.
        
        Args:
            password: Password to evaluate
            
        Returns:
            (strength_level, label, color, details_dict)
        """
        if not password:
            return self.STRENGTH_VERY_WEAK, self.STRENGTH_LABELS[0], self.STRENGTH_COLORS[0], {}

        # Calculate base entropy
        entropy = self._calculate_entropy(password)
        
        # Analyze patterns
        pattern_penalty = self._analyze_patterns(password)
        
        # Adjusted entropy score
        adjusted_entropy = max(0, entropy - pattern_penalty)

        # Determine strength level
        if adjusted_entropy < 20:
            strength = self.STRENGTH_VERY_WEAK
        elif adjusted_entropy < 40:
            strength = self.STRENGTH_WEAK
        elif adjusted_entropy < 60:
            strength = self.STRENGTH_FAIR
        elif adjusted_entropy < 90:
            strength = self.STRENGTH_GOOD
        else:
            strength = self.STRENGTH_VERY_STRONG

        details = {
            "length": len(password),
            "entropy": round(entropy, 2),
            "pattern_penalty": round(pattern_penalty, 2),
            "adjusted_entropy": round(adjusted_entropy, 2),
            "has_uppercase": any(c.isupper() for c in password),
            "has_lowercase": any(c.islower() for c in password),
            "has_digits": any(c.isdigit() for c in password),
            "has_symbols": any(c in string.punctuation for c in password),
            "has_spaces": " " in password
        }

        return strength, self.STRENGTH_LABELS[strength], self.STRENGTH_COLORS[strength], details

    def _calculate_entropy(self, password: str) -> float:
        """
        Calculate Shannon entropy of password.
        Formula: H = L × log₂(N)
        where L = password length, N = size of character alphabet
        """
        charset_size = 0
        
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in string.punctuation for c in password):
            charset_size += 32
        if any(c == " " for c in password):
            charset_size += 1

        if charset_size == 0:
            return 0

        entropy = len(password) * math.log2(charset_size)
        return entropy

    def _analyze_patterns(self, password: str) -> float:
        """Detect common patterns and return entropy penalty."""
        penalty = 0
        password_lower = password.lower()

        # Check for common patterns
        for pattern in self.COMMON_PATTERNS:
            if pattern in password_lower:
                penalty += 10

        # Check for sequential characters
        if self._has_sequential_chars(password):
            penalty += 5

        # Check for repeated characters
        if self._has_repeated_chars(password):
            penalty += 3

        # Check for keyboard walks (qwerty, asdfgh, etc.)
        if self._has_keyboard_walk(password):
            penalty += 8

        return penalty

    def _has_sequential_chars(self, password: str) -> bool:
        """Check for sequential characters like 'abc' or '123'."""
        for i in range(len(password) - 2):
            c1, c2, c3 = ord(password[i]), ord(password[i + 1]), ord(password[i + 2])
            if c2 - c1 == 1 and c3 - c2 == 1:
                return True
        return False

    def _has_repeated_chars(self, password: str) -> bool:
        """Check for repeated characters like 'aaa' or '1111'."""
        for i in range(len(password) - 2):
            if password[i] == password[i + 1] == password[i + 2]:
                return True
        return False

    def _has_keyboard_walk(self, password: str) -> bool:
        """Check for keyboard walking patterns."""
        keyboard_patterns = [
            "qwerty", "asdfgh", "zxcvbn", "qazwsx", "qweasd"
        ]
        password_lower = password.lower()
        for pattern in keyboard_patterns:
            if pattern in password_lower:
                return True
        return False
