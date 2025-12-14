# Dependency Analyzer

## Overview

Analyze project dependencies for security vulnerabilities, outdated packages, license issues, and optimization opportunities.

## Usage

Type `/dependency-analyzer` to analyze project dependencies.

## Parameters

- `action`: Action to perform (analyze, update, audit, optimize) (default: analyze)
- `severity`: Minimum severity to report (low, medium, high, critical) (default: medium)
- `auto_fix`: Automatically fix issues (default: false)
- `check_licenses`: Check license compatibility (default: true)

## Example Usage

### Full Analysis

```
/dependency-analyzer
Action: analyze
Check Licenses: true
```

### Security Audit

```
/dependency-analyzer
Action: audit
Severity: high
```

### Update Outdated Packages

```
/dependency-analyzer
Action: update
Auto Fix: true
```

### Optimize Dependencies

```
/dependency-analyzer
Action: optimize
```

## Workflow

1. **Dependency Discovery**:
   - Parse `pyproject.toml`
   - Analyze `uv.lock`
   - Identify direct vs transitive dependencies
   - Map dependency tree

2. **Security Audit**:
   - Check CVE databases
   - Scan for known vulnerabilities
   - Identify affected versions
   - Suggest safe versions

3. **Version Analysis**:
   - Check for outdated packages
   - Identify breaking changes
   - Suggest update strategy
   - Estimate update effort

4. **License Compliance**:
   - Extract license info
   - Check compatibility
   - Identify conflicts
   - Flag restrictive licenses

5. **Optimization**:
   - Find unused dependencies
   - Identify duplicates
   - Suggest lighter alternatives
   - Calculate size savings

## Analysis Report Format

```markdown
# Dependency Analysis Report

## Summary
- Total Dependencies: 47 (12 direct, 35 transitive)
- Vulnerabilities: 2 high, 1 medium
- Outdated: 8 packages
- Unused: 3 packages
- License Issues: 0

## 🚨 Security Vulnerabilities

### Critical (0)
None ✅

### High (2)

#### 1. requests (CVE-2023-32681)
**Current Version**: 2.28.0
**Fixed Version**: 2.31.0+
**Severity**: High
**Impact**: Certificate validation bypass
**Action**: Update to 2.31.0
**Command**: `uv add "requests>=2.31.0"`

#### 2. cryptography (CVE-2023-49083)
**Current Version**: 40.0.0
**Fixed Version**: 41.0.6+
**Severity**: High
**Impact**: Memory corruption
**Action**: Update to 41.0.6
**Command**: `uv add "cryptography>=41.0.6"`

### Medium (1)

#### 1. pillow (CVE-2023-44271)
**Current Version**: 9.5.0
**Fixed Version**: 10.0.1+
**Severity**: Medium
**Impact**: DoS via crafted image
**Action**: Update to 10.0.1

## 📦 Outdated Packages (8)

| Package | Current | Latest | Breaking? | Update Command |
|---------|---------|--------|-----------|----------------|
| fastapi | 0.100.0 | 0.109.0 | No | `uv add "fastapi>=0.109.0"` |
| pydantic | 2.4.0 | 2.5.3 | No | `uv add "pydantic>=2.5.3"` |
| sqlalchemy | 2.0.20 | 2.0.25 | No | `uv add "sqlalchemy>=2.0.25"` |

## 🗑️ Unused Dependencies (3)

These packages are in pyproject.toml but not imported:
- `colorama` - Remove with: `uv remove colorama`
- `python-dotenv` - Remove with: `uv remove python-dotenv`
- `requests-mock` - Move to dev: `uv remove requests-mock && uv add --dev requests-mock`

**Potential Savings**: ~15 MB, faster installs

## 📄 License Analysis

### Compatible Licenses ✅
- MIT: 35 packages
- Apache-2.0: 8 packages
- BSD-3-Clause: 4 packages

### Attention Required ⚠️
None - All licenses compatible with project (MIT)

## 🎯 Optimization Opportunities

### 1. Replace Heavy Dependencies
- `pandas` (50 MB) → Consider `polars` (5 MB) for data processing
- `pillow` (10 MB) → Consider `pillow-simd` (faster, same size)

### 2. Duplicate Functionality
- Both `requests` and `httpx` present
- Recommendation: Standardize on `httpx` (async support)

### 3. Transitive Dependency Bloat
- `boto3` pulls in 15 AWS packages
- Consider using `boto3-stubs` for type hints only

## 📊 Dependency Tree (Top Level)

```
fastapi==0.100.0
├── pydantic==2.4.0
│   └── typing-extensions==4.8.0
├── starlette==0.27.0
│   └── anyio==3.7.1
└── uvicorn==0.23.0
    └── click==8.1.7

sqlalchemy==2.0.20
├── greenlet==2.0.2
└── typing-extensions==4.8.0
```

## 🔧 Recommended Actions

1. **Immediate** (Security):
   ```bash
   uv add "requests>=2.31.0" "cryptography>=41.0.6"
   ```

2. **Short-term** (Maintenance):
   ```bash
   uv add "fastapi>=0.109.0" "pydantic>=2.5.3" "sqlalchemy>=2.0.25"
   ```

3. **Long-term** (Optimization):
   ```bash
   uv remove colorama python-dotenv
   # Consider migrating from requests to httpx
   ```

## 📈 Impact Summary

- Security: 3 vulnerabilities fixed
- Maintenance: 8 packages updated
- Size: ~15 MB saved
- Performance: Faster installs
```

## Actions

### Analyze
- Full dependency report
- Security vulnerabilities
- Outdated packages
- License compliance

### Update
- Update outdated packages
- Respect version constraints
- Test after updates
- Generate changelog

### Audit
- Security-focused scan
- CVE database check
- Vulnerability report
- Remediation steps

### Optimize
- Remove unused dependencies
- Suggest lighter alternatives
- Reduce bundle size
- Improve install speed

## Best Practices

- Run weekly security audits
- Update dependencies regularly
- Test after updates
- Review breaking changes
- Check license compatibility
- Remove unused dependencies
- Document dependency decisions

## Integration

### Pre-commit Hook
```yaml
- id: dependency-audit
  name: Dependency Security Audit
  entry: uv run python -m app.tools.dependency_analyzer --action audit
  language: system
  pass_filenames: false
```

### CI/CD Pipeline
```yaml
- name: Dependency Analysis
  run: uv run python -m app.tools.dependency_analyzer --action analyze
```

### Scheduled Job
```bash
# Weekly dependency audit
0 9 * * 1 cd /project && uv run python -m app.tools.dependency_analyzer --action audit
```

## Related Commands

- `/optimize-imports` - Optimize import statements
- `/validate-architecture` - Validate package usage
- `/qa-critic` - Review dependency patterns
