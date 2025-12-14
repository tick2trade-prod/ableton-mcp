# 4000 INDEX: Workflows Registry

**Category**: Workflow Definitions
**Range**: 4000-4999

## Overview

Registry of all available workflows with IDs, descriptions, and parameters.

## Workflows

### Phase 1: Core Workflows (4001-4005)
- **4001**: `workflow-pr-create` - Create GitHub PR
- **4002**: `workflow-merge-deploy` - Merge and deploy PR
- **4003**: `workflow-code-review` - Code review process
- **4004**: `workflow-test-suite-full` - Full test suite
- **4005**: `workflow-feature-breakdown` - Break down features

### Phase 2: Bug/Hotfix Workflows (4006-4010)
- **4006**: `workflow-bug-triage` - Bug triage process
- **4007**: `workflow-quick-fix` - Quick bug fix
- **4008**: `workflow-hotfix-branch` - Hotfix branching
- **4009**: `workflow-emergency-fix` - Emergency fix
- **4010**: `workflow-emergency-deploy` - Emergency deployment

### Phase 3: Feature Development (4011-4015)
- **4011**: `workflow-feature-research` - Feature research
- **4012**: `workflow-feature-design` - Feature design
- **4013**: `workflow-api-design` - API design
- **4014**: `workflow-schema-design` - Schema design
- **4015**: `workflow-feature-flag-setup` - Feature flag setup

### Phase 4: Testing & Quality (4016-4020)
- **4016**: `workflow-integration-test` - Integration testing
- **4017**: `workflow-api-test` - API testing
- **4018**: `workflow-smoke-test` - Smoke testing
- **4019**: `workflow-load-test` - Load testing
- **4020**: `workflow-security-test` - Security testing

## Usage

```
/exec-workflow workflow_id="4001" params='{"title": "feat: add auth"}'
```
