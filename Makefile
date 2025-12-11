# Ableton MCP Makefile
# Simple commands for development and testing

# Paths
LOG_FILE := "/Users/$(USER)/Library/Preferences/Ableton/Live 12.3.1/Log.txt"
REMOTE_SCRIPT_SRC := AbletonMCP_Remote_Script
REMOTE_SCRIPT_DST := "/Users/$(USER)/Music/Ableton/User Library/Remote Scripts/AbletonMCP"

.PHONY: help install install-dev test test-live test-session test-clip test-device \
        test-connection check-port logs logs-mcp run run-dev lint pre-commit deploy-script

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'

# === Setup ===
install: ## Install dependencies
	uv sync

install-dev: ## Install with dev dependencies
	uv sync --extra dev
	uv run pre-commit install

deploy-script: ## Copy Remote Script to Ableton
	@mkdir -p $(REMOTE_SCRIPT_DST)
	cp $(REMOTE_SCRIPT_SRC)/__init__.py $(REMOTE_SCRIPT_DST)/

# === Testing ===
test: ## Run all tests
	uv run pytest tests/ -v

test-live: ## Run only live Ableton tests
	uv run pytest tests/ -v -m live

test-session: ## Run session/track tests
	uv run pytest tests/ -v -m session

test-clip: ## Run clip tests
	uv run pytest tests/ -v -m clip

test-device: ## Run device tool tests
	uv run pytest tests/test_tools.py -v -m device

test-techno: ## Run techno production test suite
	uv run pytest tests/techno/ -v -s

test-one: ## Run a specific test file or function (usage: make test-one TEST=test_name)
	uv run pytest tests/ -v -k "$(TEST)"

# === Connection ===
test-connection: ## Test socket connection to Ableton
	@echo "Testing connection to Ableton on port 9877..."
	@echo '{"type": "get_session_info", "params": {}}' | nc -w 3 localhost 9877 && echo "" || echo "Failed: Is Ableton running with AbletonMCP?"

check-port: ## Check if Ableton Remote Script is listening
	@lsof -i :9877 2>/dev/null && echo "✓ Port 9877 active" || echo "✗ Port 9877 not in use"

# === Logs ===
logs: ## Tail Ableton log file
	@tail -50 $(LOG_FILE)

logs-mcp: ## Show only AbletonMCP log entries
	@grep -i "AbletonMCP\|RemoteScriptMessage" $(LOG_FILE) | tail -30

# === Run ===
run: ## Run MCP server (production)
	uvx ableton-mcp

run-dev: ## Run MCP server from local source
	uv run ableton-mcp

# === Code Quality ===
lint: ## Run linter
	uv run ruff check .

pre-commit: ## Run pre-commit on all files
	uv run pre-commit run --all-files

# === Pre-Merge Verification ===
verify: ## Run all pre-merge checks
	@echo "🔍 Running pre-merge verification..."
	@echo "1. Pre-commit hooks..."
	@uv run pre-commit run --all-files || (echo "❌ Pre-commit failed" && exit 1)
	@echo "2. Tests..."
	@uv run pytest tests/ -v --tb=short || (echo "❌ Tests failed" && exit 1)
	@echo "3. Connection check..."
	@lsof -i :9877 2>/dev/null || echo "⚠️  Ableton not connected (optional)"
	@echo "✅ All checks passed!"

