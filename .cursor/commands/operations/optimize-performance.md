# Feature: Optimize

**Rank**: 3 - Feature-Based Commands

## Overview

Performance optimization with profiling, analysis, and validation.

## Usage

```
/feature-optimize target="app/api/users.py" focus="database"
```

## Parameters

- `target`: Code to optimize (required)
- `focus`: database | cpu | memory | network (default: "all")
- `benchmark`: Run benchmarks (default: true)

## Workflow

1. Profile current performance
2. Identify bottlenecks
3. Apply optimizations
4. Run benchmarks
5. Compare before/after

## Output

```json
{
  "improvements": {
    "response_time": "-45%",
    "memory_usage": "-30%"
  }
}
```
