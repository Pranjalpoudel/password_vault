# API Documentation

## VaultAPI Class

High-level programmatic interface for password vault operations.

### Initialization

```python
from database import VaultDatabase
from api import VaultAPI

db = VaultDatabase(
    host="localhost",
    user="postgres",
    password="",
    database="password_vault"
)

api = VaultAPI(db)
```

## Authentication Methods

### `authenticate(username: str, password: str) -> Dict`

Authenticate user with credentials.

**Parameters:**
- `username` (str): User's username
- `password` (str): User's master password

**Returns:**
```python
{
    "success": bool,
    "user_id": int or None,
    "message": str
}
```

**Example:**
```python
result = api.authenticate("alice", "MyPassword123!")
if result["success"]:
    user_id = result["user_id"]
    print(f"Logged in as user {user_id}")
else:
    print(result["message"])
```

### `register(username: str, password: str) -> Dict`

Register a new user.

**Parameters:**
- `username` (str): Desired username (3-50 chars)
- `password` (str): Master password (8+ chars, mixed case + digits)

**Returns:**
```python
{
    "success": bool,
    "message": str
}
```

**Example:**
```python
result = api.register("bob", "BobPassword456!")
if result["success"]:
    print("Registration successful")
```

## Credential Management

### `get_credentials(search_term: str = "") -> Dict`

Retrieve credentials from vault.

**Parameters:**
- `search_term` (str, optional): Filter by service name

**Returns:**
```python
{
    "success": bool,
    "count": int,
    "entries": [
        {
            "entry_id": int,
            "service_name": str,
            "service_username": str,
            "created_at": datetime,
            "updated_at": datetime
        },
        ...
    ]
}
```

**Example:**
```python
# Get all credentials
result = api.get_credentials()
print(f"Total entries: {result['count']}")

# Search specific service
gmail_creds = api.get_credentials(search_term="Gmail")
for entry in gmail_creds["entries"]:
    print(f"{entry['service_name']}: {entry['service_username']}")
```

### `add_credential(service_name: str, username: str, password: str, notes: str = "") -> Dict`

Add new credential to vault.

**Parameters:**
- `service_name` (str): Service/platform name (2-100 chars)
- `username` (str): Username for the service
- `password` (str): Password for the service
- `notes` (str, optional): Additional notes

**Returns:**
```python
{
    "success": bool,
    "message": str
}
```

**Example:**
```python
result = api.add_credential(
    service_name="Gmail",
    username="alice@gmail.com",
    password="GmailPassword123!",
    notes="Personal email account"
)
if result["success"]:
    print("Credential added")
```

### `delete_credential(entry_id: int) -> Dict`

Delete credential from vault.

**Parameters:**
- `entry_id` (int): ID of credential to delete

**Returns:**
```python
{
    "success": bool,
    "message": str
}
```

**Example:**
```python
result = api.delete_credential(entry_id=5)
if result["success"]:
    print("Credential deleted")
```

### `logout() -> Dict`

Logout current user and clear session.

**Returns:**
```python
{
    "success": bool,
    "message": str
}
```

**Example:**
```python
api.logout()
print("Session cleared")
```

## Password Generation

### Generate Secure Password

```python
from generator import PasswordGenerator

gen = PasswordGenerator()

# Default (16 chars, all character types)
password = gen.generate()

# Custom length
password = gen.generate(length=24)

# Specific character types
password = gen.generate(
    length=20,
    use_uppercase=True,
    use_lowercase=True,
    use_digits=True,
    use_symbols=False
)

print(f"Generated: {password}")
```

## Password Strength Checking

### Check Password Strength

```python
from generator import PasswordStrengthChecker

checker = PasswordStrengthChecker()

password = "MySecurePassword123!"
strength, label, color, details = checker.check(password)

print(f"Strength: {label}")  # "Good", "Very Strong", etc.
print(f"Entropy: {details['entropy']} bits")
print(f"Details: {details}")
```

**Response Structure:**
```python
{
    "length": 20,
    "entropy": 125.5,
    "pattern_penalty": 0,
    "adjusted_entropy": 125.5,
    "has_uppercase": True,
    "has_lowercase": True,
    "has_digits": True,
    "has_symbols": True,
    "has_spaces": False
}
```

## Error Handling

All API methods return standardized responses with `success` boolean.

```python
# Always check success flag
result = api.get_credentials()

if not result["success"]:
    error_msg = result.get("message", "Unknown error")
    print(f"Error: {error_msg}")
else:
    entries = result.get("entries", [])
    # Process entries
```

## Authentication State

The VaultAPI maintains authentication state:

```python
api.authenticate("user", "pass")

# User is authenticated
api.add_credential(...)  # Works

api.logout()

# User is NOT authenticated
api.get_credentials()  # Returns error
```

## Rate Limiting

Account lockout after 5 failed authentication attempts:

```python
# First 4 attempts fail
for i in range(4):
    api.authenticate("user", "wrongpass")
    # Still allowed to try

# 5th attempt
result = api.authenticate("user", "wrongpass")
# Account now locked for 10 minutes

result = api.authenticate("user", "correctpass")
print(result["message"])  # "Account is locked. Try again later."
```

## Security Best Practices

1. **Never hardcode credentials:**
   ```python
   # Bad
   api.authenticate("admin", "password123")
   
   # Good
   import os
   password = os.getenv("VAULT_PASSWORD")
   api.authenticate("admin", password)
   ```

2. **Always validate input:**
   ```python
   from utils import ValidationUtils
   
   valid, msg = ValidationUtils.validate_password(user_password)
   if not valid:
       print(f"Invalid: {msg}")
   ```

3. **Handle exceptions:**
   ```python
   try:
       result = api.get_credentials()
   except Exception as e:
       print(f"API error: {e}")
   ```

4. **Clear sensitive data:**
   ```python
   password = api.get_credentials()
   # Use password
   del password  # Clear from memory
   ```

## Example: Complete Workflow

```python
from api import VaultAPI
from database import VaultDatabase
from generator import PasswordGenerator

# Connect to database
db = VaultDatabase()
api = VaultAPI(db)

# Register new user
api.register("john_doe", "SecurePassword123!")

# Authenticate
auth_result = api.authenticate("john_doe", "SecurePassword123!")
if not auth_result["success"]:
    print("Authentication failed")
    exit(1)

# Generate password for new service
gen = PasswordGenerator()
gmail_password = gen.generate(length=20)

# Add credential
api.add_credential(
    service_name="Gmail",
    username="john@gmail.com",
    password=gmail_password,
    notes="Personal email"
)

# Get all credentials
creds = api.get_credentials()
print(f"Stored {creds['count']} credentials")

# Search for specific service
gmail_entries = api.get_credentials(search_term="Gmail")
for entry in gmail_entries["entries"]:
    print(f"Found: {entry['service_name']}")

# Logout
api.logout()
print("Session ended")
```

## Rate Limits & Quotas

| Operation | Limit |
|-----------|-------|
| Login attempts | 5 per 10 minutes |
| Credential storage | 500+ per user |
| Search results | No limit |
| API calls | No throttling (local) |

## Troubleshooting

### "Not authenticated" error
```
Solution: Call authenticate() first before any vault operations
```

### "Invalid username or password"
```
Solution: 
1. Verify username is correct
2. Check password (case-sensitive)
3. Ensure account is not locked
```

### "Database connection error"
```
Solution:
1. Verify PostgreSQL is running
2. Check database credentials in .env
3. Ensure database exists
```

## Version

**API Version:** 1.0  
**Last Updated:** July 1, 2026

---

For more information, see [README.md](README.md) and [SECURITY.md](SECURITY.md)
