# Blueprint Decoder - Security & Compliance Documentation

## Executive Summary

The Blueprint Decoder is designed with security and privacy as first-class concerns. This document outlines the security measures, compliance controls, and incident response procedures.

## Security Measures

### 1. Input Validation

**URL Whitelist Enforcement**
- Only URLs in the approved whitelist can be accessed
- Whitelist includes: `internal.company.com`, `secure.blueprint.io`
- All other URLs are rejected with clear error messages
- Whitelist validation is enforced at every request

```python
# Whitelist validation example
APPROVED_SOURCES = [
    "https://internal.company.com",
    "https://secure.blueprint.io",
]

def validate_url(url):
    """Verify URL is in whitelist before proceeding"""
    for source in APPROVED_SOURCES:
        if url.startswith(source):
            return True
    return False  # Reject any URL not in whitelist
```

**Timeout Protection**
- All network requests timeout after 30 seconds
- Prevents resource exhaustion from slow/malicious servers
- Configurable via environment variable: `DECODER_TIMEOUT_SECONDS`

### 2. Secret Handling

**Encryption at Rest**
- Secrets are encrypted using AES-256-GCM before storage
- Encryption key is stored in secure key management service (AWS KMS / Azure Key Vault)
- No plaintext secrets in database or logs

**Encryption in Transit**
- All network communication uses TLS 1.3
- Certificate pinning for critical connections
- Mutual TLS (mTLS) for service-to-service communication

**Secret Masking in Logs**
- Extracted secrets are NEVER logged in plaintext
- Secrets are replaced with `***REDACTED***` in logs
- Only metadata about secrets (count, types) is logged

```python
# Example: Proper secret handling in logs
logger.info(f"Decoded {len(secrets)} secrets from {url}")  # ✓ Good
# logger.info(f"Secrets found: {secrets}")  # ✗ Bad - logs secrets
```

**Secret Output Masking**
- API responses can optionally mask secret values
- Use `?mask_secrets=true` query parameter
- Default: secrets are included only with valid authentication

### 3. Access Control

**API Authentication**
- All requests require API key authentication (Bearer token)
- Keys are issued per service/team
- Keys rotate every 90 days

**Role-Based Access Control (RBAC)**
- `reader`: Can only view decoded secrets
- `admin`: Can manage whitelist and configuration
- `operz`: Can deploy and manage infrastructure

**Audit Logging**
All access is logged with:
- User/service identity
- Action performed (read, write, delete)
- IP address and timestamp
- Success/failure status

```
2024-02-27T13:45:22Z [AUDIT] user=alice action=decode url=internal.company.com status=success ip=10.0.1.5
2024-02-27T13:46:15Z [AUDIT] user=malicious-bot action=decode url=evil.com status=REJECTED ip=203.0.113.42
```

### 4. Data Privacy

**Data Retention**
- Decoded secrets are retained for 7 days maximum
- Logs are rotated every 30 days
- Audit logs retained for 1 year (compliance requirement)
- User can request data deletion anytime (GDPR)

**Data Minimization**
- Only store what's necessary
- Don't log full request/response bodies
- Use hashed identifiers where possible

**Personally Identifiable Information (PII)**
- If secrets contain PII (user IDs, emails), they're flagged for special handling
- Extra encryption layer for PII-flagged data
- Restricted access (compliance team approval required)

## Compliance Checklist

- [x] **No secrets in code**: Verified via automated scanning
- [x] **No secrets in logs**: Logging middleware masks all sensitive data
- [x] **Secrets encrypted at rest**: AES-256-GCM encryption
- [x] **Secrets encrypted in transit**: TLS 1.3 enforced
- [x] **All access logged**: Audit middleware logs all operations
- [x] **Access control**: API key + RBAC enforced
- [x] **Incident response plan**: Documented and tested quarterly
- [x] **Code reviewed**: All changes require security team sign-off
- [x] **Dependency scanning**: Weekly automated scans for vulnerabilities
- [x] **Penetration tested**: Third-party pen test completed annually

## Vulnerability Disclosure

If you discover a security vulnerability:

1. **Do NOT** post it publicly
2. **DO** email security@company.com with:
   - Description of vulnerability
   - Steps to reproduce
   - Impact assessment
   - Suggested fix (optional)

3. We will:
   - Acknowledge within 24 hours
   - Fix within 7 days for critical issues
   - Credit you in release notes (if desired)
   - Provide a bounty (if eligible)

## Incident Response

### Security Incident Classification

**Critical** (Response required within 1 hour)
- Secret compromise or leakage
- Unauthorized access
- Data exfiltration
- System unavailability

**High** (Response required within 4 hours)
- Failed authentication attempts spike
- Suspicious activity detected
- Configuration drift

**Medium** (Response required within 24 hours)
- Minor security finding
- Potential vulnerability
- Access control misconfiguration

### Incident Response Procedure

1. **Detection**: Alert triggered or report received
2. **Assessment**: Determine severity and scope
3. **Containment**: Stop the bleeding (disable accounts, block IPs, etc.)
4. **Eradication**: Remove root cause
5. **Recovery**: Restore normal operations
6. **Post-Incident**: Review and improve

### Security Incident Contacts

- **Primary**: security@company.com
- **Escalation**: @security-team on Slack
- **Emergency (life/death)**: Local law enforcement first, then security team

## Configuration

### Environment Variables for Security

```bash
# Encryption key (store in secure secret manager ONLY)
ENCRYPTION_KEY_ID=arn:aws:kms:us-east-1:123456789:key/12345678-1234

# URL whitelist (comma-separated)
WHITELIST_URLS=https://internal.company.com,https://secure.blueprint.io

# Timeout (seconds)
DECODER_TIMEOUT_SECONDS=30

# Secret masking
MASK_SECRETS_IN_OUTPUT=true
MASK_SECRETS_IN_LOGS=true

# Audit logging
AUDIT_LOG_ENABLED=true
AUDIT_LOG_LEVEL=INFO

# IP allowlist (optional, for extra security)
IP_ALLOWLIST=10.0.0.0/8,172.16.0.0/12
```

## Review Schedule

- **Daily**: Monitoring alerts, failed auth attempts
- **Weekly**: Dependency security scans
- **Monthly**: Access review, log review
- **Quarterly**: Penetration testing, incident response drill
- **Annually**: Third-party security audit, architecture review

## References

- **OWASP Top 10**: https://owasp.org/Top10/
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework
- **Company Security Policy**: https://wiki.company.com/security-policy
- **PCI DSS Compliance**: https://www.pcisecuritystandards.org/

## Approval

This security documentation is approved by:

- [ ] Security Team Lead: ___________________ Date: ______
- [ ] Compliance Officer: ___________________ Date: ______
- [ ] Engineering Lead: ___________________ Date: ______

**Last Updated**: 2024-02-27
**Next Review**: 2024-05-27
