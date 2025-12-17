#!/bin/bash
# ableton-mcp-install.sh - Install ableton_mcp to Antigravity MCP config
set -e

CONFIG_FILE="$HOME/.gemini/antigravity/mcp_config.json"
PROJECT_DIR="/Users/alexzh/ableton-mcp"

echo "=== Ableton MCP Install ==="

# Check if config file exists
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "❌ Config file not found: $CONFIG_FILE"
    exit 1
fi

# Check if already installed
if grep -q '"ableton_mcp"' "$CONFIG_FILE"; then
    echo "✅ ableton_mcp already in config"
    exit 0
fi

# Backup config
cp "$CONFIG_FILE" "$CONFIG_FILE.bak.$(date +%Y%m%d_%H%M%S)"
echo "📦 Backed up config"

# Add ableton_mcp using jq
if command -v jq &> /dev/null; then
    jq '.mcpServers.ableton_mcp = {
        "command": "uv",
        "args": ["run", "--directory", "'"$PROJECT_DIR"'", "python", "-m", "MCP_Server.server"],
        "env": {"PYTHONPATH": "'"$PROJECT_DIR"'"}
    }' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    echo "✅ Added ableton_mcp to config"
else
    echo "❌ jq not installed. Install with: brew install jq"
    echo ""
    echo "Manual addition required. Add this to $CONFIG_FILE:"
    echo '"ableton_mcp": {'
    echo '  "command": "uv",'
    echo '  "args": ["run", "--directory", "'"$PROJECT_DIR"'", "python", "-m", "MCP_Server.server"],'
    echo '  "env": {"PYTHONPATH": "'"$PROJECT_DIR"'"}'
    echo '}'
    exit 1
fi

echo ""
echo "=== Done ==="
echo "Restart Antigravity to load new MCP server"
