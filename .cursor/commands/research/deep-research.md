# Deep Research & Memorize

## Overview

"Think-First" research command that performs deep research on a topic and saves findings to GAM long-term memory.

## Usage

Type `/deep-research` followed by your research topic.

## Parameters

- `topic`: Research topic or question (required)
- `depth`: Research depth (quick, standard, deep) (default: standard)
- `save_to_gam`: Save findings to memory (default: true)
- `generate_report`: Generate markdown report (default: true)

## Example Usage

### Standard Research

```
/deep-research
Topic: How to implement vector search with Redis
Depth: standard
```

### Deep Dive

```
/deep-research
Topic: FastAPI best practices for production deployment
Depth: deep
Save to GAM: true
Generate Report: true
```

### Quick Lookup

```
/deep-research
Topic: Pydantic v2 migration guide
Depth: quick
```

## Workflow

1. **Plan Research**:
   - Generate 3 specific search queries based on user topic
   - Use `thinking_tool` to validate queries cover breadth and depth
   - Example: "FastAPI production" → ["FastAPI deployment best practices", "FastAPI performance optimization", "FastAPI security checklist"]

2. **Execute Search**:
   - Call `tavily_search` for each query in parallel
   - Call `gam.research_memory` to cross-reference existing knowledge
   - Deduplicate results

3. **Synthesize**:
   - Combine all results into structured markdown report
   - *Structure:*
     - Executive Summary
     - Technical Details
     - Code Examples
     - Best Practices
     - Common Pitfalls
     - References

4. **Memorize**:
   - Call `gam.memorize_content()` with synthesized report
   - Confirm: "Findings saved to GAM for future retrieval"
   - Tag with topic keywords for easy retrieval

## Research Depth

### Quick (1-2 minutes)
- 1-2 search queries
- GAM memory lookup only
- Brief summary

### Standard (3-5 minutes)
- 3-4 search queries
- GAM + web search
- Structured report

### Deep (5-10 minutes)
- 5-7 search queries
- Multiple sources
- Comprehensive report with examples

## Best Practices

- Use before starting unfamiliar tasks
- Review existing GAM memory first
- Save findings for team knowledge base
- Generate reports for documentation
- Cross-reference multiple sources
- Validate code examples before use

## Output Format

```markdown
# Research Report: [Topic]

## Executive Summary
[2-3 sentence overview]

## Technical Details
[Key concepts, architecture, patterns]

## Code Examples
[Tested, working examples]

## Best Practices
[Do's and don'ts]

## Common Pitfalls
[Known issues and solutions]

## References
[Sources with links]
```

## Related Commands

- `/validate-architecture` - Validate research findings
- `/generate-code-streaming` - Generate based on research
- `/research-memory` - Search existing GAM memory
- `/memorize-content` - Save custom content to GAM
