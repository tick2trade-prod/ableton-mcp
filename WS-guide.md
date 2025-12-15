# Multi-Agent Workspace Guide

**Workspace:** WS-ableton-mcp
**Last Updated:** 2025-12-13
**IDEs:** Antigravity, Cursor
**AI Tools:** claude-cli, gemini-cli, codex-cli, ollama (local)

---

## 🎯 Workspace Overview

### Project Domains

```
ableton-mcp/              → Music Production + AI Integration
├── Focus: Ableton Live control via MCP
├── Domain: Audio synthesis, MIDI, techno production
└── Primary Agents: Claude (architecture), Ollama (local experimentation)

ollama_crewai_lab/        → Code Generation + AI Orchestration
├── Focus: Local LLM-powered development workflows
├── Domain: Python, CrewAI, agent coordination
└── Primary Agents: Ollama (local), Codex (code gen), Gemini (research)

defi-dev-tools/           → DeFi Development Utilities
gam-deepagents/           → Gaming + Deep Agents
ableton-midi-mcp/         → MIDI Protocol Integration
expert-deepagents-stg/    → Staging for Agent Experiments
ubuntu-2404-fresh-setup/  → Infrastructure & DevOps
.gemini/                  → Gemini Configuration & Context
```

---

## 🤖 Agent Role Specialization

### 1. **Claude (claude-cli)** - Architect & Orchestrator
**Best For:**
- System architecture and design decisions
- Complex refactoring across multiple files
- MCP server integration and protocol design
- Code review and security analysis
- Long-form documentation and specifications

**Project Mapping:**
- `ableton-mcp`: Primary agent for MCP protocol design, audio DSP architecture
- `ollama_crewai_lab`: Agent orchestration patterns, workflow design

**Usage Pattern:**
```bash
# In ableton-mcp/
claude "Design an MCP tool for stem separation with Redis caching"

# In ollama_crewai_lab/
claude "Review the CrewAI workflow and suggest optimization patterns"
```

---

### 2. **Gemini (gemini-cli)** - Researcher & Context Specialist
**Best For:**
- Broad codebase exploration and understanding
- API documentation research
- Multi-modal analysis (diagrams, specs, audio concepts)
- Rapid prototyping of complex algorithms
- Comparative analysis between approaches

**Project Mapping:**
- `ableton-mcp`: Audio processing research, VST protocol investigation
- `defi-dev-tools`: Smart contract patterns, DeFi protocol research
- `gam-deepagents`: Game AI patterns, reinforcement learning research

**Usage Pattern:**
```bash
# Research phase
gemini "Analyze all MIDI handling patterns across ableton-mcp and ableton-midi-mcp"

# Multi-modal understanding
gemini "Explain the signal flow in this audio processing chain" --image spectrogram.png
```

---

### 3. **Codex (codex-cli)** - Code Generator & Implementer
**Best For:**
- Rapid code generation from specifications
- Boilerplate and utility function creation
- Test generation and edge case coverage
- API client implementation
- Data transformation pipelines

**Project Mapping:**
- `ollama_crewai_lab`: Python utility generation, agent task scripts
- `ableton-mcp`: MIDI message handlers, audio buffer processing
- `defi-dev-tools`: Smart contract testing utilities

**Usage Pattern:**
```bash
# Generate implementations
codex "Create a Redis-backed cache decorator for audio processing results"

# Test generation
codex "Generate pytest tests for the StemAnalyzer class with edge cases"
```

---

### 4. **Ollama (Local)** - Fast Iteration & Privacy
**Best For:**
- Offline development and sensitive code
- Rapid iteration without API costs
- Low-latency completions for autocomplete
- Experimentation with custom models
- Integration with local tools (CrewAI, LangChain)

**Recommended Models:**
- `deepseek-coder-v2` (33B): Best for complex code understanding
- `codellama:34b`: Optimized for code generation
- `mixtral:8x7b`: General reasoning and architecture
- `llama3.3:70b`: Latest capabilities, balanced performance

**Project Mapping:**
- `ollama_crewai_lab`: **Primary agent** for all local development
- `ableton-mcp`: Fast experimentation with audio algorithms
- All projects: Privacy-sensitive code, API key handling

**Usage Pattern:**
```bash
# Direct model interaction
ollama run deepseek-coder-v2 "Optimize this audio buffer processing loop"

# CrewAI integration (in ollama_crewai_lab/)
python crew_run.py --task "generate MIDI pattern variations"
```

---

## 🔄 Multi-Agent Workflow Patterns

### Pattern 1: Sequential Pipeline (Research → Design → Implement)

```bash
# Step 1: Research (Gemini)
gemini "What are the best practices for real-time audio processing in Python?"
# Output: Save findings to docs/research/audio-processing.md

# Step 2: Architecture (Claude)
claude "Design a real-time audio processor based on docs/research/audio-processing.md"
# Output: Architecture spec in specs/0008-realtime-audio.md

# Step 3: Implementation (Codex or Ollama)
codex "Implement the audio processor from specs/0008-realtime-audio.md"
# Output: src/audio/realtime_processor.py
```

**Use Cases:**
- New feature development with unclear requirements
- Experimental features requiring research
- Complex integrations (e.g., Ableton Live + MCP + Redis)

---

### Pattern 2: Parallel Specialization

```bash
# Terminal 1: Claude handles architecture
claude "Design the MCP server structure for Ableton integration"

# Terminal 2: Gemini researches APIs
gemini "Find all available Ableton Live MIDI remote script APIs"

# Terminal 3: Ollama generates test data
ollama run codellama "Generate realistic MIDI test patterns for techno music"

# Terminal 4: Codex implements utilities
codex "Create MIDI message validation utilities"
```

**Use Cases:**
- Large features with independent components
- Time-sensitive development
- Exploring multiple approaches simultaneously

---

### Pattern 3: Iterative Refinement (Ollama → Claude)

```bash
# Fast iteration with local model
ollama run deepseek-coder-v2 "Create a basic beat generator"
# Test locally, iterate quickly

# Once stable, upgrade quality with Claude
claude "Refactor this beat generator for production use with proper error handling"
# Polish, optimize, add robustness
```

**Use Cases:**
- Cost-sensitive development
- Rapid prototyping phase
- Learning new domains (music production, DeFi)

---

### Pattern 4: Consensus Review (Multi-Agent Validation)

```bash
# Implementation
codex "Implement ERC20 token transfer handler" > defi-dev-tools/src/transfer.py

# Security review by multiple agents
claude "Review src/transfer.py for security vulnerabilities"
gemini "Analyze src/transfer.py for common DeFi exploits"
ollama run deepseek-coder-v2 "Check src/transfer.py for reentrancy issues"

# Compare outputs, merge best insights
```

**Use Cases:**
- Security-critical code (DeFi, authentication)
- High-risk refactoring
- Code review before production deployment

---

## 📁 Project-Specific Workflows

### Ableton-MCP: Music Production AI

**Goal:** Use AI to control Ableton Live, generate techno patterns, process audio

#### Recommended Agent Flow:

1. **Music Theory Research** (Gemini)
   ```bash
   gemini "What are the key elements of Berlin-style techno?"
   # → Save to docs/music-theory/techno-patterns.md
   ```

2. **MIDI Pattern Generation** (Ollama + CrewAI)
   ```bash
   cd ../ollama_crewai_lab
   # Use CrewAI with local Ollama for pattern generation
   python generate_patterns.py --genre techno --bpm 135
   # → Output: MIDI files to ableton-mcp/patterns/
   ```

3. **MCP Tool Implementation** (Claude)
   ```bash
   cd ../ableton-mcp
   claude "Create MCP tools for: play_pattern, adjust_tempo, apply_effect"
   # → Implements in src/ableton_mcp/tools/
   ```

4. **Audio Processing** (Codex)
   ```bash
   codex "Implement stem separation using Demucs with Redis caching"
   # → Creates src/audio/stem_separator.py
   ```

5. **Integration Testing** (Claude)
   ```bash
   claude "Create end-to-end test: generate pattern → send to Ableton → verify playback"
   ```

#### Active Development Commands:

```bash
# Start Ableton MCP server
docker-compose up -d

# Quick iteration on MIDI patterns (local, fast)
ollama run deepseek-coder-v2 "Generate a 4-bar techno kick pattern in MIDI"

# Production-quality tool development
claude "Add error handling and logging to the pattern player"

# Research new audio effects
gemini "Compare audio compression algorithms for techno production"
```

---

### Ollama-CrewAI-Lab: Code Generation Workflows

**Goal:** Use local LLMs for assisted development, agent orchestration experiments

#### Recommended Agent Flow:

1. **Workflow Design** (Claude)
   ```bash
   claude "Design a CrewAI workflow for automated code review"
   # → Creates workflow spec in specs/crew-workflows/code-review.md
   ```

2. **Agent Implementation** (Local Ollama)
   ```bash
   ollama run deepseek-coder-v2 "Implement the code review crew based on spec"
   # → Fast iteration without API costs
   ```

3. **Utility Generation** (Codex)
   ```bash
   codex "Create helper functions for parsing code review feedback"
   ```

4. **Cross-Project Integration** (Gemini)
   ```bash
   gemini "How can we use this code review crew for ableton-mcp development?"
   ```

#### CrewAI Multi-Agent Pattern:

```python
# Example: Music production crew
from crewai import Agent, Task, Crew

# Agent 1: Pattern Generator (Ollama - deepseek-coder-v2)
pattern_generator = Agent(
    role="MIDI Pattern Generator",
    goal="Create techno MIDI patterns",
    llm="ollama/deepseek-coder-v2"
)

# Agent 2: Music Theorist (Ollama - mixtral)
theorist = Agent(
    role="Music Theory Advisor",
    goal="Ensure patterns follow techno conventions",
    llm="ollama/mixtral:8x7b"
)

# Agent 3: Quality Checker (Ollama - llama3.3)
quality_checker = Agent(
    role="Pattern Quality Analyst",
    goal="Validate MIDI patterns for playability",
    llm="ollama/llama3.3:70b"
)

# Orchestrate
crew = Crew(
    agents=[pattern_generator, theorist, quality_checker],
    tasks=[generate_task, review_task, validate_task],
    verbose=True
)
```

---

## 🛠️ Tool Selection Decision Tree

```
Need to make a decision?
│
├─ Is it architectural/design? → Claude
├─ Is it research/exploration? → Gemini
├─ Is it code generation? → Codex (cloud) or Ollama (local)
├─ Is it sensitive/offline? → Ollama only
├─ Is it multi-modal (images, audio)? → Gemini
└─ Is it rapid iteration? → Ollama (fastest)

Writing code?
│
├─ Boilerplate/utilities? → Codex
├─ Complex algorithms? → Claude or deepseek-coder-v2
├─ Need tests? → Codex (fast) or Claude (comprehensive)
└─ Prototyping? → Ollama (iterate until stable, then Claude for polish)

Need review?
│
├─ Security-critical? → Claude + Gemini (consensus)
├─ Architecture review? → Claude
├─ Code quality? → All agents (compare outputs)
└─ Performance? → Gemini (research) + Claude (implementation)
```

---

## 🔗 Context Management Strategies

### 1. Shared Context Files (Single Source of Truth)

```bash
ableton-mcp/
├── .context/
│   ├── current-session.md      # Active work, updated by all agents
│   ├── decisions.md            # Architecture decisions (ADRs)
│   ├── research-notes.md       # Gemini research output
│   └── todos.md                # Task tracking across agents
```

**Usage:**
```bash
# Before switching agents, update context
echo "## Claude Session - 2025-12-13\n- Implemented MCP tool X\n- TODO: Add error handling" >> .context/current-session.md

# Next agent reads context
gemini "Read .context/current-session.md and continue the work"
```

---

### 2. Agent Handoff Protocol

**Template for switching agents:**

```markdown
## Handoff: Claude → Ollama
**Date:** 2025-12-13 14:30
**Task:** Implement beat generator
**Status:** Architecture complete (specs/beat-generator.md)
**Next Steps:**
1. Implement core BeatGenerator class
2. Add tempo adjustment logic
3. Create unit tests
**Context Files:**
- specs/beat-generator.md
- src/audio/base_generator.py (reference implementation)
**Notes:** Use 4/4 time signature, BPM range 120-150
```

Save to `.context/handoffs/2025-12-13-beat-generator.md`

---

### 3. MCP Server as Context Bridge

Use Redis MCP server to share state between agents:

```python
# Claude writes design decisions to Redis
import redis
r = redis.Redis()
r.json.set("context:ableton:architecture", "$", {
    "pattern": "factory",
    "tools": ["play_pattern", "adjust_tempo"],
    "dependencies": ["redis", "mcp"]
})

# Ollama reads context later
context = r.json.get("context:ableton:architecture")
# Use context for implementation
```

**Benefits:**
- Real-time context sharing
- Structured data (JSON)
- Persistent across sessions
- Queryable by all agents

---

### 4. Git Commits as Agent Boundaries

```bash
# Claude completes architecture phase
git add specs/ docs/
git commit -m "feat(architecture): MCP tool design for Ableton integration

Agent: Claude
Phase: Architecture
Files: specs/0008-ableton-tools.md
Next: Implementation by Codex/Ollama"

# Next agent starts fresh with clear context
codex "Read git log -1 and implement the spec"
```

---

## 🎛️ IDE Integration Patterns

### Antigravity IDE

**Recommended Setup:**
```json
// .antigravity/settings.json
{
  "ai.providers": [
    {"name": "claude", "priority": 1, "use_for": ["architecture", "review"]},
    {"name": "ollama", "priority": 2, "use_for": ["autocomplete", "quick_edits"]},
    {"name": "codex", "priority": 3, "use_for": ["generation"]}
  ],
  "ai.context.auto_include": [
    ".context/**/*.md",
    "specs/**/*.md",
    "AGENTS.md"
  ]
}
```

**Workflow:**
- Use Ollama for real-time autocomplete (low latency)
- Trigger Claude for complex refactoring (⌘+Shift+A)
- Use Codex for "generate function from comment"

---

### Cursor IDE

**Recommended Setup:**
```json
// .cursor/settings.json
{
  "cursor.aiProvider": "claude",  // Primary for chat
  "cursor.autocompleteProvider": "ollama",  // Fast local completions
  "cursor.context.includeDirs": [
    "../ollama_crewai_lab",
    ".context"
  ]
}
```

**Multi-Agent Pattern:**
1. **Cursor Chat (Claude):** Architecture questions, design discussions
2. **Cursor Autocomplete (Ollama):** Fast completions, no API costs
3. **External CLI (Gemini):** Deep research in separate terminal

**Keyboard Shortcuts:**
- `⌘+K` → Cursor chat (Claude)
- `⌘+I` → Inline edit (Ollama autocomplete)
- Terminal → `gemini "research query"`

---

## 🚀 Advanced Patterns

### Pattern A: Agent Swarm for Code Review

```bash
#!/bin/bash
# scripts/swarm-review.sh

FILE=$1
OUTPUT="reviews/$(basename $FILE).md"

echo "# Multi-Agent Code Review: $FILE\n" > $OUTPUT

# Parallel review by all agents
{
  claude "Review $FILE for architecture and design" >> $OUTPUT &
  gemini "Review $FILE for best practices and patterns" >> $OUTPUT &
  codex "Review $FILE for bugs and edge cases" >> $OUTPUT &
  ollama run deepseek-coder-v2 "Review $FILE for performance" >> $OUTPUT &
}
wait

echo "Review complete: $OUTPUT"
```

Usage:
```bash
./scripts/swarm-review.sh src/audio/stem_separator.py
```

---

### Pattern B: CrewAI + Multiple LLM Backends

```python
# ollama_crewai_lab/crews/music_production_crew.py

from crewai import Agent, Task, Crew, LLM

# Mix local (Ollama) and cloud (Claude) agents
claude_llm = LLM(model="claude-sonnet-4-5", api_key=os.getenv("ANTHROPIC_API_KEY"))
ollama_llm = LLM(model="ollama/deepseek-coder-v2", base_url="http://localhost:11434")

# High-level orchestration: Claude (best reasoning)
conductor = Agent(
    role="Music Production Conductor",
    goal="Orchestrate techno track creation",
    llm=claude_llm
)

# Pattern generation: Ollama (fast, local)
pattern_gen = Agent(
    role="MIDI Pattern Generator",
    goal="Create drum and bass patterns",
    llm=ollama_llm
)

# Quality control: Claude (best judgment)
quality = Agent(
    role="Track Quality Analyst",
    goal="Ensure professional sound",
    llm=claude_llm
)

crew = Crew(agents=[conductor, pattern_gen, quality])
result = crew.kickoff(inputs={"genre": "techno", "bpm": 135})
```

**Cost Optimization:**
- Use Claude for critical decisions (10-20% of calls)
- Use Ollama for repetitive tasks (80-90% of calls)
- Monitor with `.env.metrics` logging

---

### Pattern C: Iterative Co-Creation

```
Human: "Create a techno track with driving bassline"
   ↓
Claude: "Here's the architecture and composition structure"
   ↓ (saves to specs/track-001.md)
   ↓
Ollama (CrewAI): Generates MIDI patterns based on spec
   ↓ (saves to patterns/track-001/*.mid)
   ↓
Gemini: "Analyze patterns for music theory correctness"
   ↓ (provides feedback)
   ↓
Ollama: Refines patterns based on feedback
   ↓
Codex: "Generate Python script to send patterns to Ableton via MCP"
   ↓
Human: Tests in Ableton, provides feedback
   ↓
Claude: "Adjust arrangement based on human feedback"
   ↓
Final track produced 🎵
```

---

## 📊 Monitoring & Metrics

### Track Agent Usage

```bash
# .context/metrics.json
{
  "2025-12-13": {
    "claude": {"calls": 45, "tokens": 125000, "cost": 2.50},
    "gemini": {"calls": 23, "tokens": 89000, "cost": 0.89},
    "codex": {"calls": 67, "tokens": 156000, "cost": 3.12},
    "ollama": {"calls": 234, "tokens": 450000, "cost": 0.00}
  }
}
```

**Analysis Script:**
```python
# scripts/analyze_usage.py
import json

with open('.context/metrics.json') as f:
    data = json.load(f)

for date, usage in data.items():
    total_cost = sum(agent['cost'] for agent in usage.values())
    ollama_percent = usage['ollama']['calls'] / sum(a['calls'] for a in usage.values()) * 100
    print(f"{date}: ${total_cost:.2f} total, {ollama_percent:.1f}% local")
```

**Optimization Goals:**
- Keep >60% of calls on Ollama (local, free)
- Use Claude for <20% of calls (high-value tasks)
- Monitor cost per feature delivered

---

## 🎯 Best Practices Summary

### DO:
✅ Start research with Gemini (broad exploration)
✅ Use Claude for architecture and critical decisions
✅ Prototype rapidly with Ollama (local, fast)
✅ Generate boilerplate with Codex
✅ Keep shared context in `.context/` directory
✅ Use MCP/Redis for agent-to-agent state sharing
✅ Commit after each agent phase with clear messages
✅ Run parallel agents for independent tasks
✅ Use CrewAI for multi-step workflows in ollama_crewai_lab
✅ Review security-critical code with multiple agents

### DON'T:
❌ Use cloud APIs for sensitive code (use Ollama)
❌ Mix agent contexts without handoff protocol
❌ Skip research phase on unfamiliar domains
❌ Use Claude for simple boilerplate (waste of cost/quality)
❌ Forget to update `.context/current-session.md`
❌ Run sequential tasks in parallel (dependency issues)
❌ Use large models (Claude/Gemini) for autocomplete
❌ Start coding without architecture (especially music/audio)

---

## 🔮 Future Enhancements

### Planned Integrations:
1. **Ableton Live MCP Server** → Direct DAW control from any agent
2. **CrewAI Music Production Crew** → Automated track generation
3. **Redis Context Store** → Shared agent memory across sessions
4. **Ollama Fine-tuned Models** → Custom models for techno generation
5. **Multi-Agent Workflow Engine** → Automated agent handoffs

### Experiment Ideas:
- Use Gemini for audio spectrogram analysis (multi-modal)
- Train custom Ollama model on techno MIDI datasets
- Create "music theory validation agent" with Claude
- Build agent swarm for parallel track generation
- Implement "creative disagreement" pattern (agents debate approaches)

---

## 📚 Reference

### Quick Command Reference:

```bash
# Claude (architecture)
claude "Design X"
claude --file specs/feature.md "Implement this spec"

# Gemini (research)
gemini "Research Y"
gemini --context .context/ "Analyze codebase for pattern Z"

# Codex (generation)
codex "Generate tests for module X"
codex "Create utility functions for Y"

# Ollama (local)
ollama run deepseek-coder-v2 "Quick implementation of X"
ollama run mixtral:8x7b "Explain architecture Y"
ollama run llama3.3:70b "Review code for issues"

# CrewAI (orchestration)
cd ../ollama_crewai_lab
python crew_run.py --workflow music_production --task "generate techno track"
```

### Context Files to Maintain:

```
.context/
├── current-session.md       # Active work log
├── decisions.md             # Architecture Decision Records (ADRs)
├── research-notes.md        # Gemini research findings
├── todos.md                 # Cross-agent task list
├── handoffs/               # Agent-to-agent handoff logs
│   └── YYYY-MM-DD-*.md
└── metrics.json            # Usage tracking
```

---

**Last Updated:** 2025-12-13
**Maintained By:** Multi-agent collaboration (Claude + Gemini + Codex + Ollama)
**Version:** 2.0.0
