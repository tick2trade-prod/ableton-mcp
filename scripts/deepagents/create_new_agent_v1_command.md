# Create New Agent MCP Command

## Primary Objective

**Trigger create-new-agent MCP server tools for automating DeepAgent creation.**

This command provides access to the `create-new-agent` MCP server (`scripts/deepagents/create_new_agent_v1.py`) which automates the creation of new DeepAgents following proven patterns.

---

## 💰 Cost-Free Usage with Ollama

**With Ollama (local LLM), sequential-thinking is FREE and improves performance!**

### Quick Setup with Ollama

1. **Install and start Ollama:**

   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh

   # Start Ollama
   ollama serve

   # Pull a model
   ollama pull llama3.2
   ```

2. **Configure MCP (default configuration works):**

   ```json
   {
     "mcpServers": {
       "create-new-agent": {
         "command": "uv",
         "args": [
           "run",
           "--directory",
           "${workspaceFolder}",
           "python",
           "${workspaceFolder}/scripts/deepagents/create_new_agent_v1.py"
         ],
         "env": {
           "PYTHONPATH": "${workspaceFolder}"
         }
       }
     }
   }
   ```

3. **Use with full features:**

   ```
   Create new agent: code_generator
   Description: Generates Python code based on requirements
   Requirements: Should use filesystem MCP and support validation
   ```

**What you get (all enabled by default):**

- ✅ **Sequential-thinking** - FREE with Ollama - Improves planning structure
- ✅ **LangChain Documentation** - DeepAgents best practices
- ✅ **Context7 Library Docs** - Library documentation
- ✅ **Codebase Search** - Pattern analysis from existing agents
- ✅ **SOTA Researcher** - Research agent patterns
- ✅ **Filesystem** - Write generated files
- ✅ **Memory** - Cache agent specifications

**Total cost: $0.00** (with Ollama + free tools) 🎉

---

## Installation & Setup

### Step 1: Run the Installer (Required)

Before using Create New Agent, ensure prerequisites are configured:

```bash
# Install sota_researcher_v1 first (used internally)
uv run python scripts/deepagents/install_sota_researcher_v1.py --install
```

### Step 2: Verify Installation

After installation, validate everything works:

```bash
uv run python scripts/deepagents/install_sota_researcher_v1.py --validate-only
```

---

## How to Run the Create New Agent MCP Server

### Option 1: In Cursor (Recommended)

The MCP server is automatically started by Cursor when configured in `.cursor/mcp.json`.

#### 1. Verify MCP Configuration

The server should be configured in `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "create-new-agent": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "${workspaceFolder}",
        "python",
        "${workspaceFolder}/scripts/deepagents/create_new_agent_v1.py"
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
Create agent spec: code_generator
Description: Generates Python code based on requirements
Requirements: Should use filesystem MCP
```

---

## Available Tools

### 1. `create_agent_spec`

Research and create agent specification.

**Parameters:**

- `agent_name` (required): Name of agent to create (e.g., "code_generator")
- `description` (required): What the agent should do
- `requirements` (optional): Specific requirements or features

**Returns:**

- `success`: bool - Whether spec creation succeeded
- `spec`: dict - Agent specification with functions, MCP tools, system prompt
- `latency_ms`: float - Creation latency in milliseconds

**Example Usage:**

```
Create agent spec: code_generator
Description: Generates Python code based on requirements
Requirements: Should use filesystem MCP and support validation
```

### 2. `generate_agent_files`

Generate all 5 required files from specification.

**Parameters:**

- `spec` (required): Agent specification from `create_agent_spec`
- `output_dir` (optional): Directory to save files

**Returns:**

- `success`: bool - Whether generation succeeded
- `files`: dict - Generated file contents (agent_main.py, mcp_server.py, etc.)
- `file_paths`: dict - Suggested file paths
- `latency_ms`: float - Generation latency

**Example Usage:**

```
Generate agent files from spec: {spec from create_agent_spec}
```

### 3. `validate_agent_files`

Validate generated files.

**Parameters:**

- `files` (required): Dictionary of filename -> file content

**Returns:**

- `valid`: bool - Whether files are valid
- `errors`: list - Syntax errors found
- `warnings`: list - Pattern warnings
- `latency_ms`: float - Validation latency

**Example Usage:**

```
Validate agent files: {files from generate_agent_files}
```

---

## Usage Examples

### Complete Workflow

**Step 1: Create Specification**

```
Create agent spec: code_generator
Description: Generates Python code based on requirements
Requirements: Should use filesystem MCP, support validation, follow sota_researcher_v1 pattern
```

**Step 2: Generate Files**

```
Generate agent files from spec: {use spec from step 1}
```

**Step 3: Validate Files**

```
Validate agent files: {use files from step 2}
```

### Quick Agent Creation

```
Create new agent: test_runner
Description: Runs tests and reports results
```

---

## MCP Server Details

**Server Name:** `create-new-agent`
**Script Location:** `scripts/deepagents/create_new_agent_v1.py`
**MCP Configuration:** Defined in `.cursor/mcp.json`

**Underlying Implementation:**

**DeepAgents Mode (Default Implementation):**

- **DeepAgents**: Uses `create_deep_agent` for automatic orchestration
- **MCP Tools**: Automatically loads tools from configured MCP servers:
  - **sequential-thinking**: Structures planning approach
  - **docs-langchain**: DeepAgents documentation and best practices
  - **Context7**: Library documentation
  - **indexing-semantic-search-v2**: Codebase pattern search
  - **sota-researcher**: Research agent patterns (used internally)
  - **filesystem**: Write generated files
  - **memory**: Cache agent specifications
- **Built-in Capabilities**:
  - **Planning Tool**: `write_todos` for task decomposition
  - **Filesystem Middleware**: Automatic context management
  - **SubAgent Support**: Automatic parallelization for complex tasks
- **Automatic Planning**: Agent uses `write_todos` tool automatically
- **Pattern Following**: Generates files following sota_researcher_v1 pattern exactly

**Performance Characteristics:**

- **Latency**: 5-10 minutes for complete agent creation (research + generation)
- **Quality**: Follows proven patterns from sota_researcher_v1
- **Completeness**: Generates all 5 required files

---

## Generated Files

The agent generates 5 files following the sota_researcher_v1 pattern:

1. **`{agent_name}_v1.py`** - Main agent implementation
   - Follows `sota_researcher_v1.py` structure
   - Uses DeepAgents for orchestration
   - Includes MCP tool integration

2. **`mcp_server_{agent_name}_v1.py`** - MCP server wrapper
   - Follows `mcp_server_deepagents_v1.py` pattern
   - Exposes agent functions as MCP tools

3. **`evaluate_{agent_name}_v1.py`** - Evaluation script
   - Follows `evaluate_sota_researcher_v1.py` pattern
   - MLflow integration
   - Test data creation

4. **`test_{agent_name}_v1.py`** - Test file
   - Follows `test_sota_researcher_v1.py` pattern
   - Unit and integration tests
   - Mock MCP tools

5. **`{agent_name}_v1_command.md`** - Command documentation
   - Follows `sota_researcher_v1_command.md` pattern
   - Usage examples
   - Installation guide

---

## Best Practices

1. **Be specific**: Provide clear agent name and description
2. **Include requirements**: Specify MCP tools and features needed
3. **Review generated files**: Always review before using
4. **Run tests**: Execute generated tests to verify
5. **Validate**: Use validate_agent_files before committing

---

## Troubleshooting

### First: Run the Installer

If you're experiencing issues, **first run the installer**:

```bash
uv run python scripts/deepagents/install_sota_researcher_v1.py --install
```

### Server Not Starting

1. **Check MCP Configuration:**

   ```bash
   cat ~/.cursor/mcp.json | jq '.mcpServers["create-new-agent"]'
   ```

2. **Verify Dependencies:**

   ```bash
   uv run python -c "from deepagents import create_deep_agent; print('DeepAgents available')"
   ```

3. **Test Server Directly:**

   ```bash
   uv run python scripts/deepagents/create_new_agent_v1.py
   ```

### Validation Errors

If validation fails:

- Check syntax errors in generated files
- Verify imports are correct
- Ensure patterns match sota_researcher_v1

---

## Evaluation

### MLflow Evaluation

The create_new_agent_v1 agent can be evaluated using MLflow for tracking performance.

**Run evaluation:**

```bash
uv run python scripts/deepagents/evaluate_create_new_agent_v1.py
```

**Features:**

- Tests agent creation quality
- Measures latency for each step
- Logs results to local MLflow instance
- Creates test dataset with agent creation scenarios

**Prerequisites:**

- MLflow server running locally or SQLite backend configured
- All MCP tools available

**View results:**

- Check MLflow UI at the configured tracking URI (default: `sqlite:///mlflow.db`)

---

*This command connects to the create-new-agent MCP server. The MCP server must be running and configured in `.cursor/mcp.json`.*
