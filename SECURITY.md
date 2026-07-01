# Security Policy & Best Practices

## Security First

This document outlines the security measures implemented and best practices for using Secure Password Vault.

## Implemented Security Measures

### Authentication & Hashing

- **PBKDF2-HMAC-SHA256** with 260,000 iterations (OWASP recommended)
- Unique per-user **32-byte random salts**
- **Constant-time password comparison** to prevent timing attacks
- **Account lockout** after 5 failed attempts within 10 minutes

### Database Security

- **Parameterized SQL queries** - eliminates SQL injection attacks
- **Foreign key constraints** - ensures referential integrity
- **Cascade delete** - prevents orphaned records
- **User isolation** - credentials only accessible to owner

### Credential Storage

- Passwords stored in PostgreSQL with appropriate encoding
- **No plaintext passwords** ever stored or logged
- **Audit logging** for all operations

### Cryptographic Standards

- Uses Python's built-in `secrets` module for random generation
- OS-level entropy (`os.urandom`) for cryptographic operations
- **SHA256** for hashing functions
- Follows OWASP guidelines for password storage

## Audit Logging

All operations are logged with:

- User ID and timestamp
- Action type (LOGIN, ADD, UPDATE, DELETE, VIEW)
- Entry ID (where applicable)
- IP address of the request

Audit logs help detect:

- Unauthorized access attempts
- Suspicious activity patterns
- Data modification history

## Deployment Security

### Network Security

- Always use HTTPS in production
- Restrict database access to localhost or VPN
- Use firewalls to limit port exposure
- Implement rate limiting on login endpoints

### Environment Security

```bash
# Use environment variables for sensitive data
export DB_PASSWORD="your_secure_password"
export DB_HOST="your_db_server"

# Never commit .env files
# Use .env.example as template only
```

### PostgreSQL Hardening

```sql
-- Create dedicated database user (not postgres)
CREATE USER vault_user WITH PASSWORD 'strong_password';

-- Grant minimal required permissions
GRANT CONNECT ON DATABASE password_vault TO vault_user;
GRANT USAGE ON SCHEMA public TO vault_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO vault_user;

-- Restrict to specific tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO vault_user;
```

## Vulnerability Reporting

### Responsible Disclosure

If you discover a security vulnerability:

1. **DO NOT** post on public forums or open GitHub issues
2. Email: **security@dlytica.academy** with:
   - Vulnerability description
   - Affected components
   - Potential impact
   - Suggested fix (optional)
   - Your contact information

3. We will:
   - Acknowledge receipt within 48 hours
   - Confirm vulnerability status within 1 week
   - Release patch within 30 days
   - Credit you in security advisories (if desired)

## Security Checklist for Deployment

- [ ] Change default PostgreSQL password
- [ ] Configure environment variables securely
- [ ] Enable PostgreSQL SSL connections
- [ ] Set up firewall rules
- [ ] Enable audit logging
- [ ] Implement log rotation
- [ ] Set up monitoring alerts
- [ ] Regular backups enabled
- [ ] Keep Python and dependencies updated
- [ ] Disable debug mode in production

## Regular Maintenance

### Update Schedule

```bash
# Check for updates monthly
pip list --outdated

# Update dependencies safely
pip install --upgrade psycopg2-binary
pip install --upgrade cryptography

# Test after updates
python -m unittest discover tests
```

### Monitoring

- Monitor audit logs for suspicious patterns
- Check failed login attempts
- Review system resource usage
- Verify backup integrity

## Security Testing

### Run Security Tests

```bash
# Test password hashing strength
python -m unittest tests.test_auth.TestAuthManager

# Test SQL injection prevention
# All queries use parameterized statements

# Test user isolation
python -m unittest tests.test_integration.TestVaultIntegration
```

### Penetration Testing

Before production deployment:

1. SQL injection testing
2. Authentication bypass attempts
3. Authorization boundary testing
4. Credential leakage analysis
5. Timing attack testing

## Known Limitations

1. **GUI-only**: No API endpoint authentication (use programmatic VaultAPI for external access)
2. **Local storage**: Vault database must be on same machine or accessible LAN
3. **No encryption at rest**: Database passwords should be protected by OS
4. **Master password recovery**: No password recovery mechanism (intentional)

## Future Security Improvements

- [ ] Database encryption at rest
- [ ] Hardware security module (HSM) integration
- [ ] Multi-factor authentication (2FA)
- [ ] End-to-end encryption for exports
- [ ] Zero-knowledge architecture
- [ ] Biometric authentication

## Security References

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-3/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/sql-createuser.html)

## Questions?

Email: **security@dlytica.academy**

---

**Last Updated:** July 1, 2026  
**Version:** 1.0
