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

## Ableton Configuration

| Setting | Value |
|---------|-------|
| `ABLETON_VERSION` | 12.3.1 |
| `ABLETON_EDITION` | Intro (Student) |
| `ABLETON_MAX_TRACKS` | 16 |

---

## Test Steps

1. [ ] Clear existing tracks (keep 2 default)
2. [ ] Set tempo to 130 BPM
3. [ ] Create 6 MIDI tracks:
   - Kick Heavy
   - Sub Bass
   - Acid Lead
   - Stab
   - Hi-Hats
   - Perc
4. [ ] Add 4-bar clips with patterns
5. [ ] Start playback
6. [ ] Verify in Ableton

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
