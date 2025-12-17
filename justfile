# Ableton MCP - Command Runner
# Run `just` to see all recipes

set dotenv-load := true
set export := true

# ============================================================
# SETUP
# ============================================================

# Show all recipes
default:
    @just --list

# Create config.yaml from template
setup:
    @test -f config.yaml || cp config.template.yaml config.yaml
    @echo "✅ Config created. Edit config.yaml if needed."

# Install dependencies
install:
    uv sync --all-groups --upgrade

# Full setup (deps + config + hooks)
init: install setup
    uv run pre-commit install
    @echo "✅ Project initialized!"

# ============================================================
# CI / VALIDATION
# ============================================================

# Full CI pipeline (no Ableton required)
ci: lint test doctor-quick
    @echo "✅ CI passed!"

# Full CI with live Ableton connection
ci-live: lint test doctor
    @echo "✅ CI-Live passed!"

# Quick validation
quick: doctor-quick
    @echo "✅ Quick check passed!"

# Pre-merge validation
pre-merge: lint test doctor-quick
    @echo "✅ Ready to merge!"

# ============================================================
# BUILD
# ============================================================

# Build MCP (auto-detects edition)
build:
    @echo "🔨 Building MCP..."
    @uv run python -c "from MCP_Server.server import mcp; print('✅ MCP imports OK')"

# Build for specific edition (for testing)
build-edition edition="suite":
    @echo "🔨 Building for {{edition}}..."
    ABLETON_EDITION={{edition}} uv run python -c "from MCP_Server.edition import Edition, get_edition; print(f'Edition: {get_edition().name}')"

# Deploy Remote Script to Ableton
deploy:
    @echo "🚀 Deploying Remote Script..."
    .venv/bin/python scripts/deploy.py

# ============================================================
# RUN
# ============================================================

# Run MCP server (auto-detects edition)
run:
    uv run python -m MCP_Server.server

# Run as Intro edition (for testing)
run-intro:
    ABLETON_EDITION=intro uv run python -m MCP_Server.server

# Run as Suite edition
run-suite:
    ABLETON_EDITION=suite uv run python -m MCP_Server.server

# ============================================================
# TEST
# ============================================================

# Run all tests
test:
    uv run pytest tests/ -v

# Run specific test
test-one name:
    uv run pytest tests/ -v -k "{{name}}"

# Run live Ableton tests
test-live:
    uv run pytest tests/ -v -m live

# ============================================================
# DOCTOR
# ============================================================

# Full doctor check (requires Ableton)
doctor:
    @echo "🏥 Running doctor checks..."
    @uv run python scripts/doctor.py

# Quick doctor (no Ableton needed)
doctor-quick:
    @echo "⚡ Quick doctor check..."
    @./scripts/ableton-mcp/ableton-mcp-install-doctor.sh
    @./scripts/ableton-mcp/ableton-mcp-config-doctor.sh
    @echo "✅ Quick check passed!"

# ============================================================
# MCP MANAGEMENT
# ============================================================

# Install MCP to Antigravity config
mcp-install:
    @./scripts/ableton-mcp/ableton-mcp-install.sh

# Show MCP config
mcp-config:
    @./scripts/ableton-mcp/ableton-mcp-config.sh

# List available MCP tools
mcp-tools:
    @./scripts/ableton-mcp/ableton-mcp-available-tools-doctor.sh

# Test MCP connection
mcp-test:
    @./scripts/ableton-mcp/ableton-mcp-connection-test.sh

# ============================================================
# LINT
# ============================================================

# Run linter
lint:
    uv run pre-commit run --all-files

# Format code
format:
    uv run pre-commit run --all-files

# ============================================================
# UTILS
# ============================================================

# Tail Ableton logs
logs:
    @tail -50 ~/Library/Preferences/Ableton/Live\ 12.3.1/Log.txt

# Check if Ableton port is active
check-port:
    @lsof -i :9877 2>/dev/null && echo "✓ Port 9877 active" || echo "✗ Port 9877 not in use"

# Clean tracks in Ableton
clean-tracks:
    @echo "🧹 Cleaning tracks..."
    .venv/bin/python scripts/clear_tracks.py
