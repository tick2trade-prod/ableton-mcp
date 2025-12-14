# Workflow: Test Suite Full

## Overview

Run complete test suite including unit tests, integration tests, E2E tests, and quality checks. Ensures code quality and prevents regressions.

## Usage

Type `/workflow-test-suite-full` before creating PR or after addressing review feedback.

## Parameters

- `test_types`: Comma-separated test types (default: "all") - Options: unit, integration, e2e, performance, security
- `coverage_threshold`: Minimum coverage % (default: 80)
- `fail_fast`: Stop on first failure (default: false)
- `parallel`: Run tests in parallel (default: true)
- `verbose`: Verbose output (default: false)
- `generate_report`: Generate HTML report (default: true)
- `update_snapshots`: Update test snapshots (default: false)

## Workflow Steps

### 1. Pre-Test Setup

```bash
# Ensure dependencies are installed
uv sync --all-groups

# Start required services (Docker)
docker-compose up -d redis postgres

# Wait for services to be ready
./scripts/wait-for-services.sh

# Set test environment variables
export TESTING=true
export DATABASE_URL=postgresql://test:test@localhost:5432/test_db
export REDIS_URL=redis://localhost:6379/0
```

### 2. Unit Tests

```bash
# Run unit tests with coverage
uv run pytest tests/unit/ \
  --cov=app \
  --cov-report=term \
  --cov-report=html \
  --cov-report=xml \
  --cov-fail-under=80 \
  -v \
  $([ "$PARALLEL" = "true" ] && echo "-n auto") \
  $([ "$FAIL_FAST" = "true" ] && echo "-x")

# Expected output:
# - All unit tests pass
# - Coverage >= 80%
# - No skipped tests (unless marked)
```

### 3. Integration Tests

```bash
# Run integration tests
uv run pytest tests/integration/ \
  -v \
  --tb=short \
  $([ "$PARALLEL" = "true" ] && echo "-n auto") \
  $([ "$FAIL_FAST" = "true" ] && echo "-x")

# Tests include:
# - Database interactions
# - Redis caching
# - External API calls (mocked)
# - Service-to-service communication
```

### 4. End-to-End Tests

```bash
# Start application in test mode
uv run uvicorn app.main:app --port 8000 &
APP_PID=$!

# Wait for app to be ready
./scripts/wait-for-http.sh http://localhost:8000/health

# Run E2E tests
uv run pytest tests/e2e/ \
  --base-url=http://localhost:8000 \
  -v \
  $([ "$FAIL_FAST" = "true" ] && echo "-x")

# Cleanup
kill $APP_PID
```

### 5. Performance Tests

```bash
# Run performance benchmarks
uv run pytest tests/performance/ \
  --benchmark-only \
  --benchmark-autosave \
  --benchmark-compare \
  -v

# Check for performance regressions
# - API response time < 200ms
# - Database query time < 50ms
# - Memory usage < 500MB
```

### 6. Security Tests

```bash
# Static security analysis
uv run bandit -r app/ -ll -f json -o security-report.json

# Dependency vulnerability scan
uv run safety check --json > safety-report.json

# OWASP ZAP scan (if E2E tests ran)
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t http://localhost:8000 \
  -r zap-report.html

# SQL injection tests
uv run pytest tests/security/test_sql_injection.py -v

# XSS tests
uv run pytest tests/security/test_xss.py -v
```

### 7. Code Quality Checks

```bash
# Linting
uv run ruff check . --output-format=json > ruff-report.json

# Type checking
uv run mypy app/ --json-report mypy-report.json

# Code complexity
uv run radon cc app/ -a -nb -j > complexity-report.json

# Code duplication
uv run pylint app/ \
  --disable=all \
  --enable=duplicate-code \
  --output-format=json > duplication-report.json
```

### 8. Generate Reports

```bash
# Combine all reports
python scripts/generate_test_report.py \
  --coverage coverage.xml \
  --security security-report.json \
  --quality ruff-report.json \
  --output test-report.html

# Upload to CI/CD artifacts
# Upload to code coverage service (e.g., Codecov)
```

### 9. Cleanup

```bash
# Stop services
docker-compose down

# Remove test artifacts
rm -rf .pytest_cache htmlcov .coverage

# Reset test database
psql -U postgres -c "DROP DATABASE IF EXISTS test_db"
```

## Example Usage

### Full Test Suite (Default)
```
/workflow-test-suite-full
test_types: all
coverage_threshold: 80
parallel: true
generate_report: true
```

### Unit Tests Only (Fast)
```
/workflow-test-suite-full
test_types: unit
parallel: true
fail_fast: true
verbose: false
```

### Pre-Merge Validation
```
/workflow-test-suite-full
test_types: unit,integration
coverage_threshold: 85
fail_fast: false
generate_report: true
```

### Security Audit
```
/workflow-test-suite-full
test_types: security
generate_report: true
```

### Performance Regression Check
```
/workflow-test-suite-full
test_types: performance
fail_fast: true
```

## Integration with Other Workflows

### Called By
- `/workflow-implement` - After code generation
- `/workflow-code-review` - During review
- `/workflow-merge-deploy` - Before merge
- `/workflow-refactor-execute` - After refactoring
- All workflows that modify code

### Calls
- `uv run pytest` - Test runner
- `docker-compose` - Service orchestration
- `uv run bandit` - Security scanning
- `uv run mypy` - Type checking
- `uv run ruff` - Linting

## Test Organization

```
tests/
├── unit/                    # Fast, isolated tests
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/             # Service integration tests
│   ├── test_database.py
│   ├── test_redis.py
│   └── test_api_integration.py
├── e2e/                     # End-to-end tests
│   ├── test_user_flows.py
│   └── test_api_endpoints.py
├── performance/             # Performance benchmarks
│   ├── test_api_performance.py
│   └── test_database_performance.py
├── security/                # Security tests
│   ├── test_sql_injection.py
│   ├── test_xss.py
│   └── test_authentication.py
└── conftest.py              # Shared fixtures
```

## Test Markers

```python
# Unit tests (fast, no external dependencies)
@pytest.mark.unit
def test_user_model():
    pass

# Integration tests (require services)
@pytest.mark.integration
def test_database_connection():
    pass

# E2E tests (full application)
@pytest.mark.e2e
def test_user_registration_flow():
    pass

# Slow tests (> 1 second)
@pytest.mark.slow
def test_large_data_processing():
    pass

# Performance tests
@pytest.mark.benchmark
def test_api_response_time():
    pass
```

## Coverage Requirements

| Component | Minimum Coverage |
|-----------|------------------|
| Models | 90% |
| Services | 85% |
| API Endpoints | 80% |
| Utils | 75% |
| Overall | 80% |

## Performance Benchmarks

| Metric | Threshold |
|--------|-----------|
| API Response Time (p95) | < 200ms |
| Database Query Time | < 50ms |
| Memory Usage | < 500MB |
| Startup Time | < 5s |

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Fast Tests**: Unit tests should run in < 1s each
3. **Fixtures**: Use pytest fixtures for setup/teardown
4. **Mocking**: Mock external services in unit tests
5. **Assertions**: Use descriptive assertion messages
6. **Coverage**: Aim for 80%+ coverage, 100% for critical paths

## Related Commands

- `/workflow-implement` - Generate code with tests
- `/workflow-code-review` - Review includes test validation
- `/workflow-merge-deploy` - Deploy after tests pass
- `/workflow-smoke-test` - Quick validation after deploy
- `/workflow-integration-test` - Integration tests only

## Output

Returns:
```json
{
  "status": "passed",
  "total_tests": 245,
  "passed": 243,
  "failed": 0,
  "skipped": 2,
  "duration_seconds": 45.3,
  "coverage_percentage": 84.5,
  "coverage_threshold": 80,
  "reports": {
    "html": "htmlcov/index.html",
    "xml": "coverage.xml",
    "json": "test-report.json"
  },
  "quality_checks": {
    "linting": "passed",
    "type_checking": "passed",
    "security": "passed",
    "complexity": "passed"
  }
}
```

## Error Handling

- **Failed tests**: Report failures with stack traces
- **Low coverage**: Fail if below threshold
- **Service unavailable**: Retry connection 3 times
- **Timeout**: Kill hanging tests after 5 minutes
- **Out of memory**: Reduce parallel workers
- **Flaky tests**: Re-run failed tests once
