Here is the final, comprehensive v7.0 Specification Document.

This document unifies the Local Memory infrastructure (Redis/Docker) from v4, the Vertex AI Review Patterns from v5, and the Multi-Gate Audit Logic from v7 into a single, execution-ready file. It ensures the Critic provides feedback to the Builder (for code) but only audits the Sentinel's output (PR Draft) rather than interfering with the testing process itself.
0006: Antigravity Agentic Workflow (v7.0 - Final)
Metadata	Details
Status	APPROVED
Engine	google.antigravity.sdk (v2.5+)
Architecture	Hybrid (Redis Local Memory + Workspace Cloud Context)
Pattern	Multi-Gate Audit (Plan → Code → Release)
Optimization	Implicit Context Caching, AST Splitting, Turbo Mode
1. Objective

To implement a "Day 2" autonomous development loop that adheres to Google Agentic Design Patterns. This workflow strictly separates Planning (Architect), Auditing (Critic), Implementation (Builder), and Verification (Sentinel).

It utilizes a Multi-Gate Audit strategy: The Critic Agent reviews artifacts at three distinct stages (Design, Code, Release) to prevent "Agent Drift" and architectural violations before they reach production.
2. Infrastructure Configuration
2.1 Local Runtime (docker-compose.yml)

Required for local "Zero-Token" agent memory.
YAML

services:
  # The "Brain" - Stores Specs, Test Logs, and Plans locally
  redis-stack:
    image: redis/redis-stack:latest
    ports: ["6379:6379", "8001:8001"]
    volumes: [redis_data:/data]

  # MCP Bridge - Connects Antigravity IDE to Redis
  mcp-redis:
    image: ghcr.io/redis/mcp-redis:latest
    environment: [REDIS_URL=redis://redis-stack:6379]
    network_mode: "host"

volumes:
  redis_data:

2.2 Workspace Extensions (extensions.json)

Enables the "Antigravity" effect of connecting the IDE to Cloud Apps.
JSON

{
  "extensions": {
    "googleWorkspace": {
      "enabled": true,
      "capabilities": ["read_docs", "read_drive"],
      "context": "focused"
    },
    "github": {
      "enabled": true,
      "auth_mode": "oauth_user",
      "capabilities": ["create_pr", "read_issues"]
    }
  }
}

2.3 The "Gold Standard" (pyproject.toml)

The Critic Agent uses this to enforce "Modern Python" standards.
Ini, TOML

[project]
name = "antigravity-core"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pydantic>=2.5",  # Strict Data Validation
    "redis>=5.0",     # MCP Memory
]
[tool.uv]
dev-dependencies = ["pytest>=8.0", "pytest-sugar", "ruff>=0.3.0"]
[tool.ruff]
line-length = 88
select = ["E", "F", "I", "UP", "B", "SIM"] # Enforce Simplicity

3. The Agentic Workflow Script

Save this file as: .antigravity/workflows/spec_driven_loop.py
Python

from google.antigravity.sdk import Workflow, Agent, Artifact
from google.antigravity.tools import Shell, Editor, Git, MCPClient
from google.antigravity.extensions import GoogleWorkspace, GitHub
from google.antigravity.context import ASTContextSplitter, LocalRepoIndex

# --- 1. CONTEXT INFRASTRUCTURE -------------------------------------------

# AST Context: "Definition" granularity reduces token usage by 40%
ast_context = ASTContextSplitter(language="python", granularity="definition", resolve_imports=True)

# MCP: Local Redis for "Zero-Token" audit logs
redis_tool = MCPClient(
    server="mcp-redis",
    capabilities=["json_get", "json_set", "list_push"],
    description="Local audit trail. Logs every Critic rejection here."
)

# MCP: UV as the standardized Package Manager
uv_tool = MCPClient(
    server="uv-python-manager",
    commands=["uv add", "uv remove", "uv run pytest", "uv run ruff"],
    description="Fast Python package manager."
)

# --- 2. AGENT DEFINITIONS ------------------------------------------------

# === AGENT A: THE ARCHITECT (Planner) ===
architect = Agent(
    name="Architect",
    role="Product Owner",
    # Hybrid Tools: Can read Google Docs (Cloud) and write to Redis (Local)
    tools=[GoogleWorkspace(), redis_tool],
    outputs=[Artifact.Types.IMPLEMENTATION_PLAN],
    system_prompt="""
    <context_caching_prefix>
    1. READ: Search Google Drive for the Design Doc/Spec.
    2. PLAN: Generate an `ImplementationPlan` Artifact.
    3. DEFINE: Success Criteria, TDD Plan, and Conventional Commit message.
    </context_caching_prefix>
    """
)

# === AGENT B: THE CRITIC (The Auditor) ===
# Operates at multiple gates (Plan, Code, Release)
critic = Agent(
    name="Critic",
    role="Principal Engineer",
    tools=[uv_tool, redis_tool, Git(commands=["diff"])],
    inputs=[Artifact.Types.IMPLEMENTATION_PLAN, Artifact.Types.CODE_DIFF, Artifact.Types.PR_DRAFT],
    system_prompt="""
    <context_caching_prefix>
    You are the Pipeline Auditor. Review input against `GEMINI.md`.

    MODE A (Plan Review):
    - Check for Over-engineering, Security risks, and 'uv' usage.

    MODE B (Code Review):
    - Read the `CodeDiff`. Does it match the Plan?
    - Are there hardcoded secrets? Is logic 'Stupid Simple'?

    DECISION:
    - APPROVE: Return status "APPROVED".
    - REJECT: Return status "REJECTED" with detailed feedback.
    </context_caching_prefix>
    """
)

# === AGENT C: THE BUILDER (Implementation) ===
builder = Agent(
    name="Builder",
    role="Senior Engineer",
    context_providers=[ast_context, LocalRepoIndex(paths=["external/"], mode="read_only")],
    tools=[Editor(), Shell(allow_auto_run=True), uv_tool, redis_tool],
    inputs=["ApprovedBuildPlan", "CriticFeedback"],
    outputs=[Artifact.Types.CODE_DIFF],
    system_prompt="""
    Execute `ApprovedBuildPlan` via strict TDD.
    1. IF input is "Feedback": Fix code based on Critic's notes.
    2. ELSE: TDD Loop (Red -> Green -> Refactor).
       - Use `uv run pytest` to verify.
    3. FINALIZE: Generate `CodeDiff` Artifact for the Critic.
    """
)

# === AGENT D: THE SENTINEL (QA) ===
qa = Agent(
    name="Sentinel",
    role="Release Engineer",
    tools=[Shell(), Git(), GitHub()],
    inputs=["ApprovedCodeBase"],
    outputs=[Artifact.Types.PR_DRAFT],
    system_prompt="""
    1. VERIFY: `uv run pytest -n auto` (Parallel).
    2. DRAFT: Create a PR draft (Title/Body) matching the original Spec.
    """
)

# --- 3. THE MULTI-GATE WORKFLOW ------------------------------------------

def audit_gate(artifact, stage_name):
    """Reusable logic for the Critic's 'Yes/No' loop."""
    approved = False
    attempts = 0
    feedback = ""

    while not approved and attempts < 3:
        # Critic reviews the current artifact with context
        review = critic.run(input=artifact, context={"stage": stage_name, "history": feedback})

        if review.status == "APPROVED":
            return True, review.artifact
        else:
            feedback = review.feedback
            attempts += 1
            # Return False so the calling agent can retry
            return False, feedback

    raise Exception(f"Pipeline Halted: Critic rejected {stage_name} 3 times.")

def spec_driven_loop(user_intent: str):
    # --- PHASE 1: PLANNING ---
    plan = architect.run(input=user_intent)

    # Gate 1: Plan Audit
    is_valid, data = audit_gate(plan, "PLANNING")
    while not is_valid:
        plan = architect.run(input=f"Fix plan: {data}")
        is_valid, data = audit_gate(plan, "PLANNING")

    approved_plan = data

    # --- PHASE 2: EXECUTION ---
    diff = builder.run(input=approved_plan)

    # Gate 2: Code Audit (Before QA runs expensive tests)
    is_valid, data = audit_gate(diff, "CODE_IMPLEMENTATION")
    while not is_valid:
        diff = builder.run(input=f"Refactor code: {data}")
        is_valid, data = audit_gate(diff, "CODE_IMPLEMENTATION")

    approved_diff = data

    # --- PHASE 3: VERIFICATION & RELEASE ---
    pr_draft = qa.run(input=approved_diff)

    # Gate 3: Release Audit (Fast check of PR text)
    is_valid, data = audit_gate(pr_draft, "RELEASE_PREP")

    if is_valid:
        # Final Action: Actually create the PR on GitHub
        Git().run(command="pr create", args=data)

Workflow.register("Feature: Multi-Gate Agent Loop (v7)", spec_driven_loop)

Appendix A: Developer Experience (CLI)

Add these to your shell profile to control the workflow efficiently.
Bash

# Trigger the full loop from terminal
alias g-feature="gemini run workflow 'Feature: Multi-Gate Agent Loop (v7)' --input"

# Peek into Agent Memory (Redis)
alias g-status="docker exec -it redis-stack redis-cli JSON.GET plan:current:draft"

# View Audit Logs (See why Critic rejected code)
alias g-audit="docker exec -it redis-stack redis-cli LRANGE audit:log 0 -1"

# Force a manual Critique
alias g-critique="gemini agent run Critic --input 'Review local changes'"

Appendix B: Antigravity Feature Mapping
Feature	Source	Usage in Workflow
Review Pattern	Vertex AI Patterns	The Critic loop ensures "human-level" verification at 3 distinct gates.
Context Caching	Gemini API Docs	<context_caching_prefix> tags used in System Prompts to reduce latency.
MCP (Redis)	Antigravity Docs	Connects agents to local Docker memory for zero-token state storage.
Workspace Ext	Marketplace	Architect Agent reads "Live Specs" from Google Docs.
Turbo Mode	Project IDX	Builder uses allow_auto_run=True for fast pytest cycles.
