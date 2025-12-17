# Add MCP Tool

Workflow for adding a new MCP tool to the Ableton-MCP server.

## Current Tools

32 tools available. View with:

```bash
just mcp-tools
```

Full documentation in `TOOLS.md`.

## Step-by-Step Process

### 1. Define Tool in MCP Server

Edit `MCP_Server/server.py`:

```python
@mcp.tool()
def my_new_tool(param1: str, param2: int = 0) -> str:
    """
    Description of what the tool does.

    Parameters:
    - param1: Description of param1
    - param2: Description of param2 (default: 0)
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("my_new_tool", {
            "param1": param1,
            "param2": param2
        })
        return f"Success: {result}"
    except Exception as e:
        logger.exception("Error in my_new_tool")
        return f"Error: {e}"
```

### 2. Add Handler in Remote Script

Edit `AbletonMCP_Remote_Script/__init__.py`:

Add command to main thread list (~line 236):
```python
"my_new_tool",
```

Add handler call in main_thread_task (~line 430):
```python
elif command_type == "my_new_tool":
    param1 = params.get("param1", "")
    param2 = params.get("param2", 0)
    result = self._my_new_tool(param1, param2)
```

Add handler method:
```python
def _my_new_tool(self, param1, param2):
    """Implementation using Live API."""
    try:
        # Your implementation here
        result = {"status": "success"}
        return result
    except Exception as e:
        self.log_message(f"Error in my_new_tool: {e}")
        raise
```

### 3. Verify Syntax

```bash
python3 -m py_compile MCP_Server/server.py
python3 -m py_compile AbletonMCP_Remote_Script/__init__.py
```

### 4. Test Tool Count

```bash
just mcp-tools
```

Should show increased count.

### 5. Test Connection

```bash
just mcp-test
```

### 6. Run Doctor

```bash
just doctor
```

### 7. Update Documentation

Update `TOOLS.md` with new tool in appropriate category.

### 8. Create Test (Optional)

Add test in `tests/test_tools.py`:

```python
def test_my_new_tool():
    # Call the tool
    # Assert expected result
    pass
```

## Edition Filtering (Optional)

For Suite-only tools:

```python
from MCP_Server.edition import requires_edition, Edition

@mcp.tool()
@requires_edition(Edition.SUITE)
def suite_only_tool() -> str:
    """This tool requires Suite edition."""
    ...
```

## Checklist

- [ ] Tool defined in `server.py`
- [ ] Handler added to `__init__.py`
- [ ] Command routing added
- [ ] Syntax check passes
- [ ] Tool appears in `just mcp-tools`
- [ ] `just doctor` passes
- [ ] `TOOLS.md` updated
