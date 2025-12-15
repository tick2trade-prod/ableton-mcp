# Workflow: Load Test

**Phase**: 4 - Testing & Quality
**ID**: 4019

## Overview

Run load tests to identify performance bottlenecks.

## Usage

```
/workflow-load-test target="https://api.example.com" users=1000 duration="5m"
```

## Parameters

- `target`: Target URL (required)
- `users`: Concurrent users (default: 100)
- `duration`: Test duration (default: "5m")
- `ramp_up`: Ramp-up time (default: "1m")

## Workflow Steps

1. Configure load test
2. Ramp up users
3. Run sustained load
4. Collect metrics
5. Generate report

## Output

```json
{
  "requests_per_second": 500,
  "avg_response_time": "150ms",
  "p95_response_time": "300ms",
  "error_rate": "0.5%"
}
```
