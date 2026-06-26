"""
Authentication module for Secure Password Vault.
Handles user registration, login, and password hashing.
"""

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Optional, Tuple
from database import VaultDatabase


class AuthManager:
    """Manages user authentication and password security."""

    PBKDF2_ITERATIONS = 260000
    SALT_LENGTH = 32
    LOCK_THRESHOLD = 5  # Failed attempts to trigger lock
    LOCK_DURATION = 10  # Minutes

    def __init__(self, db: VaultDatabase):
        """Initialize with database connection."""
        self.db = db

    @staticmethod
    def generate_salt() -> str:
        """Generate a cryptographically secure random salt."""
        return secrets.token_hex(AuthManager.SALT_LENGTH)

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        """
        Hash password using PBKDF2-HMAC-SHA256.
        
        Args:
            password: The plaintext password
            salt: The salt hex string
            
        Returns:
            The password hash hex digest
        """
        salt_bytes = bytes.fromhex(salt)
        hash_obj = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt_bytes,
            AuthManager.PBKDF2_ITERATIONS
        )
        return hash_obj.hex()

    @staticmethod
    def verify_password(password: str, salt: str, stored_hash: str) -> bool:
        """
        Verify a password against stored hash using constant-time comparison.
        
        Args:
            password: The plaintext password to verify
            salt: The salt hex string
            stored_hash: The stored password hash
            
        Returns:
            True if password matches, False otherwise
        """
        computed_hash = AuthManager.hash_password(password, salt)
        return hmac.compare_digest(computed_hash, stored_hash)

    def register_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Register a new user with a master password.
        
        Args:
            username: Unique username
            password: Master password
            
        Returns:
            (success, message)
        """
        # Validate inputs
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long."
        
        if not password or len(password) < 8:
            return False, "Password must be at least 8 characters long."

        # Check if username already exists
        query = "SELECT user_id FROM users WHERE username = %s"
        result = self.db.execute_query_single(query, (username,))
        if result:
            return False, "Username already exists."

        try:
            # Generate salt and hash password
            salt = self.generate_salt()
            password_hash = self.hash_password(password, salt)

            # Insert user into database
            insert_query = """
                INSERT INTO users (username, password_hash, salt, created_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            """
            self.db.execute_query(insert_query, (username, password_hash, salt))
            
            return True, f"User '{username}' registered successfully."
        except Exception as e:
            return False, f"Registration failed: {str(e)}"

    def login_user(self, username: str, password: str, ip_address: str = "0.0.0.0") -> Tuple[bool, Optional[int], str]:
        """
        Authenticate user and log the attempt.
        
        Args:
            username: Username
            password: Master password
            ip_address: IP address of login attempt
            
        Returns:
            (success, user_id, message)
        """
        # Get user from database
        query = """
            SELECT user_id, password_hash, salt, account_locked, locked_until
            FROM users WHERE username = %s
        """
        result = self.db.execute_query_single(query, (username,))

        if not result:
            return False, None, "Invalid username or password."

        user_id, stored_hash, salt, locked, locked_until = result

        # Check if account is locked
        if locked and locked_until:
            if datetime.now() < locked_until:
                return False, None, "Account is locked. Try again later."
            else:
                # Unlock the account
                unlock_query = """
                    UPDATE users SET account_locked = FALSE, locked_until = NULL
                    WHERE user_id = %s
                """
                self.db.execute_query(unlock_query, (user_id,))

        # Verify password
        if not self.verify_password(password, salt, stored_hash):
            # Log failed attempt and check lock threshold
            self._log_failed_attempt(user_id, ip_address)
            return False, None, "Invalid username or password."

        # Update last login
        update_query = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = %s"
        self.db.execute_query(update_query, (user_id,))

        # Log successful login
        log_query = """
            INSERT INTO audit_log (user_id, action, action_time, ip_address)
            VALUES (%s, %s, CURRENT_TIMESTAMP, %s)
        """
        self.db.execute_query(log_query, (user_id, "LOGIN", ip_address))

        return True, user_id, "Login successful."

    def _log_failed_attempt(self, user_id: int, ip_address: str) -> None:
        """Track failed login attempts and lock account if threshold exceeded."""
        log_query = """
            INSERT INTO audit_log (user_id, action, action_time, ip_address)
            VALUES (%s, %s, CURRENT_TIMESTAMP, %s)
        """
        self.db.execute_query(log_query, (user_id, "LOGIN_FAILED", ip_address))

        # Count recent failed attempts (within lock duration window)
        count_query = """
            SELECT COUNT(*) FROM audit_log
            WHERE user_id = %s AND action = %s
            AND action_time > CURRENT_TIMESTAMP - INTERVAL '%d minutes'
        """ % (self.LOCK_DURATION,)
        
        result = self.db.execute_query_single(count_query, (user_id, "LOGIN_FAILED"))
        
        if result and result[0] >= self.LOCK_THRESHOLD:
            # Lock the account
            locked_until = datetime.now() + timedelta(minutes=self.LOCK_DURATION)
            lock_query = """
                UPDATE users SET account_locked = TRUE, locked_until = %s
                WHERE user_id = %s
            """
            self.db.execute_query(lock_query, (locked_until, user_id))
