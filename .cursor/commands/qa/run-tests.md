# Op: Test Run

**Rank**: 4 - Atomic Operation Commands

## Overview

Run specific test file or test case.

## Usage

```
/op-test-run test_path="tests/test_auth.py::test_login" verbose=true
```

## Parameters

- `test_path`: Test file or case (required)
- `verbose`: Verbose output (default: false)
- `coverage`: Enable coverage (default: false)

## Implementation

```bash
uv run pytest $test_path $([ "$verbose" = "true" ] && echo "-v")
```

## Output

```json
{"tests_run": 1, "passed": 1, "duration": "0.5s"}
```
