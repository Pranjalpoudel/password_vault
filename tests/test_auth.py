"""
Unit tests for authentication module.
"""

import unittest
import tempfile
from pathlib import Path
from database import VaultDatabase
from auth import AuthManager


class TestAuthManager(unittest.TestCase):
    """Test cases for AuthManager."""

    def setUp(self):
        """Set up test fixtures."""
        self.auth = AuthManager(VaultDatabase())

    def test_generate_salt(self):
        """Test salt generation."""
        salt1 = AuthManager.generate_salt()
        salt2 = AuthManager.generate_salt()
        
        self.assertNotEqual(salt1, salt2)
        self.assertEqual(len(salt1), 64)  # 32 bytes = 64 hex chars

    def test_hash_password(self):
        """Test password hashing."""
        password = "TestPassword123!"
        salt = AuthManager.generate_salt()
        hash1 = AuthManager.hash_password(password, salt)
        hash2 = AuthManager.hash_password(password, salt)
        
        self.assertEqual(hash1, hash2)  # Same input = same hash
        self.assertIsInstance(hash1, str)

    def test_verify_password(self):
        """Test password verification."""
        password = "TestPassword123!"
        salt = AuthManager.generate_salt()
        password_hash = AuthManager.hash_password(password, salt)
        
        self.assertTrue(AuthManager.verify_password(password, salt, password_hash))
        self.assertFalse(AuthManager.verify_password("WrongPassword", salt, password_hash))

    def test_password_hashing_different_salts(self):
        """Test that different salts produce different hashes."""
        password = "TestPassword123!"
        salt1 = AuthManager.generate_salt()
        salt2 = AuthManager.generate_salt()
        
        hash1 = AuthManager.hash_password(password, salt1)
        hash2 = AuthManager.hash_password(password, salt2)
        
        self.assertNotEqual(hash1, hash2)


if __name__ == "__main__":
    unittest.main()
