# Workflow: AI-Driven Incident Management

## Overview

Summarize alerts, propose runbook steps, correlate logs/metrics, and draft status updates, reducing mean time to resolution (MTTR).

## Usage

```bash
/workflow-incident-mgmt
```

## Parameters

- `alert_id`: Alert/incident identifier (required)
- `severity`: critical, high, medium, low (required)
- `auto_mitigate`: Attempt automatic mitigation (default: false)
- `notify_oncall`: Notify on-call engineer (default: true)
- `create_postmortem`: Generate postmortem (default: true)

## Incident Response Workflow

```python
# 1. Alert Triage
- Classify severity
- Identify affected services
- Correlate with recent changes

# 2. Investigation
- Analyze logs
- Review metrics
- Check dependencies
- Identify root cause

# 3. Mitigation
- Propose runbook steps
- Execute safe mitigations
- Rollback if needed
- Monitor impact

# 4. Communication
- Draft status updates
- Notify stakeholders
- Update incident tracker

# 5. Postmortem
- Document timeline
- Identify root cause
- List action items
- Share learnings
```

## Output

```json
{
  "incident_id": "INC-2024-001",
  "severity": "critical",
  "mttr_minutes": 15,
  "root_cause": "Database connection pool exhaustion",
  "mitigation_applied": "Increased pool size",
  "postmortem_url": "..."
}
```
