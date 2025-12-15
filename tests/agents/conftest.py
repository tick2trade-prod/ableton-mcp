"""Pytest fixtures for agent tests.

Provides mocked MCP client and common test utilities.
"""

from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_mcp_client():
    """Mock MCP client for testing agents without live Ableton connection.

    Returns:
        Mock: MCP client with common methods mocked
    """
    client = Mock()

    # Mock common MCP methods
    client.create_clip = Mock(return_value=Mock(success=True, message="Clip created"))
    client.set_clip_launch_mode = Mock(return_value=Mock(success=True))
    client.set_clip_quantization = Mock(return_value=Mock(success=True))
    client.set_follow_action = Mock(return_value=Mock(success=True))
    client.create_effect_rack = Mock(return_value=Mock(success=True))
    client.add_chain_to_rack = Mock(return_value=Mock(success=True))
    client.set_device_parameter = Mock(return_value=Mock(success=True))

    return client


@pytest.fixture
def mock_agent_logger():
    """Mock logger for agent testing."""
    return Mock()
