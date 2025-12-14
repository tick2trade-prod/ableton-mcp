# Workflow: Full Feature Lifecycle

**Phase**: 3 - Feature Development
**ID**: 4010

## Overview

Orchestrates the entire feature development lifecycle from research to verification. This acts as a master controller calling sub-workflows sequentially.

## Usage

/workflow-feature-lifecycle feature="Dark Mode Support" complexity="medium"

## Parameters

- `feature`: The name of the feature (required)
- `complexity`: small | medium | large (default: "medium")
- `skip_research`: boolean (default: false)
- `dry_run`: boolean (default: false)

## Workflow Steps

### 1. Initialization & Research
*Triggers: `/workflow-feature-research`*
- Scans existing codebase for conflicts.
- Fetches external documentation if needed.
- **Output**: Requirements document.

### 2. Architecture & Design
*Triggers: `/workflow-feature-design`*
- Creates the technical specification.
- Generates architecture diagrams.
- **Output**: `docs/design/<feature>.md`.

### 3. Strategy & Decomposition
*Triggers: `/workflow-feature-breakdown`*
- Breaks the design into atomic, verifiable tasks.
- Estimates effort and identifies critical path.
- **Output**: `tasks.json`.

### 4. Safety Setup
*Triggers: `/workflow-feature-flag-setup`*
- Wraps the new entry points in feature flags.
- **Output**: Feature flag configuration code.

### 5. Execution
*Triggers: `/workflow-feature-implement`*
- Iterates through `tasks.json`.
- Implements code and tests.
- **Output**: Source code changes.

### 6. Verification
*Triggers: `/workflow-feature-verify`*
- Runs the test suite.
- Validates feature flag toggles.
- **Output**: Verification Report.

## Orchestration Logic

```javascript
// Pseudo-code for Cursor Agent orchestration
async function executeFeatureLifecycle(featureName) {

    // Step 1: Research
    const research = await executeCommand(`/workflow-feature-research feature="${featureName}"`);
    if (!research.memorized) throw new Error("Research failed");

    // Step 2: Design
    const design = await executeCommand(`/workflow-feature-design feature="${featureName}"`);

    // Step 3: Breakdown
    // Pass the design doc path to the breakdown tool
    const breakdown = await executeCommand(`/workflow-feature-breakdown feature_description="${featureName}" context="${design.design_doc}"`);

    // Step 4: Flags
    await executeCommand(`/workflow-feature-flag-setup feature="${featureName}"`);

    // Step 5: Implement
    // Loop through tasks defined in Step 3
    await executeCommand(`/workflow-feature-implement plan="${breakdown.tasks}"`);

    // Step 6: Verify
    const verification = await executeCommand(`/workflow-feature-verify feature="${featureName}"`);

    return verification.ready_for_pr ? "SUCCESS" : "FAILURE";
}
