# Changelog - Secure Password Vault

## v0.1.0 - Initial Release (2026-07-01)

### Added

- **Authentication Module** (`auth.py`): User registration and login with PBKDF2-HMAC-SHA256 password hashing
- **Database Module** (`database.py`): PostgreSQL interface with schema initialization (users, vault_entries, audit_log tables)
- **Vault Module** (`vault.py`): Full CRUD operations for credential management with audit logging
- **Generator Module** (`generator.py`): Cryptographically secure password generator and Shannon entropy-based strength checker
- **GUI Application** (`main.py`): Tkinter-based desktop interface for user-friendly interaction
- **Unit Tests**: Comprehensive test coverage for authentication and password generation
- Account lockout after 5 failed login attempts within 10 minutes
- Parameterized SQL queries to prevent injection attacks
- Audit logging for all vault operations (LOGIN, ADD, UPDATE, DELETE, VIEW)
- Cross-platform support (Windows, Linux, macOS)
