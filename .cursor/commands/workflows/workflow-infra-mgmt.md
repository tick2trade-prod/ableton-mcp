# Workflow: Intelligent Infrastructure Management

## Overview

AI agents provision, configure, and scale cloud resources based on application demands, integrating security protocols directly into workflow.

## Usage

```bash
/workflow-infra-mgmt
```

## Parameters

- `action`: provision, scale, configure, monitor (required)
- `cloud_provider`: aws, gcp, azure (required)
- `resource_type`: compute, storage, database, network (required)
- `auto_scale`: Enable auto-scaling (default: true)
- `security_hardening`: Apply security best practices (default: true)

## Infrastructure Operations

```python
# Provisioning
- Create resources
- Configure networking
- Set up security groups
- Apply tags

# Scaling
- Monitor metrics
- Predict demand
- Scale up/down
- Cost optimization

# Configuration
- Apply best practices
- Security hardening
- Backup configuration
- Disaster recovery

# Monitoring
- Resource utilization
- Cost tracking
- Security alerts
- Performance metrics
```

## Output

```json
{
  "resources_provisioned": ["ec2-instance-1", "rds-db-1"],
  "auto_scaling_enabled": true,
  "security_score": 9.2,
  "estimated_monthly_cost": 450
}
```
