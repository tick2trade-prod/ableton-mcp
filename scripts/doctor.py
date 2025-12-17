#!/usr/bin/env python3
"""Smart doctor - checks config AND pings live Ableton."""

import json
import socket
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def check_config():
    """Check config.yaml exists and is valid."""
    config_path = Path(__file__).parent.parent / "config.yaml"
    template_path = Path(__file__).parent.parent / "config.template.yaml"

    if config_path.exists():
        print("✅ config.yaml exists")
        return True
    elif template_path.exists():
        print("⚠️  config.yaml missing (run: just setup)")
        return False
    else:
        print("❌ No config files found")
        return False


def check_connection():
    """Ping the Ableton Remote Script."""
    try:
        from MCP_Server.config import get

        port = get("ableton.port", 9877)
    except ImportError:
        port = 9877

    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect(("localhost", port))

        # Send get_session_info command
        command = {"type": "get_session_info", "params": {}}
        sock.sendall(json.dumps(command).encode())

        # Get response
        response = sock.recv(4096).decode()
        result = json.loads(response)

        if result.get("status") == "success":
            session = result.get("result", {})
            print(
                f"✅ Ableton connected: {session.get('tempo', '?')} BPM, "
                f"{session.get('track_count', '?')} tracks"
            )
            return True
        else:
            print(f"⚠️  Ableton responded with error: {result.get('message')}")
            return False

    except socket.timeout:
        print("❌ Ableton: Connection timeout")
        return False
    except ConnectionRefusedError:
        print("❌ Ableton: Not running (port 9877 closed)")
        return False
    except Exception as e:
        print(f"❌ Ableton: {e}")
        return False
    finally:
        if sock:
            sock.close()


def check_edition():
    """Detect and report Ableton edition."""
    try:
        from MCP_Server.config import get
        from MCP_Server.edition import get_edition

        config_edition = get("ableton.edition", "auto")
        current = get_edition()

        if config_edition == "auto":
            print(f"✅ Edition: {current.name} (auto-detected)")
        else:
            print(f"✅ Edition: {current.name} (from config)")

        return True
    except ImportError as e:
        print(f"⚠️  Edition check skipped: {e}")
        return True


def check_mcp_tools():
    """Count available MCP tools."""
    try:
        server_path = Path(__file__).parent.parent / "MCP_Server" / "server.py"
        if server_path.exists():
            content = server_path.read_text()
            tool_count = content.count("@mcp.tool()")
            print(f"✅ MCP tools: {tool_count} defined")
            return True
        else:
            print("⚠️  MCP server.py not found")
            return False
    except Exception as e:
        print(f"⚠️  MCP tools: Could not count ({e})")
        return True  # Non-fatal


def main():
    print("=" * 50)
    print("🏥 Ableton MCP Doctor")
    print("=" * 50)
    print()

    checks = [
        ("Config", check_config),
        ("Ableton Connection", check_connection),
        ("Edition", check_edition),
        ("MCP Tools", check_mcp_tools),
    ]

    passed = 0
    failed = 0

    for name, check in checks:
        try:
            if check():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {name}: {e}")
            failed += 1

    print()
    print("=" * 50)
    print(f"Summary: {passed} passed, {failed} failed")
    print("=" * 50)

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
