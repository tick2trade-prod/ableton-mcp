"""Pytest configuration and fixtures for Ableton MCP integration tests.

All tests run against a LIVE Ableton instance - no mocks.
Requires: Ableton Live running with AbletonMCP control surface enabled.
"""
import socket
import json
import pytest


# === Fixtures ===

@pytest.fixture(scope="session")
def ableton_socket():
    """Create socket connection to Ableton Remote Script."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    try:
        sock.connect(("localhost", 9877))
        yield sock
    except ConnectionRefusedError:
        pytest.skip("Ableton not running or AbletonMCP not enabled")
    finally:
        sock.close()


@pytest.fixture
def send_command(ableton_socket):
    """Fixture to send commands to Ableton and get response."""
    def _send(command_type: str, params: dict = None):
        command = {"type": command_type, "params": params or {}}
        ableton_socket.sendall(json.dumps(command).encode("utf-8"))

        # Receive response
        chunks = []
        while True:
            chunk = ableton_socket.recv(8192)
            if not chunk:
                break
            chunks.append(chunk)
            try:
                data = b"".join(chunks)
                return json.loads(data.decode("utf-8"))
            except json.JSONDecodeError:
                continue
        return None
    return _send


# === Markers ===

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "live: requires live Ableton connection")
    config.addinivalue_line("markers", "session: session/track tests")
    config.addinivalue_line("markers", "clip: clip manipulation tests")
    config.addinivalue_line("markers", "device: device/rack tests")
    config.addinivalue_line("markers", "browser: browser navigation tests")
    config.addinivalue_line("markers", "transport: playback control tests")
