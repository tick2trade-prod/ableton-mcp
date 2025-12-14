# Autonomous Research

## Overview

Autonomous research workflow that uses GAM memory first, then Tavily for latest information, memorizes findings, and can generate code or provide insights.

## Usage

Type `/autonomous-research` followed by your research topic.

## Parameters

- `topic`: Research topic (required)
- `research_questions`: Optional list of specific research questions
- `generate_code`: Whether to generate example code (default: false)
- `language`: Programming language for code generation (default: python)

## Example Usage

### Research Only

```
/autonomous-research
Topic: Ollama integration patterns for code generation
Research Questions:
- How to properly configure Ollama for local LLM?
- What are best practices for tool calling with Ollama?
- How to optimize Ollama performance?
```

### Research with Code Generation

```
/autonomous-research
Topic: FastAPI async patterns with Redis caching
Generate Code: true
Language: python
```

### Comprehensive Research

```
/autonomous-research
Topic: Workflow orchestration for code generation using available packages
Research Questions:
- How to use celery for async task execution?
- How to use prefect for workflow orchestration?
- How to integrate MLflow for experiment tracking?
Generate Code: true
Language: python
```

## Workflow

1. **Memory Research**: Check GAM memory for existing knowledge (via `app.research.AutonomousResearcher`)
2. **Web Research**: Use Tavily for latest documentation and best practices
3. **Memorization**: Save comprehensive findings to GAM memory
4. **Code Generation** (optional): Generate example code using findings (via `app.generation.CodeGenerator`)

## Implementation

This command uses the `app.research.AutonomousResearcher` class from the refactored `app/` structure:
- Core GAM integration: `app.core.GAMMemoryManager`
- Research orchestration: `app.research.AutonomousResearcher`
- Code generation: `app.generation.CodeGenerator`

## Best Practices

- Use specific, descriptive research topics
- Include research questions for focused research
- Memorize all findings for future use
- Generate code when examples are needed
- Leverage Docker services (MLflow, Redis, PostgreSQL) when applicable

## Requirements

- Ollama server running (for code generation)
- TAVILY_API_KEY set (for web research)
- Java/JDK installed (for GAM BM25 retriever, optional)
