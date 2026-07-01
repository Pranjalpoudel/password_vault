# Deployment Guide

## Prerequisites

- Python 3.10+
- PostgreSQL 14+
- 500 MB disk space
- Linux/Windows/macOS

## Production Deployment

### Step 1: System Setup

```bash
# Update system packages
apt-get update && apt-get upgrade -y  # Linux only

# Install PostgreSQL (if not installed)
# Windows: Download from https://www.postgresql.org/download/windows/
# macOS: brew install postgresql
# Linux: apt-get install postgresql postgresql-contrib
```

### Step 2: Database Preparation

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE password_vault;
CREATE USER vault_user WITH PASSWORD 'very_strong_password_here';
GRANT CONNECT ON DATABASE password_vault TO vault_user;
GRANT USAGE ON SCHEMA public TO vault_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO vault_user;
```

### Step 3: Application Setup

```bash
# Clone repository
git clone https://github.com/Pranjalpoudel/password_vault.git
cd password_vault

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env

# Edit .env with production settings
# Set: DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, APP_DEBUG=False
nano .env  # or use your editor
```

### Step 4: Database Initialization

```bash
# Run setup script
python setup_database.py

# Follow prompts and enter your database credentials
```

### Step 5: Run Tests

```bash
# Run comprehensive tests
python -m unittest discover tests

# Expected output: OK (no failures)
```

### Step 6: Launch Application

```bash
# Start the vault
python main.py

# Application window opens
# Register admin user
# Start using the vault
```

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV DB_HOST=postgres
ENV DB_PORT=5432
ENV DB_USER=vault_user
ENV DB_PASSWORD=changeme
ENV DB_NAME=password_vault

CMD ["python", "main.py"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_USER: vault_user
      POSTGRES_PASSWORD: changeme
      POSTGRES_DB: password_vault
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  vault:
    build: .
    depends_on:
      - postgres
    environment:
      DB_HOST: postgres
      DB_PORT: 5432
      DB_USER: vault_user
      DB_PASSWORD: changeme
      DB_NAME: password_vault
    volumes:
      - ./logs:/app/logs
    ports:
      - "8000:8000"

volumes:
  postgres_data:
```

### Deploy with Docker

```bash
# Build and start
docker-compose up -d

# Initialize database
docker-compose exec vault python setup_database.py

# Check logs
docker-compose logs -f vault
```

## Systemd Service (Linux)

Create `/etc/systemd/system/password-vault.service`:

```ini
[Unit]
Description=Secure Password Vault
After=network.target postgresql.service

[Service]
Type=simple
User=vault
WorkingDirectory=/opt/password_vault
Environment="PATH=/opt/password_vault/venv/bin"
ExecStart=/opt/password_vault/venv/bin/python /opt/password_vault/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:

```bash
# Enable and start service
sudo systemctl enable password-vault
sudo systemctl start password-vault

# Check status
sudo systemctl status password-vault

# View logs
sudo journalctl -u password-vault -f
```

## Backup Strategy

### Automated Backup

```bash
#!/bin/bash
# backup_vault.sh

BACKUP_DIR="/backups/password_vault"
DB_NAME="password_vault"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Backup database
pg_dump -U vault_user $DB_NAME > "$BACKUP_DIR/db_$TIMESTAMP.sql"

# Compress
gzip "$BACKUP_DIR/db_$TIMESTAMP.sql"

# Keep only last 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_DIR/db_$TIMESTAMP.sql.gz"
```

### Restore from Backup

```bash
# Restore database
gunzip < backup_20260701_120000.sql.gz | psql -U vault_user password_vault
```

## Monitoring & Maintenance

### Monitoring Checklist
- [ ] Disk space usage
- [ ] Database performance
- [ ] Application logs
- [ ] Failed login attempts
- [ ] Backup completion

### Performance Tuning

```sql
-- Add indexes for frequently searched columns
CREATE INDEX idx_service_name ON vault_entries(service_name);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM vault_entries WHERE service_name LIKE '%gmail%';
```

### Log Rotation

```bash
# Edit /etc/logrotate.d/password-vault
/opt/password_vault/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 vault vault
    sharedscripts
    postrotate
        systemctl reload password-vault > /dev/null 2>&1 || true
    endscript
}
```

## SSL/TLS Configuration

For production with database over network:

```bash
# Generate SSL certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

# Configure PostgreSQL
# Edit postgresql.conf:
ssl = on
ssl_cert_file = '/path/to/cert.pem'
ssl_key_file = '/path/to/key.pem'
```

## Troubleshooting

### Database Connection Issues
```
Error: "could not connect to server"
Solution: 
1. Verify PostgreSQL is running
2. Check DB_HOST, DB_PORT in .env
3. Verify credentials
```

### Permission Errors
```
Error: "permission denied"
Solution:
1. Check user permissions in PostgreSQL
2. Verify directory ownership
3. Run: sudo chown -R vault:vault /opt/password_vault
```

### Performance Issues
```sql
-- Check slow queries
SELECT query, calls, mean_time FROM pg_stat_statements 
ORDER BY mean_time DESC LIMIT 10;

-- Vacuum and analyze
VACUUM ANALYZE;
```

## Upgrade Guide

```bash
# Backup first!
./backup_vault.sh

# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run tests
python -m unittest discover tests

# Restart application
systemctl restart password-vault
```

## Support & Contact

- **Issues:** https://github.com/Pranjalpoudel/password_vault/issues
- **Email:** dev@dlytica.academy
- **Security:** security@dlytica.academy

---

**Last Updated:** July 1, 2026
