# Gemini CLI Headless Mode

> Source: [https://geminicli.com/docs/cli/headless](https://geminicli.com/docs/cli/headless)

## Overview

Headless mode allows non-interactive use of Gemini CLI for scripting and automation.

## Usage

### Basic Headless Command

```bash
gemini --headless "Generate a Python function for BPM detection"
```

### With Input Files

```bash
gemini --headless "Explain this code" -f tests/test_tools.py
```

### Pipeline Usage

```bash
cat error.log | gemini --headless "Summarize these errors"
```

## Automation Scripts

### Test Analysis

```bash
#!/bin/bash
# analyze_tests.sh

pytest tests/ -v 2>&1 | gemini --headless "Analyze these test results and suggest fixes"
```

### Code Review

```bash
#!/bin/bash
# review.sh

git diff HEAD~1 | gemini --headless "Review these changes for issues"
```

### Documentation Generation

```bash
#!/bin/bash
# generate_docs.sh

for file in src/**/*.py; do
  gemini --headless "Generate docstrings for:" -f "$file" > "${file%.py}.md"
done
```

## ableton-mcp Automation

### Test Automation

```bash
#!/bin/bash
# scripts/analyze_failing_tests.sh

failing_tests=$(pytest tests/ -v 2>&1 | grep FAILED)

if [ -n "$failing_tests" ]; then
  echo "$failing_tests" | gemini --headless \
    "These Ableton MCP tests failed. Analyze and suggest fixes based on common patterns."
fi
```

### Track Script Generation

```bash
#!/bin/bash
# scripts/generate_track.sh

TRACK_TYPE=$1
TRACK_NAME=$2

gemini --headless \
  "Generate an Ableton track script for a $TRACK_TYPE track named $TRACK_NAME
   following the patterns in live_set/lily_palmer/i_am_machine/" \
  -d live_set/lily_palmer/i_am_machine/ \
  > "live_set/new/${TRACK_NAME}.py"
```

### MCP Tool Generation

```bash
#!/bin/bash
# scripts/new_mcp_tool.sh

TOOL_NAME=$1
DESCRIPTION=$2

gemini --headless \
  "Create a new MCP tool named $TOOL_NAME that: $DESCRIPTION
   Follow the patterns in mcp_servers/" \
  -d mcp_servers/ \
  > "mcp_servers/new/${TOOL_NAME}.py"
```

## Output Formats

### JSON Output

```bash
gemini --headless --json "List files in tests/"
```

### Quiet Mode

```bash
gemini --headless --quiet "Run tests" 2>/dev/null
```

### Stream Output

```bash
gemini --headless --stream "Generate documentation"
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review

on: pull_request

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Gemini CLI
        run: npm install -g @google/gemini-cli
      - name: Run AI Review
        env:
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
        run: |
          git diff origin/main | gemini --headless "Review these changes"
```

### Makefile Integration

```makefile
# Makefile

.PHONY: ai-review
ai-review:
	git diff HEAD~1 | gemini --headless "Review my changes"

.PHONY: ai-docs
ai-docs:
	gemini --headless "Generate README from code" -d src/ > README.md
```

## Related Pages

- [Commands](commands.md) - All CLI options
- [MCP](mcp.md) - Use MCP tools in headless mode
- [Examples](examples.md) - More examples
