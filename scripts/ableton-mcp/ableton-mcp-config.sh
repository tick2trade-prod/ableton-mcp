#!/bin/bash
# ableton-mcp-config.sh - Show current MCP configuration
set -e

echo "=== Ableton MCP Configuration ==="

CONFIG_FILE="$HOME/.gemini/antigravity/mcp_config.json"

echo ""
echo "Config file: $CONFIG_FILE"
echo ""

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "❌ Config file not found"
    exit 1
fi

if command -v jq &>/dev/null; then
    echo "All MCP Servers:"
    echo "----------------"
    jq -r '.mcpServers | keys[]' "$CONFIG_FILE" | while read server; do
        DISABLED=$(jq -r ".mcpServers.\"$server\".disabled // false" "$CONFIG_FILE")
        if [[ "$DISABLED" == "true" ]]; then
            echo "  ⚪ $server (disabled)"
        else
            echo "  🟢 $server"
        fi
    done

    echo ""
    echo "ableton_mcp details:"
    echo "--------------------"
    if jq -e '.mcpServers.ableton_mcp' "$CONFIG_FILE" &>/dev/null; then
        jq '.mcpServers.ableton_mcp' "$CONFIG_FILE"
    else
        echo "  (not configured)"
    fi
else
    echo "Install jq for formatted output: brew install jq"
    cat "$CONFIG_FILE"
fi

echo ""
echo "=== Done ==="
