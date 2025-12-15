# Validate Architecture

## Overview

Runs the "Critic" agent to check for hallucinations and anti-patterns before coding begins. Prevents wasted effort on invalid approaches.

## Usage

Type `/validate-architecture` followed by your proposed plan or code snippet.

## Parameters

- `plan`: Architecture plan or code snippet to validate (required)
- `tech_stack`: Technologies being used (optional)
- `strict_mode`: Fail on any warnings (default: false)

## Example Usage

### Validate Plan

```
/validate-architecture
Plan: Use FastAPI with SQLAlchemy and Pydantic for REST API
Tech Stack: Python 3.12, FastAPI, SQLAlchemy, PostgreSQL
```

### Validate Code Snippet

```
/validate-architecture
Plan: |
  from some_package import NonExistentClass

  def process():
      return NonExistentClass().method()
Strict Mode: true
```

### Quick Package Check

```
/validate-architecture
Plan: Install and use langchain-anthropic, fastmcp, deepagents
```

## Workflow

1. **Package Verification**:
   - Extract all `import` statements or dependency requirements
   - Call `package_tool.validate_dependencies(deps_list)`
   - **CRITICAL**: If any package returns `exists=False`, halt and report "Hallucination Detected"

2. **Anti-Pattern Scan**:
   - Search GAM memory for "bugs" or "failures" related to current tech stack
   - If match found (similarity > 0.8), alert: "This approach previously failed due to [reason]"

3. **Architecture Critique**:
   - Invoke `Critic` agent with `CRITIC_SYSTEM_PROMPT`
   - Request `QAReport` (JSON)
   - If `score < 80`, output `suggested_fix` and do not proceed to code generation

4. **Output**:
   - Display checklist:
     - [ ] Packages Validated
     - [ ] Security Scan Passed (No shell injections)
     - [ ] Memory Check Passed (No known failures)
     - [ ] Architecture Score: X/100

## Best Practices

- Run before starting any new feature
- Use strict_mode for production code
- Review suggested fixes carefully
- Update GAM memory with validation results
- Fail fast on hallucinated packages

## Related Commands

- `/generate-code-streaming` - Generate after validation
- `/batch-implement` - Batch generation after validation
- `/deep-research` - Research before planning
