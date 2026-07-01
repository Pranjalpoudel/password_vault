# Contributing to Secure Password Vault

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and professional
- Report security vulnerabilities privately
- No spam or unsolicited promotion
- Maintain confidentiality of sensitive data

## How to Contribute

### 1. Fork and Clone

```bash
git clone https://github.com/yourusername/password_vault.git
cd password_vault
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/your-bug-fix
```

### 3. Development Setup

```bash
pip install -r requirements.txt
python setup_database.py
python -m unittest discover tests
```

### 4. Make Your Changes

- Follow PEP 8 style guide
- Add type hints to functions
- Update docstrings with clear descriptions
- Add unit tests for new features

### 5. Testing

```bash
# Run all tests
python -m unittest discover tests

# Run specific test
python -m unittest tests.test_auth

# Check test coverage (if coverage installed)
coverage run -m unittest discover tests
coverage report
```

### 6. Commit Guidelines

- Use meaningful commit messages
- Reference issues: "Fixes #123"
- Use conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
- Keep commits atomic and logical

Example:

```
feat: Add two-factor authentication support

- Implement TOTP-based 2FA
- Add recovery codes generation
- Update UI with 2FA setup wizard
- Add comprehensive tests for 2FA flows

Fixes #456
```

### 7. Submit Pull Request

- Provide clear description of changes
- Reference related issues
- Ensure all tests pass
- Respond to code review feedback

## Coding Standards

### Style Guide

```python
# Good
def hash_password(password: str, salt: str) -> str:
    """Hash password using PBKDF2-HMAC-SHA256.

    Args:
        password: The plaintext password
        salt: The salt hex string

    Returns:
        The password hash hex digest
    """
    # Implementation
    pass

# Avoid
def hp(p, s):
    # implementation
    pass
```

### Security Requirements

- Always use parameterized queries (never string concatenation)
- Use constant-time comparison for sensitive data
- Never log passwords or sensitive credentials
- Use cryptographically secure random generation
- Validate all user inputs

## Areas for Contribution

### High Priority

- [ ] REST API endpoints
- [ ] Database encryption at rest
- [ ] Multi-factor authentication
- [ ] Export/import functionality
- [ ] Search optimization

### Medium Priority

- [ ] Web UI (Flask/React)
- [ ] Mobile app support
- [ ] Cloud backup integration
- [ ] Audit log analysis tools
- [ ] Performance benchmarking

### Low Priority

- [ ] Theme customization
- [ ] Keyboard shortcuts
- [ ] Plugin system
- [ ] Auto-lock on inactivity

## Reporting Bugs

### Security Issues

**DO NOT** open a public issue for security vulnerabilities. Email: security@dlytica.academy

### Regular Bugs

Include:

1. Python version and OS
2. Steps to reproduce
3. Expected vs actual behavior
4. Relevant error messages
5. Code snippet if applicable

## Questions?

- Check existing issues first
- Review documentation
- Ask in discussions
- Email: dev@dlytica.academy

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in the CONTRIBUTORS.md file and project README.

Thank you for making Secure Password Vault better! 🚀
