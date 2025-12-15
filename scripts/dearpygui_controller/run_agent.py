#!/usr/bin/env python3
"""Run a single agent from the command line.

Usage:
    cd /Users/alexzh/ableton-mcp/scripts
    uv run python dearpygui_controller/run_agent.py composer
    uv run python dearpygui_controller/run_agent.py verifier
"""

import asyncio
import sys
from pathlib import Path

# Ensure package is importable
scripts_dir = Path(__file__).parent.parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from dearpygui_controller.agents import (
    ArrangerAgent,
    ComposerAgent,
    MixerAgent,
    ResearchAgent,
    SoundDesignAgent,
    VerifierAgent,
)


async def run_research():
    """Run the research agent."""
    agent = ResearchAgent(verbose=True)
    agent.set_log_callback(print)
    result = await agent.execute(topic="techno rumble kick production")
    print(f"\n{'=' * 60}")
    print(f"Result: {result.message}")
    if result.data:
        print(f"Techniques: {result.data.get('techniques', [])[:2]}")
    return result


async def run_composer():
    """Run the composer agent."""
    agent = ComposerAgent(verbose=True)
    agent.set_log_callback(print)

    # Just generate patterns (don't need MCP connection)
    print("\n=== Generating Patterns ===")

    kick = agent.generate_kick_pattern(bars=2)
    print(f"Kick pattern: {len(kick)} notes")

    hihat = agent.generate_hihat_pattern(bars=1)
    print(f"Hi-hat pattern: {len(hihat)} notes")

    bass = agent.generate_bass_pattern(bars=1)
    print(f"Bass pattern: {len(bass)} notes")

    print("\n=== Sample Kick Notes ===")
    for note in kick[:4]:
        print(
            f"  Beat {note['start_time']}: pitch={note['pitch']}, vel={note['velocity']}"
        )

    return True


async def run_mixer():
    """Run the mixer agent."""
    agent = MixerAgent(verbose=True)
    agent.set_log_callback(print)

    from dearpygui_controller.config import TRACKS

    print("\n=== Device Chains ===")
    for track in TRACKS[:4]:
        chain = agent.get_chain_for_track(track)
        vol = agent.get_volume_for_track(track)
        devices = [d["name"] for d in chain]
        print(f"{track.name}: {devices} @ {vol}dB")

    return True


async def run_verifier():
    """Run the verifier agent."""
    agent = VerifierAgent(verbose=True)
    agent.set_log_callback(print)
    result = await agent.execute()
    print(result.data.get("report", ""))
    return result


async def run_arranger():
    """Run the arranger agent."""
    agent = ArrangerAgent(verbose=True)
    agent.set_log_callback(print)
    result = await agent.execute(structure="techno_basic")
    print(f"Result: {result.message}")
    return result


async def run_sound_design():
    """Run the sound design agent."""
    agent = SoundDesignAgent(verbose=True)
    agent.set_log_callback(print)
    result = await agent.execute()
    print(f"Result: {result.message}")
    return result


AGENTS = {
    "research": run_research,
    "arranger": run_arranger,
    "composer": run_composer,
    "sound_design": run_sound_design,
    "mixer": run_mixer,
    "verifier": run_verifier,
}


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_agent.py <agent>")
        print(f"Available agents: {', '.join(AGENTS.keys())}")
        sys.exit(1)

    agent_name = sys.argv[1].lower()
    if agent_name not in AGENTS:
        print(f"Unknown agent: {agent_name}")
        print(f"Available: {', '.join(AGENTS.keys())}")
        sys.exit(1)

    print(f"\n{'=' * 60}")
    print(f"Running {agent_name.upper()} Agent")
    print(f"{'=' * 60}\n")

    asyncio.run(AGENTS[agent_name]())

    print(f"\n{'=' * 60}")
    print("Done!")


if __name__ == "__main__":
    main()
