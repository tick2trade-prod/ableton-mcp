"""Tests for LLM module."""

import pytest
from ableton_lite.config import Config
from ableton_lite.llm.sql_generator import SQLGenerator


@pytest.fixture
def sql_gen():
    """Create SQL generator with Ollama disabled for testing."""
    config = Config(ollama_enabled=False)
    return SQLGenerator(config)


def test_extract_sql_plain():
    """Test extracting plain SQL."""
    config = Config(ollama_enabled=False)
    sql_gen = SQLGenerator(config)

    result = sql_gen._extract_sql("SELECT * FROM agents")
    assert result == "SELECT * FROM agents"


def test_extract_sql_code_block():
    """Test extracting SQL from code block."""
    config = Config(ollama_enabled=False)
    sql_gen = SQLGenerator(config)

    response = """Here's the query:
```sql
SELECT * FROM agents WHERE status = 'active'
```
"""
    result = sql_gen._extract_sql(response)
    assert result == "SELECT * FROM agents WHERE status = 'active'"


def test_is_safe_sql_select():
    """Test that SELECT is considered safe."""
    config = Config(ollama_enabled=False)
    sql_gen = SQLGenerator(config)

    assert sql_gen._is_safe_sql("SELECT * FROM agents")
    assert sql_gen._is_safe_sql("SELECT COUNT(*) FROM tasks WHERE status = 'pending'")


def test_is_safe_sql_dangerous():
    """Test that dangerous operations are blocked."""
    config = Config(ollama_enabled=False)
    sql_gen = SQLGenerator(config)

    assert not sql_gen._is_safe_sql("DROP TABLE agents")
    assert not sql_gen._is_safe_sql("DELETE FROM agents")
    assert not sql_gen._is_safe_sql("INSERT INTO agents (name) VALUES ('test')")
    assert not sql_gen._is_safe_sql("UPDATE agents SET model = 'new'")
    assert not sql_gen._is_safe_sql("CREATE TABLE foo (id INT)")


@pytest.mark.asyncio
async def test_translate_disabled():
    """Test translation when Ollama is disabled."""
    config = Config(ollama_enabled=False)
    sql_gen = SQLGenerator(config)

    result = await sql_gen.translate("show all agents")
    assert not result["success"]
    assert "disabled" in result["error"].lower()
