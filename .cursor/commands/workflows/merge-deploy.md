# Workflow: Merge & Deploy

## Overview

Merge approved PR and deploy to production. Handles merge strategies, deployment verification, and rollback procedures.

## Usage

Type `/workflow-merge-deploy` after PR is approved and all checks pass.

## Parameters

- `pr_number`: PR number to merge (required)
- `merge_strategy`: Merge strategy (default: "squash") - Options: squash, merge, rebase
- `deploy_environment`: Target environment (default: "production") - Options: staging, production
- `deploy_strategy`: Deployment strategy (default: "rolling") - Options: rolling, blue-green, canary
- `canary_percentage`: Percentage for canary deployment (default: 10)
- `auto_rollback`: Enable auto-rollback on errors (default: true)
- `run_smoke_tests`: Run smoke tests after deploy (default: true)
- `notify_team`: Send deployment notification (default: true)

## Workflow Steps

### 1. Pre-Merge Validation

```bash
# Check PR status
gh pr view $PR_NUMBER --json state,mergeable,reviewDecision

# Verify all checks passed
gh pr checks $PR_NUMBER --watch

# Verify approvals
gh pr view $PR_NUMBER --json reviews

# Check for merge conflicts
gh pr view $PR_NUMBER --json mergeable
```

### 2. Merge PR

```bash
# Squash merge (default)
gh pr merge $PR_NUMBER --squash --delete-branch

# Merge commit (preserves history)
gh pr merge $PR_NUMBER --merge --delete-branch

# Rebase (linear history)
gh pr merge $PR_NUMBER --rebase --delete-branch
```

### 3. Deployment Strategy

#### Rolling Deployment (Default)
```bash
# Deploy to production gradually
# - Update 25% of instances
# - Wait for health checks
# - Update next 25%
# - Repeat until 100%

kubectl rollout status deployment/app-name
kubectl rollout history deployment/app-name
```

#### Blue-Green Deployment
```bash
# Deploy to green environment
# Switch traffic from blue to green
# Keep blue as rollback target

# Deploy to green
kubectl apply -f k8s/green-deployment.yaml

# Switch traffic
kubectl patch service app-service -p '{"spec":{"selector":{"version":"green"}}}'

# Verify green is healthy
kubectl get pods -l version=green
```

#### Canary Deployment
```bash
# Deploy canary with X% traffic
# Monitor metrics
# Gradually increase traffic
# Full rollout or rollback

# Deploy canary
kubectl apply -f k8s/canary-deployment.yaml

# Route 10% traffic to canary
kubectl apply -f k8s/canary-service.yaml

# Monitor error rates, latency
# If healthy, increase to 50%, then 100%
```

### 4. Post-Deployment Verification

```bash
# Run smoke tests
uv run pytest tests/smoke/ -v

# Check deployment status
kubectl get deployments
kubectl get pods

# Verify health endpoints
curl https://api.example.com/health

# Check error rates in monitoring
# Check latency metrics
# Check resource usage
```

### 5. Rollback (if needed)

```bash
# Automatic rollback on failure
if [ "$AUTO_ROLLBACK" = "true" ]; then
  # Detect failures
  if [ $ERROR_RATE -gt 5 ]; then
    echo "Error rate exceeded threshold, rolling back..."

    # Kubernetes rollback
    kubectl rollout undo deployment/app-name

    # Verify rollback
    kubectl rollout status deployment/app-name

    # Notify team
    slack-notify "⚠️ Deployment rolled back due to high error rate"
  fi
fi
```

### 6. Notifications

```bash
# Slack notification
curl -X POST $SLACK_WEBHOOK \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "🚀 Deployed PR #123 to production",
    "attachments": [{
      "color": "good",
      "fields": [
        {"title": "PR", "value": "#123", "short": true},
        {"title": "Author", "value": "alice", "short": true},
        {"title": "Environment", "value": "production", "short": true},
        {"title": "Strategy", "value": "rolling", "short": true}
      ]
    }]
  }'
```

## Example Usage

### Standard Production Deploy
```
/workflow-merge-deploy
pr_number: 123
merge_strategy: squash
deploy_environment: production
deploy_strategy: rolling
```

### Canary Deploy with Monitoring
```
/workflow-merge-deploy
pr_number: 456
merge_strategy: squash
deploy_strategy: canary
canary_percentage: 10
auto_rollback: true
run_smoke_tests: true
```

### Staging Deploy (No Notifications)
```
/workflow-merge-deploy
pr_number: 789
deploy_environment: staging
notify_team: false
```

### Blue-Green Deploy
```
/workflow-merge-deploy
pr_number: 321
deploy_strategy: blue-green
auto_rollback: true
```

## Integration with Other Workflows

### Called By
- `/workflow-implement` - After code review
- `/workflow-quick-fix` - After bug fix approval
- `/workflow-emergency-fix` - After hotfix approval
- All workflows that complete with approved PR

### Calls
- `gh pr merge` - Merge PR
- `kubectl rollout` - Deploy to Kubernetes
- `/workflow-smoke-test` - Verify deployment
- `/workflow-monitor-metrics` - Monitor deployment health

## Deployment Strategies Comparison

| Strategy | Speed | Risk | Rollback | Use Case |
|----------|-------|------|----------|----------|
| **Rolling** | Fast | Low | Easy | Standard deploys |
| **Blue-Green** | Medium | Very Low | Instant | Critical services |
| **Canary** | Slow | Very Low | Easy | High-risk changes |

## Monitoring Checklist

After deployment, monitor:
- ✅ Error rate (should be < 1%)
- ✅ Response time (p50, p95, p99)
- ✅ CPU/Memory usage
- ✅ Database connections
- ✅ Queue depth
- ✅ Cache hit rate

## Best Practices

1. **Merge Strategy**:
   - Use `squash` for clean history
   - Use `merge` to preserve commit history
   - Use `rebase` for linear history

2. **Deployment Strategy**:
   - Use `rolling` for most deploys
   - Use `canary` for high-risk changes
   - Use `blue-green` for zero-downtime critical services

3. **Smoke Tests**:
   - Always run smoke tests after deploy
   - Include health checks, critical paths
   - Fail fast if smoke tests fail

4. **Auto-Rollback**:
   - Enable for production deploys
   - Set appropriate error thresholds
   - Monitor for 5-10 minutes post-deploy

5. **Notifications**:
   - Notify team of all production deploys
   - Include PR link, author, changes
   - Tag on-call engineer

## Related Commands

- `/workflow-pr-create` - Create PR before merge
- `/workflow-code-review` - Review before merge
- `/workflow-smoke-test` - Verify deployment
- `/workflow-monitor-metrics` - Monitor post-deploy
- `/workflow-rollback-plan` - Manual rollback procedure

## Output

Returns:
```json
{
  "merge_status": "success",
  "merge_commit": "abc123def",
  "deployment_id": "deploy-456",
  "environment": "production",
  "strategy": "rolling",
  "health_status": "healthy",
  "smoke_tests": "passed",
  "rollback_available": true,
  "deployed_at": "2025-12-04T10:30:00Z"
}
```

## Error Handling

- **Merge conflicts**: Abort and notify author
- **Failed checks**: Block merge until fixed
- **Deployment failure**: Auto-rollback if enabled
- **Smoke test failure**: Rollback immediately
- **Health check failure**: Rollback and alert on-call
