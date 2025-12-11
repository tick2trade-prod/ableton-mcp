#!/bin/bash
# Safe Docker Desktop Installation Script for macOS
# This script checks if Docker is installed and installs it via Homebrew if needed

set -e  # Exit on error

echo "🐳 Docker Desktop Installation Script"
echo "======================================"
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This script is designed for macOS only"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Docker is already installed
if command_exists docker; then
    echo "✅ Docker is already installed"
    docker --version

    # Check if Docker daemon is running
    if docker info >/dev/null 2>&1; then
        echo "✅ Docker daemon is running"
        echo ""
        echo "🎉 Docker Desktop is already set up and running!"
        exit 0
    else
        echo "⚠️  Docker is installed but daemon is not running"
        echo "   Please start Docker Desktop from Applications"
        echo "   Or run: open -a Docker"
        exit 1
    fi
fi

echo "📦 Docker not found. Proceeding with installation..."
echo ""

# Check if Homebrew is installed
if ! command_exists brew; then
    echo "❌ Error: Homebrew is not installed"
    echo "   Please install Homebrew first: https://brew.sh"
    echo "   Run: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

echo "✅ Homebrew found: $(brew --version | head -n1)"
echo ""

# Update Homebrew
echo "📦 Updating Homebrew..."
brew update

# Install Docker Desktop
echo ""
echo "📥 Installing Docker Desktop..."
echo "   This may take several minutes..."
brew install --cask docker

# Wait for installation to complete
echo ""
echo "⏳ Installation complete. Starting Docker Desktop..."
open -a Docker

# Wait for Docker to start
echo "⏳ Waiting for Docker daemon to start (this may take 30-60 seconds)..."
TIMEOUT=60
ELAPSED=0

while ! docker info >/dev/null 2>&1; do
    if [ $ELAPSED -ge $TIMEOUT ]; then
        echo "⚠️  Docker daemon did not start within ${TIMEOUT} seconds"
        echo "   Please check Docker Desktop manually"
        echo "   You can run: ./scripts/doctor_docker_desktop.sh"
        exit 1
    fi

    echo -n "."
    sleep 2
    ELAPSED=$((ELAPSED + 2))
done

echo ""
echo ""
echo "🎉 Success! Docker Desktop is installed and running"
echo ""
docker --version
docker compose version
echo ""
echo "✅ Next steps:"
echo "   1. Run: docker compose up -d"
echo "   2. Verify: docker compose ps"
echo "   3. Test Redis: docker exec -it redis-stack redis-cli PING"
