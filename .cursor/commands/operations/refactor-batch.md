# Refactor Batch

## Overview

Apply refactoring patterns across multiple files in parallel. Perfect for large-scale code modernization, pattern migration, or technical debt cleanup.

## Usage

Type `/refactor-batch` followed by refactoring description.

## Parameters

- `pattern`: Refactoring pattern to apply (required)
- `target`: Files or directories to refactor (default: current directory)
- `max_concurrent`: Maximum parallel operations (default: 5)
- `dry_run`: Preview changes without applying (default: false)
- `backup`: Create backups before refactoring (default: true)

## Guardrails (must follow before running)

- Read `AGENTS.md` and service-specific guides in target area; respect submodule rules (no stray pointer changes).
- Start with `dry_run: true` to preview; only flip to apply after reviewing the plan with a human.
- Keep backups enabled unless the target dir already has an agreed rollback path.
- Run `make validate-submodules` (root) if any refactor touches git submodules or nested repos.
- Add or update tests when behavior changes; never skip existing test suites without a note and reason.
- For MCP adapters (e.g., AbletonMCP), verify upstream tool contracts and connection settings before altering call sites.

## Example Usage

### Modernize Async Patterns

```
/refactor-batch
Pattern: Convert all synchronous database calls to async/await
Target: app/services/
Max Concurrent: 5
Dry Run: false
```

### Type Hints Migration

```
/refactor-batch
Pattern: Add comprehensive type hints to all functions
Target: app/
Backup: true
```

### Hard Guardrails for External Tooling (AbletonMCP example)

```
/refactor-batch
Pattern: Align AbletonMCP tool invocations with upstream 16-tool set; add import guards
Target: deepagents_mcp_ableton/
Dry Run: true
Backup: true
Notes: Verify ableton-mcp import path (ableton_mcp.MCP_Server.server) and keep dependency hints intact.
```

### Error Handling Standardization

```
/refactor-batch
Pattern: Replace print statements with proper logging
Target: app/
Max Concurrent: 3
```

### Dependency Injection

```
/refactor-batch
Pattern: Refactor to use FastAPI dependency injection instead of globals
Target: app/api/
```

## Workflow

1. **Analyze Target Files**:
   - Scan specified files/directories
   - Identify refactoring candidates
   - Estimate impact and complexity

2. **Generate Refactoring Plan**:
   - Use Critic agent to validate pattern
   - Check for breaking changes
   - Identify dependencies between files

3. **Parallel Execution**:
   - Process independent files concurrently
   - Handle dependent files sequentially
   - Create backups if enabled

4. **Validation**:
   - Run linters on refactored code
   - Execute tests to ensure no breakage
   - Generate diff summary

5. **Rollback Support**:
   - Keep backups for 24 hours
   - Provide rollback command if issues found

## Common Refactoring Patterns

- **Async Migration**: Sync → async/await
- **Type Safety**: Add type hints, use Pydantic
- **Error Handling**: Try/except → custom exceptions
- **Logging**: Print → structured logging
- **Testing**: Add missing tests
- **Documentation**: Add docstrings
- **Security**: Fix SQL injection, XSS vulnerabilities
- **Performance**: Optimize queries, add caching

## Best Practices

- Always use dry_run first to preview changes
- Keep backups enabled for safety
- Run tests after refactoring (or explain why they were skipped)
- Refactor in small batches
- Review diffs carefully
- Commit frequently
 - When changing dependency imports, include explicit guardrails/error messages so failures are obvious to users

## Safety Features

- Automatic backup creation
- Dry-run mode for preview
- Test execution validation
- Rollback support
- Dependency analysis

## Related Commands

- `/qa-critic` - Validate refactoring quality
- `/batch-implement` - Generate new code
- `/validate-architecture` - Check patterns
