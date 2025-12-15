Consider using ableton_codegen to figure out how to get access to the available default sounds to avoid this issue if needed. We should add tests in @testsif we're missing coverage to avoid this issue in the future. 
use ableton_codegen = ["embed_ableton_docs", "search_ableton_docs", "get_docs_index_stats", "search_ableton_guides", "search_device_docs", "search_production_technique", "analyze_track_script", "analyze_all_track_scripts", "generate_track_code", "validate_track_code", "get_codegen_status"]

### You may not have access to this file, but this is the currently installed .gemini MCPs that are accesible in Antigravity IDE.   /Users/alexzh/.gemini/antigravity/mcp_config.json. Now notice that we're locally building out this 'ableton-mcp' as the primary project we're working on locally. However we're not running a 'ableton-mcp' since we're acessing it and using it locally. 

```
{
  "mcpServers": {
    "redis": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-redis"
      ],
      "env": {
        "REDIS_URL": "redis://localhost:8001/"
      }
    },
    "sota_researcher_v2": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/Users/alexzh/ableton-mcp",
        "python",
        "/Users/alexzh/ableton-mcp/scripts/deepagents/sota_researcher_v2.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/alexzh/ableton-mcp"
      }
    },
    "deepagents": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/Users/alexzh/ableton-mcp",
        "python",
        "/Users/alexzh/ableton-mcp/scripts/deepagents/mcp_server_deepagents_v2.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/alexzh/ableton-mcp"
      }
    },
    "research_mcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/Users/alexzh/ableton-mcp",
        "python",
        "/Users/alexzh/ableton-mcp/scripts/research_mcp/mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/alexzh/ableton-mcp"
      }
    },
    "ableton_codegen": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/Users/alexzh/ableton-mcp",
        "python",
        "/Users/alexzh/ableton-mcp/scripts/ableton_cache_ast_codegen_mcp/mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/alexzh/ableton-mcp"
      }
    }
  }
}
```

### Recommendation context
Based on the sonic profile of "I Am Machine" by Lily Palmer (Peak Time Techno, ~135 BPM) and your goal to stay "simple," here is exactly which Ableton Live Stock Assets you should use to recreate each element.

You do not need external plugins. The "Core Library" has everything.

1. The Low End (Kick & Rumble)

The track is defined by a massive, distorted kick with a reverb "rumble" tail.

The Kick:

Browser Path: Packs > Core Library > Drums > Samples > Kicks > Kick 909.aif

Why: It’s the industry standard. Use Drum Buss (Drive: 20%+, Boom: 20%) to make it punch like the track.

The Rumble:

Source: Use the same Kick 909.

Processing Chain: Send the kick to a Return Track with: Reverb (Decay: 600ms, Size: 100%) -> Overdrive -> EQ Eight (Cut everything above 150Hz). This creates that rolling thunder sound.

2. Percussion (The "Train" Rhythm)

Techno relies on "rolling" 16th-note hats to create momentum.

Open Hi-Hat:

Browser Path: Packs > Core Library > Drums > Samples > Hihats > Hihat 909 Open.aif

Placement: Place on the "off-beat" (steps 3, 7, 11, 15).

Closed Hi-Hat (The Driver):

Browser Path: Packs > Core Library > Drums > Samples > Hihats > Hihat 909 Closed.aif

Placement: Place on every 16th note between the kicks.

The Ride:

Browser Path: Packs > Core Library > Drums > Samples > Cymbals > Ride 909.aif

Usage: Bring this in during high-energy sections (the drop).

3. The Synths (Hypnotic Stabs)

Lily Palmer uses dark, repetitive synth stabs.

The "Acid" Squelch:

Instrument: Analog

Preset: Sounds > Bass > Acid Example (or init patch).

Tweak: Turn up the Resonance on Filter 1 and map the Frequency to a knob. This mimics the TB-303 sound.

The Dark Stab:

Instrument: Operator

Algorithm: Select the "FM" algorithm (boxes stacked vertically).

Settings: Set Oscillator B to a slightly higher Coarse tuning (e.g., 2 or 3) to add a metallic, techno texture. Add Echo for that dubby delay.

4. The Vocals ("I Am Machine")

The Robot Voice:

Tool: Vocoder

Technique: Record yourself saying "I Am Machine."

Carrier: Load Operator (Saw wave) on a separate track.

Routing: Set the Vocoder's "Carrier" audio from the Operator track. This forces your voice to sound like the synthesizer.
