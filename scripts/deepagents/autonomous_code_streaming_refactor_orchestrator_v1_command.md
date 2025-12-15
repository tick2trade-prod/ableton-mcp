# Autonomous Code Streaming Refactor Orchestrator MCP Command

## Primary Objective

**Trigger autonomous-code-refactor MCP server tools for autonomous code refactoring workflows using streaming code generation.**

This command provides access to the `autonomous-code-refactor` MCP server (`scripts/deepagents/autonomous_code_streaming_refactor_orchestrator_v1.py`) which orchestrates code refactoring workflows using streaming code generation with Ollama.

---

## 💰 Cost-Free Usage with Ollama

**With Ollama (local LLM), all code generation is FREE!**

### Quick Setup with Ollama

1. **Install and start Ollama:**

   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh

   # Start Ollama
   ollama serve

   # Pull recommended models
   ollama pull codellama
   ollama pull llama3.2
   ```

2. **Configure MCP (add to ~/.cursor/mcp.json):**

   ```json
   {
     "mcpServers": {
       "autonomous-code-refactor": {
         "command": "uv",
         "args": [
           "run",
           "--directory",
           "${workspaceFolder}",
           "python",
           "${workspaceFolder}/scripts/deepagents/autonomous_code_streaming_refactor_orchestrator_v1.py"
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
   Analyze codebase for refactoring: scripts/deepagents/
   Refactoring goals: Improve error handling, add type hints, extract common patterns
   ```

**What you get (all enabled by default):**

- ✅ **Ollama Streaming Code Generation** - FREE local LLM for real-time code refactoring
- ✅ **Semantic Codebase Search** - Find patterns using indexing-semantic-search-v2
- ✅ **Structure-Aware Search** - Find complete functions/classes for refactoring
- ✅ **Git Integration** - Branch management, commit refactored code
- ✅ **Filesystem Operations** - Read/write code files
- ✅ **Sequential Thinking** - Structured refactoring planning (FREE with Ollama)
- ✅ **GitHub Integration** - PR creation for refactored code

**Total cost: $0.00** (with Ollama + free tools) 🎉

---

## Installation & Setup

### Step 1: Install Dependencies

```bash
# Install required packages
uv sync

# Ensure Ollama is running
ollama serve

# Pull recommended models
ollama pull codellama
```

### Step 2: Verify Installation

```bash
# Test Ollama
ollama run codellama "Hello, world!"

# Test agent
uv run python scripts/deepagents/autonomous_code_streaming_refactor_orchestrator_v1.py
```

---

## Available Tools

### 1. `analyze_codebase_for_refactoring`

Analyze codebase and identify refactoring opportunities.

**Parameters:**

- `target_path` (required): Path to analyze (file or directory)
- `refactoring_goals` (optional): List of refactoring goals

**Returns:**

- `success`: bool - Whether analysis succeeded
- `analysis`: dict - Analysis results with refactoring opportunities
- `target_path`: str - Analyzed path
- `refactoring_goals`: list - Refactoring goals
- `latency_ms`: float - Analysis latency in milliseconds

**Example Usage:**

```
Analyze codebase for refactoring: scripts/deepagents/
Refactoring goals: Improve error handling, add type hints, extract common patterns
```

### 2. `stream_refactor_code`

Stream refactored code generation using Ollama.

**Parameters:**

- `code` (required): Original code to refactor
- `refactoring_type` (required): Type of refactoring (e.g., "improve_error_handling", "extract_function")
- `model` (optional, default: "codellama"): Ollama model to use

**Returns:**

- `success`: bool - Whether refactoring succeeded
- `refactored_code`: str - Refactored code
- `original_length`: int - Length of original code
- `refactored_length`: int - Length of refactored code
- `latency_ms`: float - Refactoring latency in milliseconds

**Example Usage:**

```
Stream refactor code:
Code: def process(data): return [x*2 for x in data if x > 0]
Refactoring type: improve_error_handling
```

### 3. `orchestrate_refactoring_workflow`

Orchestrate complete refactoring workflow from analysis through PR creation.

**Parameters:**

- `target_path` (required): Path to refactor (file or directory)
- `refactoring_plan` (optional): Refactoring plan (if None, will be generated)
- `workflow_steps` (optional): List of steps to execute (default: all steps)

**Returns:**

- `success`: bool - Whether workflow succeeded
- `workflow_results`: dict - Results for each workflow step
- `target_path`: str - Refactored path
- `workflow_steps`: list - Executed workflow steps
- `latency_ms`: float - Total workflow latency

**Workflow Steps:**

- `setup` - Create git branch, initialize structure
- `analysis` - Analyze codebase, identify opportunities
- `refactor` - Generate refactored code using streaming
- `validate` - Run tests, check syntax, ensure compatibility
- `review` - Generate review checklist
- `pr_creation` - Create pull request

**Example Usage:**

```
Orchestrate refactoring workflow: scripts/deepagents/create_new_agent_v1.py
Refactoring plan: Extract streaming codegen into separate module, add error handling
Steps: analysis, refactor, validate, review
```

---

## Usage Examples

### Analyze Codebase

```
Analyze codebase for refactoring: scripts/deepagents/
Refactoring goals: Improve error handling, add type hints, extract common patterns
```

### Stream Refactor Code

```
Stream refactor code:
Code: |
  def process_data(data):
      result = []
      for item in data:
          if item > 0:
              result.append(item * 2)
      return result
Refactoring type: improve_error_handling
Model: codellama
```

### Complete Workflow

```
Orchestrate refactoring workflow: scripts/deepagents/create_new_agent_v1.py
Refactoring plan: Extract streaming codegen, add error handling, improve type hints
Steps: setup, analysis, refactor, validate, review, pr_creation
```

### Partial Workflow

```
Orchestrate refactoring workflow: app/mcp/
Refactoring goals: Add type hints, improve documentation
Steps: analysis, refactor, validate
```

---

## MCP Server Details

**Server Name:** `autonomous-code-refactor`
**Script Location:** `scripts/deepagents/autonomous_code_streaming_refactor_orchestrator_v1.py`
**MCP Configuration:** Defined in `~/.cursor/mcp.json`

**Underlying Implementation:**

- **DeepAgents**: Uses `create_deep_agent` for automatic orchestration
- **Ollama Integration**: Cost-free streaming code generation (replaces Claude API)
- **MCP Tools**: Automatically loads tools from configured MCP servers:
  - **git** - Git operations (branch management, commits)
  - **filesystem** - File operations (read/write code files)
  - **indexing-semantic-search-v2** - Codebase search and pattern discovery
  - **sequential-thinking** - Planning (FREE with Ollama)
  - **github** - PR creation
- **Streaming Code Generation**: Real-time code refactoring with Ollama
- **State Management**: Tracks refactoring progress and checkpoints

**Performance Characteristics:**

- **Latency**: Real-time streaming feedback
- **Token Usage**: Efficient streaming reduces memory usage
- **Cost**: $0.00 (100% free with Ollama)
- **Resume Capability**: Full state persistence for large refactorings

---

## Workflow Steps Details

### 1. Setup Phase

- Create git branch for refactoring
- Initialize directories
- Create refactoring plan document
- **Tools**: git, filesystem
- **Pattern**: Direct tool calls

### 2. Analysis Phase

- Analyze codebase for refactoring opportunities
- Use semantic search to find similar patterns
- Use structure-aware search for complete functions/classes
- Identify code smells and improvements
- **Tools**: indexing-semantic-search-v2, sequential-thinking
- **Pattern**: Semantic search + planning

### 3. Refactor Phase

- Generate refactored code using streaming Ollama
- Stream code chunks in real-time
- Handle large codebases with incremental streaming
- **Tools**: Ollama (streaming code generation), filesystem
- **Pattern**: Streaming code execution

### 4. Validate Phase

- Run tests before and after refactoring
- Validate code syntax and imports
- Check for breaking changes
- Ensure backward compatibility
- **Tools**: Test tools, syntax validators
- **Pattern**: Batch validation operations

### 5. Review Phase

- Generate review checklist
- Read refactored code
- Create review comments
- **Tools**: github, filesystem
- **Pattern**: Direct tools

### 6. PR Creation Phase

- Create pull request
- Add refactoring description
- Request reviewers
- **Tools**: github
- **Pattern**: Direct tool call

---

## Best Practices

1. **Incremental Refactoring**: Refactor in small, validated chunks
2. **Safety First**: Always run tests before and after refactoring
3. **Pattern Reuse**: Use semantic search to find similar patterns
4. **Streaming Efficiency**: Stream large refactorings in batches
5. **Checkpoint System**: Save progress frequently for resume capability
6. **Validation**: Multiple validation layers (syntax, tests, compatibility)

---

## Troubleshooting

### Ollama Not Running

1. **Check Ollama:**

   ```bash
   ollama list
   ```

2. **Start Ollama:**

   ```bash
   ollama serve
   ```

3. **Pull Models:**

   ```bash
   ollama pull codellama
   ```

### MCP Server Not Starting

1. **Check MCP Configuration:**

   ```bash
   cat ~/.cursor/mcp.json | jq '.mcpServers["autonomous-code-refactor"]'
   ```

2. **Verify Dependencies:**

   ```bash
   uv run python -c "from deepagents import create_deep_agent; print('DeepAgents available')"
   ```

3. **Test Server Directly:**

   ```bash
   uv run python scripts/deepagents/autonomous_code_streaming_refactor_orchestrator_v1.py
   ```

### Streaming Code Generation Issues

1. **Check Ollama Connection:**

   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Verify Model:**

   ```bash
   ollama list | grep codellama
   ```

3. **Test Streaming:**

   ```bash
   ollama run codellama "Refactor this code: def test(): pass"
   ```

---

## Evaluation

### MLflow Evaluation

The refactor orchestrator can be evaluated using MLflow for tracking performance.

**Run evaluation:**

```bash
uv run python scripts/deepagents/evaluate_autonomous_code_streaming_refactor_orchestrator_v1.py
```

**Features:**

- Tests refactoring analysis quality
- Measures latency for each operation
- Tests streaming code generation
- Logs results to local MLflow instance
- Creates test dataset with refactoring scenarios

**Prerequisites:**

- MLflow server running locally or SQLite backend configured
- All MCP tools available
- Ollama running

**View results:**

- Check MLflow UI at the configured tracking URI (default: `sqlite:///mlflow.db`)

---

## Architecture

### Refactor Orchestrator Components

```
Autonomous Code Streaming Refactor Orchestrator v1
├── Main Agent (autonomous_code_streaming_refactor_orchestrator_v1.py)
│   ├── DeepAgents integration
│   ├── MCP tool orchestration
│   └── Refactoring workflow execution
│
├── Streaming Code Generation
│   ├── Ollama integration (ChatOllama)
│   ├── Real-time streaming with callbacks
│   └── Batch operations for efficiency
│
├── Codebase Analysis
│   ├── Semantic search (indexing-semantic-search-v2)
│   ├── Structure-aware search
│   └── Pattern discovery
│
└── MCP Server (included in main file)
    ├── FastMCP server
    └── Exposes refactoring tools
```

---

## Performance Metrics

**Expected Performance:**

- **Streaming Latency**: Real-time feedback (chunks streamed as generated)
- **Analysis Latency**: 5-15 seconds for typical codebase
- **Refactoring Latency**: 10-30 seconds for typical file
- **Workflow Latency**: 2-5 minutes for complete workflow
- **Cost**: $0.00 (100% free with Ollama)

---

## Related Patterns

- **sota_researcher_v1**: Base pattern for agent structure
- **workflow_orchestrator_hybrid_v1**: Workflow orchestration patterns
- **create_new_agent_v1**: Agent creation patterns

---

*This command connects to the autonomous-code-refactor MCP server. The MCP server must be running and configured in `~/.cursor/mcp.json`.*

--- End Command ---
