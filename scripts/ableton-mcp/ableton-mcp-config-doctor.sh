#!/bin/bash
# ableton-mcp-config-doctor.sh - Validate MCP configuration
set -e

echo "=== Ableton MCP Config Doctor ==="

CONFIG_FILE="$HOME/.gemini/antigravity/mcp_config.json"
PASS=0
FAIL=0

check() {
    if eval "$2" &>/dev/null; then
        echo "✅ $1"
        ((PASS++))
    else
        echo "❌ $1"
        ((FAIL++))
    fi
}

# Check config file valid JSON
check "Config is valid JSON" "jq empty $CONFIG_FILE"

# Check ableton_mcp entry
check "ableton_mcp server defined" "jq -e '.mcpServers.ableton_mcp' $CONFIG_FILE"

# Check not disabled
if jq -e '.mcpServers.ableton_mcp.disabled == true' "$CONFIG_FILE" &>/dev/null; then
    echo "⚠️  ableton_mcp is disabled"
    ((FAIL++))
else
    echo "✅ ableton_mcp is enabled"
    ((PASS++))
fi

# Check command is uv
check "Command is 'uv'" "jq -e '.mcpServers.ableton_mcp.command == \"uv\"' $CONFIG_FILE"

# Check project directory in args
check "Project directory in args" "jq -e '.mcpServers.ableton_mcp.args | contains([\"--directory\"])' $CONFIG_FILE"

# Show current config
echo ""
echo "Current ableton_mcp config:"
jq '.mcpServers.ableton_mcp' "$CONFIG_FILE" 2>/dev/null || echo "(not configured)"

echo ""
echo "=== Summary: $PASS passed, $FAIL failed ==="
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
