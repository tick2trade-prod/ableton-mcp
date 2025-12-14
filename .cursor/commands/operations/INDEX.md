# Operations Commands Index

Code generation and refactoring operations for direct code manipulation.

---

## Commands

| Command | Purpose | Key Features |
|---------|---------|--------------|
| `generate-code.md` | Single code generation | Streaming, structured output, GAM context |
| `generate-code-batch.md` | Batch code generation | Parallel processing, 5-20x speedup |
| `refactor-batch.md` | Batch refactoring | Pattern migration, parallel execution |

---

## Usage Patterns

### Single Code Generation
```
/generate-code
Task: Create FastAPI endpoint with async database and Redis caching
Language: python
Use Structured Output: true
```

### Parallel Feature Generation
```
/generate-code-batch
Tasks:
1. User registration endpoint
2. User login endpoint
3. User profile endpoint
Language: python
Max Concurrent: 5
```

### Large-Scale Refactoring
```
/refactor-batch
Pattern: Convert synchronous database calls to async/await
Target: app/services/
Max Concurrent: 5
Dry Run: false
```

---

## Architecture Integration

Operations use the generation layer:

```
Operations
├── Code Generation
│   ├── app.generation.CodeGenerator
│   ├── app.core.GAMMemoryManager (context)
│   └── Streaming support
│
└── Refactoring
    ├── Pattern analysis
    ├── Parallel execution
    └── Validation (linting, tests)
```

---

## Performance

### Batch Operations
- **Parallel Processing**: 5-20x speedup
- **Max Concurrent**: Default 5, configurable
- **Partial Success**: Some tasks can fail without blocking others

### Safety Features
- **Dry Run Mode**: Preview changes before applying
- **Automatic Backups**: Created before refactoring
- **Test Validation**: Run tests after changes
- **Rollback Support**: Restore from backups if needed

---

## Best Practices

1. **Use batch operations** for multiple related tasks
2. **Preview with dry run** before large refactorings
3. **Keep backups enabled** for safety
4. **Run tests after operations** to verify correctness
5. **Leverage GAM memory** for project-specific patterns

---

## Related Directories

- `/workflows/` - Complete workflows including generation
- `/qa/` - Test generation and code review
- `/generation/` - Core generation implementation
