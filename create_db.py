"""Create the password_vault database in PostgreSQL."""

from typing import Optional, Any

psycopg2: Optional[Any] = None
sql: Optional[Any] = None

try:
    import psycopg2 as psycopg2_module  # type: ignore[import-not-found]
    from psycopg2 import sql as sql_module  # type: ignore[import-not-found]
    psycopg2 = psycopg2_module
    sql = sql_module
except ImportError:
    pass  # Will be available at runtime

def create_database():
    """Create the password_vault database if it doesn't exist."""
    try:
        if psycopg2 is None:
            raise ImportError("psycopg2 not available")
        # Connect to PostgreSQL server (default postgres database)
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="postgres",
            database="postgres",  # Connect to default postgres db
            port=5432
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            ("password_vault",)
        )
        if cursor.fetchone():
            print("✓ Database 'password_vault' already exists")
        else:
            # Create database
            cursor.execute("CREATE DATABASE password_vault;")
            print("✓ Database 'password_vault' created successfully")

        cursor.close()
        conn.close()
        print("\nNow run: python main.py")

    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure PostgreSQL 18 is running")
        print("2. Check username: postgres")
        print("3. Check password: postgres")
        print("4. On Windows, start PostgreSQL service:")
        print("   Services > PostgreSQL Server 18 > Start")

if __name__ == "__main__":
    create_database()
