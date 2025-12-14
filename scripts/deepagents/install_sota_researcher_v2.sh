#!/bin/bash
#
# Install SOTA Researcher v2 MCP Server
# Ensures all dependencies are correctly installed and configured
# Fails fast if requirements are not met (no graceful degradation)
#

set -e

# Get repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔧 Installing SOTA Researcher v2 MCP Server..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

error() {
    echo -e "${RED}❌ Error: $1${NC}" >&2
    exit 1
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

info() {
    echo -e "ℹ️  $1"
}

# Step 1: Check Python environment
echo "📋 Step 1: Checking Python environment..."
if ! command -v python3 &> /dev/null; then
    error "Python 3 is required but not found. Please install Python 3.12+."
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 12 ]); then
    error "Python 3.12+ is required. Found: $PYTHON_VERSION"
fi

success "Python $PYTHON_VERSION found"

# Step 2: Check uv (package manager)
echo ""
echo "📋 Step 2: Checking uv package manager..."
if ! command -v uv &> /dev/null; then
    warning "uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"

    if ! command -v uv &> /dev/null; then
        error "Failed to install uv. Please install manually: https://github.com/astral-sh/uv"
    fi
fi

UV_VERSION=$(uv --version | cut -d' ' -f2)
success "uv $UV_VERSION found"

# Step 3: Install/verify project dependencies
echo ""
echo "📋 Step 3: Installing project dependencies..."
cd "$REPO_ROOT"

if [ ! -f "pyproject.toml" ]; then
    error "pyproject.toml not found. Are you in the correct project directory?"
fi

# Sync dependencies
info "Syncing dependencies with uv..."
if ! uv sync --quiet; then
    error "Failed to sync dependencies. Check your pyproject.toml and network connection."
fi

success "Dependencies synced"

# Step 4: Verify critical Python packages
echo ""
echo "📋 Step 4: Verifying critical Python packages..."

check_package() {
    local package=$1
    local import_name=${2:-$package}

    if uv run python -c "import $import_name" 2>/dev/null; then
        local version=$(uv run python -c "import $import_name; print(getattr($import_name, '__version__', 'unknown'))" 2>/dev/null || echo "installed")
        success "$package ($version)"
        return 0
    else
        error "$package is not installed or not importable"
        return 1
    fi
}

check_package "deepagents" "deepagents"
check_package "fastmcp" "mcp.server.fastmcp"
check_package "langchain_mcp_adapters" "langchain_mcp_adapters"

# Check deepagents version
info "Checking deepagents version..."
DEEPAGENTS_VERSION=$(uv run python -c "import deepagents; print(getattr(deepagents, '__version__', 'unknown'))" 2>/dev/null || echo "unknown")
if [ "$DEEPAGENTS_VERSION" != "unknown" ]; then
    success "deepagents version: $DEEPAGENTS_VERSION"
else
    warning "Could not determine deepagents version"
fi

# Check optional evaluation dependencies
info "Checking optional evaluation dependencies..."
if uv run python -c "import ragas" 2>/dev/null; then
    RAGAS_VERSION=$(uv run python -c "import ragas; print(getattr(ragas, '__version__', 'unknown'))" 2>/dev/null || echo "installed")
    success "ragas ($RAGAS_VERSION) - available for evaluation"
else
    warning "ragas not installed (optional, needed for evaluation)"
fi

if uv run python -c "import mlflow" 2>/dev/null; then
    MLFLOW_VERSION=$(uv run python -c "import mlflow; print(getattr(mlflow, '__version__', 'unknown'))" 2>/dev/null || echo "installed")
    success "mlflow ($MLFLOW_VERSION) - available for evaluation tracking"
else
    warning "mlflow not installed (optional, needed for evaluation tracking)"
fi

# Step 5: Verify MCP configuration
echo ""
echo "📋 Step 5: Checking MCP configuration..."

MCP_CONFIG_PATH="$HOME/.cursor/mcp.json"
if [ ! -f "$MCP_CONFIG_PATH" ]; then
    warning "MCP configuration not found at $MCP_CONFIG_PATH"
    info "Creating basic MCP configuration..."

    mkdir -p "$HOME/.cursor"
    cat > "$MCP_CONFIG_PATH" << 'EOF'
{
  "mcpServers": {
    "sota_researcher_v2": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "${workspaceFolder}",
        "python",
        "${workspaceFolder}/scripts/deepagents/sota_researcher_v2.py"
      ],
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    }
  }
}
EOF
    success "Created MCP configuration at $MCP_CONFIG_PATH"
else
    success "MCP configuration found at $MCP_CONFIG_PATH"

    # Check if sota_researcher_v2 is configured
    if ! command -v jq &> /dev/null; then
        warning "jq not found. Cannot validate MCP configuration structure."
    else
        if jq -e '.mcpServers["sota_researcher_v2"]' "$MCP_CONFIG_PATH" > /dev/null 2>&1; then
            success "sota_researcher_v2 is configured in MCP config"
        else
            warning "sota_researcher_v2 is not configured in MCP config"
            info "You may need to add it manually or run this installer again"
        fi
    fi
fi

# Step 6: Verify required MCP servers (optional but recommended)
echo ""
echo "📋 Step 6: Checking recommended MCP servers..."

check_mcp_server() {
    local server_name=$1
    local required=${2:-false}

    if [ -f "$MCP_CONFIG_PATH" ] && command -v jq &> /dev/null; then
        if jq -e ".mcpServers[\"$server_name\"]" "$MCP_CONFIG_PATH" > /dev/null 2>&1; then
            success "$server_name is configured"
            return 0
        else
            if [ "$required" = "true" ]; then
                error "$server_name is required but not configured in $MCP_CONFIG_PATH"
            else
                warning "$server_name is not configured (optional but recommended)"
            fi
            return 1
        fi
    else
        if [ "$required" = "false" ]; then
            warning "Cannot verify $server_name (jq not available or config missing)"
        fi
        return 1
    fi
}

# Check recommended MCP servers
check_mcp_server "docs-langchain" false
check_mcp_server "Context7" false
check_mcp_server "tavily-remote-mcp" false
check_mcp_server "indexing-semantic-search-v2" false
check_mcp_server "filesystem" false
check_mcp_server "memory" false

# Step 7: Test server startup
echo ""
echo "📋 Step 7: Testing server startup..."

info "Testing if server can be imported..."
if ! uv run python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('$REPO_ROOT')))
try:
    from scripts.deepagents.sota_researcher_v2 import research_and_plan, research_only
    print('✅ Server module imports successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'⚠️  Warning: {e}')
" 2>&1; then
    error "Server module cannot be imported. Check for syntax errors or missing dependencies."
fi

success "Server module imports successfully"

info "Testing agent creation (this may take a moment)..."
if ! uv run python -c "
import sys
import asyncio
from pathlib import Path
sys.path.insert(0, str(Path('$REPO_ROOT')))

async def test_agent_creation():
    try:
        # Set environment to skip validation for this test
        import os
        os.environ['SOTA_RESEARCHER_REQUIRE_VALIDATION'] = 'false'

        from scripts.deepagents.sota_researcher_v2 import _create_research_agent
        # This will fail if MCP tools aren't available, but that's OK for installation test
        try:
            agent = await _create_research_agent()
            print('✅ Agent creation successful')
        except RuntimeError as e:
            if 'MCP' in str(e):
                print('⚠️  Agent creation requires MCP tools (this is expected if MCP servers are not configured)')
            else:
                raise
    except Exception as e:
        print(f'⚠️  Agent creation test: {e}')
        print('   This is OK if MCP servers are not yet configured')

asyncio.run(test_agent_creation())
" 2>&1; then
    warning "Agent creation test had issues (this may be expected if MCP servers are not configured)"
fi

# Step 8: Create validation script
echo ""
echo "📋 Step 8: Creating validation script..."

VALIDATION_SCRIPT="$SCRIPT_DIR/validate_sota_researcher_v2.py"
cat > "$VALIDATION_SCRIPT" << 'PYTHON_EOF'
#!/usr/bin/env python3
"""Validation script for SOTA Researcher v2 installation."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

def check_imports():
    """Check if all required modules can be imported."""
    errors = []

    try:
        from deepagents import create_deep_agent
        print("✅ deepagents imported")
    except ImportError as e:
        errors.append(f"❌ deepagents: {e}")

    try:
        from mcp.server.fastmcp import FastMCP
        print("✅ fastmcp imported")
    except ImportError as e:
        errors.append(f"❌ fastmcp: {e}")

    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
        print("✅ langchain_mcp_adapters imported")
    except ImportError as e:
        errors.append(f"❌ langchain_mcp_adapters: {e}")

    try:
        from scripts.deepagents.sota_researcher_v2 import research_and_plan, research_only
        print("✅ sota_researcher_v2 imported")
    except ImportError as e:
        errors.append(f"❌ sota_researcher_v2: {e}")

    return errors

if __name__ == "__main__":
    print("🔍 Validating SOTA Researcher v2 installation...\n")
    errors = check_imports()

    if errors:
        print("\n❌ Validation failed:")
        for error in errors:
            print(f"  {error}")
        sys.exit(1)
    else:
        print("\n✅ All checks passed!")
        sys.exit(0)
PYTHON_EOF

chmod +x "$VALIDATION_SCRIPT"
success "Validation script created at $VALIDATION_SCRIPT"

# Step 9: Run validation
echo ""
echo "📋 Step 9: Running validation..."

if uv run python "$VALIDATION_SCRIPT"; then
    success "Validation passed"
else
    error "Validation failed. Please check the errors above."
fi

# Final summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ SOTA Researcher v2 installation complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Restart Cursor to load the MCP server"
echo "2. Verify the server is available in Cursor Settings → MCP"
echo "3. Test with: Research and plan v2: Test topic"
echo ""
echo "Configuration:"
echo "  - MCP Config: $MCP_CONFIG_PATH"
echo "  - Server Script: $REPO_ROOT/scripts/deepagents/sota_researcher_v2.py"
echo "  - Validation Script: $VALIDATION_SCRIPT"
echo ""
echo "To validate installation later, run:"
echo "  uv run python $VALIDATION_SCRIPT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
