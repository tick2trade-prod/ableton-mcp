#!/bin/bash
# Docker Desktop Diagnostic Script
# Checks Docker installation, configuration, and common issues

echo "🔍 Docker Desktop Diagnostic Tool"
echo "=================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check 1: Operating System
echo "1️⃣  Checking Operating System..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    print_status 0 "Running on macOS: $(sw_vers -productVersion)"
else
    print_status 1 "Not running on macOS (detected: $OSTYPE)"
fi
echo ""

# Check 2: Homebrew
echo "2️⃣  Checking Homebrew..."
if command -v brew >/dev/null 2>&1; then
    print_status 0 "Homebrew installed: $(brew --version | head -n1)"
else
    print_status 1 "Homebrew not found"
    echo "   Install from: https://brew.sh"
fi
echo ""

# Check 3: Docker CLI
echo "3️⃣  Checking Docker CLI..."
if command -v docker >/dev/null 2>&1; then
    print_status 0 "Docker CLI installed: $(docker --version)"
    DOCKER_INSTALLED=1
else
    print_status 1 "Docker CLI not found"
    echo "   Run: ./scripts/safe_docker_desktop_install.sh"
    DOCKER_INSTALLED=0
fi
echo ""

# Check 4: Docker Desktop Application
echo "4️⃣  Checking Docker Desktop Application..."
if [ -d "/Applications/Docker.app" ]; then
    print_status 0 "Docker Desktop app found in /Applications"
else
    print_status 1 "Docker Desktop app not found in /Applications"
fi
echo ""

# Check 5: Docker Daemon
echo "5️⃣  Checking Docker Daemon..."
if [ $DOCKER_INSTALLED -eq 1 ]; then
    if docker info >/dev/null 2>&1; then
        print_status 0 "Docker daemon is running"

        # Get daemon info
        echo "   Engine version: $(docker version --format '{{.Server.Version}}' 2>/dev/null || echo 'unknown')"
        echo "   Containers: $(docker ps -q | wc -l | tr -d ' ') running"
        echo "   Images: $(docker images -q | wc -l | tr -d ' ') total"
    else
        print_status 1 "Docker daemon is not running"
        print_warning "Try starting Docker Desktop:"
        echo "   - Open Docker Desktop from Applications"
        echo "   - Or run: open -a Docker"
        echo "   - Wait 30-60 seconds for daemon to start"
    fi
else
    print_status 1 "Cannot check daemon (Docker not installed)"
fi
echo ""

# Check 6: Docker Compose
echo "6️⃣  Checking Docker Compose..."
if command -v docker >/dev/null 2>&1; then
    if docker compose version >/dev/null 2>&1; then
        print_status 0 "Docker Compose available: $(docker compose version --short)"
    else
        print_status 1 "Docker Compose not available"
    fi
else
    print_status 1 "Cannot check Compose (Docker not installed)"
fi
echo ""

# Check 7: Docker Compose File
echo "7️⃣  Checking docker-compose.yml..."
if [ -f "docker-compose.yml" ]; then
    print_status 0 "docker-compose.yml found"

    # Validate compose file
    if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
        if docker compose config >/dev/null 2>&1; then
            print_status 0 "docker-compose.yml is valid"
        else
            print_status 1 "docker-compose.yml has syntax errors"
            echo "   Run: docker compose config"
        fi
    fi
else
    print_status 1 "docker-compose.yml not found in current directory"
fi
echo ""

# Check 8: Port Availability
echo "8️⃣  Checking Port Availability..."
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_status 1 "Port $1 is already in use"
        echo "   Process: $(lsof -Pi :$1 -sTCP:LISTEN | tail -n1 | awk '{print $1}')"
    else
        print_status 0 "Port $1 is available"
    fi
}

check_port 6379  # Redis
check_port 8001  # RedisInsight
echo ""

# Check 9: Running Containers
echo "9️⃣  Checking Running Containers..."
if [ $DOCKER_INSTALLED -eq 1 ] && docker info >/dev/null 2>&1; then
    CONTAINER_COUNT=$(docker ps -q | wc -l | tr -d ' ')
    if [ "$CONTAINER_COUNT" -gt 0 ]; then
        print_status 0 "$CONTAINER_COUNT container(s) running"
        echo ""
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    else
        print_warning "No containers running"
        echo "   Run: docker compose up -d"
    fi
else
    print_status 1 "Cannot check containers (Docker daemon not running)"
fi
echo ""

# Check 10: Disk Space
echo "🔟 Checking Disk Space..."
AVAILABLE_GB=$(df -g . | tail -1 | awk '{print $4}')
if [ "$AVAILABLE_GB" -gt 10 ]; then
    print_status 0 "Sufficient disk space: ${AVAILABLE_GB}GB available"
else
    print_warning "Low disk space: ${AVAILABLE_GB}GB available"
    echo "   Docker requires at least 10GB free space"
fi
echo ""

# Summary and Recommendations
echo "📋 Summary and Recommendations"
echo "==============================="

if [ $DOCKER_INSTALLED -eq 0 ]; then
    echo "🔧 Action Required: Install Docker Desktop"
    echo "   Run: ./scripts/safe_docker_desktop_install.sh"
elif ! docker info >/dev/null 2>&1; then
    echo "🔧 Action Required: Start Docker Desktop"
    echo "   Run: open -a Docker"
    echo "   Wait 30-60 seconds, then run this script again"
elif [ "$CONTAINER_COUNT" -eq 0 ]; then
    echo "🔧 Action Required: Start containers"
    echo "   Run: docker compose up -d"
else
    echo "✅ Docker Desktop is properly configured and running!"
    echo ""
    echo "🎯 Quick Commands:"
    echo "   View logs:     docker compose logs -f"
    echo "   Stop services: docker compose down"
    echo "   Restart:       docker compose restart"
    echo "   Test Redis:    docker exec -it redis-stack redis-cli PING"
fi
echo ""
