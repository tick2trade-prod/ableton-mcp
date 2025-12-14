"""SQLite database management for AbletonLite."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import aiosqlite

from ableton_lite.config import Config

# Core schema SQL
SCHEMA_SQL = """
-- Agents table (MindsDB-inspired)
CREATE TABLE IF NOT EXISTS agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    model TEXT DEFAULT 'llama3.1:8b',
    config JSON,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks/workflows
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    agent_id INTEGER REFERENCES agents(id),
    status TEXT DEFAULT 'pending',
    input JSON,
    output JSON,
    error TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Knowledge base items
CREATE TABLE IF NOT EXISTS knowledge_base (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    embedding BLOB,
    metadata JSON,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Jobs (scheduled tasks, V2)
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    schedule TEXT,  -- cron expression
    agent_id INTEGER REFERENCES agents(id),
    query TEXT NOT NULL,
    enabled BOOLEAN DEFAULT 1,
    last_run TIMESTAMP,
    next_run TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Query history for analytics
CREATE TABLE IF NOT EXISTS query_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    translated_sql TEXT,
    success BOOLEAN,
    latency_ms REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


class Database:
    """Async SQLite database manager."""

    def __init__(self, config: Config | None = None):
        """Initialize database with config."""
        self.config = config or Config.from_env()
        self._connection: aiosqlite.Connection | None = None

    @property
    def db_path(self) -> Path:
        """Get database file path."""
        return self.config.db_path

    async def connect(self) -> aiosqlite.Connection:
        """Connect to database and initialize schema."""
        if self._connection is not None:
            return self._connection

        self.config.ensure_db_dir()
        self._connection = await aiosqlite.connect(str(self.db_path))
        self._connection.row_factory = aiosqlite.Row

        # Initialize schema
        await self._connection.executescript(SCHEMA_SQL)
        await self._connection.commit()

        return self._connection

    async def close(self) -> None:
        """Close database connection."""
        if self._connection:
            await self._connection.close()
            self._connection = None

    async def execute(
        self, sql: str, params: tuple | None = None
    ) -> list[dict[str, Any]]:
        """Execute a query and return results as dicts."""
        conn = await self.connect()
        cursor = await conn.execute(sql, params or ())
        rows = await cursor.fetchall()
        await cursor.close()
        return [dict(row) for row in rows]

    async def execute_write(
        self, sql: str, params: tuple | None = None
    ) -> dict[str, Any]:
        """Execute a write query (INSERT/UPDATE/DELETE)."""
        conn = await self.connect()
        cursor = await conn.execute(sql, params or ())
        await conn.commit()
        return {
            "lastrowid": cursor.lastrowid,
            "rowcount": cursor.rowcount,
        }

    # --- Convenience methods ---

    async def insert(self, table: str, data: dict[str, Any]) -> int:
        """Insert a record and return the ID."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        result = await self.execute_write(sql, tuple(data.values()))
        return result["lastrowid"]

    async def select(
        self,
        table: str,
        where: dict[str, Any] | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """Select records from a table."""
        sql = f"SELECT * FROM {table}"
        params: list = []

        if where:
            conditions = " AND ".join(f"{k} = ?" for k in where.keys())
            sql += f" WHERE {conditions}"
            params = list(where.values())

        if limit:
            sql += f" LIMIT {limit}"

        return await self.execute(sql, tuple(params))

    async def update(
        self, table: str, data: dict[str, Any], where: dict[str, Any]
    ) -> int:
        """Update records and return affected row count."""
        set_clause = ", ".join(f"{k} = ?" for k in data.keys())
        where_clause = " AND ".join(f"{k} = ?" for k in where.keys())
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

        result = await self.execute_write(
            sql, tuple(list(data.values()) + list(where.values()))
        )
        return result["rowcount"]

    async def delete(self, table: str, where: dict[str, Any]) -> int:
        """Delete records and return affected row count."""
        where_clause = " AND ".join(f"{k} = ?" for k in where.keys())
        sql = f"DELETE FROM {table} WHERE {where_clause}"

        result = await self.execute_write(sql, tuple(where.values()))
        return result["rowcount"]

    # --- Agent methods ---

    async def create_agent(
        self, name: str, model: str = "llama3.1:8b", config: dict | None = None
    ) -> int:
        """Create a new agent."""
        return await self.insert(
            "agents",
            {
                "name": name,
                "model": model,
                "config": json.dumps(config) if config else None,
            },
        )

    async def get_agent(self, name: str) -> dict[str, Any] | None:
        """Get agent by name."""
        results = await self.select("agents", where={"name": name}, limit=1)
        return results[0] if results else None

    async def list_agents(self) -> list[dict[str, Any]]:
        """List all agents."""
        return await self.select("agents")

    # --- Task methods ---

    async def create_task(
        self, name: str, agent_id: int | None = None, input_data: dict | None = None
    ) -> int:
        """Create a new task."""
        return await self.insert(
            "tasks",
            {
                "name": name,
                "agent_id": agent_id,
                "input": json.dumps(input_data) if input_data else None,
            },
        )

    async def update_task_status(
        self,
        task_id: int,
        status: str,
        output: dict | None = None,
        error: str | None = None,
    ) -> None:
        """Update task status."""
        data = {"status": status, "updated_at": datetime.now().isoformat()}
        if status == "running":
            data["started_at"] = datetime.now().isoformat()
        if status in ("completed", "failed"):
            data["completed_at"] = datetime.now().isoformat()
        if output:
            data["output"] = json.dumps(output)
        if error:
            data["error"] = error

        await self.update("tasks", data, {"id": task_id})
