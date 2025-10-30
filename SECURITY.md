# Security Policy

## Reporting a Vulnerability

PAL-adin takes security seriously. We appreciate your efforts to responsibly disclose your findings.

### How to Report

**For security vulnerabilities, please use one of the following methods:**

1. **GitHub Security Advisories** (Preferred)
   - Go to the [Security tab](https://github.com/unown-ai/paladin/security) of this repository
   - Click "Report a vulnerability"
   - Fill out the advisory form with details

2. **Private Issue**
   - For sensitive issues that need private disclosure
   - Create a new issue and mark it as security-related
   - We'll move it to a private advisory

3. **PGP Encrypted Communication**
   - For highly sensitive disclosures
   - PGP keys available in `/.well-known/security-keys/`
   - Send encrypted details via GitHub Issues

### What to Include

When reporting a vulnerability, please include:

- **Description**: Clear description of the vulnerability
- **Impact**: Potential impact and attack scenarios
- **Reproduction**: Step-by-step instructions to reproduce
- **Affected Versions**: Which versions are affected
- **Suggested Fix**: If you have ideas on how to fix it (optional)

### Response Timeline

- **Initial Response**: Within 24-48 hours
- **Assessment**: Security Working Group will assess severity within 72 hours
- **Updates**: Regular updates on progress
- **Resolution**: Coordinated disclosure after fix is deployed
- **Public Disclosure**: 90 days from initial report (negotiable)

### Severity Levels

We use the following severity classifications:

- **Critical**: Immediate threat, active exploitation possible
  - Response: 4 hours assessment, 24 hours resolution target
  - Examples: Remote code execution, authentication bypass

- **High**: Serious security impact
  - Response: 24 hours assessment, 72 hours resolution target
  - Examples: Privilege escalation, SQL injection

- **Medium**: Moderate security impact
  - Response: 72 hours assessment, 1 week resolution target
  - Examples: XSS, CSRF, information disclosure

- **Low**: Minimal security impact
  - Response: 1 week assessment, 2 weeks resolution target
  - Examples: Security misconfigurations, minor information leaks

## Security Best Practices

### For Users

- **Keep Updated**: Always use the latest version
- **Use HTTPS**: Always access PAL-adin over HTTPS
- **Strong Passwords**: Use strong, unique passwords
- **Enable 2FA**: Enable two-factor authentication when available
- **Review Permissions**: Regularly review application permissions
- **Backup Data**: Regularly backup your data
- **Monitor Logs**: Check logs for suspicious activity

### For Developers

- **Security Reviews**: All PRs require security consideration
- **Dependency Updates**: Keep dependencies updated
- **Input Validation**: Always validate and sanitize input
- **Secure Defaults**: Use secure defaults for all configurations
- **Principle of Least Privilege**: Grant minimum necessary permissions
- **Encryption**: Use encryption for sensitive data at rest and in transit
- **Audit Logs**: Maintain comprehensive audit logs

## Security Features

PAL-adin implements the following security measures:

### Authentication & Authorization
- Zero-knowledge authentication
- End-to-end encryption (E2EE)
- Password hashing with bcrypt
- JWT-based session management
- Role-based access control (RBAC)

### Data Protection
- AES-256-GCM encryption at rest
- ChaCha20-Poly1305 for data in transit
- Full disk encryption (FDE) support
- Encrypted database backups
- Secure key management

### Infrastructure Security
- Container security with non-root users
- Network isolation with Docker networks
- Firewall rules and rate limiting
- Security headers (HSTS, CSP, etc.)
- Regular security scanning

### Privacy Features
- Local AI processing (Ollama)
- Zero-knowledge architecture
- Anonymous authentication options
- Data minimization principles
- Right to deletion (GDPR compliant)

## Vulnerability Disclosure Policy

### Public Disclosure

Once a vulnerability is fixed:

1. **Patch Released**: Security patch deployed
2. **Notification**: Users notified of update
3. **Grace Period**: 7-14 days for users to update
4. **Public Disclosure**: Full details published
5. **Credit**: Reporter credited (if desired)

### Anonymous Reporting

We support anonymous vulnerability reporting:

- Use GitHub anonymous reporting features
- Use Tor Browser for additional privacy
- We respect reporter privacy preferences
- Anonymous credit available upon request

## Recognition

We believe in recognizing security researchers:

- **Public Credit**: Listed in SECURITY.md and release notes (if desired)
- **GitHub Badge**: Security researcher badge
- **Project Recognition**: Featured in project updates
- **Anonymous Option**: Full privacy if preferred

## Scope

### In Scope

- Web application vulnerabilities
- API security issues
- Authentication/authorization bypasses
- Data exposure issues
- Cryptographic weaknesses
- Dependency vulnerabilities
- Infrastructure misconfigurations

### Out of Scope

- Social engineering attacks
- Physical attacks
- DDoS attacks
- Spam or abuse of service
- Issues in third-party services
- Already known/reported issues

## Security Audits

PAL-adin undergoes regular security audits:

- **Annual Audits**: Comprehensive security audit
- **Dependency Scanning**: Automated daily scans
- **Code Analysis**: Static analysis on all commits
- **Penetration Testing**: Community-driven testing
- **Public Reports**: Summary reports published

## Compliance

PAL-adin aims to comply with:

- **GDPR**: EU data protection regulation
- **CCPA**: California consumer privacy act
- **SOC 2**: Security and availability controls
- **OWASP Top 10**: Web application security risks
- **CWE/SANS Top 25**: Most dangerous software errors

## Security Contacts

For security-related questions or concerns:

- **GitHub Security**: Use the Security tab on this repository
- **GitHub Discussions**: Tag posts with `#security` for general questions
- **Security Working Group**: Coordinates via GitHub Security Advisories

---

**Last Updated**: 2025-01-30

**Note**: This security policy is a living document and may be updated periodically. Check back regularly for updates.
