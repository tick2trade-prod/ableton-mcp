# Implementation Plan (P4): deepagents Orchestrator — Todo + Filesystem + Subagents (Ollama)

**Status**: Active
**Version**: 2.0.0
**Last Updated**: 2025-12-14
**Depends On**: `specs/active/imp_plan_p3_scaffold.md`, `specs/active/005.md`, `specs/active/006.md`

## 1. Outcome (What P4 Delivers)

By the end of P4, the MVP orchestration is upgraded from “scripted runner” into a **deep agent**:

- explicit todo-list planning (“plan then act”)
- durable filesystem context (`live_set/lily_palmer/i_am_machine/workspace/`)
- safe subagent delegation (CrewAI roles) under a single state machine
- pause/resume/retry without losing track of progress

The DearPyGUI controller becomes a front-end to this orchestrator, not a collection of ad-hoc buttons.

## 2. Orchestrator Graph Design (LangGraph / deepagents)

### 2.1 Nodes (Minimum)

1. **Perception**
   - query Ableton state (session + track info)
   - update `state.json` snapshot
2. **Planner**
   - update todo list (next track/step)
   - choose which recipe to apply next
3. **Executor**
   - execute deterministic recipe steps via tool adapter
4. **Verifier**
   - run checks; if failures, decide retry vs HITL pause
5. **HITL Gate**
   - surface proposed changes and wait for approval in GUI

### 2.2 Control Loop

The orchestrator loop is:

`Perception → Planner → Executor → Perception → Verifier → (Planner | HITL | DONE)`

## 3. Middleware Requirements

### 3.1 TodoListMiddleware (Required)

- Todo items correspond to concrete, testable steps:
  - “Ensure 16 tracks exist”
  - “Build Kick clip”
  - “Build Rumble chain”
  - “Verify rhythm section”
- Each item has:
  - `status` (pending/in_progress/done/failed)
  - `attempts`
  - `artifacts` (links to event IDs)

### 3.2 FilesystemMiddleware (Required)

All intermediate artifacts are persisted:

- generated patterns (JSON)
- resolved URIs
- device parameter maps
- verifier reports

### 3.3 SubAgentMiddleware (Optional but Recommended)

Use subagents for reasoning and parameter selection only:

- Rhythm Programmer
- Mix Engineer
- Sound Designer
- Verifier/QA

Subagents must never bypass the recipe/tool adapter layer.

## 4. DearPyGUI ↔ Orchestrator Contract

### 4.1 Commands (UI → Orchestrator)

- `CONNECT`, `DISCONNECT`
- `RUN_ALL`, `RUN_SECTION(name)`, `RUN_TRACK(index)`
- `PAUSE`, `STOP`, `STEP`
- `APPROVE(action_id)`, `REJECT(action_id)`

### 4.2 Events (Orchestrator → UI)

- `LOG(line)`
- `PROGRESS(track_index, value)`
- `TODO_UPDATED(todo_state)`
- `VERIFICATION_REPORT(report_json)`
- `ERROR(error_json)`

## 5. Reliability Requirements

### 5.1 Idempotency

Every executor action must be safe to retry:

- “ensure track exists” should detect existing tracks
- “ensure clip exists” should not overwrite without HITL approval
- “ensure device chain exists” should detect existing devices before adding

### 5.2 Retry Policy

- default: max 3 attempts per todo item
- exponential backoff between attempts (bounded)
- on repeated failure: pause and ask for human input

## 6. Observability

Minimum:

- correlation IDs per run
- `events.jsonl` includes: timestamp, action, params (redacted if needed), result/error
- UI can filter logs by track and by todo item

Optional:

- OpenTelemetry spans around tool calls (only if already used elsewhere in repo)

## 7. Acceptance Criteria (P4 Done)

- P4-AC1: Orchestrator can resume from `state.json` + `events.jsonl` after restart.
- P4-AC2: GUI can pause/step/stop without crashing and without corrupting state.
- P4-AC3: Todo list accurately reflects what is done and what remains.
- P4-AC4: Subagents (CrewAI) can be enabled/disabled without changing recipe correctness.
