# Examples

> Source: [https://geminicli.com/docs/get-started/examples](https://geminicli.com/docs/get-started/examples)

## Basic Usage

### Simple Query
```bash
gemini "What is the MCP protocol?"
```

### File Context
```bash
gemini "Explain this code" -f main.py
```

### Directory Context
```bash
gemini "Summarize this project" -d ./src
```

## Code Generation

### Create New File
```
> Create a Python function to calculate BPM from audio samples
[Generates code and optionally writes to file]
```

### Add to Existing
```
> Add error handling to tests/test_tools.py
[Modifies existing file]
```

## Testing Workflows

### Run and Analyze
```
> Run pytest on test_tools.py and analyze any failures
[Executes tests, analyzes output]
```

### Generate Tests
```
> Generate tests for src/ableton_mcp/client.py
[Creates test file]
```

## Research

### Web Search
```
> Search for best practices in MCP server development
[Uses google_web_search]
```

### Documentation
```
> Find Ableton documentation about sidechain compression
[Uses search tools]
```

## ableton-mcp Examples

### Track Creation
```
> Create a new rumble bass track following the lily_palmer patterns
-d live_set/lily_palmer/i_am_machine/
```

### MCP Tool Development
```
> Create a new MCP tool for tempo detection based on the existing tools
-d mcp_servers/
```

### Test Debugging
```
> The test in tests/test_tools.py::test_create_track times out.
> Analyze and fix it.
-f tests/test_tools.py
```

### Research + Implement
```
> Research sidechain compression techniques for techno, then implement
> a helper function in our project
```

## Interactive Session Example

```
$ gemini
> What's the structure of this project?
[Analyzes project]

> Focus on the MCP servers
[Examines mcp_servers/]

> Create a new tool for audio analysis
[Generates code]

> Add tests for it
[Generates tests]

> Run the tests
[Executes tests]

> Fix any failures
[Iterates on fixes]
```

## Related Pages

- [Interactive Mode](interactive-mode.md) - REPL details
- [Headless](headless.md) - Scripting
- [Tools](tools.md) - Available tools
