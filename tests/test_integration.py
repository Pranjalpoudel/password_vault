"""
Integration tests for Secure Password Vault.
Tests complete workflows and integration between modules.
"""

import unittest
from database import VaultDatabase
from auth import AuthManager
from vault import CredentialVault
from generator import PasswordGenerator, PasswordStrengthChecker


class TestVaultIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""

    def setUp(self):
        """Set up test database and modules."""
        self.db = VaultDatabase()
        self.auth = AuthManager(self.db)
        self.test_user = "test_integration_user"
        self.test_password = "TestPassword123!"

    def test_complete_user_workflow(self):
        """Test complete user registration, login, and credential management."""
        # Register user
        reg_success, reg_msg = self.auth.register_user(self.test_user, self.test_password)
        self.assertTrue(reg_success)

        # Login user
        login_success, user_id, login_msg = self.auth.login_user(self.test_user, self.test_password)
        self.assertTrue(login_success)
        self.assertIsNotNone(user_id)

        # Add credentials
        vault = CredentialVault(self.db, user_id)
        add_success, add_msg = vault.add_entry(
            "GitHub",
            "test@example.com",
            "GitHubPassword123!",
            "Personal GitHub account"
        )
        self.assertTrue(add_success)

        # Search credentials
        entries = vault.list_entries("GitHub")
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["service_name"], "GitHub")

    def test_password_generation_and_strength(self):
        """Test password generation and strength evaluation."""
        gen = PasswordGenerator()
        checker = PasswordStrengthChecker()

        # Generate password
        password = gen.generate(length=20)
        self.assertEqual(len(password), 20)

        # Check strength
        strength, label, color, details = checker.check(password)
        self.assertIn(strength, range(5))
        self.assertIn("entropy", details)
        self.assertGreater(details["entropy"], 0)

    def test_multiple_credentials_for_user(self):
        """Test managing multiple credentials for single user."""
        # Setup
        reg_success, _ = self.auth.register_user("multi_test_user", "TestPassword123!")
        login_success, user_id, _ = self.auth.login_user("multi_test_user", "TestPassword123!")
        self.assertTrue(login_success)

        vault = CredentialVault(self.db, user_id)

        # Add multiple credentials
        services = ["Gmail", "GitHub", "AWS", "Banking"]
        for service in services:
            success, _ = vault.add_entry(service, f"{service}@test.com", f"{service}Pass123!", f"{service} account")
            self.assertTrue(success)

        # Verify all are stored
        all_entries = vault.list_entries()
        self.assertGreaterEqual(len(all_entries), len(services))

    def test_credential_encryption_isolation(self):
        """Test that credentials from different users are isolated."""
        # Register two users
        self.auth.register_user("user_a", "UserAPassword123!")
        self.auth.register_user("user_b", "UserBPassword123!")

        # Login both
        _, user_a_id, _ = self.auth.login_user("user_a", "UserAPassword123!")
        _, user_b_id, _ = self.auth.login_user("user_b", "UserBPassword123!")

        # Add different credentials
        vault_a = CredentialVault(self.db, user_a_id)
        vault_b = CredentialVault(self.db, user_b_id)

        vault_a.add_entry("Gmail", "user_a@gmail.com", "SecretA123!", "User A's email")
        vault_b.add_entry("Gmail", "user_b@gmail.com", "SecretB123!", "User B's email")

        # Verify isolation
        entries_a = vault_a.list_entries()
        entries_b = vault_b.list_entries()

        self.assertNotEqual(entries_a[0]["service_username"], entries_b[0]["service_username"])


if __name__ == "__main__":
    unittest.main()
