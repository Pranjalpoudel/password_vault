"""
Database module for Secure Password Vault.
Handles all PostgreSQL connections and schema initialization.
"""

import psycopg2
from psycopg2 import sql, Error
from typing import Optional, List, Dict, Any
from contextlib import contextmanager


class VaultDatabase:
    """PostgreSQL database interface for the password vault."""

    def __init__(self, host: str = "localhost", user: str = "postgres", 
                 password: str = "", database: str = "password_vault", port: int = 5432):
        """Initialize database connection parameters."""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        try:
            conn = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            yield conn
            conn.close()
        except Error as e:
            print(f"Database connection error: {e}")
            raise

    def initialize_schema(self) -> bool:
        """Create tables if they don't exist."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Create users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id SERIAL PRIMARY KEY,
                        username VARCHAR(255) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        salt VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        account_locked BOOLEAN DEFAULT FALSE,
                        locked_until TIMESTAMP
                    )
                """)

                # Create vault_entries table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS vault_entries (
                        entry_id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        service_name VARCHAR(255) NOT NULL,
                        service_username VARCHAR(255),
                        service_password TEXT NOT NULL,
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                    )
                """)

                # Create audit_log table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS audit_log (
                        log_id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        action VARCHAR(50) NOT NULL,
                        entry_id INTEGER,
                        action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ip_address VARCHAR(45),
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                    )
                """)

                # Create indexes for performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_vault_entries_user_id ON vault_entries(user_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_log_user_id ON audit_log(user_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_log_action_time ON audit_log(action_time)")

                conn.commit()
                print("Database schema initialized successfully.")
                return True

        except Error as e:
            print(f"Error initializing schema: {e}")
            return False

    def execute_query(self, query: str, params: tuple = None, fetch: bool = False) -> Optional[Any]:
        """Execute a parameterized query."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                
                if fetch:
                    result = cursor.fetchall()
                    conn.commit()
                    return result
                else:
                    conn.commit()
                    return cursor.rowcount
        except Error as e:
            print(f"Query execution error: {e}")
            return None

    def execute_query_single(self, query: str, params: tuple = None) -> Optional[tuple]:
        """Execute a query and fetch a single row."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                result = cursor.fetchone()
                conn.commit()
                return result
        except Error as e:
            print(f"Query execution error: {e}")
            return None
