# 0002: i_o Alchemy Techno Demo

| Field | Value |
|-------|-------|
| Branch | `feature/0001-rack-chain-tools` |
| Type | Demo / Integration Test |
| Status | ✅ macOS Working |

---

## Objective
Create a rerunnable integration test that demonstrates the MCP by generating an i_o style techno track in Ableton Live.

## Prerequisites
- [x] Ableton Live running with AbletonMCP control surface
- [x] `make test-connection` passes
- [x] macOS setup documented
- [x] Analysis dependencies available (See [0004-feature-librosa-analyze-track.md](./0004-feature-librosa-analyze-track.md))
- [x] Reference Assets: `assets/audio/reference/ALCHEMY_I_O.mp3`

## Ableton Configuration

| Setting | Value |
|---------|-------|
| `ABLETON_VERSION` | 12.3.1 |
| `ABLETON_EDITION` | Intro (Student) |
| `ABLETON_MAX_TRACKS` | 16 |

---

## Implementation Checklist

### Test Structure
- [x] `tests/techno/conftest.py` (Fixtures)
- [x] `tests/techno/test_instruments.py` (Sound Loading)
- [x] `tests/techno/test_patterns.py` (Pattern Logic)
- [x] `tests/techno/test_arrangement.py` (Full Track)

### Test Steps (Arrangement)
1. [x] Clear tracks / Setup
2. [x] Set tempo (Spec says 130, Analysis TBD)
3. [x] Create/Reuse 6 Tracks
4. [x] Load Instruments (Dynamic Search)
5. [x] Create Clips with "Alchemy" Patterns
    - [x] Kick: driving 4/4
    - [x] Bass: rolling offbeat (E Minor)
    - [x] Lead: acid/303 style (E Minor)
6. [x] Start playback
7. [x] Verify Output

## External Dependencies Policy

Any git submodules in `external/` (e.g., `redis-mcp`) must adhere to strict READ-ONLY rules:

1.  **Read-Only**: Do not edit files inside `external/`. Changes will be ignored or lost.
2.  **No Imports**: Do not import code from `external/` into the main project. Use them for reference only.
3.  **Excluded**: `external/` must be excluded from:
    *   Tests (`pytest` norecursedirs)
    *   Linting (`pre-commit` exclude)
    *   Formatting
4.  **Version Control**: Pin submodules to specific commit SHAs. Do not track branches.
5.  **Git Configuration**: Use `ignore = dirty` in `.gitmodules`.

## Sound Design Goals

| Track | Pattern | Effect Chain |
|-------|---------|--------------|
| **Kick Heavy** | 4-on-floor, 130 BPM | Saturator (Heavy), EQ Eight |
| **Sub Bass** | E minor rumble | Sidechain to kick, Saturator |
| **Acid Lead** | 303-style pattern | Auto Filter + LFO, Ping Pong Delay |
| **Stab** | Offbeat hits | Reverb, Chorus |
| **Hi-Hats** | 16ths + open hats | EQ Eight (hi-pass) |
| **Perc** | Claps on 2&4, ride | Drum Bus |

---

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| macOS | ✅ Working | Tested on Live 12.3.1 Intro |
| Windows | ⏳ Pending | Need to test Remote Script path |

## Run Test

```bash
make test-one TEST=test_io_techno
# or
pytest tests/test_io_techno.py -v
```
```

## Recent Progress
- **Build & Deploy**: Implemented robust `Makefile` targets (`build-local`, `build-docker-local`), `config.yaml` for environment variables, and `scripts/deploy.py`.
- **Clean Slate**: Added `scripts/clear_tracks.py` to programmatically reset the Ableton session (down to 1 track) before tests.
- **Tool Documentation**: Created `TOOLS.md` listing all 27 available MCP tools.
- **Linting**: Enforced strict `pre-commit` checks (ruff, large file exclusion) and fixed existing codebase issues.
- **Robustness**: Added fallback logic for instrument loading in `tests/techno/test_arrangement.py` to handle missing specific presets by falling back to generic devices.

## Remaining Tasks
- [x] Verify `scripts/clear_tracks.py` works consistently (deletes down to 1 track).
- [x] Confirm `make build-local-no-cache-clean` passes locally with a fresh state.
- [x] Address any lingering reference audio file warnings in pre-commit (handled via exclude).
