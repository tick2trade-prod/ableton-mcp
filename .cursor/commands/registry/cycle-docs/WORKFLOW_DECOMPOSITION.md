# 20 Software Engineering PR Workflows - Decomposed

Research-backed workflows for completing PRs in startup environments, decomposed into granular cursor commands.

**Research Summary**: 18 results memorized covering PR workflows, agile practices, GitHub best practices, and startup engineering patterns.

---

## 🎯 Workflow Categories

1. **Papercut Bugfixes** (Workflows 1-4)
2. **Feature Development** (Workflows 5-10)
3. **Large System Changes** (Workflows 11-15)
4. **Maintenance & Ops** (Workflows 16-20)

---

## 📋 20 PR Workflows

### Category 1: Papercut Bugfixes (Quick Wins)

#### Workflow 1: **Simple Bug Fix**
**Trigger**: User reports UI glitch, typo, or minor logic error

**Steps**:
1. `/workflow-bug-triage` - Reproduce bug, identify root cause
2. `/workflow-quick-fix` - Write minimal fix + test
3. `/workflow-pr-create` - Create PR with bug reference
4. `/workflow-fast-review` - Request expedited review
5. `/workflow-merge-deploy` - Merge and deploy immediately

**Commands Needed**:
- `workflow-bug-triage.md`
- `workflow-quick-fix.md`
- `workflow-pr-create.md`
- `workflow-fast-review.md`
- `workflow-merge-deploy.md`

---

#### Workflow 2: **CSS/Style Fix**
**Trigger**: Visual inconsistency or responsive design issue

**Steps**:
1. `/workflow-visual-bug-capture` - Screenshot before/after
2. `/workflow-css-fix` - Update styles with browser testing
3. `/workflow-visual-regression-test` - Run visual diff tests
4. `/workflow-pr-create` - Create PR with screenshots
5. `/workflow-design-review` - Get designer approval

**Commands Needed**:
- `workflow-visual-bug-capture.md`
- `workflow-css-fix.md`
- `workflow-visual-regression-test.md`
- `workflow-design-review.md`

---

#### Workflow 3: **Dependency Update**
**Trigger**: Security alert or outdated package

**Steps**:
1. `/workflow-dependency-audit` - Check for breaking changes
2. `/workflow-update-lockfile` - Update package versions
3. `/workflow-test-suite-full` - Run all tests
4. `/workflow-changelog-update` - Document changes
5. `/workflow-pr-create` - Create dependency update PR

**Commands Needed**:
- `workflow-dependency-audit.md`
- `workflow-update-lockfile.md`
- `workflow-test-suite-full.md`
- `workflow-changelog-update.md`

---

#### Workflow 4: **Hotfix Production Bug**
**Trigger**: Critical production issue

**Steps**:
1. `/workflow-incident-triage` - Assess severity, create incident
2. `/workflow-hotfix-branch` - Create hotfix from main/prod
3. `/workflow-emergency-fix` - Minimal fix, no refactoring
4. `/workflow-smoke-test` - Quick validation
5. `/workflow-emergency-deploy` - Deploy with rollback plan

**Commands Needed**:
- `workflow-incident-triage.md`
- `workflow-hotfix-branch.md`
- `workflow-emergency-fix.md`
- `workflow-smoke-test.md`
- `workflow-emergency-deploy.md`

---

### Category 2: Feature Development (Standard Work)

#### Workflow 5: **Small Feature (1-3 files)**
**Trigger**: Small feature request or enhancement

**Steps**:
1. `/workflow-feature-research` - Research requirements, edge cases
2. `/workflow-feature-design` - Write design doc (1-pager)
3. `/workflow-implement` - Plan → Code → Test
4. `/workflow-qa-loop` - Generate → Critique → Fix
5. `/workflow-pr-create` - Create feature PR
6. `/workflow-code-review` - Address review comments
7. `/workflow-merge-deploy` - Merge and deploy

**Commands Needed**:
- `workflow-feature-research.md`
- `workflow-feature-design.md`
- `workflow-implement.md` ✅ (from your list)
- `workflow-qa-loop.md` ✅ (from your list)
- `workflow-code-review.md`

---

#### Workflow 6: **Medium Feature (4-10 files)**
**Trigger**: Feature requiring multiple components

**Steps**:
1. `/workflow-research` - Research → Plan → Memorize ✅
2. `/workflow-feature-breakdown` - Break into subtasks
3. `/workflow-batch-code` - Parallel code generation ✅
4. `/workflow-integration-test` - Test component interactions
5. `/workflow-qa-loop` - QA feedback loop ✅
6. `/workflow-pr-create` - Create feature PR
7. `/workflow-stakeholder-demo` - Demo to stakeholders
8. `/workflow-merge-deploy` - Merge and deploy

**Commands Needed**:
- `workflow-feature-breakdown.md`
- `workflow-integration-test.md`
- `workflow-stakeholder-demo.md`

---

#### Workflow 7: **Feature with API Changes**
**Trigger**: Feature requiring new API endpoints

**Steps**:
1. `/workflow-api-design` - Design API contract (OpenAPI)
2. `/workflow-api-review` - Review with team
3. `/workflow-implement-backend` - Implement endpoints
4. `/workflow-implement-frontend` - Implement UI
5. `/workflow-api-test` - Integration + E2E tests
6. `/workflow-api-docs` - Generate API documentation
7. `/workflow-pr-create` - Create API PR
8. `/workflow-merge-deploy` - Deploy with versioning

**Commands Needed**:
- `workflow-api-design.md`
- `workflow-api-review.md`
- `workflow-implement-backend.md`
- `workflow-implement-frontend.md`
- `workflow-api-test.md`
- `workflow-api-docs.md`

---

#### Workflow 8: **Feature with Database Migration**
**Trigger**: Feature requiring schema changes

**Steps**:
1. `/workflow-schema-design` - Design schema changes
2. `/workflow-migration-create` - Generate migration scripts
3. `/workflow-migration-test` - Test up/down migrations
4. `/workflow-implement` - Implement feature code
5. `/workflow-data-migration-plan` - Plan data backfill
6. `/workflow-rollback-plan` - Document rollback procedure
7. `/workflow-pr-create` - Create migration PR
8. `/workflow-staged-deploy` - Deploy to staging first

**Commands Needed**:
- `workflow-schema-design.md`
- `workflow-migration-create.md`
- `workflow-migration-test.md`
- `workflow-data-migration-plan.md`
- `workflow-rollback-plan.md`
- `workflow-staged-deploy.md`

---

#### Workflow 9: **Feature with Feature Flag**
**Trigger**: Feature requiring gradual rollout

**Steps**:
1. `/workflow-feature-flag-setup` - Create feature flag
2. `/workflow-implement` - Implement behind flag
3. `/workflow-test-flag-on-off` - Test both states
4. `/workflow-pr-create` - Create PR (flag off by default)
5. `/workflow-merge-deploy` - Deploy to production
6. `/workflow-gradual-rollout` - Enable for % of users
7. `/workflow-monitor-metrics` - Monitor performance/errors
8. `/workflow-flag-cleanup` - Remove flag after full rollout

**Commands Needed**:
- `workflow-feature-flag-setup.md`
- `workflow-test-flag-on-off.md`
- `workflow-gradual-rollout.md`
- `workflow-monitor-metrics.md`
- `workflow-flag-cleanup.md`

---

#### Workflow 10: **A/B Test Feature**
**Trigger**: Feature requiring experimentation

**Steps**:
1. `/workflow-experiment-design` - Define hypothesis, metrics
2. `/workflow-ab-test-setup` - Configure experiment framework
3. `/workflow-implement-variants` - Implement A/B variants
4. `/workflow-analytics-integration` - Add tracking events
5. `/workflow-pr-create` - Create experiment PR
6. `/workflow-merge-deploy` - Deploy experiment
7. `/workflow-monitor-experiment` - Monitor statistical significance
8. `/workflow-experiment-conclude` - Analyze results, pick winner

**Commands Needed**:
- `workflow-experiment-design.md`
- `workflow-ab-test-setup.md`
- `workflow-implement-variants.md`
- `workflow-analytics-integration.md`
- `workflow-monitor-experiment.md`
- `workflow-experiment-conclude.md`

---

### Category 3: Large System Changes (Complex Work)

#### Workflow 11: **Major Refactoring**
**Trigger**: Technical debt or architecture improvement

**Steps**:
1. `/workflow-refactor-analysis` - Analyze current code, identify issues
2. `/workflow-refactor-plan` - Create refactoring plan
3. `/workflow-refactor-incremental` - Break into small PRs
4. `/workflow-test-coverage-increase` - Add tests before refactoring
5. `/workflow-refactor-execute` - Execute refactoring step-by-step
6. `/workflow-performance-benchmark` - Compare before/after
7. `/workflow-pr-create` - Create refactoring PR
8. `/workflow-merge-deploy` - Deploy with monitoring

**Commands Needed**:
- `workflow-refactor-analysis.md`
- `workflow-refactor-plan.md`
- `workflow-refactor-incremental.md`
- `workflow-test-coverage-increase.md`
- `workflow-refactor-execute.md`
- `workflow-performance-benchmark.md`

---

#### Workflow 12: **Service Extraction (Microservice)**
**Trigger**: Extract functionality into separate service

**Steps**:
1. `/workflow-service-boundary-design` - Define service boundaries
2. `/workflow-api-contract-design` - Design inter-service API
3. `/workflow-service-scaffold` - Scaffold new service
4. `/workflow-migrate-logic` - Move business logic
5. `/workflow-dual-write-phase` - Write to both old/new
6. `/workflow-data-migration` - Migrate existing data
7. `/workflow-cutover-plan` - Plan traffic cutover
8. `/workflow-deprecate-old-code` - Remove old implementation

**Commands Needed**:
- `workflow-service-boundary-design.md`
- `workflow-api-contract-design.md`
- `workflow-service-scaffold.md`
- `workflow-migrate-logic.md`
- `workflow-dual-write-phase.md`
- `workflow-data-migration.md`
- `workflow-cutover-plan.md`
- `workflow-deprecate-old-code.md`

---

#### Workflow 13: **Performance Optimization**
**Trigger**: Slow page load, high latency, or resource usage

**Steps**:
1. `/workflow-performance-profile` - Profile and identify bottlenecks
2. `/workflow-optimization-plan` - Plan optimization strategy
3. `/workflow-implement-optimization` - Implement fixes
4. `/workflow-load-test` - Run load tests
5. `/workflow-performance-compare` - Compare metrics before/after
6. `/workflow-pr-create` - Create optimization PR
7. `/workflow-canary-deploy` - Deploy to small % of traffic
8. `/workflow-monitor-metrics` - Monitor performance metrics

**Commands Needed**:
- `workflow-performance-profile.md`
- `workflow-optimization-plan.md`
- `workflow-implement-optimization.md`
- `workflow-load-test.md`
- `workflow-performance-compare.md`
- `workflow-canary-deploy.md`

---

#### Workflow 14: **Security Vulnerability Fix**
**Trigger**: Security scan alert or vulnerability report

**Steps**:
1. `/workflow-security-triage` - Assess severity (CVSS score)
2. `/workflow-vulnerability-research` - Research exploit vectors
3. `/workflow-security-fix` - Implement fix
4. `/workflow-security-test` - Run security tests
5. `/workflow-dependency-audit` - Check transitive dependencies
6. `/workflow-pr-create` - Create security PR (private if needed)
7. `/workflow-emergency-deploy` - Deploy ASAP
8. `/workflow-security-disclosure` - Notify affected users

**Commands Needed**:
- `workflow-security-triage.md`
- `workflow-vulnerability-research.md`
- `workflow-security-fix.md`
- `workflow-security-test.md`
- `workflow-security-disclosure.md`

---

#### Workflow 15: **Database Migration (Zero Downtime)**
**Trigger**: Large-scale schema change in production

**Steps**:
1. `/workflow-migration-strategy` - Plan multi-phase migration
2. `/workflow-backward-compatible-schema` - Add new columns (nullable)
3. `/workflow-dual-write-code` - Write to old + new columns
4. `/workflow-backfill-data` - Migrate existing data
5. `/workflow-verify-data-integrity` - Validate migration
6. `/workflow-switch-read-path` - Read from new columns
7. `/workflow-deprecate-old-schema` - Remove old columns
8. `/workflow-cleanup-migration-code` - Remove dual-write logic

**Commands Needed**:
- `workflow-migration-strategy.md`
- `workflow-backward-compatible-schema.md`
- `workflow-dual-write-code.md`
- `workflow-backfill-data.md`
- `workflow-verify-data-integrity.md`
- `workflow-switch-read-path.md`
- `workflow-cleanup-migration-code.md`

---

### Category 4: Maintenance & Operations (DevOps)

#### Workflow 16: **CI/CD Pipeline Update**
**Trigger**: Improve build/deploy pipeline

**Steps**:
1. `/workflow-pipeline-analysis` - Analyze current pipeline
2. `/workflow-pipeline-design` - Design improvements
3. `/workflow-pipeline-implement` - Update CI/CD config
4. `/workflow-pipeline-test` - Test on feature branch
5. `/workflow-pr-create` - Create pipeline PR
6. `/workflow-merge-deploy` - Merge and monitor builds

**Commands Needed**:
- `workflow-pipeline-analysis.md`
- `workflow-pipeline-design.md`
- `workflow-pipeline-implement.md`
- `workflow-pipeline-test.md`

---

#### Workflow 17: **Infrastructure as Code Update**
**Trigger**: Update Terraform, CloudFormation, or K8s config

**Steps**:
1. `/workflow-infra-plan` - Run terraform plan
2. `/workflow-infra-review` - Review resource changes
3. `/workflow-infra-test` - Test in staging environment
4. `/workflow-pr-create` - Create infrastructure PR
5. `/workflow-infra-apply` - Apply changes with approval
6. `/workflow-monitor-infrastructure` - Monitor resource health

**Commands Needed**:
- `workflow-infra-plan.md`
- `workflow-infra-review.md`
- `workflow-infra-test.md`
- `workflow-infra-apply.md`
- `workflow-monitor-infrastructure.md`

---

#### Workflow 18: **Documentation Update**
**Trigger**: Outdated docs or new feature documentation

**Steps**:
1. `/workflow-docs-audit` - Identify outdated sections
2. `/workflow-docs-write` - Write/update documentation
3. `/workflow-docs-review` - Technical writer review
4. `/workflow-docs-test` - Test code examples
5. `/workflow-pr-create` - Create docs PR
6. `/workflow-docs-publish` - Publish to docs site

**Commands Needed**:
- `workflow-docs-audit.md`
- `workflow-docs-write.md`
- `workflow-docs-review.md`
- `workflow-docs-test.md`
- `workflow-docs-publish.md`

---

#### Workflow 19: **Monitoring/Alerting Setup**
**Trigger**: Add observability for new feature

**Steps**:
1. `/workflow-metrics-design` - Define key metrics
2. `/workflow-instrumentation` - Add logging/metrics
3. `/workflow-dashboard-create` - Create monitoring dashboard
4. `/workflow-alert-rules` - Configure alert thresholds
5. `/workflow-pr-create` - Create monitoring PR
6. `/workflow-test-alerts` - Test alert firing
7. `/workflow-merge-deploy` - Deploy and verify metrics

**Commands Needed**:
- `workflow-metrics-design.md`
- `workflow-instrumentation.md`
- `workflow-dashboard-create.md`
- `workflow-alert-rules.md`
- `workflow-test-alerts.md`

---

#### Workflow 20: **Technical Debt Cleanup**
**Trigger**: Scheduled tech debt sprint

**Steps**:
1. `/workflow-tech-debt-inventory` - List all tech debt items
2. `/workflow-tech-debt-prioritize` - Prioritize by impact
3. `/workflow-tech-debt-plan` - Create cleanup plan
4. `/workflow-implement` - Implement cleanup
5. `/workflow-test-suite-full` - Ensure no regressions
6. `/workflow-pr-create` - Create cleanup PR
7. `/workflow-merge-deploy` - Deploy and monitor

**Commands Needed**:
- `workflow-tech-debt-inventory.md`
- `workflow-tech-debt-prioritize.md`
- `workflow-tech-debt-plan.md`

---

## 📊 Summary Statistics

- **Total Workflows**: 20
- **Unique Commands Needed**: 89
- **Commands Already Exist**: 5 (research, implement, qa-loop, batch-code, full-feature)
- **New Commands to Create**: 84

---

## 🎯 Command Categories

### Core Workflow Commands (5 existing)
- `workflow-research.md` ✅
- `workflow-implement.md` ✅
- `workflow-qa-loop.md` ✅
- `workflow-batch-code.md` ✅
- `workflow-full-feature.md` ✅

### Bug/Fix Commands (10)
- `workflow-bug-triage.md`
- `workflow-quick-fix.md`
- `workflow-visual-bug-capture.md`
- `workflow-css-fix.md`
- `workflow-hotfix-branch.md`
- `workflow-emergency-fix.md`
- `workflow-incident-triage.md`
- `workflow-security-triage.md`
- `workflow-security-fix.md`
- `workflow-vulnerability-research.md`

### Feature Development Commands (15)
- `workflow-feature-research.md`
- `workflow-feature-design.md`
- `workflow-feature-breakdown.md`
- `workflow-api-design.md`
- `workflow-api-review.md`
- `workflow-implement-backend.md`
- `workflow-implement-frontend.md`
- `workflow-schema-design.md`
- `workflow-feature-flag-setup.md`
- `workflow-test-flag-on-off.md`
- `workflow-experiment-design.md`
- `workflow-ab-test-setup.md`
- `workflow-implement-variants.md`
- `workflow-analytics-integration.md`
- `workflow-stakeholder-demo.md`

### Testing Commands (12)
- `workflow-test-suite-full.md`
- `workflow-smoke-test.md`
- `workflow-integration-test.md`
- `workflow-visual-regression-test.md`
- `workflow-api-test.md`
- `workflow-migration-test.md`
- `workflow-load-test.md`
- `workflow-security-test.md`
- `workflow-pipeline-test.md`
- `workflow-infra-test.md`
- `workflow-docs-test.md`
- `workflow-test-alerts.md`

### Deployment Commands (10)
- `workflow-merge-deploy.md`
- `workflow-emergency-deploy.md`
- `workflow-staged-deploy.md`
- `workflow-gradual-rollout.md`
- `workflow-canary-deploy.md`
- `workflow-monitor-metrics.md`
- `workflow-monitor-experiment.md`
- `workflow-monitor-infrastructure.md`
- `workflow-infra-apply.md`
- `workflow-docs-publish.md`

### PR/Review Commands (5)
- `workflow-pr-create.md`
- `workflow-fast-review.md`
- `workflow-code-review.md`
- `workflow-design-review.md`
- `workflow-api-review.md`

### Refactoring/Migration Commands (15)
- `workflow-refactor-analysis.md`
- `workflow-refactor-plan.md`
- `workflow-refactor-incremental.md`
- `workflow-refactor-execute.md`
- `workflow-migration-create.md`
- `workflow-migration-strategy.md`
- `workflow-data-migration-plan.md`
- `workflow-data-migration.md`
- `workflow-backfill-data.md`
- `workflow-dual-write-phase.md`
- `workflow-dual-write-code.md`
- `workflow-cutover-plan.md`
- `workflow-switch-read-path.md`
- `workflow-deprecate-old-code.md`
- `workflow-cleanup-migration-code.md`

### Architecture/Design Commands (10)
- `workflow-service-boundary-design.md`
- `workflow-api-contract-design.md`
- `workflow-service-scaffold.md`
- `workflow-migrate-logic.md`
- `workflow-backward-compatible-schema.md`
- `workflow-performance-profile.md`
- `workflow-optimization-plan.md`
- `workflow-implement-optimization.md`
- `workflow-performance-compare.md`
- `workflow-performance-benchmark.md`

### DevOps/Infrastructure Commands (10)
- `workflow-pipeline-analysis.md`
- `workflow-pipeline-design.md`
- `workflow-pipeline-implement.md`
- `workflow-infra-plan.md`
- `workflow-infra-review.md`
- `workflow-dependency-audit.md`
- `workflow-update-lockfile.md`
- `workflow-changelog-update.md`
- `workflow-rollback-plan.md`
- `workflow-verify-data-integrity.md`

### Documentation/Monitoring Commands (8)
- `workflow-docs-audit.md`
- `workflow-docs-write.md`
- `workflow-docs-review.md`
- `workflow-api-docs.md`
- `workflow-metrics-design.md`
- `workflow-instrumentation.md`
- `workflow-dashboard-create.md`
- `workflow-alert-rules.md`

### Cleanup/Maintenance Commands (4)
- `workflow-flag-cleanup.md`
- `workflow-tech-debt-inventory.md`
- `workflow-tech-debt-prioritize.md`
- `workflow-tech-debt-plan.md`

### Quality/Coverage Commands (3)
- `workflow-test-coverage-increase.md`
- `workflow-experiment-conclude.md`
- `workflow-security-disclosure.md`

---

## 🚀 Implementation Priority

### Phase 1: Core Workflows (High Priority)
1. `workflow-pr-create.md` - Used by all workflows
2. `workflow-merge-deploy.md` - Used by all workflows
3. `workflow-code-review.md` - Used by most workflows
4. `workflow-test-suite-full.md` - Used by many workflows
5. `workflow-feature-breakdown.md` - Critical for medium/large features

### Phase 2: Bug/Hotfix Workflows (High Priority)
6. `workflow-bug-triage.md`
7. `workflow-quick-fix.md`
8. `workflow-hotfix-branch.md`
9. `workflow-emergency-fix.md`
10. `workflow-emergency-deploy.md`

### Phase 3: Feature Development (Medium Priority)
11. `workflow-feature-research.md`
12. `workflow-feature-design.md`
13. `workflow-api-design.md`
14. `workflow-schema-design.md`
15. `workflow-feature-flag-setup.md`

### Phase 4: Testing & Quality (Medium Priority)
16. `workflow-integration-test.md`
17. `workflow-api-test.md`
18. `workflow-smoke-test.md`
19. `workflow-load-test.md`
20. `workflow-security-test.md`

### Phase 5: Advanced Workflows (Lower Priority)
21-84. Remaining specialized commands

---

## 📁 Recommended Directory Structure

```
.cursor/commands/app/workflows/
├── 00-core/
│   ├── workflow-pr-create.md
│   ├── workflow-merge-deploy.md
│   ├── workflow-code-review.md
│   └── workflow-test-suite-full.md
├── 01-bugs/
│   ├── workflow-bug-triage.md
│   ├── workflow-quick-fix.md
│   ├── workflow-hotfix-branch.md
│   └── workflow-emergency-fix.md
├── 02-features/
│   ├── workflow-feature-research.md
│   ├── workflow-feature-design.md
│   ├── workflow-feature-breakdown.md
│   └── workflow-api-design.md
├── 03-testing/
│   ├── workflow-integration-test.md
│   ├── workflow-api-test.md
│   └── workflow-load-test.md
├── 04-deployment/
│   ├── workflow-staged-deploy.md
│   ├── workflow-gradual-rollout.md
│   └── workflow-canary-deploy.md
├── 05-refactoring/
│   ├── workflow-refactor-analysis.md
│   ├── workflow-refactor-plan.md
│   └── workflow-refactor-execute.md
└── 06-infrastructure/
    ├── workflow-pipeline-analysis.md
    ├── workflow-infra-plan.md
    └── workflow-monitoring-setup.md
```

---

## 🎯 Next Steps

1. **Implement Phase 1** (5 core commands) - Highest ROI
2. **Implement Phase 2** (5 bug/hotfix commands) - Critical for startups
3. **Validate with real workflows** - Test on actual tickets
4. **Iterate based on usage** - Track which commands are most used
5. **Expand incrementally** - Add Phase 3-5 as needed

This decomposition provides a complete toolkit for any PR workflow in a startup environment! 🚀
