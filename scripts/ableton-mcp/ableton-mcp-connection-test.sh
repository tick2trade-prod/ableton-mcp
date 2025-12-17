#!/bin/bash
# ableton-mcp-connection-test.sh - Test MCP connection to Ableton
set -e

echo "=== Ableton MCP Connection Test ==="

PORT=9877

# Check if port is listening
if lsof -i :$PORT &>/dev/null; then
    echo "✅ Port $PORT is listening"
else
    echo "❌ Port $PORT not listening"
    echo "   → Open Ableton Live with AbletonMCP Control Surface enabled"
    exit 1
fi

# Try to connect
echo "Testing socket connection..."
if echo '{"type":"get_session_info","params":{}}' | nc -w 2 localhost $PORT | grep -q "status"; then
    echo "✅ MCP responds to commands"
else
    echo "⚠️  Socket open but no valid response"
    echo "   → Check Ableton Log.txt for errors"
fi

echo ""
echo "=== Done ==="
