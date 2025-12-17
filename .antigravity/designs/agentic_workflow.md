# Agentic Workflow Design

## Antigravity + Ollama Agent Integration

> Date: 2025-12-16

---

## 1. Workflow Architecture

### Three-Layer Agent System

```
┌─────────────────────────────────────────────────────────────┐
│              Layer 1: Antigravity IDE Agents                 │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ Planning Agent  │  │   Fast Agent    │                   │
│  │ (high-level)    │  │ (execution)     │                   │
│  └────────┬────────┘  └────────┬────────┘                   │
└───────────┼────────────────────┼────────────────────────────┘
            │                    │
            ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│              Layer 2: Specialist Ollama Agents               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │Percussion│ │Synthesiz.│ │ Vocals   │ │ Effects  │       │
│  │  Agent   │ │  Agent   │ │  Agent   │ │  Agent   │       │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘       │
│       │            │            │            │              │
│       └────────────┴────────────┴────────────┘              │
│                         │                                    │
│                         ▼                                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Stem Comparison Agent                     │  │
│  │  (librosa analysis + Ollama interpretation)           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│              Layer 3: MCP Tools (FastMCP)                    │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐              │
│  │ session    │ │ tracks     │ │ stems      │              │
│  │ tools      │ │ tools      │ │ tools      │              │
│  └────────────┘ └────────────┘ └────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Antigravity Workflow Files

### Location: `.agent/workflows/`

#### `/recreate-stem` Workflow

```markdown
---
description: Recreate a single stem from I Am Machine
---

1. Load the stem audio file for analysis
2. Start Ollama if not running: `ollama serve`
3. Run analysis on stem:
   ```bash
   python -c "from agents import analyze_stem; analyze_stem('drums')"
   ```
4. // turbo
   Create track in Ableton using appropriate agent
5. Compare recreated track to original stem
6. If similarity < 80%, iterate with suggestions
7. Export final track when complete
```

#### `/analyze-song` Workflow

```markdown
---
description: Full song analysis and stem extraction
---

1. Import MP3 to Ableton Live
2. Run stem separation (High Quality mode)
3. Export stems to `stems/i_am_machine/`
4. Analyze each stem for characteristics:
   - BPM/tempo
   - Key/scale
   - Frequency content
   - Transient analysis
5. Generate analysis report
```

#### `/compare-tracks` Workflow

```markdown
---
description: Compare recreated track to original stem
---

1. // turbo
   Export track audio: `python scripts/export_track.py {track_index}`
2. Run comparison:
   ```bash
   python -c "from agents import compare; compare('{stem}', {track})"
   ```
3. Display similarity score and differences
4. Ask Ollama for improvement suggestions
```

---

## 3. Agent Orchestration

### Option A: Sequential (Simple)

```python
async def recreate_song():
    stems = ["drums", "bass", "vocals", "others"]

    for stem in stems:
        agent = get_agent_for_stem(stem)
        result = await agent.execute()

        while result.similarity < 0.8:
            suggestions = await ollama_suggest(result.diff)
            result = await agent.refine(suggestions)

        log(f"{stem}: {result.similarity:.0%}")
```

### Option B: Parallel (Advanced)

```python
async def recreate_song():
    stems = ["drums", "bass", "vocals", "others"]

    tasks = [
        recreate_stem(stem)
        for stem in stems
    ]

    results = await asyncio.gather(*tasks)

    # Final mix
    await MixerAgent().execute()
```

---

## 4. Ollama Integration Points

### Current Agent Pattern
```python
class BaseAgent:
    ollama_model: str = "llama3"
    ollama_base_url: str = "http://localhost:11434"
```

### Enhanced Pattern with Suggestions
```python
class StemComparisonAgent(BaseAgent):
    async def get_ollama_suggestions(
        self,
        stem_name: str,
        similarity: float,
        spectral_diff: dict
    ) -> list[str]:
        prompt = f"""
        I'm recreating the {stem_name} from "I Am Machine" by Lily Palmer.
        Current similarity: {similarity:.0%}

        Spectral differences:
        - Low end (20-200Hz): {spectral_diff['low']}
        - Mids (200-2kHz): {spectral_diff['mid']}
        - Highs (2k-20kHz): {spectral_diff['high']}

        What Ableton Live 12 adjustments would improve the match?
        List 3 specific, actionable suggestions.
        """

        response = await self.ollama_query(prompt)
        return self.parse_suggestions(response)
```

### Ollama Query Method
```python
async def ollama_query(self, prompt: str) -> str:
    import httpx

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{self.ollama_base_url}/api/generate",
            json={
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]
```

---

## 5. Documentation Integration

### Using `.antigravity/docs/`

The Antigravity agent can reference documentation:

```
USER: @.antigravity/docs/mcp.md Create a stem separation tool
```

### Using `.gemini/docs/`

Gemini CLI can use documentation for headless operations:

```bash
gemini --yolo "$(cat .gemini/docs/mcp.md) Create stem separation tool"
```

### Using `.claude/docs/`

Claude CLI can reference patterns:

```bash
claude "@.claude/docs/tool-use.md Create comparison tool" -d src/
```

---

## 6. Progress Tracking

### GUI Callbacks (DearPyGUI)

```python
def update_stem_progress(stem: str, progress: float):
    """Update GUI progress bar for stem."""
    dpg.set_value(f"progress_{stem}", progress)

def show_similarity_chart(history: list[float]):
    """Display similarity improvement over iterations."""
    dpg.set_value("similarity_chart", history)
```

### Terminal Progress

```python
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("[cyan]Drums...", total=1.0)

    while not done:
        similarity = agent.get_similarity()
        progress.update(task, completed=similarity)
```

---

## 7. Error Handling

### Retry Logic

```python
async def with_retry(func, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return await func()
        except AbletonConnectionError:
            await asyncio.sleep(2 ** attempt)
    raise MaxRetriesExceeded()
```

### Graceful Degradation

```python
async def recreate_stem(stem: str):
    try:
        return await full_recreation(stem)
    except OllamaUnavailable:
        # Fall back to template-based approach
        return await template_recreation(stem)
```

---

## 8. State Management

### Persistence Between Sessions

```python
@dataclass
class RecreationState:
    stem: str
    iteration: int
    best_similarity: float
    track_index: int
    timestamp: datetime

def save_state(state: RecreationState):
    path = Path(".antigravity/state/recreation.json")
    path.write_text(state.model_dump_json())

def load_state() -> RecreationState | None:
    path = Path(".antigravity/state/recreation.json")
    if path.exists():
        return RecreationState.model_validate_json(path.read_text())
    return None
```

---

## 9. Workflow Commands

### Quick Access via `/slash-commands`

| Command | Description |
|---------|-------------|
| `/extract-stems` | Run stem separation on source MP3 |
| `/recreate drums` | Start drums recreation workflow |
| `/compare 3` | Compare track 3 to its target stem |
| `/status` | Show recreation progress for all stems |
| `/suggestions` | Get Ollama suggestions for current track |

### Implementation in `.agent/workflows/`

```markdown
# .agent/workflows/extract-stems.md
---
description: Extract stems from source audio
---
// turbo-all

1. Verify Ableton is running: `make check-port`
2. Import audio: `python scripts/import_audio.py {audio_path}`
3. Trigger separation: `python scripts/separate_stems.py`
4. Export stems: `python scripts/export_stems.py`
5. Analyze stems: `python scripts/analyze_all_stems.py`
```

---

## 10. Next Steps

### Immediate Research Tasks
1. [ ] Test Ollama llama3 for music production suggestions
2. [ ] Prototype librosa spectral comparison
3. [ ] Design state persistence schema
4. [ ] Create first workflow file

### Design Tasks
1. [ ] Define agent → MCP tool mapping
2. [ ] Design iteration limit strategy
3. [ ] Plan GUI integration points

### Documentation Tasks
1. [ ] Add workflow examples to `.antigravity/docs/`
2. [ ] Document Ollama prompting strategies
3. [ ] Create agent troubleshooting guide
