# Tool: Package Verification

## Overview

Verify package exists (PyPI/NPM). This command uses the package verification tool from `app/server/tools/package_tool.py` to check if packages exist before using them, preventing hallucinated dependencies.

## Usage

Type `/tool-package` followed by the package name and ecosystem.

## Parameters

- `package_name`: Name of package to verify (required)
- `ecosystem`: Package ecosystem (pypi, npm, cargo, go) (required)
- `version`: Specific version to check (optional)
- `check_latest`: Get latest version (default: true)
- `check_security`: Check for security advisories (default: true)

## Example Usage

### Verify Python Package

```
/tool-package
Package Name: fastapi
Ecosystem: pypi
Check Latest: true
Check Security: true
```

### Verify Specific Version

```
/tool-package
Package Name: react
Ecosystem: npm
Version: 18.2.0
```

### Verify Rust Crate

```
/tool-package
Package Name: tokio
Ecosystem: cargo
Check Latest: true
```

## Workflow

1. **Package Lookup**:
   - Query package registry API
   - Check package exists
   - Verify version if specified

2. **Version Check**:
   - Get latest version
   - Compare with requested version
   - Check version compatibility

3. **Security Check** (if enabled):
   - Query security advisories
   - Check for known vulnerabilities
   - Report CVEs and severity

4. **Metadata Retrieval**:
   - Get package description
   - Retrieve download stats
   - Check maintenance status

## Output Format

```json
{
  "package_name": "fastapi",
  "ecosystem": "pypi",
  "exists": true,
  "latest_version": "0.104.1",
  "requested_version": null,
  "version_exists": true,
  "metadata": {
    "description": "FastAPI framework, high performance, easy to learn",
    "author": "Sebastián Ramírez",
    "license": "MIT",
    "homepage": "https://fastapi.tiangolo.com",
    "downloads_last_month": 15000000,
    "last_updated": "2023-11-15"
  },
  "security": {
    "has_vulnerabilities": false,
    "advisories": [],
    "security_score": 95
  },
  "recommendations": {
    "install_command": "pip install fastapi>=0.104.1",
    "is_maintained": true,
    "is_popular": true,
    "alternatives": []
  }
}
```

## Supported Ecosystems

### PyPI (Python)

```
/tool-package
Package Name: requests
Ecosystem: pypi
```

**API**: https://pypi.org/pypi/{package}/json

### NPM (JavaScript/TypeScript)

```
/tool-package
Package Name: express
Ecosystem: npm
```

**API**: https://registry.npmjs.org/{package}

### Cargo (Rust)

```
/tool-package
Package Name: serde
Ecosystem: cargo
```

**API**: https://crates.io/api/v1/crates/{package}

### Go Modules

```
/tool-package
Package Name: github.com/gin-gonic/gin
Ecosystem: go
```

**API**: https://proxy.golang.org/{package}/@latest

## Error Handling

### Package Not Found

```json
{
  "package_name": "nonexistent-package",
  "ecosystem": "pypi",
  "exists": false,
  "error": "Package not found in PyPI registry",
  "suggestions": [
    "Check package name spelling",
    "Search PyPI: https://pypi.org/search/?q=nonexistent",
    "Consider alternative packages"
  ]
}
```

### Version Not Found

```json
{
  "package_name": "fastapi",
  "ecosystem": "pypi",
  "exists": true,
  "requested_version": "99.99.99",
  "version_exists": false,
  "error": "Version 99.99.99 not found",
  "available_versions": ["0.104.1", "0.104.0", "0.103.2"],
  "latest_version": "0.104.1"
}
```

### Security Vulnerability

```json
{
  "package_name": "vulnerable-package",
  "ecosystem": "npm",
  "exists": true,
  "security": {
    "has_vulnerabilities": true,
    "advisories": [
      {
        "cve": "CVE-2023-12345",
        "severity": "high",
        "description": "Remote code execution vulnerability",
        "affected_versions": "<1.2.3",
        "patched_version": "1.2.3"
      }
    ],
    "security_score": 35
  },
  "recommendations": {
    "action": "upgrade",
    "upgrade_to": "1.2.3",
    "alternatives": ["safe-package"]
  }
}
```

## Best Practices

- Always verify packages before adding to dependencies
- Check security advisories for production packages
- Use latest stable versions when possible
- Review package popularity and maintenance
- Consider alternatives for unmaintained packages
- Save verification results to GAM

## Integration

- Used by `/skill-planning` for dependency validation
- Invoked by `/agent-critic` during QA
- Prevents hallucinated dependencies
- Ensures package availability

## Related Commands

- `/skill-planning` - Uses for dependency validation
- `/agent-critic` - Validates dependencies in plans
- `/validate-architecture` - Architecture validation

## Source

- **File**: `app/server/tools/package_tool.py`
- **Function**: `verify_package()`, `check_security()`
- **Layer**: Tools (HOW)
