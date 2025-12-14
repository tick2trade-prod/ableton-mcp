# Research → Memorize → Generate Workflow

## Overview

Complete workflow that researches from memory, uses web search for latest information, memorizes comprehensive findings, and generates code.

## Usage

Type `/research-memorize-generate` followed by your research topic and generation task.

## Parameters

- `research_topic`: Topic to research (required)
- `research_questions`: Optional list of specific research questions
- `generation_task`: Code generation task (required)
- `language`: Programming language (default: python)

## Example Usage

### Complete Research and Code Generation

```
/research-memorize-generate
Research Topic: FastAPI async patterns
Research Questions:
- What are best practices for async database connections?
- How to use Redis for caching in FastAPI?
- What are latest patterns for error handling?
Generation Task: Create a FastAPI endpoint with async database connection and Redis caching
Language: python
```

### Research with Code Generation

```
/research-memorize-generate
Research Topic: Vector search optimization
Generation Task: Create a vector search service using LanceDB with caching and batch operations
Language: python
```

## Workflow

1. **Research from Memory**: Check GAM memory for existing knowledge (via `app.research.AutonomousResearcher`)
2. **Web Search**: Use Tavily for latest best practices and documentation
3. **Memorize**: Save comprehensive findings to GAM memory
4. **Generate**: Create code using research findings and best practices (via `app.generation.CodeGenerator`)

## Implementation

This command uses the `app.research.AutonomousResearcher` and `app.generation.CodeGenerator` classes from the refactored `app/` structure:
- Research orchestration: `app.research.AutonomousResearcher`
- Code generation: `app.generation.CodeGenerator`
- Core GAM integration: `app.core.GAMMemoryManager`

## Best Practices

- Always research from memory first (faster, local tokens)
- Use Tavily for current/real-time information
- Memorize comprehensive findings (combining memory + web)
- Generate code using research findings
- Include specific requirements in generation task
