"""CRUD operations for database."""

from typing import Any

from ableton_lite.database import Database

# Shared database instance
_db: Database | None = None


def get_db() -> Database:
    """Get shared database instance."""
    global _db
    if _db is None:
        _db = Database()
    return _db


async def query_database(sql: str) -> dict[str, Any]:
    """Execute a read-only SQL query.

    Args:
        sql: SQL query to execute (SELECT only)

    Returns:
        dict with 'results' and 'success' keys
    """
    db = get_db()

    # Safety check - only allow SELECT
    sql_upper = sql.strip().upper()
    if not sql_upper.startswith("SELECT"):
        return {
            "results": None,
            "success": False,
            "error": "Only SELECT queries are allowed",
        }

    try:
        results = await db.execute(sql)
        return {
            "results": results,
            "success": True,
            "row_count": len(results),
        }
    except Exception as e:
        return {
            "results": None,
            "success": False,
            "error": str(e),
        }


async def insert_record(table: str, data: dict[str, Any]) -> dict[str, Any]:
    """Insert a record into a table.

    Args:
        table: Table name
        data: Record data as key-value pairs

    Returns:
        dict with 'id' and 'success' keys
    """
    db = get_db()

    # Validate table name (prevent SQL injection)
    allowed_tables = ["agents", "tasks", "knowledge_base", "jobs"]
    if table not in allowed_tables:
        return {
            "id": None,
            "success": False,
            "error": f"Table '{table}' is not allowed. Allowed: {allowed_tables}",
        }

    try:
        record_id = await db.insert(table, data)
        return {
            "id": record_id,
            "success": True,
        }
    except Exception as e:
        return {
            "id": None,
            "success": False,
            "error": str(e),
        }


async def update_record(
    table: str, data: dict[str, Any], where: dict[str, Any]
) -> dict[str, Any]:
    """Update records in a table.

    Args:
        table: Table name
        data: Fields to update
        where: Conditions for update

    Returns:
        dict with 'rowcount' and 'success' keys
    """
    db = get_db()

    allowed_tables = ["agents", "tasks", "knowledge_base", "jobs"]
    if table not in allowed_tables:
        return {
            "rowcount": 0,
            "success": False,
            "error": f"Table '{table}' is not allowed",
        }

    try:
        rowcount = await db.update(table, data, where)
        return {
            "rowcount": rowcount,
            "success": True,
        }
    except Exception as e:
        return {
            "rowcount": 0,
            "success": False,
            "error": str(e),
        }


async def delete_record(table: str, where: dict[str, Any]) -> dict[str, Any]:
    """Delete records from a table.

    Args:
        table: Table name
        where: Conditions for deletion

    Returns:
        dict with 'rowcount' and 'success' keys
    """
    db = get_db()

    allowed_tables = ["tasks", "knowledge_base", "query_history"]
    if table not in allowed_tables:
        return {
            "rowcount": 0,
            "success": False,
            "error": f"Deletion not allowed on table '{table}'",
        }

    try:
        rowcount = await db.delete(table, where)
        return {
            "rowcount": rowcount,
            "success": True,
        }
    except Exception as e:
        return {
            "rowcount": 0,
            "success": False,
            "error": str(e),
        }
