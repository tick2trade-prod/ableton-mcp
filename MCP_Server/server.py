# ableton_mcp_server.py
import json
import logging
import socket
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress
from dataclasses import dataclass, field
from typing import Any

from mcp.server.fastmcp import FastMCP  # type: ignore[import-not-found]

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("AbletonMCPServer")


@dataclass
class AbletonConnection:
    host: str
    port: int
    sock: socket.socket | None = field(default=None)

    def connect(self) -> bool:
        """Connect to the Ableton Remote Script socket server"""
        if self.sock:
            return True

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            logger.info(f"Connected to Ableton at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Ableton: {e}")
            self.sock = None
            return False

    def disconnect(self):
        """Disconnect from the Ableton Remote Script"""
        if self.sock:
            try:
                self.sock.close()
            except Exception as e:
                logger.error(f"Error disconnecting from Ableton: {e}")
            finally:
                self.sock = None

    def receive_full_response(self, sock, buffer_size=8192):
        """Receive the complete response, potentially in multiple chunks"""
        chunks = []
        sock.settimeout(15.0)  # Increased timeout for operations that might take longer

        try:
            while True:
                try:
                    chunk = sock.recv(buffer_size)
                    if not chunk:
                        if not chunks:
                            raise Exception(
                                "Connection closed before receiving any data"
                            )
                        break

                    chunks.append(chunk)

                    # Check if we've received a complete JSON object
                    try:
                        data = b"".join(chunks)
                        json.loads(data.decode("utf-8"))
                        logger.info(f"Received complete response ({len(data)} bytes)")
                        return data
                    except json.JSONDecodeError:
                        # Incomplete JSON, continue receiving
                        continue
                except TimeoutError:
                    logger.warning("Socket timeout during chunked receive")
                    break
                except (ConnectionError, BrokenPipeError, ConnectionResetError) as e:
                    logger.error(f"Socket connection error during receive: {e}")
                    raise
        except Exception as e:
            logger.error(f"Error during receive: {e}")
            raise

        # If we get here, we either timed out or broke out of the loop
        if chunks:
            data = b"".join(chunks)
            logger.info(f"Returning data after receive completion ({len(data)} bytes)")
            try:
                json.loads(data.decode("utf-8"))
                return data
            except json.JSONDecodeError:
                raise Exception("Incomplete JSON response received")
        else:
            raise Exception("No data received")

    def send_command(
        self, command_type: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Send a command to Ableton and return the response"""
        if not self.sock and not self.connect():
            raise ConnectionError("Not connected to Ableton")

        command = {"type": command_type, "params": params or {}}

        # Check if this is a state-modifying command
        is_modifying_command = command_type in [
            "create_midi_track",
            "create_audio_track",
            "set_track_name",
            "create_clip",
            "add_notes_to_clip",
            "set_clip_name",
            "duplicate_clip",
            "remove_clip",
            "move_clip",
            "set_tempo",
            "fire_clip",
            "stop_clip",
            "set_device_parameter",
            "start_playback",
            "stop_playback",
            "load_instrument_or_effect",
            "load_effect_on_main",
            "set_track_volume",
            "set_master_volume",
            "create_audio_effect_rack",
            "create_rack_chain",
            "set_chain_name",
            "load_effect_to_chain",
            "get_device_parameters",
            "set_device_param",
        ]

        response_data: bytes = b""
        try:
            logger.info(f"Sending command: {command_type} with params: {params}")

            # Assert sock is not None (we checked above)
            assert self.sock is not None

            # Send the command
            self.sock.sendall(json.dumps(command).encode("utf-8"))
            logger.info("Command sent, waiting for response...")

            # For state-modifying commands, add a small delay to give Ableton time to process
            if is_modifying_command:
                import time

                time.sleep(0.1)  # 100ms delay

            # Set timeout based on command type
            timeout = 15.0 if is_modifying_command else 10.0
            self.sock.settimeout(timeout)

            # Receive the response
            response_data = self.receive_full_response(self.sock)
            logger.info(f"Received {len(response_data)} bytes of data")

            # Parse the response
            response = json.loads(response_data.decode("utf-8"))
            logger.info(f"Response parsed, status: {response.get('status', 'unknown')}")

            if response.get("status") == "error":
                logger.error(f"Ableton error: {response.get('message')}")
                raise Exception(response.get("message", "Unknown error from Ableton"))

            # For state-modifying commands, add another small delay after receiving response
            if is_modifying_command:
                import time

                time.sleep(0.1)  # 100ms delay

            return response.get("result", {})
        except TimeoutError:
            logger.error("Socket timeout while waiting for response from Ableton")
            self.sock = None
            raise Exception("Timeout waiting for Ableton response")
        except (ConnectionError, BrokenPipeError, ConnectionResetError) as e:
            logger.error(f"Socket connection error: {e}")
            self.sock = None
            raise Exception(f"Connection to Ableton lost: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response from Ableton: {e}")
            if response_data:
                logger.error(f"Raw response (first 200 bytes): {response_data[:200]}")
            self.sock = None
            raise Exception(f"Invalid response from Ableton: {e}")
        except Exception as e:
            logger.error(f"Error communicating with Ableton: {e}")
            self.sock = None
            raise Exception(f"Communication error with Ableton: {e}")


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[dict[str, Any]]:
    """Manage server startup and shutdown lifecycle"""
    try:
        logger.info("AbletonMCP server starting up")

        try:
            get_ableton_connection()
            logger.info("Successfully connected to Ableton on startup")
        except Exception as e:
            logger.warning(f"Could not connect to Ableton on startup: {e}")
            logger.warning("Make sure the Ableton Remote Script is running")

        yield {}
    finally:
        global _ableton_connection
        if _ableton_connection:
            logger.info("Disconnecting from Ableton on shutdown")
            _ableton_connection.disconnect()
            _ableton_connection = None
        logger.info("AbletonMCP server shut down")


# Create the MCP server with lifespan support
mcp = FastMCP("AbletonMCP", lifespan=server_lifespan)

# Global connection for resources
_ableton_connection = None


def get_ableton_connection():
    """Get or create a persistent Ableton connection"""
    global _ableton_connection

    if _ableton_connection is not None:
        try:
            # Test the connection with a simple ping
            # We'll try to send an empty message, which should fail if the connection is dead
            # but won't affect Ableton if it's alive
            _ableton_connection.sock.settimeout(1.0)
            _ableton_connection.sock.sendall(b"")
            return _ableton_connection
        except Exception as e:
            logger.warning(f"Existing connection is no longer valid: {e}")
            with suppress(Exception):
                _ableton_connection.disconnect()
            _ableton_connection = None

    # Connection doesn't exist or is invalid, create a new one
    if _ableton_connection is None:
        # Try to connect up to 3 times with a short delay between attempts
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                logger.info(
                    f"Connecting to Ableton (attempt {attempt}/{max_attempts})..."
                )
                _ableton_connection = AbletonConnection(host="localhost", port=9877)
                if _ableton_connection.connect():
                    logger.info("Created new persistent connection to Ableton")

                    # Validate connection with a simple command
                    try:
                        # Get session info as a test
                        _ableton_connection.send_command("get_session_info")
                        logger.info("Connection validated successfully")
                        return _ableton_connection
                    except Exception as e:
                        logger.error(f"Connection validation failed: {e}")
                        _ableton_connection.disconnect()
                        _ableton_connection = None
                        # Continue to next attempt
                else:
                    _ableton_connection = None
            except Exception as e:
                logger.error(f"Connection attempt {attempt} failed: {e}")
                if _ableton_connection:
                    _ableton_connection.disconnect()
                    _ableton_connection = None

            # Wait before trying again, but only if we have more attempts left
            if attempt < max_attempts:
                import time

                time.sleep(1.0)

        # If we get here, all connection attempts failed
        if _ableton_connection is None:
            logger.error("Failed to connect to Ableton after multiple attempts")
            raise Exception(
                "Could not connect to Ableton. Make sure the Remote Script is running."
            )

    return _ableton_connection


# Core Tool endpoints


@mcp.tool()
def get_session_info() -> str:
    """Get detailed information about the current Ableton session"""
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("get_session_info")
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.exception("Error getting session info from Ableton")
        return f"Error getting session info: {e}"


@mcp.tool()
def get_track_info(track_index: int) -> str:
    """
    Get detailed information about a specific track in Ableton.

    Parameters:
    - track_index: The index of the track to get information about
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("get_track_info", {"track_index": track_index})
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.exception("Error getting track info from Ableton")
        return f"Error getting track info: {e}"


@mcp.tool()
def create_midi_track(index: int = -1) -> str:
    """
    Create a new MIDI track in the Ableton session.

    Parameters:
    - index: The index to insert the track at (-1 = end of list)
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("create_midi_track", {"index": index})
        return f"Created new MIDI track: {result.get('name', 'unknown')}"
    except Exception as e:
        logger.exception("Error creating MIDI track")
        return f"Error creating MIDI track: {e}"


@mcp.tool()
def create_audio_track(index: int = -1) -> str:
    """
    Create a new audio track in the Ableton session.

    Parameters:
    - index: The index to insert the track at (-1 = end of list)
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("create_audio_track", {"index": index})
        return f"Created new audio track: {result.get('name', 'unknown')}"
    except Exception as e:
        logger.exception("Error creating audio track")
        return f"Error creating audio track: {e}"


@mcp.tool()
def load_audio_file(track_index: int, file_path: str, clip_slot: int = 0) -> str:
    """
    Load an audio file onto an audio track.

    Note: The file must be accessible via Ableton's browser (in User Library,
    project folder, or added to Places). For external files, add them to
    Ableton's User Library first or drag them into the project manually.

    Parameters:
    - track_index: The index of the audio track to load onto
    - file_path: Path to the audio file or browser URI (query:...)
    - clip_slot: The clip slot index to load into (default: 0)
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command(
            "load_audio_file",
            {
                "track_index": track_index,
                "file_path": file_path,
                "clip_slot": clip_slot,
            },
        )
        if result.get("loaded"):
            return (
                f"Loaded audio file '{result.get('file_name')}' on track {track_index}"
            )
        else:
            return f"Could not load audio file: {result.get('error', 'Unknown error')}. {result.get('suggestion', '')}"
    except Exception as e:
        logger.exception("Error loading audio file")
        return f"Error loading audio file: {e}"


@mcp.tool()
def get_clip_notes(track_index: int, clip_index: int) -> str:
    """
    Get all MIDI notes from a clip.

    Parameters:
    - track_index: The index of the track containing the clip
    - clip_index: The index of the clip slot containing the clip
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command(
            "get_clip_notes",
            {"track_index": track_index, "clip_index": clip_index},
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.exception("Error getting clip notes")
        return f"Error getting clip notes: {e}"


@mcp.tool()
def separate_stems(track_index: int, clip_index: int = 0) -> str:
    """
    Separate an audio clip into stems (Vocals, Drums, Bass, Others).

    IMPORTANT: Ableton 12.3's stem separation feature is not accessible via the
    Live API. This tool provides guidance for manual stem separation.

    To separate stems manually in Ableton:
    1. Select the audio clip you want to separate
    2. Go to Create menu > "Separate Stems to New Audio Tracks"
       OR right-click the clip > "Separate Stems to New Audio Tracks"
    3. Choose quality mode: High Speed or High Quality
    4. Wait for processing (may take several minutes for long tracks)
    5. Stems will appear in a new Group Track with sub-tracks for each stem

    Parameters:
    - track_index: The index of the track containing the audio clip
    - clip_index: The index of the clip slot containing the clip (default: 0)

    Returns information about the track and guidance for manual separation.
    """
    try:
        ableton = get_ableton_connection()
        # Get track info to verify it's an audio track with a clip
        result = ableton.send_command("get_track_info", {"track_index": track_index})

        track_name = result.get("name", f"Track {track_index}")
        clip_slots = result.get("clip_slots", [])

        has_clip = False
        clip_name = "Unknown"
        if clip_index < len(clip_slots):
            slot = clip_slots[clip_index]
            has_clip = slot.get("has_clip", False)
            if has_clip and slot.get("clip"):
                clip_name = slot["clip"].get("name", "Unknown")

        if not has_clip:
            return f"No clip found at track {track_index}, slot {clip_index}. Load an audio clip first."

        return f"""Stem separation guidance for '{clip_name}' on track '{track_name}':

1. In Ableton, select the clip at track {track_index}, slot {clip_index}
2. Go to Create menu > "Separate Stems to New Audio Tracks"
   OR right-click the clip > "Separate Stems to New Audio Tracks"
3. Choose quality mode:
   - High Speed: Faster processing, good for previewing
   - High Quality: Better separation quality, slower
4. Wait for processing to complete
5. A new Group Track will be created with 4 stem tracks:
   - Vocals
   - Drums
   - Bass
   - Others

After separation, the stems will be saved to:
  <Project>/Samples/Processed/Stems/

Note: Stem separation requires Ableton Live Suite and is computationally intensive.
"""
    except Exception as e:
        logger.exception("Error with stem separation")
        return f"Error: {e}"


@mcp.tool()
def delete_track(track_index: int) -> str:
    """
    Delete a track at the specified index.

    Parameters:
    - track_index: The index of the track to delete
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command("delete_track", {"track_index": track_index})
        return f"Deleted track {track_index}"
    except Exception as e:
        logger.exception("Error deleting track")
        return f"Error deleting track: {e}"


@mcp.tool()
def set_track_name(track_index: int, name: str) -> str:
    """
    Set the name of a track.

    Parameters:
    - track_index: The index of the track to rename
    - name: The new name for the track
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command(
            "set_track_name", {"track_index": track_index, "name": name}
        )
        return f"Renamed track to: {result.get('name', name)}"
    except Exception as e:
        logger.exception("Error setting track name")
        return f"Error setting track name: {e}"


@mcp.tool()
def create_clip(track_index: int, clip_index: int, length: float = 4.0) -> str:
    """
    Create a new MIDI clip in the specified track and clip slot.

    Parameters:
    - track_index: The index of the track to create the clip in
    - clip_index: The index of the clip slot to create the clip in
    - length: The length of the clip in beats (default: 4.0)
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command(
            "create_clip",
            {"track_index": track_index, "clip_index": clip_index, "length": length},
        )
        return f"Created new clip at track {track_index}, slot {clip_index} with length {length} beats"
    except Exception as e:
        logger.exception("Error creating clip")
        return f"Error creating clip: {e}"


@mcp.tool()
def add_notes_to_clip(
    track_index: int, clip_index: int, notes: list[dict[str, int | float | bool]]
) -> str:
    """
    Add MIDI notes to a clip.

    Parameters:
    - track_index: The index of the track containing the clip
    - clip_index: The index of the clip slot containing the clip
    - notes: List of note dictionaries, each with pitch, start_time, duration, velocity, and mute
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command(
            "add_notes_to_clip",
            {"track_index": track_index, "clip_index": clip_index, "notes": notes},
        )
        return f"Added {len(notes)} notes to clip at track {track_index}, slot {clip_index}"
    except Exception as e:
        logger.exception("Error adding notes to clip")
        return f"Error adding notes to clip: {e}"


@mcp.tool()
def set_clip_name(track_index: int, clip_index: int, name: str) -> str:
    """
    Set the name of a clip.

    Parameters:
    - track_index: The index of the track containing the clip
    - clip_index: The index of the clip slot containing the clip
    - name: The new name for the clip
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command(
            "set_clip_name",
            {"track_index": track_index, "clip_index": clip_index, "name": name},
        )
        return f"Renamed clip at track {track_index}, slot {clip_index} to '{name}'"
    except Exception as e:
        logger.exception("Error setting clip name")
        return f"Error setting clip name: {e}"


@mcp.tool()
def duplicate_clip(
    source_track_index: int,
    source_clip_index: int,
    dest_track_index: int,
    dest_clip_index: int,
) -> str:
    """
    Duplicate a clip from one slot to another (can be on the same or different track).

    Note: This tool only supports MIDI clips. Attempting to duplicate audio or non-MIDI clips
    will result in an error.

    Parameters:
    - source_track_index: The index of the track containing the source clip
    - source_clip_index: The index of the clip slot containing the source clip
    - dest_track_index: The index of the destination track
    - dest_clip_index: The index of the destination clip slot (must be empty)
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command(
            "duplicate_clip",
            {
                "source_track_index": source_track_index,
                "source_clip_index": source_clip_index,
                "dest_track_index": dest_track_index,
                "dest_clip_index": dest_clip_index,
            },
        )
        return f"Duplicated clip from track {source_track_index}, slot {source_clip_index} to track {dest_track_index}, slot {dest_clip_index}"
    except Exception as e:
        logger.exception("Error duplicating clip")
        return f"Error duplicating clip: {e}"


@mcp.tool()
def empty_clip_slot(track_index: int, clip_index: int) -> str:
    """
    Empty a clip slot.

    Note: This tool only supports MIDI clips. Attempting to empty audio or non-MIDI clip slots
    will result in an error.

    Parameters:
    - track_index: The index of the track containing the clip
    - clip_index: The index of the clip slot to empty
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command(
            "remove_clip", {"track_index": track_index, "clip_index": clip_index}
        )
        return f"Emptied clip slot at track {track_index}, slot {clip_index}"
    except Exception as e:
        logger.exception("Error emptying clip slot")
        return f"Error emptying clip slot: {e}"


@mcp.tool()
def relocate_clip(
    source_track_index: int,
    source_clip_index: int,
    dest_track_index: int,
    dest_clip_index: int,
) -> str:
    """
    Relocate a clip from one slot to another (can be on the same or different track).
    This duplicates the clip to the destination and empties the source.

    Note: This tool only supports MIDI clips. Attempting to relocate audio or non-MIDI clips
    will result in an error.

    Parameters:
    - source_track_index: The index of the track containing the source clip
    - source_clip_index: The index of the clip slot containing the source clip
    - dest_track_index: The index of the destination track
    - dest_clip_index: The index of the destination clip slot (must be empty)
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command(
            "move_clip",
            {
                "source_track_index": source_track_index,
                "source_clip_index": source_clip_index,
                "dest_track_index": dest_track_index,
                "dest_clip_index": dest_clip_index,
            },
        )
        return f"Relocated clip from track {source_track_index}, slot {source_clip_index} to track {dest_track_index}, slot {dest_clip_index}"
    except Exception as e:
        logger.exception("Error relocating clip")
        return f"Error relocating clip: {e}"


@mcp.tool()
def set_tempo(tempo: float) -> str:
    """
    Set the tempo of the Ableton session.

    Parameters:
    - tempo: The new tempo in BPM
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command("set_tempo", {"tempo": tempo})
        return f"Set tempo to {tempo} BPM"
    except Exception as e:
        logger.exception("Error setting tempo")
        return f"Error setting tempo: {e}"


@mcp.tool()
def set_track_volume(track_index: int, volume: float) -> str:
    """
    Set the volume of a track.

    Parameters:
    - track_index: The index of the track to adjust
    - volume: The volume level (0.0 to 1.0, where 0.85 is 0dB)
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command(
            "set_track_volume", {"track_index": track_index, "volume": volume}
        )
        return f"Set track {track_index} volume to {volume}"
    except Exception as e:
        logger.exception("Error setting track volume")
        return f"Error setting track volume: {e}"


@mcp.tool()
def set_master_volume(volume: float) -> str:
    """
    Set the volume of the master track.

    Parameters:
    - volume: The volume level (0.0 to 1.0, where 0.85 is 0dB)
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command("set_master_volume", {"volume": volume})
        return f"Set master volume to {volume}"
    except Exception as e:
        logger.exception("Error setting master volume")
        return f"Error setting master volume: {e}"


@mcp.tool()
def load_effect_on_main(uri: str) -> str:
    """
    Load an audio effect onto the main output track.

    Parameters:
    - uri: The URI of the effect to load (e.g., 'query:AudioFx#Glue%20Compressor')
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("load_effect_on_master", {"uri": uri})
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.exception("Error loading effect on main")
        return f"Error loading effect on main: {e}"


@mcp.tool()
def create_audio_effect_rack(track_index: int, device_index: int = -1) -> str:
    """
    Create an empty Audio Effect Rack on a track.

    Parameters:
    - track_index: The index of the track to add the rack to
    - device_index: Position in device chain to insert the rack (-1 = append to end)
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command(
            "create_audio_effect_rack",
            {"track_index": track_index, "device_index": device_index},
        )
        return f"Created Audio Effect Rack on track {track_index}"
    except Exception as e:
        logger.exception("Error creating audio effect rack")
        return f"Error creating audio effect rack: {e}"


@mcp.tool()
def create_rack_chain(track_index: int, device_index: int, chain_name: str = "") -> str:
    """
    Create a new chain in an Audio Effect Rack or Instrument Rack.

    Parameters:
    - track_index: The index of the track containing the rack
    - device_index: The index of the rack device on the track
    - chain_name: Optional name for the new chain
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command(
            "create_rack_chain",
            {
                "track_index": track_index,
                "device_index": device_index,
                "chain_name": chain_name,
            },
        )
        chain_idx = result.get("chain_index", "?")
        return f"Created chain '{chain_name}' (index {chain_idx}) in rack at track {track_index}, device {device_index}"
    except Exception as e:
        logger.exception("Error creating rack chain")
        return f"Error creating rack chain: {e}"


@mcp.tool()
def get_device_parameters(
    track_index: int,
    device_index: int,
    chain_index: int = -1,
    rack_device_index: int = -1,
) -> str:
    """
    Get all parameters of a device.

    Parameters:
    - track_index: The index of the track containing the device
    - device_index: The index of the device on the track, or within the chain if chain_index >= 0
    - chain_index: Optional chain index if the device is inside a rack chain (-1 = device is on track)
    - rack_device_index: The index of the rack device on the track (required when chain_index >= 0)
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command(
            "get_device_parameters",
            {
                "track_index": track_index,
                "device_index": device_index,
                "chain_index": chain_index,
                "rack_device_index": rack_device_index,
            },
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.exception("Error getting device parameters")
        return f"Error getting device parameters: {e}"


@mcp.tool()
def set_device_parameter(
    track_index: int,
    device_index: int,
    parameter_name: str,
    value: float,
    chain_index: int = -1,
    rack_device_index: int = -1,
) -> str:
    """
    Set a parameter value on a device.

    Parameters:
    - track_index: The index of the track containing the device
    - device_index: The index of the device on the track, or within the chain if chain_index >= 0
    - parameter_name: The name of the parameter to set
    - value: The value to set (normalized 0.0-1.0 for most parameters)
    - chain_index: Optional chain index if the device is inside a rack chain (-1 = device is on track)
    - rack_device_index: The index of the rack device on the track (required when chain_index >= 0)
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command(
            "set_device_param",
            {
                "track_index": track_index,
                "device_index": device_index,
                "parameter_name": parameter_name,
                "value": value,
                "chain_index": chain_index,
                "rack_device_index": rack_device_index,
            },
        )
        return f"Set '{parameter_name}' to {value} on device {device_index}"
    except Exception as e:
        logger.exception("Error setting device parameter")
        return f"Error setting device parameter: {e}"


@mcp.tool()
def load_effect_to_chain(
    track_index: int, rack_device_index: int, chain_index: int, effect_uri: str
) -> str:
    """
    Load an audio effect into a specific chain of a rack.

    Parameters:
    - track_index: The index of the track containing the rack
    - rack_device_index: The index of the rack device on the track
    - chain_index: The index of the chain to load the effect into
    - effect_uri: The browser URI of the effect to load
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command(
            "load_effect_to_chain",
            {
                "track_index": track_index,
                "rack_device_index": rack_device_index,
                "chain_index": chain_index,
                "effect_uri": effect_uri,
            },
        )
        return f"Loaded effect into chain {chain_index} of rack on track {track_index}"
    except Exception as e:
        logger.exception("Error loading effect to chain")
        return f"Error loading effect to chain: {e}"


@mcp.tool()
def set_sidechain_input(
    track_index: int,
    device_index: int,
    source_track_index: int,
) -> str:
    """
    Set the sidechain input source for a compressor or other sidechain-capable device.

    Parameters:
    - track_index: The index of the track containing the device
    - device_index: The index of the device on the track (e.g., Compressor)
    - source_track_index: The index of the track to use as sidechain source
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command(
            "set_sidechain_input",
            {
                "track_index": track_index,
                "device_index": device_index,
                "source_track_index": source_track_index,
            },
        )
        return f"Set sidechain input on track {track_index} device {device_index} to source track {source_track_index}"
    except Exception as e:
        logger.exception("Error setting sidechain input")
        return f"Error setting sidechain input: {e}"


@mcp.tool()
def create_return_track(name: str = "") -> str:
    """
    Create a new return track.

    Parameters:
    - name: Optional name for the return track
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("create_return_track", {"name": name})
        idx = result.get("index", "?")
        return f"Created return track '{name}' at index {idx}"
    except Exception as e:
        logger.exception("Error creating return track")
        return f"Error creating return track: {e}"


@mcp.tool()
def set_send_level(track_index: int, return_index: int, level: float) -> str:
    """
    Set the send level from a track to a return track.

    Parameters:
    - track_index: The index of the source track
    - return_index: The index of the return track (0 = A, 1 = B, etc.)
    - level: The send level (0.0 to 1.0, where 0.85 is 0dB)
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command(
            "set_send_level",
            {"track_index": track_index, "return_index": return_index, "level": level},
        )
        return f"Set send from track {track_index} to return {return_index} at level {level}"
    except Exception as e:
        logger.exception("Error setting send level")
        return f"Error setting send level: {e}"


@mcp.tool()
def load_instrument_or_effect(track_index: int, uri: str) -> str:
    """
    Load an instrument or effect onto a track using its URI.

    Parameters:
    - track_index: The index of the track to load the instrument on
    - uri: The URI of the instrument or effect to load (e.g., 'query:Synths#Instrument%20Rack:Bass:FileId_5116')
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command(
            "load_browser_item", {"track_index": track_index, "item_uri": uri}
        )

        # Check if the instrument was loaded successfully
        if result.get("loaded", False):
            new_devices = result.get("new_devices", [])
            if new_devices:
                return f"Loaded instrument with URI '{uri}' on track {track_index}. New devices: {', '.join(new_devices)}"
            else:
                devices = result.get("devices_after", [])
                return f"Loaded instrument with URI '{uri}' on track {track_index}. Devices on track: {', '.join(devices)}"
        else:
            return f"Failed to load instrument with URI '{uri}'"
    except Exception as e:
        logger.exception("Error loading instrument by URI")
        return f"Error loading instrument by URI: {e}"


@mcp.tool()
def fire_clip(track_index: int, clip_index: int) -> str:
    """
    Start playing a clip.

    Parameters:
    - track_index: The index of the track containing the clip
    - clip_index: The index of the clip slot containing the clip
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command(
            "fire_clip", {"track_index": track_index, "clip_index": clip_index}
        )
        return f"Started playing clip at track {track_index}, slot {clip_index}"
    except Exception as e:
        logger.exception("Error firing clip")
        return f"Error firing clip: {e}"


@mcp.tool()
def stop_clip(track_index: int, clip_index: int) -> str:
    """
    Stop playing a clip.

    Parameters:
    - track_index: The index of the track containing the clip
    - clip_index: The index of the clip slot containing the clip
    """
    try:
        ableton = get_ableton_connection()
        ableton.send_command(
            "stop_clip", {"track_index": track_index, "clip_index": clip_index}
        )
        return f"Stopped clip at track {track_index}, slot {clip_index}"
    except Exception as e:
        logger.exception("Error stopping clip")
        return f"Error stopping clip: {e}"


@mcp.tool()
def start_playback() -> str:
    """Start playing the Ableton session."""
    try:
        ableton = get_ableton_connection()
        ableton.send_command("start_playback")
        return "Started playback"
    except Exception as e:
        logger.exception("Error starting playback")
        return f"Error starting playback: {e}"


@mcp.tool()
def stop_playback() -> str:
    """Stop playing the Ableton session."""
    try:
        ableton = get_ableton_connection()
        ableton.send_command("stop_playback")
        return "Stopped playback"
    except Exception as e:
        logger.exception("Error stopping playback")
        return f"Error stopping playback: {e}"


@mcp.tool()
def get_browser_tree(category_type: str = "all") -> str:
    """
    Get a hierarchical tree of browser categories from Ableton.

    Parameters:
    - category_type: Type of categories to get ('all', 'instruments', 'sounds', 'drums', 'audio_effects', 'midi_effects')
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command(
            "get_browser_tree", {"category_type": category_type}
        )

        # Check if we got any categories
        if "available_categories" in result and len(result.get("categories", [])) == 0:
            available_cats = result.get("available_categories", [])
            return (
                f"No categories found for '{category_type}'. "
                f"Available browser categories: {', '.join(available_cats)}"
            )

        # Format the tree in a more readable way
        total_folders = result.get("total_folders", 0)
        formatted_output = (
            f"Browser tree for '{category_type}' (showing {total_folders} folders):\n\n"
        )

        def format_tree(item, indent=0):
            output = ""
            if item:
                prefix = "  " * indent
                name = item.get("name", "Unknown")
                path = item.get("path", "")
                has_more = item.get("has_more", False)

                # Add this item
                output += f"{prefix}• {name}"
                if path:
                    output += f" (path: {path})"
                if has_more:
                    output += " [...]"
                output += "\n"

                # Add children
                for child in item.get("children", []):
                    output += format_tree(child, indent + 1)
            return output

        # Format each category
        for category in result.get("categories", []):
            formatted_output += format_tree(category)
            formatted_output += "\n"

        return formatted_output
    except Exception as e:
        error_msg = str(e)
        if "Browser is not available" in error_msg:
            logger.exception("Browser is not available in Ableton")
            return "Error: The Ableton browser is not available. Make sure Ableton Live is fully loaded and try again."
        elif "Could not access Live application" in error_msg:
            logger.exception("Could not access Live application")
            return "Error: Could not access the Ableton Live application. Make sure Ableton Live is running and the Remote Script is loaded."
        else:
            logger.exception("Error getting browser tree")
            return f"Error getting browser tree: {error_msg}"


@mcp.tool()
def get_browser_items_at_path(path: str) -> str:
    """
    Get browser items at a specific path in Ableton's browser.

    Parameters:
    - path: Path in the format "category/folder/subfolder"
            where category is one of the available browser categories in Ableton
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("get_browser_items_at_path", {"path": path})

        # Check if there was an error with available categories
        if "error" in result and "available_categories" in result:
            error = result.get("error", "")
            available_cats = result.get("available_categories", [])
            return (
                f"Error: {error}\n"
                f"Available browser categories: {', '.join(available_cats)}"
            )

        return json.dumps(result, indent=2)
    except Exception as e:
        error_msg = str(e)
        if "Browser is not available" in error_msg:
            logger.exception("Browser is not available in Ableton")
            return "Error: The Ableton browser is not available. Make sure Ableton Live is fully loaded and try again."
        elif "Could not access Live application" in error_msg:
            logger.exception("Could not access Live application")
            return "Error: Could not access the Ableton Live application. Make sure Ableton Live is running and the Remote Script is loaded."
        elif "Unknown or unavailable category" in error_msg:
            logger.exception("Invalid browser category")
            return f"Error: {error_msg}. Please check the available categories using get_browser_tree."
        elif "Path part" in error_msg and "not found" in error_msg:
            logger.exception("Path not found")
            return f"Error: {error_msg}. Please check the path and try again."
        else:
            logger.exception("Error getting browser items at path")
            return f"Error getting browser items at path: {error_msg}"


@mcp.tool()
def load_drum_kit(track_index: int, rack_uri: str, kit_path: str) -> str:
    """
    Load a drum rack and then load a specific drum kit into it.

    Parameters:
    - track_index: The index of the track to load on
    - rack_uri: The URI of the drum rack to load (e.g., 'Drums/Drum Rack')
    - kit_path: Path to the drum kit inside the browser (e.g., 'drums/acoustic/kit1')
    """
    try:
        ableton = get_ableton_connection()

        # Step 1: Load the drum rack
        result = ableton.send_command(
            "load_browser_item", {"track_index": track_index, "item_uri": rack_uri}
        )

        if not result.get("loaded", False):
            return f"Failed to load drum rack with URI '{rack_uri}'"

        # Step 2: Get the drum kit items at the specified path
        kit_result = ableton.send_command(
            "get_browser_items_at_path", {"path": kit_path}
        )

        if "error" in kit_result:
            return f"Loaded drum rack but failed to find drum kit: {kit_result.get('error')}"

        # Step 3: Find a loadable drum kit
        kit_items = kit_result.get("items", [])
        loadable_kits = [item for item in kit_items if item.get("is_loadable", False)]

        if not loadable_kits:
            return f"Loaded drum rack but no loadable drum kits found at '{kit_path}'"

        # Step 4: Load the first loadable kit
        kit_uri = loadable_kits[0].get("uri")
        ableton.send_command(
            "load_browser_item", {"track_index": track_index, "item_uri": kit_uri}
        )

        return f"Loaded drum rack and kit '{loadable_kits[0].get('name')}' on track {track_index}"
    except Exception as e:
        logger.exception("Error loading drum kit")
        return f"Error loading drum kit: {e}"


# Main execution
def main():
    """Run the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()
