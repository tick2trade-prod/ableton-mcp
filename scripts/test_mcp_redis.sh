#!/bin/bash
# Test Redis MCP Server Connectivity
# Spawns the mcp/redis Docker image and checks if it can connect to the local Redis Stack

echo "🧪 Testing Redis MCP Server..."
echo "=============================="

# Check if Redis Stack is running
if ! docker ps | grep -q "redis-stack"; then
    echo "❌ redis-stack container is not running"
    echo "   Run: docker compose up -d"
    exit 1
fi
echo "✅ redis-stack is running"

# Run MCP Server via Docker
# We use host.docker.internal to access the Redis Stack running on localhost ports
echo "🚀 Spawning mcp/redis container..."

# Send JSON-RPC initialize request
# We pipe this into the container which is running in interactive mode
RPC_REQUEST='{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test-script", "version": "1.0"}}, "id": 1}'

echo "📤 Sending JSON-RPC initialize request..."
echo "$RPC_REQUEST" | docker run --rm -i \
    --add-host=host.docker.internal:host-gateway \
    -e REDIS_URL=redis://host.docker.internal:6379/0 \
    -e MCP_REDIS_LOG_LEVEL=DEBUG \
    mcp/redis > /tmp/mcp_test_output 2>&1

# Check if output contains JSON-RPC response
if grep -q "jsonrpc" /tmp/mcp_test_output; then
    echo "✅ Received JSON-RPC response"
    grep "jsonrpc" /tmp/mcp_test_output | head -n 1
else
    echo "❌ No valid JSON-RPC response received"
    echo "   Container Output:"
    cat /tmp/mcp_test_output
    exit 1
fi

echo ""
echo "🎉 MCP Redis setup is verified!"
echo "   To use in your client config:"
echo "   Command: docker"
echo "   Args: run -i --rm --add-host=host.docker.internal:host-gateway -e REDIS_URL=redis://host.docker.internal:6379/0 mcp/redis"
