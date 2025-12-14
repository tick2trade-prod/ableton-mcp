"""Agent management tools."""

from typing import Any

from ableton_lite.tools.crud import get_db


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
        dict with 'id', 'name', and 'success' keys
    """
    db = get_db()

    try:
        agent_id = await db.create_agent(name, model, config)
        return {
            "id": agent_id,
            "name": name,
            "model": model,
            "success": True,
        }
    except Exception as e:
        return {
            "id": None,
            "name": name,
            "success": False,
            "error": str(e),
        }


async def get_agent(name: str) -> dict[str, Any]:
    """Get agent by name.

    Args:
        name: Agent name

    Returns:
        Agent dict or error
    """
    db = get_db()

    try:
        agent = await db.get_agent(name)
        if agent:
            return {
                "agent": agent,
                "success": True,
            }
        return {
            "agent": None,
            "success": False,
            "error": f"Agent '{name}' not found",
        }
    except Exception as e:
        return {
            "agent": None,
            "success": False,
            "error": str(e),
        }


async def list_agents() -> dict[str, Any]:
    """List all agents.

    Returns:
        dict with 'agents' list and 'success' key
    """
    db = get_db()

    try:
        agents = await db.list_agents()
        return {
            "agents": agents,
            "count": len(agents),
            "success": True,
        }
    except Exception as e:
        return {
            "agents": [],
            "count": 0,
            "success": False,
            "error": str(e),
        }
