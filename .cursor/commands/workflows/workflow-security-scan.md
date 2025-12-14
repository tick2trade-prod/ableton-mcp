# Workflow: Security-Enhanced Code Generation

## Overview

Generate code with built-in security analysis, static analysis, and fuzz testing. Proactively identifies and mitigates vulnerabilities during code generation.

## Usage

```bash
/workflow-security-scan
```

## Parameters

- `feature_name`: Feature to implement with security (required)
- `scan_depth`: shallow, standard, deep (default: standard)
- `auto_fix`: Automatically fix vulnerabilities (default: true)
- `block_on_critical`: Block on critical vulnerabilities (default: true)
- `compliance_standards`: Comma-separated standards - owasp, pci-dss, hipaa, gdpr (default: "owasp")

## Security Checks

```python
# 1. Static Analysis (SAST)
- SQL injection
- XSS vulnerabilities
- CSRF vulnerabilities
- Authentication bypass
- Authorization issues
- Secrets in code
- Insecure dependencies

# 2. Dynamic Analysis (DAST)
- Runtime vulnerabilities
- Memory leaks
- Buffer overflows
- Race conditions

# 3. Dependency Scanning
- Known vulnerabilities (CVE)
- Outdated packages
- License compliance

# 4. Fuzz Testing
- Input validation
- Edge cases
- Error handling
```

## Output

```json
{
  "vulnerabilities_found": 3,
  "critical": 0,
  "high": 1,
  "medium": 2,
  "auto_fixed": 2,
  "manual_review_required": 1,
  "compliance_status": {
    "owasp": "pass",
    "pci-dss": "fail"
  }
}
```
