# Op: Package Check

**Rank**: 4 - Atomic Operation Commands

## Overview

Verify package exists on PyPI/NPM.

## Usage

```
/op-package-check package="fastapi" ecosystem="pypi"
```

## Parameters

- `package`: Package name (required)
- `ecosystem`: pypi | npm (default: "pypi")
- `version`: Specific version (optional)

## Implementation

```python
from app.server.tools.package_tool import verify_package

result = await verify_package(package_name=package, ecosystem=ecosystem)
```

## Output

```json
{"exists": true, "latest_version": "0.109.0"}
```
