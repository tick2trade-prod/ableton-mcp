"""FastMCP server for AbletonLite."""

from typing import Any

from fastmcp import FastMCP

from ableton_lite.config import Config
from ableton_lite.database import Database
from ableton_lite.llm.ollama_client import OllamaClient
from ableton_lite.llm.sql_generator import SQLGenerator

# Initialize MCP server
mcp = FastMCP("ableton_lite")

# Shared instances
_config: Config | None = None
_db: Database | None = None
_sql_gen: SQLGenerator | None = None
_ollama: OllamaClient | None = None


def get_config() -> Config:
    """Get shared config."""
    global _config
    if _config is None:
        _config = Config.from_env()
    return _config


async def get_db() -> Database:
    """Get shared database."""
    global _db
    if _db is None:
        _db = Database(get_config())
        await _db.connect()
    return _db


def get_sql_gen() -> SQLGenerator:
    """Get shared SQL generator."""
    global _sql_gen
    if _sql_gen is None:
        _sql_gen = SQLGenerator(get_config())
    return _sql_gen


def get_ollama() -> OllamaClient:
    """Get shared Ollama client."""
    global _ollama
    if _ollama is None:
        _ollama = OllamaClient(get_config())
    return _ollama


# ============================================================
# Database Tools
# ============================================================


@mcp.tool()
async def query_database(sql: str) -> dict[str, Any]:
    """Execute a read-only SQL query against the AbletonLite database.

    Args:
        sql: SQL SELECT query to execute

    Returns:
        Query results with success status
    """
    db = await get_db()

    sql_upper = sql.strip().upper()
    if not sql_upper.startswith("SELECT"):
        return {"success": False, "error": "Only SELECT queries are allowed"}

    try:
        results = await db.execute(sql)
        return {"success": True, "results": results, "row_count": len(results)}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def ask_database(question: str) -> dict[str, Any]:
    """Ask a question in natural language and get SQL results.

    Uses Ollama to translate natural language to SQL, then executes it.

    Args:
        question: Natural language question about the database

    Returns:
        SQL query used and results
    """
    db = await get_db()
    sql_gen = get_sql_gen()

    result = await sql_gen.ask(question, db.execute)
    return result


@mcp.tool()
async def insert_record(table: str, data: dict[str, Any]) -> dict[str, Any]:
    """Insert a record into a table.

    Args:
        table: Table name (agents, tasks, knowledge_base, jobs)
        data: Record data as key-value pairs

    Returns:
        Inserted record ID
    """
    db = await get_db()

    allowed = ["agents", "tasks", "knowledge_base", "jobs"]
    if table not in allowed:
        return {"success": False, "error": f"Table must be one of: {allowed}"}

    try:
        record_id = await db.insert(table, data)
        return {"success": True, "id": record_id}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def update_record(
    table: str, data: dict[str, Any], where: dict[str, Any]
) -> dict[str, Any]:
    """Update records in a table.

    Args:
        table: Table name
        data: Fields to update
        where: Conditions for matching records

    Returns:
        Number of rows affected
    """
    db = await get_db()

    allowed = ["agents", "tasks", "knowledge_base", "jobs"]
    if table not in allowed:
        return {"success": False, "error": f"Table must be one of: {allowed}"}

    try:
        rowcount = await db.update(table, data, where)
        return {"success": True, "rowcount": rowcount}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def delete_record(table: str, where: dict[str, Any]) -> dict[str, Any]:
    """Delete records from a table.

    Args:
        table: Table name (tasks, knowledge_base, query_history only)
        where: Conditions for matching records to delete

    Returns:
        Number of rows deleted
    """
    db = await get_db()

    # More restrictive for delete
    allowed = ["tasks", "knowledge_base", "query_history"]
    if table not in allowed:
        return {"success": False, "error": f"Delete only allowed on: {allowed}"}

    try:
        rowcount = await db.delete(table, where)
        return {"success": True, "rowcount": rowcount}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================
# Agent Tools
# ============================================================


@mcp.tool()
async def create_agent(
    name: str,
    model: str = "llama3.1:8b",
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a new agent.

    Args:
        name: Unique agent name
        model: Ollama model to use
        config: Optional agent configuration

    Returns:
        Created agent details
    """
    db = await get_db()

    try:
        agent_id = await db.create_agent(name, model, config)
        return {"success": True, "id": agent_id, "name": name, "model": model}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def get_agent(name: str) -> dict[str, Any]:
    """Get agent by name.

    Args:
        name: Agent name

    Returns:
        Agent details or error if not found
    """
    db = await get_db()

    try:
        agent = await db.get_agent(name)
        if agent:
            return {"success": True, "agent": agent}
        return {"success": False, "error": f"Agent '{name}' not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def list_agents() -> dict[str, Any]:
    """List all agents.

    Returns:
        List of all registered agents
    """
    db = await get_db()

    try:
        agents = await db.list_agents()
        return {"success": True, "agents": agents, "count": len(agents)}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================
# Status Tools
# ============================================================


@mcp.tool()
async def get_status() -> dict[str, Any]:
    """Get AbletonLite server status.

    Returns:
        Server status including database and Ollama availability
    """
    config = get_config()
    ollama = get_ollama()

    ollama_available = await ollama.is_available()

    return {
        "success": True,
        "server": "ableton_lite",
        "version": "0.1.0",
        "database": str(config.db_path),
        "ollama_enabled": config.ollama_enabled,
        "ollama_available": ollama_available,
        "ollama_model": config.ollama_model,
    }


# ============================================================
# Server Entry Point
# ============================================================


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
