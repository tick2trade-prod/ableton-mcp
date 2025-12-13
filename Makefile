# Ableton MCP Makefile
# Simple commands for development and testing

# Paths
LOG_FILE := "/Users/$(USER)/Library/Preferences/Ableton/Live 12.3.1/Log.txt"
REMOTE_SCRIPT_SRC := AbletonMCP_Remote_Script

.PHONY: help install setup test test-live test-session test-clip test-device \
        test-connection check-port logs logs-mcp run run-dev lint pre-commit \
        deploy-script clean-tracks build build-clean verify install-analysis \
        check-ffmpeg test-techno test-one build-docker-local \
        install-gui run-visualizer analyze-asset

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# === Setup ===
install: ## Sync dependencies
	uv sync --all-groups --upgrade

setup: install ## Setup dev environment (install deps + hooks)
	uv run pre-commit install

# === Build & Deploy ===
deploy-script: ## Deploy Remote Script to Ableton User Library
	@echo "🚀 Deploying Remote Script via scripts/deploy.py..."
	@.venv/bin/python scripts/deploy.py

clean-tracks: ## Clear all tracks in Ableton
	@echo "🧹 Cleaning Ableton tracks (via scripts/clear_tracks.py)..."
	@.venv/bin/python scripts/clear_tracks.py

build: setup lint test verify ## Run full local build
	@echo "✅ Build passed!"

build-techno-clean: deploy-script clean-tracks test-techno ## Run techno tests with clean tracks
	@echo "✅ Techno workflow complete!"

build-techno-clean-i-o: deploy-script clean-tracks test-alchemy ## Build I/O Alchemy recreation
	@echo "✅ I/O Alchemy recreation complete!"

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
	.venv/bin/pytest tests/techno/ -v -s

test-alchemy: ## Run I/O Alchemy arrangement tests
	.venv/bin/pytest tests/techno/test_alchemy_arrangement.py -v -s

test-one: ## Run a specific test file or function (usage: make test-one TEST=test_name)
	uv run pytest tests/ -v -k "$(TEST)"

test-recreation: ## Run signal recreation tests
	.venv/bin/pytest tests/techno/test_signal_recreation.py -v -s

# === Code Quality ===
lint: ## Run pre-commit checks on all files
	uv run pre-commit run --all-files

format: ## Auto-format code
	uv run pre-commit run --all-files

# === Pre-Merge Verification ===
verify: ## Run integrity checks
	@echo "🔍 Running pre-merge verification..."
	@echo "1. Tests..."
	@uv run pytest tests/ -v --tb=short || (echo "❌ Tests failed" && exit 1)
	@echo "2. Connection check..."
	@lsof -i :9877 2>/dev/null || echo "⚠️  Ableton not connected (optional)"
	@echo "✅ All checks passed!"

# === Utils ===
check-ffmpeg: ## Check if ffmpeg is installed
	@which ffmpeg >/dev/null 2>&1 && echo "✓ ffmpeg installed" || (echo "✗ ffmpeg not found. Install with: brew install ffmpeg" && exit 1)

# === GUI & Analysis ===
install-gui: ## Install GUI dependencies
	@echo "📦 Installing GUI dependencies..."
	uv pip install ".[gui]"
	@echo "✅ GUI dependencies installed!"

run-visualizer: ## Launch audio visualizer
	@echo "🎨 Launching visualizer..."
	.venv/bin/python -m app.visualizer.main

analyze-asset: ## Analyze audio file (usage: make analyze-asset FILE=path/to/audio.wav)
	@if [ -z "$(FILE)" ]; then echo "Error: FILE argument required"; exit 1; fi
	.venv/bin/python -m src.ableton_mcp.analysis.track "$(FILE)"

analyze-stems: ## Analyze separated stems
	@echo "📊 Analyzing stems..."
	@mkdir -p assets/analysis
	@.venv/bin/python analysis/analyze_stems.py assets/audio/stems/htdemucs_ft/ALCHEMY_I_O --output assets/analysis/stem_analysis.json

separate-stems: ## Separate reference track into stems
	@echo "🔬 Separating ALCHEMY_I_O.mp3 into stems..."
	@mkdir -p assets/audio/stems
	@.venv/bin/python -m demucs --mp3 -n htdemucs_ft -o assets/audio/stems assets/audio/reference/ALCHEMY_I_O.mp3

check-port: ## Check if Ableton Remote Script is listening
	@lsof -i :9877 2>/dev/null && echo "✓ Port 9877 active" || echo "✗ Port 9877 not in use"

logs: ## Tail Ableton log file
	@tail -50 $(LOG_FILE)

logs-mcp: ## Show only AbletonMCP log entries
	@grep -i "AbletonMCP\|RemoteScriptMessage" $(LOG_FILE) | tail -30

run: ## Run MCP server (production)
	uvx ableton-mcp

run-dev: ## Run MCP server from local source
	uv run ableton-mcp
