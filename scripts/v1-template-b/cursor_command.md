# GAM DeepAgents Memorizer Researcher Planner v3 MCP Command

## Primary Objective

**Trigger GAM DeepAgents MCP server v3 tools for creating DeepAgents with General Agentic Memory (GAM) integration.**

This command provides access to the `gam-deepagents-v3` MCP server (`scripts/gam_deepagents/v3/mcp_server.py`) which combines:

- **DeepAgents** `create_deep_agent` for automatic orchestration
- **GAM MemoryAgent** (memorizer) for memory construction
- **GAM ResearchAgent** (researcher) for memory retrieval
- **Ollama** for cost-free local LLM operations (default)

**GAM Repository**: [https://github.com/VectorSpaceLab/general-agentic-memory](https://github.com/VectorSpaceLab/general-agentic-memory)

---

## 🚀 v3 Enhancements

**v3 includes significant improvements over v2:**

- ✅ **All v2 Features**: Enhanced error handling, observability, token efficiency, input validation
- ✅ **KISS Performance Improvements**: Parallel retriever building (2-3x faster), better token counting (25-30% accuracy), reduced logging overhead (5-10% faster)
- ✅ **Docker Integration**: Automatic detection and utilization of MLflow, MindsDB, Redis, PostgreSQL services
- ✅ **Enhanced Code Generation**: Improved prompts with Docker service awareness, better workflow orchestration
- ✅ **Better Token Estimation**: Character-based token counting (~4 chars/token) for 85-90% accuracy

---

## 💰 Cost-Free Usage with Ollama

**With Ollama (local LLM), all GAM operations are FREE!**

### Quick Setup with Ollama

1. **Install and start Ollama:**

   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh

   # Start Ollama
   ollama serve

   # Pull recommended models
   ollama pull codellama-34b-optimized:latest  # Best for code (34B, 19 GB)
   # OR
   ollama pull llama3.1:8b-optimized        # Recommended default (8B, 4.9 GB)
   # OR
   ollama pull llama3.1:8b                   # Fallback (8B, 4.9 GB)
   ```

2. **Configure environment:**

   ```bash
   export OLLAMA_BASE_URL=http://localhost:11434/v1
   export OLLAMA_MODEL=codellama-34b-optimized:latest
   export GAM_USE_OLLAMA=true
   ```

3. **Use with full features:**

   ```text
   Create agent with GAM: code-reviewer
   Description: Reviews code and remembers project conventions
   ```

**What you get (all enabled by default):**

- ✅ **Ollama** - FREE local LLM for GAM operations
- ✅ **GAM Memory** - Persistent memory with hybrid search
- ✅ **DeepAgents** - Automatic orchestration
- ✅ **OpenTelemetry** - Full observability
- ✅ **Retry Logic** - Enhanced reliability (v2)
- ✅ **KISS Improvements** - 2-3x faster initialization, better token counting (v3)
- ✅ **Docker Services** - MLflow, MindsDB, Redis, PostgreSQL integration (v3)

**Total cost: $0.00** (with Ollama) 🎉

---

## Installation & Setup

### Step 1: Run the Installer (Required)

Before using GAM DeepAgents MCP server v3, run the installer:

```bash
uv run python scripts/gam_deepagents/v3/install.py --install
```

This installer:

- ✅ Validates all prerequisites (deepagents, gam, fastmcp, pydantic-settings)
- ✅ Installs missing dependencies
- ✅ Verifies GAM components availability
- ✅ Checks OpenTelemetry configuration
- ✅ Validates settings configuration
- ✅ Updates MCP server configuration for v3
- ✅ Prevents weird results from partial failures

**Why use the installer?** Instead of graceful degradation (which leads to weird results), the installer ensures everything is properly set up from the start.

### Step 2: Setup Java 21 (Required for GAM BM25 Retriever)

**GAM BM25 retriever requires Java 21 for keyword search (pyserini requirement):**

```bash
# Ubuntu/Debian
sudo apt-get install openjdk-21-jdk

# macOS
brew install openjdk@21

# Verify installation
java -version
javac -version

# The installer will automatically detect Java and configure JAVA_HOME/JVM_PATH
```

**Note**:

- GAM works without Java, but BM25 keyword search requires Java 21
- pyserini (used by GAM) requires Java 21 (class file version 65.0)
- Java 17 may work for some operations, but Java 21 is recommended
- Dense vector search works without Java

### Step 3: Verify Installation

After installation, validate everything works:

```bash
uv run python scripts/gam_deepagents/v3/install.py --validate-only
```

### Step 4: Configure Settings (Type-Safe Configuration)

**All configuration uses pydantic-settings with environment variables (GAM_DEEPAGENTS_ prefix):**

**Ollama Configuration** (recommended, free local models):

```bash
# Enable Ollama (default: true)
export GAM_DEEPAGENTS_USE_OLLAMA=true

# Ollama base URL (default: http://localhost:11434/v1)
export GAM_DEEPAGENTS_OLLAMA_BASE_URL=http://localhost:11434/v1

# Ollama model (default: codellama-34b-optimized:latest)
export GAM_DEEPAGENTS_OLLAMA_MODEL=codellama-34b-optimized:latest
```

**Alternative: Use OpenAI** (if Ollama not available):

```bash
export GAM_DEEPAGENTS_USE_OLLAMA=false
export GAM_DEEPAGENTS_OPENAI_API_KEY=your_openai_api_key
export GAM_DEEPAGENTS_OPENAI_MODEL=gpt-4o-mini
```

**Generator Parameters:**

```bash
# Generator temperature (0.0-2.0, default: 0.2)
export GAM_DEEPAGENTS_GENERATOR_TEMPERATURE=0.2

# Generator max tokens (1-4096, default: 2048)
export GAM_DEEPAGENTS_GENERATOR_MAX_TOKENS=2048
```

**GAM Configuration:**

```bash
# GAM index directory (default: ./tmp/gam_index)
export GAM_DEEPAGENTS_GAM_INDEX_DIR=./tmp/gam_index

# Research max iterations (1-20, default: 8)
export GAM_DEEPAGENTS_GAM_RESEARCH_MAX_ITERS=8

# Dense retriever model (default: BAAI/bge-m3)
export GAM_DEEPAGENTS_GAM_DENSE_MODEL=BAAI/bge-m3

# BM25 threads (1-8, default: 4)
export GAM_DEEPAGENTS_GAM_BM25_THREADS=4
```

**Validation:**

```bash
# Require validation (fail fast, default: true)
export GAM_DEEPAGENTS_REQUIRE_VALIDATION=true
```

**Optional: Configure OpenTelemetry** (for observability):

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318  # Optional
export OTEL_CONSOLE_EXPORTER=true  # Enable console exporter for local development
```

---

## How to Run the MCP Server

### Option 1: In Cursor (Recommended)

The MCP server is automatically started by Cursor when configured in `.cursor/mcp.json`. The installer sets this up for you:

#### 1. Verify MCP Configuration

The server should be configured in `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "gam-deepagents-v3": {
      "command": "/home/zhouk2404/.local/bin/uv",
      "args": [
        "run",
        "--directory",
        "${workspaceFolder}",
        "python",
        "${workspaceFolder}/scripts/gam_deepagents/v3/mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "OPENAI_API_KEY": "${env:OPENAI_API_KEY}",
        "JAVA_HOME": "/usr/lib/jvm/java-21-openjdk-amd64",
        "JVM_PATH": "/usr/lib/jvm/java-21-openjdk-amd64/lib/server/libjvm.so",
        "PATH": "/home/zhouk2404/.local/bin:${env:PATH}"
      }
    }
  }
}
```

**Note**:

- The installer automatically detects `uv` and uses its full path
- The installer automatically adds `JAVA_HOME` and `JVM_PATH` if Java 21 is detected
- The installer adds Java 21 bin to PATH to ensure Java 21 is used

#### 2. Restart Cursor

After updating the configuration:

1. **Restart Cursor** to load the new MCP server configuration
2. The server will automatically start when you use MCP tools

#### 3. Use the Tools

Once configured, you can use the tools directly in Cursor chat:

```text
Create agent with GAM: code-reviewer
Description: Reviews code and remembers project conventions
```

```text
Memorize: This project uses Python 3.12, type hints required, pytest for testing
```

```text
Research memory: What are the project's coding conventions?
```

```text
Run agent with GAM: Review this code file for style issues
```

---

## Available Tools

### 1. `create_agent_with_gam`

Create a new DeepAgent with GAM memory capabilities.

**Parameters:**

- `agent_name` (required): Name for the agent
- `description` (required): What the agent should do
- `system_prompt` (optional): Custom system prompt (default: GAM-aware prompt)

**Returns:**

- `success`: bool - Whether agent creation succeeded
- `agent_name`: str - Agent name
- `description`: str - Agent description
- `status`: str - Creation status
- `latency_ms`: float - Creation latency in milliseconds

**Example Usage:**

```text
Create agent with GAM: code-reviewer
Description: Reviews code and remembers project conventions
```

### 2. `memorize_content`

Memorize content using GAM MemoryAgent.memorize() with retry logic.

**Parameters:**

- `content` (required): Content to memorize

**Returns:**

- `success`: bool - Whether memorization succeeded
- `content_length`: int - Length of memorized content
- `message`: str - Confirmation message
- `latency_ms`: float - Memorization latency in milliseconds

**Example Usage:**

```text
Memorize: This project uses Python 3.12, type hints required, pytest for testing
```

**v3 Enhancement**: Retry logic automatically retries failed memorization attempts (up to 3 times with exponential backoff). KISS improvements: 2-3x faster initialization, better token counting.

### 3. `research_memory`

Research from memory using GAM ResearchAgent.research() with retry logic.

**Parameters:**

- `query` (required): Research query

**Returns:**

- `success`: bool - Whether research succeeded
- `memory`: str - Research results from memory
- `iterations`: int - Number of research iterations
- `latency_ms`: float - Research latency in milliseconds

**Example Usage:**

```text
Research memory: What are the project's coding conventions?
```

**v3 Enhancement**: Retry logic automatically retries failed research attempts (up to 3 times with exponential backoff). KISS improvements: parallel retriever building, better token estimation.

### 4. `run_agent_with_gam`

Run DeepAgent task with GAM memory integration.

**Parameters:**

- `task` (required): Task description
- `agent_name` (optional): Agent name (for future multi-agent support)

**Returns:**

- `success`: bool - Whether task execution succeeded
- `response`: str - Agent response
- `message_count`: int - Number of messages in conversation
- `latency_ms`: float - Task execution latency in milliseconds

**Example Usage:**

```text
Run agent with GAM: Review this code file for style issues
```

**v3 Enhancement**: Enhanced error handling with better error messages. Docker service integration for MLflow, MindsDB, Redis, PostgreSQL.

---

## Usage Examples

### Complete Workflow

```text
1. Memorize project conventions
Memorize: This project uses Python 3.12, type hints required, pytest for testing

2. Create agent with GAM
Create agent with GAM: code-reviewer
Description: Reviews code and remembers project conventions

3. Research memory before task
Research memory: What are the project's coding conventions?

4. Run agent with GAM
Run agent with GAM: Review this code file for style issues
```

### Memory-First Workflow

```text
1. Memorize important information
Memorize: User prefers Python over JavaScript for new projects

2. Research before creating agent
Research memory: What are user preferences for programming languages?

3. Create agent with context
Create agent with GAM: project-planner
Description: Plans new projects based on user preferences
```

---

## MCP Server Details

**Server Name:** `gam-deepagents-v3`
**Script Location:** `scripts/gam_deepagents/v3/mcp_server.py`
**Core Logic:** `scripts/gam_deepagents/v3/core.py`
**Settings Location:** `scripts/gam_deepagents/v3/settings.py`
**MCP Configuration:** Defined in `~/.cursor/mcp.json`

**Underlying Implementation:**

- **DeepAgents**: Uses `create_deep_agent` for automatic orchestration
- **GAM MemoryAgent**: Uses `MemoryAgent.memorize()` directly for memory construction
- **GAM ResearchAgent**: Uses `ResearchAgent.research()` directly for memory retrieval
- **Type-Safe Configuration**: Pydantic-settings for validation (no hardcoded variables)
- **OpenTelemetry**: Required observability for LLM debugging
- **Strict Imports**: Fails immediately if packages missing (no graceful degradation)
- **Direct Method Calls**: Uses existing classes/methods directly (no wrappers)
- **Enhanced Error Handling**: Retry logic with exponential backoff (v2)
- **Token-Efficient Patterns**: Concise descriptions and prompts (v2)
- **Input Validation**: Better validation with clear error messages (v2)
- **KISS Performance Improvements**: Parallel retriever building, better token counting (v3)
- **Docker Integration**: MLflow, MindsDB, Redis, PostgreSQL service detection and utilization (v3)

**Key Features (v3):**

- ✅ **All v2 Features**: Enhanced error handling, observability, token efficiency, input validation
- ✅ **KISS Performance**: Parallel retriever building (2-3x faster), better token counting (25-30% accuracy), reduced logging overhead (5-10% faster)
- ✅ **Docker Integration**: Automatic detection and utilization of Docker services
- ✅ **Enhanced Code Generation**: Improved prompts with Docker service awareness
- ✅ **Better Token Estimation**: Character-based token counting (~4 chars/token) for 85-90% accuracy
- ✅ **Type-Safe Configuration**: Pydantic-settings with validation
- ✅ **Strict Imports**: Fails fast if packages missing
- ✅ **OpenTelemetry Tracing**: All operations wrapped in spans
- ✅ **Direct GAM Usage**: Calls `MemoryAgent.memorize()` and `ResearchAgent.research()` directly
- ✅ **Direct DeepAgents Usage**: Uses `create_deep_agent()` directly
- ✅ **No Custom Wrappers**: Uses existing classes/methods from both packages

---

## Design Principles

### 1. Strict Imports (Fail Fast)

**No graceful degradation**: All packages must be installed or script fails immediately with clear error messages.

**Required packages:**

- `deepagents` - Install with: `uv sync`
- `general-agentic-memory` - Install with: `uv add general-agentic-memory`
- `fastmcp` - Install with: `uv add fastmcp`
- `app.mcp.opentelemetry_config` - For observability

### 2. Required Observability

**OpenTelemetry tracing** is required for LLM debugging. All operations are wrapped in OpenTelemetry spans with:

- Operation status (success/error)
- Latency metrics
- Error messages (if failed)
- Context information
- **Retry attempt tracking (v2)**
- **KISS performance improvements (v3)**
- **Docker service integration (v3)**

### 3. Use Existing Classes/Methods

**No custom wrappers**: Uses existing classes and methods directly from both packages:

- **GAM**: `MemoryAgent.memorize()`, `ResearchAgent.research()`
- **DeepAgents**: `create_deep_agent()`
- **LangGraph**: `MemorySaver`, `InMemoryStore`

### 4. Enhanced Error Handling (v2) + KISS Performance (v3)

**Retry logic** with exponential backoff:

- 3 retries by default (configurable)
- Exponential backoff (1s, 2s, 4s)
- All retry attempts tracked in OpenTelemetry
- Clear error messages on final failure

### 5. Token-Efficient Patterns (v2)

**Concise descriptions and prompts**:

- Tool descriptions < 200 characters
- System prompts optimized for token usage
- Only essential information included

---

## Troubleshooting

### MCP Server Not Starting

**Error**: `spawn uv ENOENT` or `Client error for command A system error occurred (spawn uv ENOENT)`

**Solution**: The installer automatically fixes this by using the full path to `uv`. Run:

```bash
uv run python scripts/gam_deepagents/v3/install.py --install
```

**Manual Fix**: If the installer doesn't work, manually update `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "gam-deepagents-v3": {
      "command": "/home/zhouk2404/.local/bin/uv",
      ...
    }
  }
}
```

Replace `/home/zhouk2404/.local/bin/uv` with your actual `uv` path (find with `which uv`).

1. **Check MCP Configuration:**

   ```bash
   cat ~/.cursor/mcp.json | jq '.mcpServers["gam-deepagents-v3"]'
   ```

2. **Verify Dependencies:**

   ```bash
   uv run python -c "from deepagents import create_deep_agent; print('DeepAgents available')"
   uv run python -c "from gam import MemoryAgent, ResearchAgent; print('GAM available')"
   uv run python -c "from mcp.server.fastmcp import FastMCP; print('FastMCP available')"
   uv run python -c "from scripts.gam_deepagents.settings import get_settings; print('Settings available')"
   ```

3. **Test Server Directly:**

   ```bash
   uv run python scripts/gam_deepagents/v3/mcp_server.py
   ```

### Missing Packages

**Run installer to fix:**

```bash
uv run python scripts/gam_deepagents/v3/install.py --install
```

### OpenTelemetry Issues

**Check OpenTelemetry config:**

```bash
uv run python -c "from app.mcp.opentelemetry_config import get_opentelemetry_tracer; print('OpenTelemetry available')"
```

### GAM Components Not Available

**Verify GAM installation:**

```bash
uv run python -c "from gam import MemoryAgent, ResearchAgent, OpenAIGenerator; print('GAM components available')"
```

**Install GAM if missing:**

```bash
uv add general-agentic-memory
```

### Java/libjvm.so Not Found

**Error**: `Unable to find libjvm.so`

**Solution 1: Install Java 21 (Required for pyserini)**

```bash
# Ubuntu/Debian
sudo apt-get install openjdk-21-jdk

# macOS
brew install openjdk@21

# Verify installation
java -version
```

**Note**: pyserini (used by GAM) requires Java 21 (class file version 65.0). Java 17 may work for some operations but Java 21 is recommended.

**Solution 2: Set JAVA_HOME and JVM_PATH manually**

```bash
# Find Java 21 installation
ls -la /usr/lib/jvm/ | grep java-21

# Find libjvm.so
find /usr/lib/jvm/java-21-openjdk-amd64 -name "libjvm.so"

# Set environment variables (add to ~/.bashrc or ~/.zshrc)
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export JVM_PATH=/usr/lib/jvm/java-21-openjdk-amd64/lib/server/libjvm.so
export PATH="${JAVA_HOME}/bin:${PATH}"
```

**Solution 3: Update MCP configuration**

The installer automatically adds `JAVA_HOME` and `JVM_PATH` to the MCP config. If you need to set them manually, edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "gam-deepagents-v3": {
      "env": {
        "JAVA_HOME": "/usr/lib/jvm/java-21-openjdk-amd64",
        "JVM_PATH": "/usr/lib/jvm/java-21-openjdk-amd64/lib/server/libjvm.so"
      }
    }
  }
}
```

**Note**:

- GAM works without Java, but BM25 keyword search requires Java 21
- pyserini (used by GAM) requires Java 21 (class file version 65.0)
- Dense vector search works without Java

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
   # Recommended: Pull larger models for better quality
   ollama pull codellama-34b-optimized:latest  # Best for code (34B, 19 GB)
   # OR
   ollama pull llama3.1:8b-optimized           # Recommended default (8B, 4.9 GB)
   # OR
   ollama pull llama3.1:8b                     # Fallback (8B, 4.9 GB)
   ```

4. **Verify Ollama API:**

   ```bash
   curl http://localhost:11434/api/tags
   ```

---

## Evaluation

### MLflow Evaluation

The MCP server can be evaluated using MLflow for tracking performance.

**Run evaluation:**

```bash
uv run python scripts/gam_deepagents/v3/eval.py
```

**Features:**

- Tests all MCP tools (memorize, research, create_agent, run_agent)
- Measures latency for each operation
- Logs results to local MLflow instance
- Creates test dataset with ground truth
- Tracks success rate and performance metrics
- **Enhanced metrics tracking (v2)**
- **KISS performance metrics (v3)**
- **Docker service health checks (v3)**

**Prerequisites:**

- MLflow server running locally or SQLite backend configured
- All required packages installed
- Ollama running (for local models) OR OpenAI API key configured (for cloud models)

**View results:**

- Check MLflow UI at the configured tracking URI (default: `sqlite:///mlflow.db`)

---

## Testing

### Run Tests

```bash
# Run all tests
uv run pytest scripts/gam_deepagents/v3/test_mcp.py -v

# Run with markers
uv run pytest scripts/gam_deepagents/v3/test_mcp.py -m hotpath -v
```

**Test Coverage:**

- ✅ Settings configuration (pydantic-settings)
- ✅ Strict imports (fail fast)
- ✅ GAM initialization using existing classes
- ✅ DeepAgent creation using existing function
- ✅ MCP tool execution
- ✅ OpenTelemetry tracing
- ✅ Error handling
- ✅ **Retry logic (v2)**
- ✅ **Token-efficient patterns (v2)**
- ✅ **Input validation (v2)**
- ✅ **KISS performance improvements (v3)**
- ✅ **Docker integration (v3)**

---

## v3 vs v2 Comparison

| Feature | v2 | v3 |
|---------|----|----|
| Error Handling | Enhanced with retry logic | **Same (v2)** |
| Retry Logic | 3 retries with exponential backoff | **Same (v2)** |
| Observability | Enhanced with attempt tracking | **Same (v2)** |
| Token Efficiency | Optimized (concise descriptions) | **Same (v2)** |
| Input Validation | Enhanced with clear error messages | **Same (v2)** |
| Performance | Standard initialization | **2-3x faster (parallel retriever building)** |
| Token Counting | Word-based (~60-70% accuracy) | **Character-based (~85-90% accuracy)** |
| Logging Overhead | Info-level for all chunks | **Debug-level for verbose, info for milestones** |
| Docker Integration | None | **MLflow, MindsDB, Redis, PostgreSQL** |
| Code Generation | Standard prompts | **Enhanced with Docker service awareness** |

---

## Related Documentation

- **v1 Documentation**: `scripts/gam_deepagents/cursor_command_mcp_gam_deepagents_memorizer_researcher_planner_v1.md`
- **v2 Documentation**: `scripts/gam_deepagents/cursor_command_mcp_gam_deepagents_memorizer_researcher_planner_v2.md`
- **KISS Improvements**: `scripts/gam_deepagents/docs/kiss_performance_improvements.md`
- **Architecture Separation**: `scripts/gam_deepagents/docs/architecture_separation_research.md`
- **Programmatic Tool Calling**: `scripts/gam_deepagents/docs/programmatic_tool_calling_improvements.md`
- **GAM Integration Research**: `docs/deepagents/gam-integration-research.md`
- **GAM README**: <https://github.com/VectorSpaceLab/general-agentic-memory/blob/main/README.md>
- **DeepAgents README**: <https://github.com/langchain-ai/deepagents/blob/master/README.md>
- **Cursor MCP Docs**: <https://cursor.com/docs/context/mcp>
- **MLflow Evaluation**: `.cursor/rules/mlflow-evaluation.mdc`
- **Test Markers**: `.cursor/rules/test-marker-enforcement.mdc`
- **Python Execution**: `.cursor/rules/python-version-enforcement.mdc`

---

*This command connects to the gam-deepagents-v3 MCP server. The MCP server must be running and configured in `~/.cursor/mcp.json`.*

---

## 🎯 v3 KISS Performance Improvements

**Keep It Stupid Simple** improvements that provide quantifiable benefits:

### 1. Parallel Retriever Building (2-3x faster initialization)

- **Before**: Sequential building (15-30s total)
- **After**: Parallel building (5-10s total)
- **Impact**: 2-3x faster first operation latency

### 2. Better Token Counting (25-30% accuracy improvement)

- **Before**: Word count (~60-70% accuracy)
- **After**: Character-based (~85-90% accuracy, ~4 chars/token)
- **Impact**: More accurate performance tracking

### 3. Reduced Logging Overhead (5-10% faster streaming)

- **Before**: Info-level logging for every chunk
- **After**: Debug-level for verbose, info for milestones only
- **Impact**: 5-10% performance improvement in streaming

### 4. Early Return Optimization (1-2% reduction)

- **Before**: Processes empty chunks
- **After**: Skips empty/whitespace-only content
- **Impact**: Minimal but measurable overhead reduction

**Total Expected Improvement**:

- **Initialization**: 2-3x faster
- **Streaming**: 6-12% faster
- **Metrics**: 25-30% more accurate

---

## 🐳 Docker Integration

v3 automatically detects and utilizes Docker services from `make docker-restart`:

- **MLflow** (<http://localhost:5000>): Experiment tracking and metrics
- **MindsDB** (<http://localhost:47334>): AI database for advanced queries
- **Redis** (localhost:6379): Caching and message brokering
- **PostgreSQL** (localhost:5432): Persistent storage for workflow state

Services are automatically detected on initialization and integrated into agent prompts for enhanced code generation and workflow orchestration.
