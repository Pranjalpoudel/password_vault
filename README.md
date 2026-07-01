# Secure Password Vault

A desktop-based password management application built with Python, Tkinter, and PostgreSQL. Designed for secure, offline credential storage with cryptographic hashing and comprehensive audit logging.

## Features

- **Secure Authentication**: PBKDF2-HMAC-SHA256 hashing with unique per-user salts (260,000 iterations)
- **Credential Vault**: Full CRUD operations for managing passwords with service metadata
- **Password Generator**: Cryptographically secure random password generation with configurable character sets
- **Strength Evaluator**: Shannon entropy-based password strength assessment with visual feedback
- **Audit Logging**: Complete audit trail of all vault operations (login, add, update, delete, view)
- **Account Protection**: Automatic lockout after 5 failed login attempts within 10 minutes
- **Cross-Platform**: Works on Windows 10+, Ubuntu 22.04+, and macOS 12+
- **No External Dependencies**: Uses standard Python cryptography and psycopg2

## Project Structure

```
.
├── main.py                 # Tkinter GUI application
├── auth.py                 # Authentication and registration
├── vault.py                # Credential CRUD operations
├── generator.py            # Password generation & strength checking
├── database.py             # PostgreSQL interface
├── requirements.txt        # Python dependencies
├── tests/
│   ├── test_auth.py       # Authentication tests
│   └── test_generator.py  # Password generation tests
├── README.md
└── CHANGELOG.md
```

## Installation

### Prerequisites

- Python 3.10 or newer
- PostgreSQL 14 or newer
- pip package manager

### Setup

1. **Clone the project** (if applicable) or navigate to the folder:

   ```bash
   cd d:\extraproject\folder
   ```

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure PostgreSQL** (if not already running):
   - Ensure PostgreSQL is installed and running on `localhost:5432`
   - Create a database named `password_vault` (optional—database.py will handle initialization)

4. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### Getting Started

1. **Launch** the application using `python main.py`
2. **Register** a new account with a strong master password (minimum 8 characters)
3. **Login** with your credentials
4. **Manage credentials** in the vault:
   - **Add Entry**: Store service name, username, password, and notes
   - **Search**: Filter entries by service name
   - **Edit/Delete**: Modify or remove existing entries
   - **Generate Password**: Create secure passwords with custom parameters

### Password Generation

- Configure character types (uppercase, lowercase, digits, symbols)
- Adjust length (8–64 characters, default 16)
- Real-time strength evaluation with entropy calculation
- Copy-to-clipboard functionality for easy insertion

## Security

### Authentication

- Master password never stored in plaintext
- PBKDF2-HMAC-SHA256 with 260,000 iterations (OWASP recommended)
- Unique random salt per user (32 bytes)
- Constant-time password comparison to prevent timing attacks

### Database

- Parameterized SQL queries eliminate injection attacks
- Foreign key constraints ensure referential integrity
- Cascade delete prevents orphaned entries
- Normalized schema design (3NF)

### Audit Trail

- All operations logged with timestamp and IP address
- Account lockout mechanism after repeated failed attempts
- Complete activity history for security review

## API Reference

### Authentication (`auth.py`)

```python
from database import VaultDatabase
from auth import AuthManager

db = VaultDatabase()
auth = AuthManager(db)

# Register
success, msg = auth.register_user("alice", "MyStrongPassword123!")

# Login
success, user_id, msg = auth.login_user("alice", "MyStrongPassword123!")
```

### Vault Operations (`vault.py`)

```python
from vault import CredentialVault

vault = CredentialVault(db, user_id)

# Add entry
success, msg = vault.add_entry("Gmail", "alice@gmail.com", "SecurePass!", "Personal email")

# List entries
entries = vault.list_entries()
entries = vault.list_entries(search_term="Gmail")

# Get entry details
entry = vault.get_entry(entry_id)

# Update entry
success, msg = vault.update_entry(entry_id, service_password="NewPassword!")

# Delete entry
success, msg = vault.delete_entry(entry_id)
```

### Password Generation (`generator.py`)

```python
from generator import PasswordGenerator, PasswordStrengthChecker

gen = PasswordGenerator()
password = gen.generate(length=20, use_symbols=True)

checker = PasswordStrengthChecker()
strength, label, color, details = checker.check(password)
# label: "Very Weak" | "Weak" | "Fair" | "Good" | "Very Strong"
# details: {"length": 20, "entropy": 125.5, "has_uppercase": True, ...}
```

## Database Schema

### users

```sql
user_id (PK) | username (UNIQUE) | password_hash | salt | created_at | last_login | account_locked | locked_until
```

### vault_entries

```sql
entry_id (PK) | user_id (FK) | service_name | service_username | service_password | notes | created_at | updated_at
```

### audit_log

```sql
log_id (PK) | user_id (FK) | action | entry_id (nullable) | action_time | ip_address
```

## Testing

Run unit tests:

```bash
python -m unittest discover tests
```

Or individual test suites:

```bash
python -m unittest tests.test_auth
python -m unittest tests.test_generator
```

## Performance

- Password verification: <100ms
- Credential search: <200ms (for 500+ entries)
- Password generation: <10ms
- Database queries: Optimized with indexes on user_id and action_time

## Troubleshooting

### PostgreSQL Connection Error

- Ensure PostgreSQL is running: `pg_ctl -D "C:\Program Files\PostgreSQL\data" start` (Windows)
- Check credentials in `database.py` (default: `localhost:5432`, user: `postgres`)
- Verify database exists or let the app create it

### GUI Rendering Issues

- Ensure Tkinter is installed: `python -m tkinter`
- On Linux: `sudo apt-get install python3-tk`
- On macOS: Included with Python.org installer

## License

This project is provided as-is for educational and personal use.

## References

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Python hashlib Documentation](https://docs.python.org/3/library/hashlib.html)
- [PostgreSQL 14 Documentation](https://www.postgresql.org/docs/14/)

````

List pending tasks:

```bash
python file1.py list
````

List all tasks including completed ones:

```bash
python file1.py list --all
```

Complete a task:

```bash
python file1.py complete 1
```

Delete a task:

```bash
python file1.py delete 1
```

Search tasks:

```bash
python file1.py search roadmap
```

Show statistics:

```bash
python file1.py stats
```

Show a compact summary:

```bash
python file1.py summary
```

## Project structure

- file1.py - the main CLI application
- tests/test_file1.py - regression tests for core task operations
- README.md - overview and usage guide
- .gitignore - local exclusions for Python development
- requirements.txt - dependency placeholder for future growth

## Development approach

This project is being built in small, reviewable phases. The commit history is meant to reflect a calm workflow where each step adds a little more value without trying to do everything at once.

Planned phases include:

1. scaffold the project structure
2. add core task persistence and data handling
3. expand CLI commands for everyday use
4. improve test coverage and documentation
5. refine the UX and prepare future features

## Future ideas

- add due dates and reminders
- support tags and categories
- export and import task lists
- add a web or GUI version
- add automated tests in CI

## Notes

The project is intentionally simple so it can serve as a practical example of incremental development and gradual Git history growth.
