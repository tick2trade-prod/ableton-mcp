"""Test script for newly implemented agents."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.dearpygui_controller.agents import (
    ArrangementAgent,
    EffectsChainAgent,
    MasteringAgent,
    ModulationAgent,
    PercussionAgent,
    SynthesizerAgent,
    TransitionAgent,
    VocalsAgent,
)


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_result(agent_name: str, result):
    """Print agent execution result."""
    status = "✓ SUCCESS" if result.success else "✗ FAILED"
    print(f"\n{agent_name}: {status}")
    print(f"  Message: {result.message}")

    if result.data:
        print("  Data:")
        for key, value in result.data.items():
            if isinstance(value, list) and len(value) > 0:
                print(f"    {key}: {len(value)} items")
                for item in value[:3]:  # Show first 3 items
                    print(f"      - {item}")
                if len(value) > 3:
                    print(f"      ... and {len(value) - 3} more")
            elif isinstance(value, dict):
                print(f"    {key}:")
                for k, v in value.items():
                    print(f"      {k}: {v}")
            else:
                print(f"    {key}: {value}")

    if result.errors:
        print("  Errors:")
        for error in result.errors:
            print(f"    - {error}")


async def test_synthesizer_agent():
    """Test SynthesizerAgent."""
    print_section("Testing SynthesizerAgent")

    agent = SynthesizerAgent(verbose=True)
    print(f"Role: {agent.get_role()}")
    print(f"Goal: {agent.get_goal()}")

    # Test configuring all synth tracks
    result = await agent.execute()
    print_result("SynthesizerAgent", result)

    return result.success


async def test_percussion_agent():
    """Test PercussionAgent."""
    print_section("Testing PercussionAgent")

    agent = PercussionAgent(verbose=True)
    print(f"Role: {agent.get_role()}")
    print(f"Goal: {agent.get_goal()}")

    # Test creating percussion patterns
    result = await agent.execute(bars=4)
    print_result("PercussionAgent", result)

    return result.success


async def test_vocals_agent():
    """Test VocalsAgent."""
    print_section("Testing VocalsAgent")

    agent = VocalsAgent(verbose=True)
    print(f"Role: {agent.get_role()}")
    print(f"Goal: {agent.get_goal()}")

    # Test processing vocal tracks
    result = await agent.execute()
    print_result("VocalsAgent", result)

    return result.success


async def test_transition_agent():
    """Test TransitionAgent."""
    print_section("Testing TransitionAgent")

    agent = TransitionAgent(verbose=True)
    print(f"Role: {agent.get_role()}")
    print(f"Goal: {agent.get_goal()}")

    # Test configuring transitions
    result = await agent.execute()
    print_result("TransitionAgent", result)

    return result.success


async def test_modulation_agent():
    """Test ModulationAgent."""
    print_section("Testing ModulationAgent")

    agent = ModulationAgent(verbose=True)
    print(f"Role: {agent.get_role()}")
    print(f"Goal: {agent.get_goal()}")

    # Test applying modulation
    result = await agent.execute()
    print_result("ModulationAgent", result)

    return result.success


async def test_effects_chain_agent():
    """Test EffectsChainAgent."""
    print_section("Testing EffectsChainAgent")

    agent = EffectsChainAgent(verbose=True)
    print(f"Role: {agent.get_role()}")
    print(f"Goal: {agent.get_goal()}")

    # Test configuring sidechain
    result = await agent.execute(mode="sidechain")
    print_result("EffectsChainAgent (Sidechain)", result)

    # Test configuring bass mono
    result2 = await agent.execute(mode="bass_mono")
    print_result("EffectsChainAgent (Bass Mono)", result2)

    return result.success and result2.success


async def test_arrangement_agent():
    """Test ArrangementAgent."""
    print_section("Testing ArrangementAgent")

    agent = ArrangementAgent(verbose=True)
    print(f"Role: {agent.get_role()}")
    print(f"Goal: {agent.get_goal()}")

    # Test creating arrangement
    result = await agent.execute(mode="markers")
    print_result("ArrangementAgent", result)

    return result.success


async def test_mastering_agent():
    """Test MasteringAgent."""
    print_section("Testing MasteringAgent")

    agent = MasteringAgent(verbose=True)
    print(f"Role: {agent.get_role()}")
    print(f"Goal: {agent.get_goal()}")

    # Test mastering (analyze only in mock mode)
    result = await agent.execute(analyze_only=False)
    print_result("MasteringAgent", result)

    return result.success


async def main():
    """Run all agent tests."""
    print("\n" + "█" * 70)
    print("  I AM MACHINE - Agent Test Suite")
    print("█" * 70)
    print("\nRunning in MOCK MODE (no Ableton connection required)")

    results = {}

    # Run tests
    results["Synthesizer"] = await test_synthesizer_agent()
    results["Percussion"] = await test_percussion_agent()
    results["Vocals"] = await test_vocals_agent()
    results["Transition"] = await test_transition_agent()
    results["Modulation"] = await test_modulation_agent()
    results["EffectsChain"] = await test_effects_chain_agent()
    results["Arrangement"] = await test_arrangement_agent()
    results["Mastering"] = await test_mastering_agent()

    # Summary
    print_section("Test Summary")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for agent_name, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status:8s} {agent_name}Agent")

    print(f"\n  Total: {passed}/{total} agents passed")

    if passed == total:
        print("\n  🎉 All agents tested successfully!")
        return 0
    else:
        print(f"\n  ⚠️  {total - passed} agent(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
