"""
Antigravity Agentic Workflow (v7.0)

Multi-Gate Audit Pattern for autonomous development loops.
Implements strict separation between Planning, Auditing,
Implementation, and Verification.
"""

from google.antigravity.context import ASTContextSplitter, LocalRepoIndex
from google.antigravity.extensions import GitHub, GoogleWorkspace
from google.antigravity.sdk import Agent, Artifact, Workflow
from google.antigravity.tools import Editor, Git, MCPClient, Shell

# --- 1. CONTEXT INFRASTRUCTURE -------------------------------------------

# AST Context: "Definition" granularity reduces token usage by 40%
ast_context = ASTContextSplitter(
    language="python", granularity="definition", resolve_imports=True
)

# MCP: Local Redis for "Zero-Token" audit logs
redis_tool = MCPClient(
    server="mcp-redis",
    capabilities=["json_get", "json_set", "list_push"],
    description="Local audit trail. Logs every Critic rejection here.",
)

# MCP: UV as the standardized Package Manager
uv_tool = MCPClient(
    server="uv-python-manager",
    commands=["uv add", "uv remove", "uv run pytest", "uv run ruff"],
    description="Fast Python package manager.",
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
    """,
)

# === AGENT B: THE CRITIC (The Auditor) ===
# Operates at multiple gates (Plan, Code, Release)
critic = Agent(
    name="Critic",
    role="Principal Engineer",
    tools=[uv_tool, redis_tool, Git(commands=["diff"])],
    inputs=[
        Artifact.Types.IMPLEMENTATION_PLAN,
        Artifact.Types.CODE_DIFF,
        Artifact.Types.PR_DRAFT,
    ],
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
    """,
)

# === AGENT C: THE BUILDER (Implementation) ===
builder = Agent(
    name="Builder",
    role="Senior Engineer",
    context_providers=[
        ast_context,
        LocalRepoIndex(paths=["external/"], mode="read_only"),
    ],
    tools=[Editor(), Shell(allow_auto_run=True), uv_tool, redis_tool],
    inputs=["ApprovedBuildPlan", "CriticFeedback"],
    outputs=[Artifact.Types.CODE_DIFF],
    system_prompt="""
    Execute `ApprovedBuildPlan` via strict TDD.
    1. IF input is "Feedback": Fix code based on Critic's notes.
    2. ELSE: TDD Loop (Red -> Green -> Refactor).
       - Use `uv run pytest` to verify.
    3. FINALIZE: Generate `CodeDiff` Artifact for the Critic.
    """,
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
    """,
)

# --- 3. THE MULTI-GATE WORKFLOW ------------------------------------------


def audit_gate(artifact, stage_name):
    """Reusable logic for the Critic's 'Yes/No' loop."""
    approved = False
    attempts = 0
    feedback = ""

    while not approved and attempts < 3:
        # Critic reviews the current artifact with context
        review = critic.run(
            input=artifact, context={"stage": stage_name, "history": feedback}
        )

        if review.status == "APPROVED":
            return True, review.artifact
        else:
            feedback = review.feedback
            attempts += 1
            # Return False so the calling agent can retry
            return False, feedback

    raise Exception(f"Pipeline Halted: Critic rejected {stage_name} 3 times.")


def spec_driven_loop(user_intent: str):
    """
    Main workflow orchestration with three audit gates.

    Args:
        user_intent: High-level description of the feature to implement

    Returns:
        None (creates PR on success)
    """
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


# Register the workflow
Workflow.register("Feature: Multi-Gate Agent Loop (v7)", spec_driven_loop)
