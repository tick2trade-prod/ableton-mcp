# Feature: Security

**Rank**: 3 - Feature-Based Commands

## Overview

Security audit and vulnerability fixes with automated scanning.

## Usage

```
/feature-security target="app/" scan_types="sql,xss,secrets"
```

## Parameters

- `target`: Code to audit (required)
- `scan_types`: sql,xss,secrets,deps (default: "all")
- `auto_fix`: Auto-fix issues (default: false)

## Workflow

1. Run security scanners
2. Identify vulnerabilities
3. Prioritize by severity
4. Apply fixes (if auto_fix)
5. Generate report

## Output

```json
{
  "vulnerabilities_found": 3,
  "vulnerabilities_fixed": 2,
  "severity": "medium"
}
```
