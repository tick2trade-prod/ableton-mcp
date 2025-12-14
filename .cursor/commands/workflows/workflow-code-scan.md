# Workflow: Real-Time Code Scanning

## Overview

Perform real-time code scanning for security vulnerabilities, code quality issues, and compliance violations before merging.

## Usage

```bash
/workflow-code-scan
```

## Parameters

- `scan_type`: security, quality, compliance, all (default: all)
- `auto_fix`: Auto-fix issues (default: false)
- `block_on_severity`: Minimum severity to block - critical, high, medium (default: critical)

## Scan Types

```python
# Security Scan
- OWASP Top 10
- CWE vulnerabilities
- Secrets detection
- Dependency vulnerabilities

# Quality Scan
- Code complexity
- Code duplication
- Code smells
- Best practices

# Compliance Scan
- License compliance
- GDPR compliance
- PCI-DSS compliance
- HIPAA compliance
```

## Output

```json
{
  "security_issues": 2,
  "quality_issues": 5,
  "compliance_issues": 0,
  "auto_fixed": 3,
  "blocked": false
}
```
