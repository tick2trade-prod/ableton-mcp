# Workflow: Feature Flag Setup

**Phase**: 3 - Feature Development
**ID**: 4015

## Overview

Create feature flag for gradual rollout.

## Usage

```
/workflow-feature-flag-setup feature="New checkout flow" default_state="off"
```

## Parameters

- `feature`: Feature name (required)
- `default_state`: on | off (default: "off")
- `rollout_strategy`: percentage | user_list (default: "percentage")

## Workflow Steps

1. Create feature flag config
2. Add flag checks to code
3. Configure rollout strategy
4. Document flag lifecycle
5. Set up monitoring

## Output

```json
{
  "flag_name": "new_checkout_flow",
  "default_state": "off",
  "rollout_strategy": "percentage",
  "monitoring_enabled": true
}
```
