# Workflow: API Test

**Phase**: 4 - Testing & Quality
**ID**: 4017

## Overview

Run API integration and E2E tests.

## Usage

```
/workflow-api-test base_url="http://localhost:8000" test_type="integration"
```

## Parameters

- `base_url`: API base URL (required)
- `test_type`: integration | e2e (default: "integration")
- `auth_token`: Auth token for protected endpoints (optional)

## Workflow Steps

1. Start API server
2. Run API tests
3. Validate responses
4. Check performance
5. Generate report

## Output

```json
{
  "endpoints_tested": 25,
  "passed": 24,
  "avg_response_time": "120ms"
}
```
