# Claude Artifacts

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## Overview

Artifacts are generated content that Claude creates during conversations.

## Types of Artifacts

### Code Files
Generated source code:
```python
# Generated: track_03_hihat.py
async def create_hihat_track():
    ...
```

### Documentation
Generated markdown, READMEs, etc.

### Plans
Implementation plans and task breakdowns.

### Diagrams
Visual representations (SVG, Mermaid).

## Working with Artifacts

### View Artifact
Claude presents artifacts inline or in dedicated view.

### Save Artifact
```
"Save that code to live_set/new/track_03_hihat.py"
```

### Modify Artifact
```
"Update the artifact to add error handling"
```

## ableton-mcp Artifacts

Common artifacts:
- Track scripts
- Test files
- MCP tools
- Documentation

### Example Flow
```
USER: Create a new track for hi-hats
CLAUDE: [Generates track script as artifact]
USER: Save it
CLAUDE: [Writes to file]
USER: Create tests for it
CLAUDE: [Generates test file as artifact]
```

## Related Pages

- [Agent Mode](agent-mode.md) - Multi-step generation
- [Commands](commands.md) - Saving artifacts
