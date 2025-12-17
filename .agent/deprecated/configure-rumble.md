---
description: Configure Track 02 Rumble with MCP verification and debugging
---

# /configure-rumble Workflow

This workflow configures Track 02 (Rumble) in Ableton Live using MCP commands, verifies the configuration, and provides debugging if things fail.

## Prerequisites
- Ableton Live 12 running
- AbletonMCP control surface enabled
- Docker compose up (for Redis)

---

## Step 1: Verify Ableton Connection

// turbo
```bash
cd /Users/alexzh/ableton-mcp && uv run python -c "
from scripts.dearpygui_controller.agents.ableton_mcp_integration_agent import AbletonMCPIntegrationAgent
agent = AbletonMCPIntegrationAgent()
result = agent.verify_connection()
if result.success:
    print('✅ Connected to Ableton!')
    print(f'   Tempo: {result.data.get(\"tempo\")} BPM')
    print(f'   Tracks: {result.data.get(\"track_count\")}')
else:
    print(f'❌ Connection failed: {result.message}')
    print('\\nTroubleshooting:')
    print('1. Is Ableton Live running?')
    print('2. Is AbletonMCP selected in Preferences > Control Surface?')
    print('3. Restart Ableton if Remote Script was updated')
"
```

---

## Step 2: Create/Configure Rumble Track

// turbo
```bash
cd /Users/alexzh/ableton-mcp && uv run python live_set/lily_palmer/i_am_machine_v3/tracks/track_02_rumble.py
```

---

## Step 3: Verify Track State via MCP Integration Agent

// turbo
```bash
cd /Users/alexzh/ableton-mcp && uv run python -c "
from scripts.dearpygui_controller.agents.ableton_mcp_integration_agent import AbletonMCPIntegrationAgent
agent = AbletonMCPIntegrationAgent()
result = agent.verify_track_state(1)  # Track 02 is index 1
if result.success:
    print('✅ Track 02 verified:')
    print(f'   Name: {result.data.get(\"name\", \"Unknown\")}')
    print(f'   Arm: {result.data.get(\"arm\", \"Unknown\")}')
else:
    print(f'❌ Track verification failed: {result.message}')
"
```

---

## Step 4: Run Integration Tests

// turbo
```bash
cd /Users/alexzh/ableton-mcp && uv run pytest tests/i_am_machine_v3/unit/test_track_02_rumble.py -v --tb=short 2>&1 | head -40
```

---

## Step 5: If Tests Fail - Read Ableton Log

Only run this if Step 4 shows failures:

```bash
cd /Users/alexzh/ableton-mcp && uv run python -c "
from scripts.dearpygui_controller.agents.ableton_mcp_integration_agent import AbletonMCPIntegrationAgent
agent = AbletonMCPIntegrationAgent()
result = agent.read_ableton_log(lines=30)
if result.success:
    print('📋 Recent Ableton Log:')
    print('-' * 50)
    print(result.data.get('content', 'No content'))
else:
    print(f'❌ Could not read log: {result.message}')
"
```

---

## Step 6: Manual Configuration Reminder

After running the above steps, you need to manually configure in Ableton:

1. **Track 02 Audio Routing**:
   - Audio From: `01 - Kick`
   - Audio From Channel: `Post FX`
   - Monitor: `In`

2. **Load Missing Devices** (if not loaded via MCP):
   - Hybrid Reverb (or Reverb)
   - Roar (or Saturator)
   - EQ Eight
   - Compressor

3. **Configure Sidechain**:
   - Click Compressor's Sidechain button
   - Audio From: `01 - Kick`
   - Ratio: `Inf:1`
   - Attack: `0.1ms`
   - Release: `1/8` (sync)

---

## Step 7: Re-run Tests to Confirm

// turbo
```bash
cd /Users/alexzh/ableton-mcp && uv run pytest tests/i_am_machine_v3/unit/test_track_02_rumble.py -v --tb=short
```
