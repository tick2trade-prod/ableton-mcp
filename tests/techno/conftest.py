
import pytest
import socket
import json
import os
import sys
import time

# Add tests root to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from tests.config import ABLETON_HOST, ABLETON_PORT, SOCKET_TIMEOUT

@pytest.fixture(scope="session")
def client():
    """Socket client helper."""
    def _send(cmd_type: str, params: dict = None, timeout: int = SOCKET_TIMEOUT) -> dict:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect((ABLETON_HOST, ABLETON_PORT))
            cmd = {"type": cmd_type, "params": params or {}}
            sock.sendall(json.dumps(cmd).encode())
            
            response = b""
            while True:
                chunk = sock.recv(32768)
                if not chunk: break
                response += chunk
                if response.strip().endswith(b"}") and response.count(b"{") == response.count(b"}"):
                    break
            return json.loads(response.decode())
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            sock.close()
    return _send

@pytest.fixture(scope="session")
def live_session(client):
    """Ensure Ableton is connected and get session state."""
    res = client("get_session_info")
    if res.get("status") != "success":
        pytest.skip("Ableton not connected")
    return res["result"]

@pytest.fixture
def find_loadable(client):
    """Helper to find first loadable item in a path."""
    def _find(path):
        res = client("get_browser_items_at_path", {"path": path})
        if res.get("status") == "success":
            for item in res["result"]["items"]:
                if item["is_loadable"]:
                    return item["uri"]
        return None
    return _find
