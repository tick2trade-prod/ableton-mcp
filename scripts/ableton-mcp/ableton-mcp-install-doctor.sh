#!/bin/bash
# ableton-mcp-install-doctor.sh - Validate installation

echo "=== Ableton MCP Install Doctor ==="

PASS=0
FAIL=0

# Check config exists
if [[ -f ~/.gemini/antigravity/mcp_config.json ]]; then
    echo "✅ Antigravity config exists"
    PASS=$((PASS+1))
else
    echo "❌ Antigravity config exists"
    FAIL=$((FAIL+1))
fi

# Check ableton_mcp in config
if grep -q 'ableton_mcp' ~/.gemini/antigravity/mcp_config.json 2>/dev/null; then
    echo "✅ ableton_mcp in config"
    PASS=$((PASS+1))
else
    echo "❌ ableton_mcp in config"
    FAIL=$((FAIL+1))
fi

# Check MCP_Server exists
if [[ -f /Users/alexzh/ableton-mcp/MCP_Server/server.py ]]; then
    echo "✅ MCP_Server/server.py exists"
    PASS=$((PASS+1))
else
    echo "❌ MCP_Server/server.py exists"
    FAIL=$((FAIL+1))
fi

# Check Remote Script exists
if [[ -f /Users/alexzh/ableton-mcp/AbletonMCP_Remote_Script/__init__.py ]]; then
    echo "✅ AbletonMCP Remote Script exists"
    PASS=$((PASS+1))
else
    echo "❌ AbletonMCP Remote Script exists"
    FAIL=$((FAIL+1))
fi

# Check Remote Script installed in Ableton
if [[ -d ~/Library/Preferences/Ableton/Live\ 12.3.1/User\ Remote\ Scripts/AbletonMCP ]]; then
    echo "✅ Remote Script in Ableton prefs"
    PASS=$((PASS+1))
else
    echo "❌ Remote Script in Ableton prefs"
    FAIL=$((FAIL+1))
fi

# Check uv installed
if command -v uv &>/dev/null; then
    echo "✅ uv installed"
    PASS=$((PASS+1))
else
    echo "❌ uv installed"
    FAIL=$((FAIL+1))
fi

# Check jq installed
if command -v jq &>/dev/null; then
    echo "✅ jq installed"
    PASS=$((PASS+1))
else
    echo "❌ jq installed"
    FAIL=$((FAIL+1))
fi

echo ""
echo "=== Summary: $PASS passed, $FAIL failed ==="
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
