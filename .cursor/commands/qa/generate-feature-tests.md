# Feature: Test

**Rank**: 3 - Feature-Based Commands

## Overview

Generate comprehensive tests for existing feature or code.

## Usage

```
/feature-test target="app/auth.py" test_types="unit,integration"
```

## Parameters

- `target`: File/feature to test (required)
- `test_types`: unit,integration,e2e (default: "unit")
- `coverage_threshold`: Minimum coverage % (default: 80)

## Workflow

1. Analyze target code
2. Identify test cases
3. Generate test files
4. Run tests
5. Report coverage

## Output

```json
{
  "tests_generated": 25,
  "coverage": "92%",
  "tests_passed": true
}
```
