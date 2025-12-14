# Workflow: Automated Compliance Checks

## Overview

Run static/dynamic analysis, secrets scanning, license checks, and open fix PRs automatically.

## Usage

```bash
/workflow-compliance-check
```

## Parameters

- `compliance_standards`: owasp, pci-dss, hipaa, gdpr, sox (required)
- `auto_fix`: Auto-create fix PRs (default: true)
- `block_on_violation`: Block deployment on violations (default: true)

## Compliance Checks

```python
# OWASP Top 10
- Injection flaws
- Broken authentication
- Sensitive data exposure
- XXE, XSS, CSRF

# PCI-DSS
- Cardholder data protection
- Encryption requirements
- Access controls

# HIPAA
- PHI protection
- Audit logging
- Access controls

# GDPR
- Data privacy
- Right to deletion
- Consent management

# License Compliance
- Open source licenses
- Commercial licenses
- License conflicts
```

## Output

```json
{
  "violations_found": 3,
  "auto_fixed": 2,
  "fix_prs_created": 2,
  "compliance_status": {
    "owasp": "pass",
    "pci-dss": "fail",
    "gdpr": "pass"
  }
}
```
