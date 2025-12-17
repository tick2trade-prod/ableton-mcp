---
description: Add a new MCP tool and validate end-to-end
---

## Add New MCP Tool

1. Define the tool in `MCP_Server/server.py`:
   - Use `@mcp.tool()` decorator
   - Add `@requires_edition(Edition.INTRO|STANDARD|SUITE)` for edition filtering
   - Include clear docstring with parameters

2. Add corresponding handler in `AbletonMCP_Remote_Script/__init__.py`:
   - Implement `_<tool_name>` method
   - Handle the command in `_process_command`

3. Update tool count:
// turbo
   ```bash
   just mcp-tools
   ```

4. Test connection:
// turbo
   ```bash
   just mcp-test
   ```

5. Run doctor to validate:
// turbo
   ```bash
   just doctor
   ```

6. Create test in `tests/test_tools.py`:
   ```python
   def test_<tool_name>():
       # Call the MCP tool
       # Assert expected result
   ```

7. Run the test:
   ```bash
   pytest tests/test_tools.py::test_<tool_name> -v
   ```

## Expected Result
- Tool appears in `just mcp-tools` output
- Doctor passes (4/4)
- Test passes
