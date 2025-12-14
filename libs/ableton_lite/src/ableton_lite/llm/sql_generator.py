"""Natural language to SQL translation."""

import re
from typing import Any

from ableton_lite.config import Config
from ableton_lite.llm.ollama_client import OllamaClient

# System prompt for SQL generation
SQL_SYSTEM_PROMPT = """You are a SQL expert. Convert natural language questions to SQLite queries.

Available tables and schemas:

agents (id, name, model, config, status, created_at, updated_at)
tasks (id, name, agent_id, status, input, output, error, started_at, completed_at, created_at)
knowledge_base (id, content, embedding, metadata, source, created_at)
jobs (id, name, schedule, agent_id, query, enabled, last_run, next_run, created_at)
query_history (id, query, translated_sql, success, latency_ms, created_at)

Rules:
1. Output ONLY the SQL query, no explanations
2. Use SQLite syntax
3. For read operations, use SELECT
4. Never use DROP, TRUNCATE, or ALTER
5. Use single quotes for string literals
6. Limit results to 100 rows by default unless specified

Examples:
- "show all agents" → SELECT * FROM agents LIMIT 100;
- "pending tasks" → SELECT * FROM tasks WHERE status = 'pending' LIMIT 100;
- "count agents" → SELECT COUNT(*) as count FROM agents;
"""


class SQLGenerator:
    """Natural language to SQL translator."""

    def __init__(self, config: Config | None = None):
        """Initialize SQL generator."""
        self.config = config or Config.from_env()
        self.ollama = OllamaClient(self.config)

    async def translate(self, question: str) -> dict[str, Any]:
        """Translate natural language to SQL.

        Returns:
            dict with 'sql' and 'success' keys
        """
        if not self.config.ollama_enabled:
            return {
                "sql": None,
                "success": False,
                "error": "Ollama is disabled",
            }

        try:
            response = await self.ollama.generate(
                prompt=question,
                system=SQL_SYSTEM_PROMPT,
            )

            # Extract SQL from response
            sql = self._extract_sql(response)

            # Validate SQL (basic safety check)
            if not self._is_safe_sql(sql):
                return {
                    "sql": sql,
                    "success": False,
                    "error": "Generated SQL contains unsafe operations",
                }

            return {
                "sql": sql,
                "success": True,
            }

        except Exception as e:
            return {
                "sql": None,
                "success": False,
                "error": str(e),
            }

    def _extract_sql(self, response: str) -> str:
        """Extract SQL query from LLM response."""
        # Remove markdown code blocks if present
        response = response.strip()

        # Match ```sql ... ``` or ``` ... ```
        sql_block = re.search(r"```(?:sql)?\s*(.*?)\s*```", response, re.DOTALL)
        if sql_block:
            return sql_block.group(1).strip()

        # If no code block, assume entire response is SQL
        return response.strip()

    def _is_safe_sql(self, sql: str) -> bool:
        """Check if SQL is safe to execute (read-only)."""
        if not sql:
            return False

        sql_upper = sql.upper()

        # Disallow dangerous operations
        dangerous = [
            "DROP",
            "DELETE",
            "TRUNCATE",
            "ALTER",
            "INSERT",
            "UPDATE",
            "CREATE",
        ]
        for keyword in dangerous:
            # Match as whole word to avoid false positives
            if re.search(rf"\b{keyword}\b", sql_upper):
                # Allow SELECT ... FROM DELETE (unlikely but safe check)
                if keyword != "DELETE" or "FROM" not in sql_upper.split("DELETE")[0]:
                    return False

        return True

    async def ask(self, question: str, execute_fn) -> dict[str, Any]:
        """Translate and execute a natural language query.

        Args:
            question: Natural language question
            execute_fn: Async function to execute SQL

        Returns:
            dict with 'question', 'sql', 'results', 'success' keys
        """
        # Translate
        translation = await self.translate(question)

        if not translation["success"]:
            return {
                "question": question,
                "sql": translation.get("sql"),
                "results": None,
                "success": False,
                "error": translation.get("error"),
            }

        # Execute
        try:
            results = await execute_fn(translation["sql"])
            return {
                "question": question,
                "sql": translation["sql"],
                "results": results,
                "success": True,
            }
        except Exception as e:
            return {
                "question": question,
                "sql": translation["sql"],
                "results": None,
                "success": False,
                "error": str(e),
            }
