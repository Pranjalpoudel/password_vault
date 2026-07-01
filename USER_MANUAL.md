# Secure Password Vault - User Manual

## Welcome!

This manual guides you through using the Secure Password Vault application. The vault securely stores and manages your passwords with enterprise-grade encryption.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Registration & Login](#registration--login)
3. [Managing Credentials](#managing-credentials)
4. [Password Generator](#password-generator)
5. [Searching & Organizing](#searching--organizing)
6. [Security Tips](#security-tips)
7. [Troubleshooting](#troubleshooting)

## Getting Started

### Installation

1. **Install Python** (3.10 or newer)
   - Windows: https://www.python.org/downloads/
   - macOS: Use homebrew or https://www.python.org/downloads/
   - Linux: `sudo apt-get install python3 python3-pip`

2. **Download and Setup**
   ```bash
   git clone https://github.com/Pranjalpoudel/password_vault.git
   cd password_vault
   pip install -r requirements.txt
   python setup_database.py
   ```

3. **Launch Application**
   ```bash
   python main.py
   ```

## Registration & Login

### First Time Setup

1. **Launch** the application
2. **Choose "Register"** button
3. **Enter Username** (3-50 characters)
   - Use letters, numbers, underscore, hyphen only
   - Choose something memorable
4. **Create Master Password** (8+ characters minimum)
   - Must contain: UPPERCASE, lowercase, and numbers
   - Example: `MyVault2024Pass`
5. **Click Register** button
6. **Wait** for confirmation message

### Logging In

1. **Enter Username** you registered
2. **Enter Master Password** (case-sensitive)
3. **Click Login** button
4. **Vault opens** when authentication succeeds

⚠️ **Important:** Your master password cannot be recovered. Write it down and keep it safe!

## Managing Credentials

### Adding a Credential

1. **Click "Add Entry"** button in vault
2. **Enter Service Name** (e.g., "Gmail", "GitHub", "Bank")
3. **Enter Username/Email** for that service
4. **Enter Password** for that service
5. **Add Notes** (optional - e.g., "Personal email account")
6. **Click Save** button

### Viewing a Credential

1. **Find** the credential in the list
2. **Double-click** to open details
3. **Click "Show/Hide"** to reveal/hide password
4. **Copy** the password if needed
5. **Make notes** if necessary

### Editing a Credential

1. **Open** the credential
2. **Change** any field you want to update
3. **Click Update** button
4. **Wait** for confirmation

### Deleting a Credential

1. **Open** the credential
2. **Click Delete** button
3. **Confirm** deletion
4. **Entry is permanently removed**

## Password Generator

### Generate a Secure Password

1. **Click "Generate Password"** button
2. **Adjust length** using the slider (8-64 characters)
   - Default: 16 (recommended for most services)
3. **Select character types:**
   - ☑ Uppercase (A-Z)
   - ☑ Lowercase (a-z)
   - ☑ Digits (0-9)
   - ☑ Symbols (!@#$%^&*)
4. **Click "Generate"** button
5. **View** strength indicator:
   - 🔴 Very Weak (avoid)
   - 🟠 Weak (acceptable)
   - 🟡 Fair (good)
   - 🟢 Good (very good)
   - 🟢🟢 Very Strong (excellent)

### Copy Password

1. After generating a password
2. **Click "Copy"** button
3. **Password is copied** to clipboard
4. **Paste** into the service's password field
5. **Click "Close"** when done

### Password Strength Explained

| Level | Entropy | What It Means |
|-------|---------|--------------|
| Very Weak | <20 bits | Easy to crack - avoid |
| Weak | 20-40 bits | Not recommended |
| Fair | 40-60 bits | Acceptable for low-security |
| Good | 60-90 bits | Recommended for most services |
| Very Strong | >90 bits | Excellent for banking/critical |

## Searching & Organizing

### Search for Credentials

1. **Find** the search box at top of vault
2. **Type** part of service name (e.g., "gmai" for Gmail)
3. **Results filter** automatically as you type
4. **Click** a result to view details

### Filtering by Priority

Credentials are automatically sorted alphabetically by service name.

**Tip:** Use naming conventions:
- Prefix critical accounts: `[CRITICAL] Bank of America`
- Prefix work accounts: `[WORK] GitHub Enterprise`

## Security Tips

### ✅ DO:

- ✅ Use a **strong master password**
- ✅ **Change passwords** regularly
- ✅ Use **unique password** for each service
- ✅ **Keep computer updated** with latest patches
- ✅ **Lock screen** when stepping away
- ✅ **Use generated passwords** from the tool
- ✅ **Write down master password** and store safely

### ❌ DON'T:

- ❌ Use **simple passwords** like "password123"
- ❌ **Reuse passwords** across services
- ❌ **Share master password** with anyone
- ❌ Write passwords on **sticky notes**
- ❌ **Store passwords** in plain text files
- ❌ Use **birthdate-based** passwords
- ❌ Leave vault **open and unattended**

### Master Password Recovery

⚠️ **No way to recover master password!**

If you forget your master password:
1. All your credentials are inaccessible
2. The database cannot be decrypted
3. You must start over with a new vault

**Solution:** Write it down and store safely!

## Troubleshooting

### "Invalid username or password" on login

**Causes:**
- Typed username wrong
- Typed password wrong (case-sensitive)
- Account locked due to multiple failed attempts

**Solutions:**
- Check username spelling
- Verify password is correct
- Wait 10 minutes if account locked
- Try again with correct credentials

### "Database connection error"

**Causes:**
- PostgreSQL is not running
- Database not initialized
- Wrong credentials in `.env`

**Solutions:**
1. Ensure PostgreSQL is installed and running
2. Run `python setup_database.py` again
3. Check database credentials in `.env` file
4. Verify PostgreSQL server is accessible

### "Service seems unresponsive"

**Causes:**
- Application frozen
- Database query taking long time
- Computer low on memory

**Solutions:**
- Close and reopen application
- Restart PostgreSQL
- Free up system memory
- Check internet connection if using network database

### Application won't start

**Causes:**
- Python 3.10+ not installed
- Dependencies not installed
- PostgreSQL not installed

**Solutions:**
```bash
# Check Python version
python --version  # Must be 3.10+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Install PostgreSQL
# Windows: Download from postgresql.org
# macOS: brew install postgresql
# Linux: sudo apt-get install postgresql
```

### Forgot Master Password

⚠️ **Recovery is NOT possible**

You must:
1. Delete the old vault database
2. Run `python setup_database.py` to create new database
3. Register with a new username
4. **Write down new master password!**

## Performance Tips

### Optimize Vault Speed

1. **Use exact service names** when searching
2. **Keep password list under 500 entries** for best performance
3. **Regularly backup** your database
4. **Use SSD** for faster disk access
5. **Close other applications** to free memory

### Backup Procedures

```bash
# Create backup
pg_dump -U postgres password_vault > backup.sql

# Restore from backup
psql -U postgres password_vault < backup.sql
```

## Getting Help

### Common Questions

**Q: Where are my passwords stored?**  
A: In PostgreSQL database on your computer. Encrypted with PBKDF2-HMAC-SHA256.

**Q: Can I access vault from another computer?**  
A: No - vault is local only for security. That's a feature!

**Q: How strong is the encryption?**  
A: OWASP-recommended 260,000 iterations with unique salts.

**Q: What happens if someone gets my database file?**  
A: Useless without your master password (260,000 iterations to crack).

**Q: Can I export passwords?**  
A: Not in v0.1.0 for security. Future versions may support encrypted exports.

### Contact Support

- **Email:** support@dlytica.academy
- **GitHub Issues:** https://github.com/Pranjalpoudel/password_vault/issues
- **Security Issues:** security@dlytica.academy

## Quick Reference

| Action | How |
|--------|-----|
| Register | Launch → Register button → Fill form |
| Login | Enter credentials → Click Login |
| Add password | Add Entry → Fill form → Save |
| View password | Double-click entry → Show/Hide button |
| Edit password | Open entry → Change fields → Update |
| Delete password | Open entry → Delete button → Confirm |
| Generate password | Generate Password → Configure → Generate |
| Search | Type in search box → View results |
| Logout | Close application (auto-logout) |

---

**Version:** 1.0  
**Last Updated:** July 1, 2026  
**For Support:** support@dlytica.academy
