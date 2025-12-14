# SOTA Researcher MCP Command v2

## Primary Objective

**Simplified SOTA researcher using DeepAgents for automatic research and planning.**

This v2 version leverages `deepagents` to automatically handle research orchestration, reducing manual code by ~60% while improving performance through built-in capabilities.

---

## Key Improvements Over v1

### Simplified Architecture

- **~60% less code**: Leverages deepagents instead of manual orchestration
- **Automatic planning**: Uses deepagents' built-in `write_todos` tool
- **Context management**: Built-in filesystem middleware handles file operations
- **Parallel processing**: Deepagents subagents handle parallel research automatically

### Performance Benefits

- **Better parallelization**: Deepagents automatically parallelizes independent tasks
- **Smarter context management**: Filesystem middleware prevents context overflow
- **Reduced overhead**: Less manual orchestration means lower latency
- **Adaptive planning**: Agent adapts research strategy based on findings

---

## Installation

**⚠️ Important: Use the installer to ensure all dependencies are correctly installed.**

The SOTA Researcher v2 requires proper installation of all dependencies. Run the installer:

```bash
# From project root
./scripts/deepagents/install_sota_researcher_v2.sh
```

The installer will:

- ✅ Verify Python 3.12+ is installed
- ✅ Install/verify uv package manager
- ✅ Install all required dependencies (deepagents, fastmcp, langchain-mcp-adapters)
- ✅ Check MCP configuration
- ✅ Validate recommended MCP servers
- ✅ Test server startup
- ✅ Create validation script

**The v2 server will fail fast if dependencies are missing** (no graceful degradation) to prevent weird results.

---

## How to Run the SOTA Researcher v2 MCP Server

### Option 1: In Cursor (Recommended)

The MCP server is automatically started by Cursor when configured in `.cursor/mcp.json`:

#### 1. Verify MCP Configuration

Add the v2 server to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "sota_researcher_v2": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "${workspaceFolder}",
        "python",
        "${workspaceFolder}/scripts/deepagents/sota_researcher_v2.py"
      ],
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    }
  }
}
```

#### 2. Restart Cursor

After updating the configuration:

1. **Restart Cursor** to load the new MCP server configuration
2. The server will automatically start when you use MCP tools

#### 3. Use the Tools

Once configured, you can use the tools directly in Cursor chat:

```
Research and plan v2: How to optimize vector search latency. Questions: What are best practices? What libraries exist?
```

Or:

```
Research v2: Vector search optimization techniques. Limit to 5 results
```

### Option 2: Manual Testing (Command Line)

To test the server manually:

```bash
# From the project root
cd /home/zhouk2404/expert-deepagents-stg

# Run the server directly (will wait for stdio input)
uv run python scripts/deepagents/sota_researcher_v2.py
```

**Note:** When run directly, the server uses stdio transport and waits for MCP protocol messages. This is mainly for testing.

### Option 3: Using Python Directly

You can also import and use the functions directly in Python:

```python
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.deepagents.sota_researcher_v2 import research_and_plan, research_only

async def main():
    # Research and plan
    result = await research_and_plan(
        topic="Vector search optimization",
        research_questions=["What are best practices?", "What libraries exist?"]
    )
    print(result)

    # Research only
    result = await research_only(
        topic="FastAPI best practices",
        max_results=5
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Available Tools

### 1. `research_and_plan`

Conduct SOTA research and create a comprehensive plan using DeepAgents.

**Parameters:**

- `topic` (required): Research topic
- `research_questions` (optional): List of specific research questions (can be provided as a list or None)
- `output_path` (optional): Path to save research results (can be a string or None)

**Returns:**

- `success`: bool - Whether research succeeded
- `research_results`: dict - Research findings (agent-generated content)
- `plan`: dict - Generated plan (agent-created)
- `latency_ms`: float - Research latency in milliseconds

**Example Usage:**

```
Research and plan v2: How to optimize vector search latency. Questions: What are best practices? What libraries exist?
```

### 2. `research_only`

Conduct research only (no planning) using DeepAgents.

**Parameters:**

- `topic` (required): Research topic
- `max_results` (optional, default: 10): Maximum number of research results (hint for agent)

**Returns:**

- `success`: bool - Whether research succeeded
- `results`: dict - Research results (agent-generated content)
- `latency_ms`: float - Research latency in milliseconds

**Example Usage:**

```
Research v2: Vector search optimization techniques. Limit to 5 results
```

---

## Usage Examples

### Research and Plan

**Basic research with plan:**

```
Research and plan v2: How to implement automated code review
```

**With specific questions (automatically parallelized by deepagents):**

```
Research and plan v2: Optimizing database queries. Questions: What indexing strategies work best? How to measure query performance? What tools are available?
```

**Save results to file:**

```
Research and plan v2: Machine learning model deployment. Save results to .cursor/research/ml_deployment.md
```

### Research Only

**Quick research:**

```
Research v2: FastAPI best practices
```

**Limited results:**

```
Research v2: Python async patterns. Show only top 3 results
```

---

## MCP Server Details

**Server Name:** `sota_researcher_v2`
**Script Location:** `scripts/deepagents/sota_researcher_v2.py`
**MCP Configuration:** Defined in `.cursor/mcp.json`

**Underlying Implementation:**

- **DeepAgents**: Uses `create_deep_agent` for automatic orchestration
- **MCP Tools**: Automatically loads tools from configured MCP servers:
  - **docs-langchain**: Searches LangChain documentation
  - **Context7**: Retrieves library documentation
  - **indexing-semantic-search-v2**: Semantic search from codebase
  - **tavily-remote-mcp**: Web search for real-time information
  - **filesystem**: Built-in filesystem middleware for file operations
  - **memory**: Memory persistence (via MCP if available)
- **Built-in Capabilities**:
  - **Planning Tool**: `write_todos` for task decomposition
  - **Filesystem Middleware**: Automatic context management
  - **SubAgent Support**: Automatic parallelization for complex tasks
- Includes OpenTelemetry tracing for observability

**Performance Characteristics:**

- **Code Reduction**: ~60% less code than v1
- **Automatic Parallelization**: Deepagents handles parallel tasks automatically
- **Context Management**: Built-in filesystem middleware prevents overflow
- **Adaptive Planning**: Agent adapts strategy based on findings

---

## How It Works

### v1 vs v2 Architecture

**v1 (Manual Orchestration):**

1. Manually calls each MCP tool
2. Manually merges results
3. Manually deduplicates
4. Manually creates plan
5. Manually saves files

**v2 (DeepAgents Orchestration):**

1. Creates deepagent with all MCP tools (cached for performance)
2. Provides research prompt
3. Agent automatically:
   - Plans research strategy
   - Calls relevant tools
   - Manages context
   - Synthesizes findings
   - Creates plan
   - Saves results

### DeepAgents Integration

SOTA Researcher v2 is built on top of the deepagents library, which provides:

- **LangGraph**: Underlying graph execution and state management
- **LangChain**: Tools and model integrations
- **LangSmith**: Observability, evaluation, and deployment

The agent is a LangGraph state graph that can be:

- Traced in LangSmith for debugging
- Evaluated using RAGAS metrics
- Deployed via LangSmith Deployment
- Monitored in production

### Built-in Capabilities

Deepagents provides powerful built-in tools that the research agent uses:

#### Planning Tool: `write_todos`

- Break down complex research tasks into discrete, manageable steps
- Track progress as each step is completed
- Adapt plans dynamically based on findings
- Example: Agent creates a todo list like "1. Research vector databases, 2. Compare performance metrics, 3. Synthesize findings"

#### Filesystem Tools: `read_file`, `write_file`, `edit_file`, `ls`, `glob`, `grep`

- **Context Management**: Save large research results to files to prevent context window overflow
- **Persistence**: Store research findings for future reference
- **Incremental Updates**: Edit files to build up research documents
- **File Operations**: List, search, and manage research files
- Example: Agent saves 50KB of research findings to a file, then reads it back when needed

#### SubAgent Tool: `task`

- Spawn specialized subagents for independent research questions
- Provides context isolation - subagents work in separate contexts
- Automatic parallelization - multiple subagents can work simultaneously
- Example: For 3 research questions, agent spawns 3 subagents that work in parallel

### DeepAgents Benefits

1. **Automatic Planning**: Agent uses `write_todos` to break down complex tasks
2. **Context Management**: Filesystem middleware automatically handles large results
3. **Parallel Processing**: Subagents automatically handle independent research questions
4. **Adaptive Strategy**: Agent adapts based on what it finds
5. **Error Recovery**: Agent can retry or adjust strategy on errors

### Performance Optimization

**Agent Caching**: The research agent is created once and cached for reuse across multiple research calls. This provides:

- **Faster Response Times**: No agent creation overhead on subsequent calls
- **Consistent State**: Same agent instance maintains context
- **Resource Efficiency**: Reduced memory and initialization costs

The agent is automatically cached after the first use and reused for all subsequent research requests.

---

## Troubleshooting

### Server Not Starting

**First, run the installer:**

```bash
./scripts/deepagents/install_sota_researcher_v2.sh
```

If issues persist:

1. **Check MCP Configuration:**

   ```bash
   cat ~/.cursor/mcp.json | jq '.mcpServers["sota_researcher_v2"]'
   ```

2. **Run Validation Script:**

   ```bash
   uv run python scripts/deepagents/validate_sota_researcher_v2.py
   ```

3. **Verify Dependencies:**

   ```bash
   uv run python -c "from deepagents import create_deep_agent; print('DeepAgents available')"
   uv run python -c "from mcp.server.fastmcp import FastMCP; print('MCP available')"
   ```

4. **Test Server Directly:**

   ```bash
   uv run python scripts/deepagents/sota_researcher_v2.py
   ```

   (Should wait for stdio input without errors)

### Tools Not Available in Cursor

1. **Restart Cursor** after updating `.cursor/mcp.json`
2. **Check Cursor MCP Settings:**
   - Open Cursor Settings → MCP
   - Verify `sota_researcher_v2` appears in the list
   - Check for any error messages

3. **Check Server Logs:**
   - Look for errors in Cursor's developer console
   - Check if the server process is running

### DeepAgents Not Available

**Run the installer:**

```bash
./scripts/deepagents/install_sota_researcher_v2.sh
```

If you still see import errors:

```bash
# Verify deepagents is installed
uv run python -c "import deepagents; print(deepagents.__version__)"

# Check if it's in the path
uv run python -c "import sys; print('\n'.join(sys.path))"

# Re-sync dependencies
uv sync
```

### MCP Tools Not Loading

**The v2 server will fail fast if MCP tools are not available** (no graceful degradation).

If you see errors about MCP tools:

1. **Run the installer** to verify MCP configuration:

   ```bash
   ./scripts/deepagents/install_sota_researcher_v2.sh
   ```

2. **Verify MCP Configuration**: Ensure other MCP servers are configured in `~/.cursor/mcp.json`
   - At least one of: `docs-langchain`, `Context7`, `tavily-remote-mcp`, `indexing-semantic-search-v2`, `filesystem`, `memory` must be configured

3. **Check MCP Client**: The v2 server automatically loads tools from configured MCP servers
   - If no tools are available, the server will raise an error with clear instructions

4. **Test MCP Client**:

   ```python
   from langchain_mcp_adapters.client import MultiServerMCPClient
   # Test client creation
   ```

---

## Best Practices

1. **Be specific**: Provide clear, focused research topics for better results
2. **Use research questions**: Frame specific questions to guide the research direction
3. **Trust the agent**: Deepagents will automatically plan and execute research
4. **Save important research**: Use `output_path` to save research results for future reference
5. **Let it parallelize**: Multiple research questions are automatically handled in parallel

---

## Research vs Planning

**Use `research_only` when:**

- You need quick information gathering
- You want to explore a topic without committing to a plan
- You're doing preliminary research
- Speed is more important than comprehensive planning

**Use `research_and_plan` when:**

- You need actionable next steps
- You want structured guidance
- You're ready to move from research to implementation
- You need comprehensive research with planning

---

## Error Handling

If research fails:

- Verify the topic is clear and specific
- Check that research questions are well-formed
- Ensure DeepAgents is properly installed
- Verify MCP tools are available
- Review error messages for specific issues

---

## Migration from v1

If you're currently using v1, migrating to v2 is straightforward:

1. **Update MCP Configuration**: Change server name from `sota-researcher` to `sota_researcher_v2`
2. **Update Tool Names**: Use `research_and_plan` and `research_only` (same names, but v2 implementation)
3. **Expect Different Output Format**: v2 returns agent-generated content instead of structured dicts
4. **Restart Cursor**: After updating configuration

**Note**: v1 and v2 can coexist - you can have both configured and choose which to use.

---

## Evaluation

SOTA Researcher v2 can be evaluated using RAGAS metrics integrated with MLflow for tracking research quality over time.

### Running Evaluations

Use the evaluation script to measure agent performance:

```bash
# Run evaluation
uv run python scripts/deepagents/evaluate_sota_researcher_v2.py
```

The evaluation script:

- Creates test datasets with research topics
- Runs the agent on test cases
- Measures quality using RAGAS metrics (answer_relevancy, context_precision, context_recall, faithfulness)
- Logs all metrics to MLflow for tracking

### Evaluation Metrics

The evaluation uses standard RAGAS metrics:

- **Answer Relevancy**: How relevant is the research output to the topic?
- **Context Precision**: How precise is the information retrieved?
- **Context Recall**: How complete is the information coverage?
- **Faithfulness**: How faithful is the output to the sources?

### MLflow Integration

All evaluation metrics are automatically logged to MLflow:

- View results in MLflow UI: `http://localhost:5000`
- Track experiments over time
- Compare different agent versions
- Monitor performance trends

### CI/CD Integration

The evaluation can be run as part of CI/CD pipelines:

```bash
# In CI/CD
uv run python scripts/deepagents/evaluate_sota_researcher_v2.py --dataset-name sota-researcher-v2-test
```

See `scripts/deepagents/evaluate_sota_researcher_v2.py` for details.

---

*This command connects to the sota_researcher_v2 MCP server. The MCP server must be running and configured in `.cursor/mcp.json`. DeepAgents must be installed for this server to work.*
