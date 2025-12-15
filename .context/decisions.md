# Architecture Decision Records (ADRs)

---

## ADR-001: Multi-Agent Workflow Strategy
**Date:** 2025-12-13
**Status:** Accepted
**Deciders:** Claude

### Context
We use multiple AI assistants (Claude, Gemini, Codex, Ollama) across 8 projects with different domains (music production, DeFi, gaming, infrastructure).

### Decision
Implement specialized agent roles:
- Claude: Architecture & orchestration
- Gemini: Research & exploration
- Codex: Code generation
- Ollama: Local iteration & privacy

### Consequences
**Positive:**
- Cost optimization (60%+ local with Ollama)
- Better quality through specialization
- Privacy for sensitive code
- Fast iteration cycles

**Negative:**
- Requires context management discipline
- Learning curve for agent selection
- Need to maintain handoff protocols

---

## ADR-002: Context Sharing via `.context/` Directory
**Date:** 2025-12-13
**Status:** Accepted
**Deciders:** Claude

### Context
Agents need to share context across sessions to maintain continuity.

### Decision
Use `.context/` directory with standardized files:
- `current-session.md` - Active work log
- `decisions.md` - This file (ADRs)
- `research-notes.md` - Findings from Gemini
- `todos.md` - Cross-agent task tracking
- `handoffs/` - Agent-to-agent transition logs

Alternative considered: Redis-only context (rejected due to lack of version control)

### Consequences
**Positive:**
- Git-tracked context history
- Human-readable markdown
- Easy agent-to-agent handoffs

**Negative:**
- Manual updates required
- Risk of stale context

---

## ADR-003: Redis MCP Server for Agent Communication
**Date:** 2025-12-13
**Status:** Proposed
**Deciders:** TBD

### Context
Agents may need real-time state sharing beyond markdown files.

### Decision (Proposed)
Use Redis MCP server for:
- Real-time agent-to-agent state
- Structured data (JSON)
- Audio processing cache
- Session memory

`.context/` remains for long-term, version-controlled decisions.

### Consequences
TBD - Needs implementation and testing

---

## Template for New ADRs

```markdown
## ADR-XXX: [Title]
**Date:** YYYY-MM-DD
**Status:** [Proposed | Accepted | Deprecated | Superseded]
**Deciders:** [Agent names]

### Context
[What is the issue we're addressing?]

### Decision
[What decision did we make?]
[Alternatives considered?]

### Consequences
**Positive:**
-

**Negative:**
-
```
