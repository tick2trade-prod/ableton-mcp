# Tool Commands (HOW Layer)

Atomic tool operations for executing specific tasks.

## Available Tools (17 total)

### GAM Memory Tools
- **gam-memorize.md** - Memorize content to GAM
- **gam-memorize-op.md** - Atomic memorize operation
- **gam-research.md** - Research from GAM memory
- **gam-tool.md** - General GAM tool operations

### Code Tools
- **coder.md** - Code generation and file operations
- **lint-code.md** - Code linting and validation
- **computer.md** - Computer use (browser automation)
- **thinking.md** - Explicit reasoning tool

### Browser Tools
- **browser-action.md** - Browser automation actions
- **browser-navigate.md** - Navigate to URL
- **browser-screenshot.md** - Capture screenshots

### Package Tools
- **verify-packages.md** - Verify package existence (PyPI/NPM)
- **check-packages.md** - Check package versions
- **package-tool.md** - General package operations

### Search & Queue
- **search.md** - Search codebase or memory
- **check-task-status.md** - Check background task status
- **queue-task.md** - Queue task for background execution

### Execution
- **execute-tool.md** - Execute any tool by configuration

## Usage Pattern

```bash
/gam-memorize content="..." entity_type="feature"
/gam-research query="authentication patterns"
/verify-packages language="python" packages="fastapi,pydantic"
/lint-code file="src/app.py"
/browser-action action="navigate" url="https://example.com"
```

## Tool Categories

1. **Memory** - GAM operations (memorize, search, retrieve)
2. **Code** - Code generation, linting, validation
3. **Browser** - Web automation and scraping
4. **Package** - Dependency verification
5. **Search** - Code and memory search
6. **Queue** - Background task management

## Related

- Agents (WHO): `/agents/INDEX.md`
- Skills (WHAT): `/skills/INDEX.md`
- Registry: `/registry/3000_INDEX_TOOLS.md`
