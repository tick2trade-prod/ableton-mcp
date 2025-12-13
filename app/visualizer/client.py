"""Socket client for communicating with Ableton Remote Script."""

import json
import logging
import socket

logger = logging.getLogger(__name__)

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 9877


class AbletonClient:
    """Simple client to send commands to Ableton Remote Script."""

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port
        self.timeout = 2.0

    def send_command(self, command: str, params: dict | None = None) -> dict:
        """Send a command to Ableton and return response."""
        if params is None:
            params = {}

        payload = {"type": command, "params": params}

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect((self.host, self.port))

                # Send
                sock.sendall(json.dumps(payload).encode("utf-8"))

                # Receive
                response = b""
                while True:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    response += chunk

                    # Check for complete JSON
                    try:
                        # Attempt to parse. If successful, we're likely done.
                        # This assumes single response per command.
                        json.loads(response.decode("utf-8"))
                        break
                    except ValueError:
                        continue

                if not response:
                    return {"status": "error", "message": "Empty response"}

                return json.loads(response.decode("utf-8"))

        except ConnectionRefusedError:
            return {
                "status": "error",
                "message": "Ableton not connected (Connection Refused)",
            }
        except TimeoutError:
            return {"status": "error", "message": "Connection timed out"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


def send(command: str, params: dict | None = None) -> dict:
    """Helper to send one-off command."""
    client = AbletonClient()
    return client.send_command(command, params)
