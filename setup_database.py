"""
Database initialization script for Secure Password Vault.
Run this once to set up PostgreSQL database and schema.
"""

from database import VaultDatabase


def main():
    """Initialize the password vault database."""
    print("Secure Password Vault - Database Initialization")
    print("=" * 50)
    
    # Get database credentials
    print("\nPostgreSQL Connection Details:")
    host = input("Host (default: localhost): ").strip() or "localhost"
    port = int(input("Port (default: 5432): ").strip() or "5432")
    user = input("User (default: postgres): ").strip() or "postgres"
    password = input("Password (default: empty): ").strip() or ""
    database = input("Database name (default: password_vault): ").strip() or "password_vault"
    
    print("\nAttempting to connect and initialize database...")
    
    try:
        # Create database connection
        db = VaultDatabase(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        
        # Initialize schema
        if db.initialize_schema():
            print("\n✓ Database initialized successfully!")
            print(f"  Host: {host}")
            print(f"  Port: {port}")
            print(f"  Database: {database}")
            print("\nTables created:")
            print("  - users")
            print("  - vault_entries")
            print("  - audit_log")
            print("\nYou can now run: python main.py")
        else:
            print("\n✗ Failed to initialize database schema.")
    
    except Exception as e:
        print(f"\n✗ Connection error: {e}")
        print("\nTroubleshooting:")
        print("  1. Ensure PostgreSQL is running")
        print("  2. Verify credentials are correct")
        print("  3. Check that the database exists or create it manually:")
        print(f"     createdb {database}")


if __name__ == "__main__":
    main()
