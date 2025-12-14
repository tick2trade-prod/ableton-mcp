#!/usr/bin/env python3
"""Tests for Ableton Code Generation MCP.

Tests cover:
- Settings loading and validation
- Code generator AST parsing
- Web search (mocked)
- MCP tool validation
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.ableton_cache_ast_codegen_mcp.code_generator import (
    AbletonCodeGenerator,
    MCPToolCall,
    TrackPattern,
)
from scripts.ableton_cache_ast_codegen_mcp.settings import (
    AbletonCodegenSettings,
    get_settings,
    reset_settings,
)
from scripts.ableton_cache_ast_codegen_mcp.web_search import (
    ABLETON_DEVICES,
    ABLETON_DOMAINS,
    AbletonWebSearch,
)


class TestSettings:
    """Test settings module."""

    def setup_method(self):
        """Reset settings before each test."""
        reset_settings()

    def test_default_settings(self):
        """Test default settings values."""
        settings = AbletonCodegenSettings()
        assert settings.chunk_size == 1000
        assert settings.chunk_overlap == 200
        assert settings.embedding_model == "all-MiniLM-L6-v2"
        assert settings.redis_index_name == "ableton_docs"

    def test_settings_singleton(self):
        """Test settings singleton pattern."""
        s1 = get_settings()
        s2 = get_settings()
        assert s1 is s2

    def test_settings_env_override(self, monkeypatch):
        """Test environment variable override."""
        reset_settings()
        monkeypatch.setenv("ABLETON_CODEGEN_CHUNK_SIZE", "2000")
        settings = AbletonCodegenSettings()
        assert settings.chunk_size == 2000


class TestCodeGenerator:
    """Test code generator."""

    def test_extract_tool_calls_simple(self):
        """Test extracting tool calls from simple code."""
        generator = AbletonCodeGenerator()
        code = """
async def create_track():
    await create_midi_track(index=0)
    await set_track_name(track_index=0, name="Kick")
"""
        calls = generator.extract_tool_calls(code)
        assert len(calls) == 2
        assert calls[0].tool_name == "create_midi_track"
        assert calls[1].tool_name == "set_track_name"

    def test_extract_tool_calls_with_args(self):
        """Test extracting tool calls with arguments."""
        generator = AbletonCodeGenerator()
        code = """
await add_notes_to_clip(track_index=0, clip_index=0, notes=[{"pitch": 60}])
"""
        calls = generator.extract_tool_calls(code)
        assert len(calls) == 1
        assert calls[0].tool_name == "add_notes_to_clip"
        assert calls[0].args.get("track_index") == 0

    def test_detect_track_type_kick(self):
        """Test track type detection for kick."""
        generator = AbletonCodeGenerator()
        assert generator.detect_track_type("track_01_kick.py") == "kick"
        assert generator.detect_track_type("bd_track.py") == "kick"

    def test_detect_track_type_snare(self):
        """Test track type detection for snare."""
        generator = AbletonCodeGenerator()
        assert generator.detect_track_type("track_07_clap.py") == "snare"
        assert generator.detect_track_type("snare_track.py") == "snare"

    def test_detect_track_type_unknown(self):
        """Test track type detection for unknown."""
        generator = AbletonCodeGenerator()
        assert generator.detect_track_type("track_mystery.py") == "unknown"

    def test_generate_track_code_basic(self):
        """Test basic track code generation."""
        generator = AbletonCodeGenerator()
        spec = {
            "name": "Test Kick",
            "type": "kick",
            "index": 0,
        }
        code = generator.generate_track_code(spec)
        assert "create_midi_track" in code
        assert "Test Kick" in code
        assert "async def create_kick_track" in code

    def test_generate_track_code_with_devices(self):
        """Test track code generation with devices."""
        generator = AbletonCodeGenerator()
        spec = {
            "name": "Synth Lead",
            "type": "lead",
            "index": 5,
            "devices": [{"name": "Wavetable", "parameters": {"cutoff": 0.5}}],
        }
        code = generator.generate_track_code(spec)
        assert "load_device" in code
        assert "Wavetable" in code
        assert "set_device_parameter" in code

    async def test_validate_code_valid(self):
        """Test code validation with valid code."""
        generator = AbletonCodeGenerator()
        code = """
async def create_track():
    await create_midi_track(index=0)
"""
        result = await generator.validate_code(code)
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    async def test_validate_code_syntax_error(self):
        """Test code validation with syntax error."""
        generator = AbletonCodeGenerator()
        code = "def broken( :"
        result = await generator.validate_code(code)
        assert result["valid"] is False
        assert len(result["errors"]) > 0


class TestWebSearch:
    """Test web search module."""

    def test_ableton_domains_defined(self):
        """Test that Ableton domains are defined."""
        assert len(ABLETON_DOMAINS) > 0
        assert "ableton.com" in ABLETON_DOMAINS

    def test_ableton_devices_defined(self):
        """Test that Ableton devices are defined."""
        assert len(ABLETON_DEVICES) > 0
        assert "Roar" in ABLETON_DEVICES
        assert "Meld" in ABLETON_DEVICES
        assert "Drift" in ABLETON_DEVICES

    def test_web_search_init(self):
        """Test web search initialization."""
        search = AbletonWebSearch(tavily_api_key="test-key")
        assert search.tavily_api_key == "test-key"
        assert search.max_results == 10


class TestMCPToolCall:
    """Test MCPToolCall class."""

    def test_to_dict(self):
        """Test MCPToolCall to dict conversion."""
        call = MCPToolCall(
            tool_name="create_midi_track",
            args={"index": 0},
            line_number=10,
        )
        d = call.to_dict()
        assert d["tool_name"] == "create_midi_track"
        assert d["args"]["index"] == 0
        assert d["line_number"] == 10


class TestTrackPattern:
    """Test TrackPattern class."""

    def test_to_dict(self):
        """Test TrackPattern to dict conversion."""
        calls = [
            MCPToolCall("create_midi_track", {"index": 0}, 1),
        ]
        pattern = TrackPattern(
            track_type="kick",
            track_name="Kick",
            tool_calls=calls,
            source_file="track_01_kick.py",
        )
        d = pattern.to_dict()
        assert d["track_type"] == "kick"
        assert len(d["tool_calls"]) == 1


class TestMCPServer:
    """Test MCP server imports and tools."""

    def test_mcp_import(self):
        """Test MCP server can be imported."""
        from scripts.ableton_cache_ast_codegen_mcp.mcp_server import mcp

        assert mcp is not None
        assert mcp.name == "ableton_codegen"

    def test_tools_registered(self):
        """Test tools are registered."""
        from scripts.ableton_cache_ast_codegen_mcp.mcp_server import (
            analyze_track_script,
            embed_ableton_docs,
            generate_track_code,
            search_ableton_docs,
            search_ableton_guides,
        )

        assert embed_ableton_docs is not None
        assert search_ableton_docs is not None
        assert search_ableton_guides is not None
        assert analyze_track_script is not None
        assert generate_track_code is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
