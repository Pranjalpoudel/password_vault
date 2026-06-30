"""
Unit tests for password generator and strength checker.
"""

import unittest
from generator import PasswordGenerator, PasswordStrengthChecker


class TestPasswordGenerator(unittest.TestCase):
    """Test cases for PasswordGenerator."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = PasswordGenerator()

    def test_generate_default_password(self):
        """Test default password generation."""
        password = self.generator.generate()
        self.assertEqual(len(password), 16)
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))

    def test_generate_custom_length(self):
        """Test password generation with custom length."""
        password = self.generator.generate(length=32)
        self.assertEqual(len(password), 32)

    def test_generate_without_symbols(self):
        """Test password generation without symbols."""
        password = self.generator.generate(use_symbols=False)
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.assertFalse(any(c in symbols for c in password))

    def test_uniqueness(self):
        """Test that generated passwords are unique."""
        passwords = [self.generator.generate() for _ in range(10)]
        self.assertEqual(len(passwords), len(set(passwords)))


class TestPasswordStrengthChecker(unittest.TestCase):
    """Test cases for PasswordStrengthChecker."""

    def setUp(self):
        """Set up test fixtures."""
        self.checker = PasswordStrengthChecker()

    def test_very_weak_password(self):
        """Test very weak password detection."""
        strength, label, color, details = self.checker.check("123")
        self.assertEqual(strength, PasswordStrengthChecker.STRENGTH_VERY_WEAK)

    def test_strong_password(self):
        """Test strong password detection."""
        strength, label, color, details = self.checker.check("MySecureP@ssw0rd2024!")
        self.assertIn(strength, [
            PasswordStrengthChecker.STRENGTH_GOOD,
            PasswordStrengthChecker.STRENGTH_VERY_STRONG
        ])

    def test_sequential_characters_penalty(self):
        """Test that sequential characters reduce strength."""
        password1 = "abcdefghijklmnop"
        password2 = "azxcvbnmasdfghjk"
        
        strength1, _, _, _ = self.checker.check(password1)
        strength2, _, _, _ = self.checker.check(password2)
        
        self.assertLess(strength1, strength2)

    def test_strength_details(self):
        """Test that strength details are returned correctly."""
        strength, label, color, details = self.checker.check("TestPassword123!")
        
        self.assertIn("length", details)
        self.assertIn("entropy", details)
        self.assertIn("has_uppercase", details)
        self.assertIn("has_lowercase", details)
        self.assertIn("has_digits", details)
        self.assertIn("has_symbols", details)


if __name__ == "__main__":
    unittest.main()
