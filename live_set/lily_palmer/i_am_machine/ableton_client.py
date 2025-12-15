#!/usr/bin/env python3
"""Shared MCP client utilities for track setup scripts.

This module centralizes the Ableton MCP communication logic, eliminating
code duplication across 16 track scripts.

Usage:
    from ableton_client import AbletonMCPClient, TRACKS

    client = AbletonMCPClient()
    client.create_midi_track(index=0)
    client.set_track_name(track_index=0, name="01-Kick")
    client.load_device(track_index=0, device_name="Drum Sampler")
"""

import json
import os
import socket
import subprocess
import time
from dataclasses import dataclass, field
from typing import Any

# Track configurations matching the spec
TRACKS = [
    {"index": 0, "name": "01-Kick", "type": "midi"},
    {"index": 1, "name": "02-Rumble", "type": "audio"},
    {"index": 2, "name": "03-RollingBass", "type": "midi"},
    {"index": 3, "name": "04-Acid", "type": "midi"},
    {"index": 4, "name": "05-ClosedHats", "type": "midi"},
    {"index": 5, "name": "06-OpenHats", "type": "midi"},
    {"index": 6, "name": "07-Clap", "type": "midi"},
    {"index": 7, "name": "08-LowTom", "type": "midi"},
    {"index": 8, "name": "09-Glitch", "type": "midi"},
    {"index": 9, "name": "10-Ride", "type": "midi"},
    {"index": 10, "name": "11-SynthStab", "type": "midi"},
    {"index": 11, "name": "12-Drone", "type": "midi"},
    {"index": 12, "name": "13-Vocal", "type": "audio"},
    {"index": 13, "name": "14-VocalFX", "type": "audio"},
    {"index": 14, "name": "15-Riser", "type": "midi"},
    {"index": 15, "name": "16-Impact", "type": "midi"},
]

# Device chain recommendations per track type
DEVICE_CHAINS = {
    "kick": ["Drum Sampler", "Channel EQ", "Saturator", "Utility"],
    "rumble": ["Reverb", "Roar", "Channel EQ", "Compressor"],
    "bass": ["Operator", "Channel EQ", "Saturator", "Compressor"],
    "acid": ["Operator", "Auto Filter", "Redux", "Compressor"],
    "hihat": ["Drum Sampler", "Channel EQ", "Saturator"],
    "clap": ["Drum Sampler", "Reverb", "Channel EQ"],
    "tom": ["Drum Sampler", "Channel EQ", "Reverb"],
    "glitch": ["Simpler", "Beat Repeat", "Phaser", "Delay"],
    "ride": ["Drum Sampler", "Channel EQ", "Saturator"],
    "synth": ["Wavetable", "Echo", "Reverb", "Channel EQ"],
    "drone": ["Operator", "Reverb", "Chorus", "Auto Filter"],
    "vocal": ["Channel EQ", "Compressor", "Reverb"],
    "fx": ["Grain Scanner", "Spectral Resonator", "Echo"],
    "riser": ["Operator", "Auto Filter", "Compressor"],
    "impact": ["Drum Sampler", "Reverb", "Saturator"],
}


@dataclass
class CommandResult:
    """Result from an MCP command."""

    success: bool
    data: dict = field(default_factory=dict)
    message: str = ""
    raw: dict = field(default_factory=dict)


class AbletonMCPClient:
    """Unified Ableton MCP client for track setup scripts."""

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        timeout: float = 15.0,
    ):
        self.host = host or self._detect_host()
        self.port = port or int(os.getenv("ABLETON_MCP_PORT", "9877"))
        self.timeout = timeout

    @staticmethod
    def _detect_host() -> str:
        """Best-effort host discovery for WSL→Windows."""
        env_host = os.getenv("ABLETON_MCP_HOST")
        if env_host:
            return env_host
        try:
            route = subprocess.check_output(
                ["sh", "-c", "ip route show default | awk '{print $3}'"],
                text=True,
            ).strip()
            if route:
                return route
        except Exception:
            pass
        return "127.0.0.1"

    def send_command(
        self,
        command_type: str,
        params: dict[str, Any] | None = None,
    ) -> CommandResult:
        """Send a JSON command to the Ableton MCP server."""
        command = {"type": command_type, "params": params or {}}

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((self.host, self.port))

            data = (json.dumps(command) + "\n").encode("utf-8")
            sock.sendall(data)

            buffer = b""
            start = time.time()

            while True:
                chunk = sock.recv(8192)
                if not chunk:
                    break
                buffer += chunk
                try:
                    result = json.loads(buffer.decode("utf-8"))
                    sock.close()
                    return CommandResult(
                        success=result.get("status") == "success",
                        data=result.get("data", result.get("result", {})),
                        message=result.get("message", ""),
                        raw=result,
                    )
                except json.JSONDecodeError:
                    if time.time() - start > self.timeout:
                        sock.close()
                        return CommandResult(
                            success=False,
                            message="Timeout waiting for response",
                        )
                    continue

            sock.close()
            return CommandResult(success=False, message="Connection closed")

        except Exception as e:
            return CommandResult(success=False, message=str(e))

    # =========================================================================
    # Session Commands
    # =========================================================================

    def get_session_info(self) -> CommandResult:
        """Get current session information."""
        return self.send_command("get_session_info")

    def set_tempo(self, tempo: float) -> CommandResult:
        """Set session tempo."""
        return self.send_command("set_tempo", {"tempo": tempo})

    def start_playback(self) -> CommandResult:
        """Start playback."""
        return self.send_command("start_playback")

    def stop_playback(self) -> CommandResult:
        """Stop playback."""
        return self.send_command("stop_playback")

    # =========================================================================
    # Track Commands
    # =========================================================================

    def create_midi_track(self, index: int = -1) -> CommandResult:
        """Create a MIDI track."""
        return self.send_command("create_midi_track", {"index": index})

    def create_audio_track(self, index: int = -1) -> CommandResult:
        """Create an audio track."""
        return self.send_command("create_audio_track", {"index": index})

    def set_track_name(self, track_index: int, name: str) -> CommandResult:
        """Set track name."""
        return self.send_command(
            "set_track_name", {"track_index": track_index, "name": name}
        )

    def ensure_track(
        self,
        target_index: int,
        name: str,
        track_type: str = "midi",
    ) -> CommandResult:
        """Ensure a track exists at the target index, creating if needed."""
        info = self.get_session_info()
        if not info.success:
            return info

        current_count = info.data.get("track_count", 0)

        if current_count <= target_index:
            if track_type == "audio":
                result = self.create_audio_track(index=-1)
            else:
                result = self.create_midi_track(index=-1)

            if not result.success:
                return result

        return self.set_track_name(target_index, name)

    def set_track_output(
        self, track_index: int, output_target: str = "Main"
    ) -> CommandResult:
        """Set the output routing of a track.

        Args:
            track_index: Track index to modify
            output_target: Target output ('Main' for master output)

        Returns:
            CommandResult with success status
        """
        return self.send_command(
            "set_track_output",
            {"track_index": track_index, "output_target": output_target},
        )

    # =========================================================================
    # Device Commands
    # =========================================================================

    def load_device(
        self,
        track_index: int,
        device_name: str,
        fallback: str | None = None,
    ) -> CommandResult:
        """Load a device onto a track."""
        result = self.send_command(
            "load_instrument_or_effect",
            {"track_index": track_index, "device_name": device_name},
        )
        if not result.success and fallback:
            return self.load_device(track_index, fallback)
        return result

    def load_browser_item(
        self,
        track_index: int,
        item_uri: str,
    ) -> CommandResult:
        """Load a browser item by URI."""
        return self.send_command(
            "load_browser_item",
            {"track_index": track_index, "item_uri": item_uri},
        )

    def set_device_parameter(
        self,
        track_index: int,
        device_index: int,
        parameter_name: str,
        value: float,
    ) -> CommandResult:
        """Set a device parameter."""
        return self.send_command(
            "set_device_parameter",
            {
                "track_index": track_index,
                "device_index": device_index,
                "parameter_name": parameter_name,
                "value": value,
            },
        )

    def load_device_chain(
        self,
        track_index: int,
        devices: list[str],
        verbose: bool = True,
    ) -> list[CommandResult]:
        """Load a chain of devices onto a track."""
        results = []
        for device in devices:
            result = self.load_device(track_index, device)
            results.append(result)
            if verbose:
                symbol = "✓" if result.success else "✗"
                print(f"     {symbol} {device}")
            time.sleep(0.2)  # Small delay between device loads
        return results

    # =========================================================================
    # Clip Commands
    # =========================================================================

    def create_clip(
        self,
        track_index: int,
        clip_index: int = 0,
        length: float = 4.0,
    ) -> CommandResult:
        """Create an empty clip."""
        return self.send_command(
            "create_clip",
            {"track_index": track_index, "clip_index": clip_index, "length": length},
        )

    def add_notes_to_clip(
        self,
        track_index: int,
        clip_index: int,
        notes: list[dict[str, Any]],
    ) -> CommandResult:
        """Add notes to a clip."""
        return self.send_command(
            "add_notes_to_clip",
            {"track_index": track_index, "clip_index": clip_index, "notes": notes},
        )

    def set_clip_name(
        self,
        track_index: int,
        clip_index: int,
        name: str,
    ) -> CommandResult:
        """Set clip name."""
        return self.send_command(
            "set_clip_name",
            {"track_index": track_index, "clip_index": clip_index, "name": name},
        )

    def fire_clip(self, track_index: int, clip_index: int) -> CommandResult:
        """Fire (play) a clip."""
        return self.send_command(
            "fire_clip",
            {"track_index": track_index, "clip_index": clip_index},
        )

    def create_pattern(
        self,
        track_index: int,
        clip_index: int,
        clip_name: str,
        notes: list[dict[str, Any]],
        length: float = 16.0,
        fire: bool = False,
    ) -> CommandResult:
        """Create a clip with notes in one call."""
        result = self.create_clip(track_index, clip_index, length)
        if not result.success:
            return result

        result = self.add_notes_to_clip(track_index, clip_index, notes)
        if not result.success:
            return result

        self.set_clip_name(track_index, clip_index, clip_name)

        if fire:
            self.fire_clip(track_index, clip_index)

        return CommandResult(success=True, message=f"Pattern '{clip_name}' created")


# Convenience function for quick setup
def setup_track(
    index: int,
    name: str,
    track_type: str = "midi",
    devices: list[str] | None = None,
    notes: list[dict[str, Any]] | None = None,
    verbose: bool = True,
) -> bool:
    """Quick setup for a single track."""
    client = AbletonMCPClient()

    if verbose:
        print(f"\n=== Setting up {name} ===")

    # Ensure track exists
    result = client.ensure_track(index, name, track_type)
    if not result.success:
        if verbose:
            print(f"   ✗ Failed to create track: {result.message}")
        return False
    if verbose:
        print(f"   ✓ Track {index}: {name}")

    # Load devices
    if devices:
        if verbose:
            print("   Loading devices:")
        client.load_device_chain(index, devices, verbose)

    # Add notes
    if notes:
        result = client.create_pattern(
            index, 0, f"{name} Pattern", notes, length=16.0, fire=True
        )
        if verbose:
            print("   ✓ Pattern added")

    return True


if __name__ == "__main__":
    # Test connection
    client = AbletonMCPClient()
    info = client.get_session_info()
    if info.success:
        print(f"Connected! Tempo: {info.data.get('tempo')} BPM")
        print(f"Tracks: {info.data.get('track_count')}")
    else:
        print(f"Connection failed: {info.message}")
