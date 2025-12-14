# Generate Code

## Overview

Generate code with streaming support using GAM memory and best practices. Supports structured outputs for better code quality.

## Usage

Type `/generate-code` followed by the code generation task.

## Parameters

- `task`: Code generation task description (required)
- `language`: Programming language (default: python)
- `agent_name`: Optional agent name
- `use_structured_output`: Use structured output format (default: false)

## Example Usage

### Basic Code Generation

```
/generate-code
Task: Create a FastAPI endpoint with async database connection using Redis for caching
Language: python
```

### Code with Structured Output

```
/generate-code
Task: Generate a Pydantic model for user authentication with validation
Language: python
Use Structured Output: true
```

### Multi-file Code Generation

```
/generate-code
Task: Create a complete authentication system with:
1. User model (Pydantic)
2. Database connection (async)
3. JWT token generation
4. Password hashing
Language: python
```

## Workflow

1. Agent researches from GAM memory for relevant patterns (via `app.core.GAMMemoryManager`)
2. Agent generates code following best practices (via `app.generation.CodeGenerator`)
3. Code is streamed for real-time feedback (async streaming supported)
4. Structured output ensures type safety (if enabled)

## Implementation

This command uses the `app.generation.CodeGenerator` class from the refactored `app/` structure:
- Core GAM integration: `app.core.GAMMemoryManager`
- Code generation: `app.generation.CodeGenerator` with streaming support
- Research integration: Automatic GAM memory research before generation

## Best Practices

- Use clear, specific task descriptions
- Specify language for better results
- Use structured output for type-safe code
- Leverage GAM memory for project-specific patterns
- Include requirements and constraints in task description
