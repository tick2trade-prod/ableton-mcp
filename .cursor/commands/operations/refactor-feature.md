# Feature: Refactor

**Rank**: 3 - Feature-Based Commands

## Overview

Refactor existing code with safety checks, tests, and validation.

## Usage

```
/feature-refactor target="app/auth.py" strategy="extract_service"
```

## Parameters

- `target`: File/directory to refactor (required)
- `strategy`: Refactoring strategy (required)
- `run_tests_before`: Run tests before (default: true)
- `run_tests_after`: Run tests after (default: true)

## Strategies

- `extract_service`: Extract business logic to service
- `split_module`: Split large module into smaller ones
- `rename`: Rename variables/functions/classes
- `simplify`: Simplify complex logic

## Workflow

1. Analyze current code
2. Run tests (baseline)
3. Apply refactoring
4. Run tests (validation)
5. Compare before/after

## Output

```json
{
  "files_modified": 5,
  "tests_passed": true,
  "complexity_reduced": "25%"
}
```
