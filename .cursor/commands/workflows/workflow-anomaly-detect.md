# Workflow: Proactive Anomaly Detection

## Overview

Flag unusual error patterns, performance regressions, and suggest mitigations to maintain system reliability.

## Usage

```bash
/workflow-anomaly-detect
```

## Parameters

- `monitoring_window_hours`: Time window to analyze (default: 24)
- `sensitivity`: low, medium, high (default: medium)
- `auto_alert`: Send alerts on anomalies (default: true)
- `suggest_mitigations`: Propose fixes (default: true)

## Anomaly Types

```python
# Performance Anomalies
- Response time spikes
- Throughput drops
- Resource exhaustion
- Database slow queries

# Error Anomalies
- Error rate increases
- New error types
- Error pattern changes
- Exception spikes

# Security Anomalies
- Failed login attempts
- Unusual access patterns
- Data exfiltration
- Privilege escalation

# Business Anomalies
- Conversion rate drops
- User engagement changes
- Revenue anomalies
```

## Detection Methods

```python
# Statistical Analysis
- Standard deviation
- Moving averages
- Percentile analysis
- Trend detection

# Machine Learning
- Isolation forests
- Autoencoders
- LSTM networks
- Clustering

# Rule-Based
- Threshold violations
- Pattern matching
- Correlation analysis
```

## Output

```json
{
  "anomalies_detected": 3,
  "severity": {
    "critical": 1,
    "high": 1,
    "medium": 1
  },
  "anomalies": [
    {
      "type": "performance",
      "metric": "response_time",
      "baseline": 150,
      "current": 850,
      "deviation": 5.67,
      "suggested_mitigation": "Scale up web servers"
    }
  ],
  "alerts_sent": 2
}
```
