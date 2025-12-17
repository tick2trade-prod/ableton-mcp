# Antigravity Documentation Index
# Source: https://antigravity.google

DOCS_BASE_URL = "https://antigravity.google"

# Documentation pages index
DOCS_PAGES = [
    "/docs/home",
    "/docs/get-started",
    "/docs/agent",
    "/docs/models",
    "/docs/agent-modes-settings",
    "/docs/rules-workflows",
    "/docs/task-groups",
    "/docs/browser-subagent",
    "/docs/secure-mode",
    "/docs/mcp",
    "/docs/artifacts",
    "/docs/task-list",
    "/docs/implementation-plan",
    "/docs/walkthrough",
    "/docs/screenshots",
    "/docs/browser-recordings",
    "/docs/knowledge",
    "/docs/editor",
    "/docs/tab",
    "/docs/command",
    "/docs/agent-side-panel",
    "/docs/review-changes-editor",
    "/docs/agent-manager",
    "/docs/workspaces",
    "/docs/playground",
    "/docs/inbox",
    "/docs/conversation-view",
    "/docs/browser-subagent-view",
    "/docs/panes",
    "/docs/review-changes-manager",
    "/docs/changes-sidebar",
    "/docs/terminal",
    "/docs/files",
    "/docs/browser",
    "/docs/chrome-extension",
    "/docs/allowlist-denylist",
    "/docs/separate-chrome-profile",
    "/docs/plans",
    "/docs/settings",
    "/docs/faq",
]


def get_full_url(path: str) -> str:
    """Get the full URL for a documentation page."""
    return f"{DOCS_BASE_URL}{path}"


def get_all_urls() -> list[str]:
    """Get all documentation URLs."""
    return [get_full_url(path) for path in DOCS_PAGES]
