Workflow: Full Feature Lifecycle (Orchestrator)

Phase: 3 - Feature Development
ID: 4010
Type: Master Controller

Overview

Orchestrates the entire feature development lifecycle from research to verification. This acts as a master controller calling sub-workflows sequentially.

Key Strategy: This workflow utilizes programmatic tgeminiool calling. When executing tasks, the agent must write and execute Python scripts to discover, import, and utilize existing tools/skills in the repository (e.g., in app/server/tools or app/server/skills) rather than hallucinating new implementations for solved problems.

Usage

/workflow-feature-lifecycle feature="<Feature Name>" complexity="<medium>"


Parameters

feature: The name of the feature (required)

complexity: small | medium | large (default: "medium")

strategy: tdd | prototype (default: "tdd")

dry_run: boolean (default: false)

Workflow Steps

1. Initialization & Research

Triggers: /workflow-feature-research

Scans existing codebase for conflicts.

Fetches external documentation if needed.

Output: Requirements document.

2. Architecture & Design

Triggers: /workflow-feature-design

Creates the technical specification.

Generates architecture diagrams.

Output: docs/design/<feature>.md.

3. Strategy & Decomposition

Triggers: /workflow-feature-breakdown

Breaks the design into atomic, verifiable tasks.

Estimates effort and identifies critical path.

Output: tasks.json.

4. Safety Setup

Triggers: /workflow-feature-flag-setup

Wraps the new entry points in feature flags.

Output: Feature flag configuration code.

5. Execution (Programmatic & TDD)

Triggers: /workflow-feature-implement

Discovery: Writes script to search app/server/tools for reusable components.

TDD Loop:

Write failing test (Red).

Write code to pass test (Green).

Refactor.

Tool Utilization: explicit instruction to import and call existing Python classes/tools rather than re-implementing logic.

Output: Source code changes and passing tests.

6. Verification

Triggers: /workflow-feature-verify

Runs the test suite.

Validates feature flag toggles.

Output: Verification Report.

Orchestration Logic

// Pseudo-code for Cursor Agent orchestration
async function executeFeatureLifecycle(featureName) {

    // Step 1: Research
    const research = await executeCommand(`/workflow-feature-research feature="${featureName}"`);

    // Step 2: Design
    const design = await executeCommand(`/workflow-feature-design feature="${featureName}"`);

    // Step 3: Breakdown
    // Pass the design doc path to the breakdown tool
    const breakdown = await executeCommand(`/workflow-feature-breakdown feature_description="${featureName}" context="${design.design_doc}"`);

    // Step 4: Flags
    await executeCommand(`/workflow-feature-flag-setup feature="${featureName}"`);

    // Step 5: Implement with Tool Discovery
    // Instruct agent to use programmatic tool calling
    await executeCommand(`/workflow-feature-implement plan="${breakdown.tasks}" mode="tdd" use_existing_tools=true`);

    // Step 6: Verify
    const verification = await executeCommand(`/workflow-feature-verify feature="${featureName}"`);

    if (verification.test_coverage < 90) {
        throw new Error("Test coverage insufficient. Refusing to merge.");
    }

    return "SUCCESS";
}


Output

{
  "feature": "Dark Mode Support",
  "lifecycle_duration": "4h 20m",
  "stages_completed": ["research", "design", "breakdown", "flag", "implement", "verify"],
  "artifacts": [
    "docs/design/dark-mode.md",
    "graph.json",
    "src/features/darkMode/"
  ],
  "final_status": "ready_for_merge"
}
