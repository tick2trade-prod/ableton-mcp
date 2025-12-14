"""Tests for database module."""

import tempfile
from pathlib import Path

import pytest
from ableton_lite.config import Config
from ableton_lite.database import Database


@pytest.fixture
async def db():
    """Create a test database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(db_path=Path(tmpdir) / "test.db")
        database = Database(config)
        await database.connect()
        yield database
        await database.close()


@pytest.mark.asyncio
async def test_create_tables(db: Database):
    """Test that schema tables are created."""
    tables = await db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    table_names = [t["name"] for t in tables]

    assert "agents" in table_names
    assert "tasks" in table_names
    assert "knowledge_base" in table_names
    assert "jobs" in table_names
    assert "query_history" in table_names


@pytest.mark.asyncio
async def test_insert_and_select(db: Database):
    """Test insert and select operations."""
    # Insert
    agent_id = await db.insert("agents", {"name": "test_agent", "model": "gpt-4"})
    assert agent_id > 0

    # Select
    agents = await db.select("agents", where={"name": "test_agent"})
    assert len(agents) == 1
    assert agents[0]["name"] == "test_agent"
    assert agents[0]["model"] == "gpt-4"


@pytest.mark.asyncio
async def test_update(db: Database):
    """Test update operation."""
    agent_id = await db.insert("agents", {"name": "update_test", "model": "v1"})

    rowcount = await db.update("agents", {"model": "v2"}, {"id": agent_id})
    assert rowcount == 1

    agents = await db.select("agents", where={"id": agent_id})
    assert agents[0]["model"] == "v2"


@pytest.mark.asyncio
async def test_delete(db: Database):
    """Test delete operation."""
    task_id = await db.insert("tasks", {"name": "delete_me"})

    rowcount = await db.delete("tasks", {"id": task_id})
    assert rowcount == 1

    tasks = await db.select("tasks", where={"id": task_id})
    assert len(tasks) == 0


@pytest.mark.asyncio
async def test_create_agent(db: Database):
    """Test create_agent convenience method."""
    agent_id = await db.create_agent(
        name="my_agent",
        model="llama3.1:8b",
        config={"temperature": 0.7},
    )
    assert agent_id > 0

    agent = await db.get_agent("my_agent")
    assert agent is not None
    assert agent["model"] == "llama3.1:8b"


@pytest.mark.asyncio
async def test_list_agents(db: Database):
    """Test list_agents method."""
    await db.create_agent("agent1")
    await db.create_agent("agent2")

    agents = await db.list_agents()
    assert len(agents) == 2
