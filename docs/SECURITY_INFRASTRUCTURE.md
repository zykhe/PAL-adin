# PAL-adin Security Infrastructure Plan

## Full Disk Encryption (FDE) Implementation

### Linux Deployment (Primary)
```bash
# LUKS2 Full Disk Encryption Setup
# 1. During OS installation, enable full disk encryption
# 2. Use strong passphrase (minimum 20 characters, high entropy)
# 3. Enable encrypted swap partition
# 4. Configure automatic unlocking with TPM2 (optional for servers)

# Example LUKS setup
cryptsetup luksFormat --type luks2 /dev/sdaX
cryptsetup open /dev/sdaX paladin_crypt
mkfs.ext4 /dev/mapper/paladin_crypt
```

### OpenBSD Deployment (Secondary)
```bash
# OpenBSD Full Disk Encryption
# 1. During installation, enable encryption for all partitions
# 2. Use strong encryption key (bioctl -c C)
# 3. Configure encrypted swap
# 4. Set up secure boot parameters
```

## End-to-End Encryption (E2EE) Architecture

### Transport Layer Security
```mermaid
graph LR
    CLIENT[Client Browser] --> TLS1_3[TLS 1.3]
    TLS1_3 --> NGINX[Nginx Reverse Proxy]
    NGINX --> INTERNAL[Internal TLS]
    INTERNAL --> API[FastAPI Backend]
    
    subgraph "Certificate Management"
        LETSENCRYPT[Let's Encrypt]
        CERTBOT[Certbot Auto-renewal]
        INTERNAL_CA[Internal CA for mTLS]
    end
    
    TLS1_3 --> LETSENCRYPT
    INTERNAL --> INTERNAL_CA
```

### Application-Level Encryption
```python
# Encryption utilities for sensitive data
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

class DataEncryption:
    def __init__(self, password: str):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher = Fernet(key)
    
    def encrypt_data(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        return self.cipher.decrypt(encrypted_data.encode()).decode()
```

## Database Security

### PostgreSQL Encryption
```sql
-- Enable Transparent Data Encryption (TDE)
-- Note: Requires PostgreSQL 15+ with enterprise features
-- Alternative: Filesystem-level encryption

-- Column-level encryption for sensitive data
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Example encrypted column
ALTER TABLE users 
ADD COLUMN encrypted_preferences BYTEA;

-- Encryption function
CREATE OR REPLACE FUNCTION encrypt_sensitive_data(data TEXT)
RETURNS BYTEA AS $$
BEGIN
    RETURN pgp_sym_encrypt(data, current_setting('app.encryption_key'));
END;
$$ LANGUAGE plpgsql;
```

### Redis Security
```bash
# Redis configuration for security
# /etc/redis/redis.conf

# Enable TLS
tls-port 6380
port 0
tls-cert-file /path/to/redis.crt
tls-key-file /path/to/redis.key
tls-ca-cert-file /path/to/ca.crt

# Enable authentication
requirepass your_strong_redis_password

# Disable dangerous commands
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command KEYS ""
rename-command CONFIG "CONFIG_b835c3f8a5d2e7n4"
```

## API Security Architecture

### Authentication & Authorization
```mermaid
graph TB
    subgraph "Auth Flow"
        USER[User] --> LOGIN[Login Request]
        LOGIN --> AUTH[Auth Service]
        AUTH --> JWT[JWT Token + Refresh Token]
        JWT --> CLIENT[Client Storage]
        CLIENT --> API[API Request]
        API --> VERIFY[Token Verification]
        VERIFY --> ACCESS[Grant/Deny Access]
    end
    
    subgraph "Token Structure"
        HEADER[Header: alg, typ]
        PAYLOAD[Payload: user_id, role, exp, iat]
        SIGNATURE[Signature: HMAC-SHA256]
    end
```

### JWT Implementation
```python
# JWT token management
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

class SecurityManager:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = os.getenv("JWT_SECRET_KEY")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 7
    
    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
```

## Network Security

### Firewall Configuration
```bash
# UFW (Uncomplicated Firewall) setup
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# IPTables rules for additional security
iptables -A INPUT -p tcp --dport 22 -s YOUR_IP -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j DROP
```

### Intrusion Detection
```yaml
# Fail2ban configuration
# /etc/fail2ban/jail.local

[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log

[nginx-http-auth]
enabled = true
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/error.log
```

## Secret Management

### Environment Variables & Secrets
```bash
# .env file structure (never commit to version control)
DATABASE_URL=postgresql://user:password@localhost/paladin
REDIS_URL=redis://localhost:6379
JWT_SECRET_KEY=your_super_secret_jwt_key_here
GLM_API_KEY=your_glm_api_key
ENCRYPTION_KEY=your_data_encryption_key

# Use Docker secrets or Kubernetes secrets in production
```

### HashiCorp Vault Integration (Future)
```python
# Vault client for secret management
import hvac

class VaultManager:
    def __init__(self, vault_url: str, token: str):
        self.client = hvac.Client(url=vault_url, token=token)
    
    def get_secret(self, path: str) -> dict:
        return self.client.secrets.kv.v2.read_secret_version(path=path)
    
    def store_secret(self, path: str, secret: dict):
        return self.client.secrets.kv.v2.create_or_update_secret(
            path=path, secret=secret
        )
```

## Backup & Recovery Security

### Encrypted Backup Strategy
```bash
#!/bin/bash
# backup.sh - Encrypted backup script

# Database backup
pg_dump paladin_db | gzip | gpg --cipher-algo AES256 --compress-algo 1 --symmetric --output backup_$(date +%Y%m%d).sql.gz.gpg

# File backup
tar -czf - /path/to/paladin/data | gpg --cipher-algo AES256 --compress-algo 1 --symmetric --output files_backup_$(date +%Y%m%d).tar.gz.gpg

# Upload to secure storage (example: AWS S3 with encryption)
aws s3 cp backup_$(date +%Y%m%d).sql.gz.gpg s3://paladin-backups/ --server-side-encryption AES256
```

### Recovery Procedures
```bash
# Disaster recovery checklist
# 1. Verify system integrity
# 2. Restore from encrypted backups
# 3. Verify data integrity
# 4. Update configuration
# 5. Test all services
# 6. Monitor for anomalies
```

## Monitoring & Auditing

### Security Monitoring
```python
# Security event logging
import logging
from datetime import datetime

class SecurityLogger:
    def __init__(self):
        self.logger = logging.getLogger('security')
        handler = logging.FileHandler('/var/log/paladin/security.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_security_event(self, event_type: str, user_id: str, details: dict):
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'details': details,
            'ip_address': request.remote_addr
        }
        self.logger.info(f"SECURITY_EVENT: {event}")
```

### Audit Trail
```sql
-- Audit table for security events
CREATE TABLE security_audit (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id VARCHAR(255),
    event_type VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    details JSONB,
    severity VARCHAR(20) DEFAULT 'INFO'
);

-- Index for performance
CREATE INDEX idx_security_audit_timestamp ON security_audit(timestamp);
CREATE INDEX idx_security_audit_user_id ON security_audit(user_id);
```

## Compliance & Legal Considerations

### Data Protection
- GDPR compliance for EU users
- Data retention policies
- Right to deletion implementation
- Privacy by design principles

### Security Best Practices
- Regular security audits
- Penetration testing
- Dependency vulnerability scanning
- Security training for developers

This security infrastructure ensures PAL-adin meets the highest standards for data protection and privacy while maintaining flexibility for future enhancements.