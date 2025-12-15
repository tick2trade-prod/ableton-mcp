# Workflow: Security Test

**Phase**: 4 - Testing & Quality
**ID**: 4020

## Overview

Run security tests including OWASP checks, SQL injection, XSS.

## Usage

```
/workflow-security-test target="app/" scan_types="sql,xss,secrets"
```

## Parameters

- `target`: Code/URL to test (required)
- `scan_types`: sql,xss,secrets,deps (default: "all")
- `severity_threshold`: Minimum severity (default: "medium")

## Workflow Steps

1. Run Bandit (Python security)
2. Run OWASP ZAP (web security)
3. Check for secrets
4. Scan dependencies
5. Generate report

## Implementation

```bash
uv run bandit -r $target -ll
docker run owasp/zap2docker-stable zap-baseline.py -t $target
uv run safety check
```

## Output

```json
{
  "vulnerabilities_found": 3,
  "severity": {"high": 1, "medium": 2},
  "scan_types": ["sql", "xss", "secrets"]
}
```
