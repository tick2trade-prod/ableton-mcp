# Ableton MCP Makefile
# Simple commands for development and testing

# Paths
LOG_FILE := "/Users/$(USER)/Library/Preferences/Ableton/Live 12.3.1/Log.txt"
REMOTE_SCRIPT_SRC := src/remote_script
DOCKER_IMAGE_NAME := ableton-mcp
DOCKER_TAG := latest

.PHONY: help install setup test test-live test-session test-clip test-device \
        test-connection check-port logs logs-mcp run run-dev lint pre-commit \
        deploy-script clean-tracks build build-clean verify install-analysis \
        check-ffmpeg test-techno test-one build-docker-local \
        install-gui run-visualizer analyze-asset

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# === Setup ===
install: ## Install dependencies using uv
	@echo "📦 Installing compilation dependencies..."
	@uv pip install --upgrade setuptools wheel build
	@echo "📦 Installing project dependencies..."
	@uv sync --all-extras

setup: install ## Initial setup (install deps + pre-commit)
	@echo "🔧 Setting up pre-commit hooks..."
	@uv run pre-commit install
	@echo "✅ Setup complete!"

# === Testing ===
test: ## Run all tests
	uv run pytest

test-live: ## Run tests requiring live Ableton connection
	uv run pytest -v -m live

test-session: ## Run session/track tests
	uv run pytest tests/test_tools.py -v -m session

test-clip: ## Run clip manipulation tests
	uv run pytest tests/test_tools.py -v -m clip

test-device: ## Run device/rack tests
	uv run pytest tests/test_tools.py -v -m device

test-techno: ## Run techno production test suite
	.venv/bin/pytest tests/techno/ -v -s

test-alchemy: ## Run I/O Alchemy arrangement tests
	.venv/bin/pytest tests/techno/test_alchemy_arrangement.py -v -s

test-one: ## Run a specific test file or function (usage: make test-one TEST=test_name)
	uv run pytest tests/ -v -k "$(TEST)"

# === Development ===
check-port: ## Check if Ableton Remote Script is listening
	@lsof -i :9877 2>/dev/null && echo "✓ Port 9877 active" || echo "✗ Port 9877 not in use"

logs: ## Tail Ableton Live logs
	@echo "📜 Tailing logs from: $(LOG_FILE)"
	@tail -f $(LOG_FILE)

logs-mcp: ## Filter logs for MCP specific messages
	@echo "🔍 Filtering MCP logs..."
	@tail -f $(LOG_FILE) | grep -i "MCP"

run: ## Run the MCP server
	uv run ableton-mcp

run-dev: ## Run server in development mode with reloading
	uv run uvicorn src.ableton_mcp.server:app --reload

lint: ## Run code linting
	uv run ruff check .

pre-commit: ## Run all pre-commit hooks manually
	uv run pre-commit run --all-files

# === Build & Deploy ===
deploy-script: ## Deploy Remote Script to Ableton User Library
	@echo "🚀 Deploying Remote Script via scripts/deploy.py..."
	@.venv/bin/python scripts/deploy.py

clean-tracks: ## Clear all tracks in Ableton
	@echo "🧹 Cleaning Ableton tracks (via scripts/clear_tracks.py)..."
	@.venv/bin/python scripts/clear_tracks.py

build: setup lint test verify ## Run full local build
	@echo "✅ Build passed!"

build-clean: ## Clean and rebuild techno track
	@$(MAKE) clean-tracks
	@$(MAKE) test-techno

verify: ## Verify project structure and imports
	@echo "🔍 Verifying project structure..."
	@if [ -d "MCP_Server" ]; then echo "❌ MCP_Server directory should not exist"; exit 1; fi
	@if [ -d "AbletonMCP_Remote_Script" ]; then echo "❌ AbletonMCP_Remote_Script directory should not exist"; exit 1; fi
	@if [ ! -d "src/ableton_mcp" ]; then echo "❌ src/ableton_mcp missing"; exit 1; fi
	@echo "✅ Project structure verified!"

build-docker-local: ## Build Docker image with environment args (usage: make build-docker-local OS=MACOS IDE=ANTIGRAVITY MODEL=GEMINI)
	@echo "🐳 Building Docker image..."
	docker build \
		--build-arg OS=$(or $(OS),MACOS) \
		--build-arg IDE=$(or $(IDE),ANTIGRAVITY) \
		--build-arg MODEL=$(or $(MODEL),GEMINI) \
		-t $(DOCKER_IMAGE_NAME):$(DOCKER_TAG) .
	@echo "✅ Docker image built: $(DOCKER_IMAGE_NAME):$(DOCKER_TAG)"

# === Utils ===
check-ffmpeg: ## Check if ffmpeg is installed
	@which ffmpeg >/dev/null 2>&1 && echo "✓ ffmpeg installed" || (echo "✗ ffmpeg not found. Install with: brew install ffmpeg" && exit 1)

install-analysis: ## Install audio analysis dependencies
	@echo "📦 Installing analysis dependencies..."
	uv pip install ".[analysis]"
	@echo "✅ Analysis dependencies installed!"

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
