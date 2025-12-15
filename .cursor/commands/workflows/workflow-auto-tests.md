# Workflow: Automated Test Case Generation

## Overview

Analyze feature specifications and existing code to automatically generate comprehensive test cases, improving test coverage and reliability.

## Usage

```bash
/workflow-auto-tests
```

## Parameters

- `feature_name`: Feature to test (required)
- `test_types`: unit, integration, e2e (default: all)
- `coverage_target`: Target coverage percentage (default: 80)
- `include_edge_cases`: Generate edge case tests (default: true)
- `auto_execute`: Execute tests after generation (default: true)

## Test Generation Strategy

```python
# 1. Analyze Feature
- Parse specifications
- Identify inputs/outputs
- Determine edge cases
- Review existing tests

# 2. Generate Tests
- Happy path tests
- Edge case tests
- Error handling tests
- Performance tests
- Security tests

# 3. Execute & Validate
- Run generated tests
- Measure coverage
- Identify gaps
- Iterate if needed
```

## Output

```json
{
  "tests_generated": 32,
  "unit_tests": 20,
  "integration_tests": 10,
  "e2e_tests": 2,
  "coverage_achieved": 87,
  "tests_passed": 31,
  "tests_failed": 1
}
```
