"""Demo script showcasing the DearPyGUI Controller features."""

import asyncio

from agent_factory import AgentFactory
from workflow_orchestrator import (
    WorkflowOrchestrator,
    WorkflowStep,
)


async def demo_agent_factory():
    """Demonstrate AgentFactory usage."""
    print("\n" + "=" * 70)
    print("  DEMO 1: Agent Factory")
    print("=" * 70)

    # List all available agents
    print("\n📋 Available Agents:")
    agents_info = AgentFactory.list_agents()
    for agent_type, info in agents_info.items():
        print(f"  • {agent_type:15s} - {info['role']}")
        print(f"    Goal: {info['goal']}")

    # Create agents by category
    print("\n📁 Agents by Category:")
    categories = AgentFactory.get_agents_by_category()
    for category, agent_types in categories.items():
        print(f"  {category.upper()}: {', '.join(agent_types)}")

    # Create a single agent
    print("\n🎹 Creating Synthesizer Agent:")
    synth_agent = AgentFactory.create("synthesizer", verbose=False)
    print(f"  Role: {synth_agent.get_role()}")
    print(f"  Goal: {synth_agent.get_goal()}")

    # Create multiple agents
    print("\n🎼 Creating Batch of Agents:")
    agents = AgentFactory.create_batch(
        ["composer", "mixer", "mastering"],
        verbose=False,
    )
    for agent_type, agent in agents.items():
        print(f"  ✓ {agent_type}: {agent.get_role()}")


async def demo_individual_agents():
    """Demonstrate individual agent execution."""
    print("\n" + "=" * 70)
    print("  DEMO 2: Individual Agents")
    print("=" * 70)

    # Synthesizer Agent
    print("\n🎛️ Testing Synthesizer Agent:")
    synth_agent = AgentFactory.create("synthesizer", verbose=False)
    result = await synth_agent.execute()
    print(f"  Status: {'✓ Success' if result.success else '✗ Failed'}")
    print(f"  Message: {result.message}")
    if result.data.get("synths"):
        for synth in result.data["synths"]:
            print(f"    - {synth['track']}: {synth['device']} ({synth['params_count']} params)")

    # Percussion Agent
    print("\n🥁 Testing Percussion Agent:")
    perc_agent = AgentFactory.create("percussion", verbose=False)
    result = await perc_agent.execute(bars=2)
    print(f"  Status: {'✓ Success' if result.success else '✗ Failed'}")
    print(f"  Message: {result.message}")
    if result.data.get("patterns"):
        for pattern in result.data["patterns"]:
            print(f"    - {pattern['track']}: {pattern['notes_count']} notes")

    # Arrangement Agent
    print("\n🎼 Testing Arrangement Agent:")
    arr_agent = AgentFactory.create("arrangement", verbose=False)
    result = await arr_agent.execute(mode="markers")
    print(f"  Status: {'✓ Success' if result.success else '✗ Failed'}")
    if result.data.get("summary"):
        summary = result.data["summary"]
        print(f"  Total Bars: {summary['total_bars']}")
        print(f"  Sections: {summary['sections']}")
        print(f"  BPM: {summary['bpm']}")
        print(f"  Duration: {summary['duration_minutes']:.2f} minutes")


async def demo_workflow():
    """Demonstrate workflow orchestration."""
    print("\n" + "=" * 70)
    print("  DEMO 3: Workflow Orchestration")
    print("=" * 70)

    # Create orchestrator
    orch = WorkflowOrchestrator(verbose=True)

    # Custom workflow
    print("\n🔄 Running Custom Workflow:")
    workflow = [
        WorkflowStep(
            name="Program Synthesizers",
            agent_type="synthesizer",
            required=True,
        ),
        WorkflowStep(
            name="Create Percussion Patterns",
            agent_type="percussion",
            params={"bars": 4},
            required=True,
        ),
        WorkflowStep(
            name="Configure Effects Routing",
            agent_type="effects_chain",
            params={"mode": "sidechain"},
            required=True,
        ),
        WorkflowStep(
            name="Structure Arrangement",
            agent_type="arrangement",
            params={"mode": "markers"},
            required=True,
        ),
    ]

    result = await orch.execute_workflow(workflow, stop_on_error=False)

    print("\n📊 Workflow Results:")
    print(f"  Success: {result.success}")
    print(f"  Duration: {result.duration:.2f}s")
    print(f"  Completed: {result.steps_completed}/{result.steps_completed + result.steps_failed}")

    print("\n📋 Step Results:")
    for step_name, step_result in result.step_results.items():
        status = "✓" if step_result.success else "✗"
        print(f"  {status} {step_name}: {step_result.message}")


async def demo_predefined_workflows():
    """Demonstrate predefined workflows."""
    print("\n" + "=" * 70)
    print("  DEMO 4: Predefined Workflows")
    print("=" * 70)

    # Quick workflow
    print("\n⚡ Quick Workflow (Testing):")
    quick_workflow = WorkflowOrchestrator.get_quick_workflow()
    print(f"  Steps: {len(quick_workflow)}")
    for step in quick_workflow:
        print(f"    - {step.name} ({step.agent_type})")

    # Full production workflow
    print("\n🎼 Full Production Workflow:")
    full_workflow = WorkflowOrchestrator.get_full_production_workflow()
    print(f"  Total Steps: {len(full_workflow)}")
    print("\n  Workflow Phases:")

    current_phase = None
    for i, step in enumerate(full_workflow, 1):
        # Group by phase
        if "Research" in step.name:
            phase = "Phase 1: Research"
        elif "Synthesizer" in step.name or "Program" in step.name:
            phase = "Phase 2: Synthesis"
        elif "Pattern" in step.name or "Percussion" in step.name:
            phase = "Phase 3: Rhythm"
        elif "Vocal" in step.name:
            phase = "Phase 4: Vocals"
        elif "Mixing" in step.name or "Routing" in step.name or "Effects" in step.name:
            phase = "Phase 5: Mixing"
        elif "Transition" in step.name or "Modulation" in step.name:
            phase = "Phase 6: Movement"
        elif "Arrangement" in step.name:
            phase = "Phase 7: Arrangement"
        elif "Master" in step.name:
            phase = "Phase 8: Mastering"
        elif "Verify" in step.name:
            phase = "Phase 9: Verification"
        else:
            phase = "Other"

        if phase != current_phase:
            current_phase = phase
            print(f"\n  {phase}")

        required_marker = "🔴" if step.required else "⚪"
        timeout_info = f" (timeout: {step.timeout}s)" if step.timeout else ""
        print(f"    {i:2d}. {required_marker} {step.name}{timeout_info}")


async def main():
    """Run all demos."""
    print("\n" + "█" * 70)
    print("  I AM MACHINE - DearPyGUI Controller Demo")
    print("  Comprehensive Multi-Agent Production System")
    print("█" * 70)

    try:
        await demo_agent_factory()
        await demo_individual_agents()
        await demo_workflow()
        await demo_predefined_workflows()

        print("\n" + "=" * 70)
        print("  ✅ Demo Complete!")
        print("=" * 70)
        print("\n💡 Next Steps:")
        print("  1. Run tests: pytest scripts/dearpygui_controller/tests/ -v")
        print("  2. Try the GUI: python scripts/dearpygui_controller/main.py")
        print("  3. Run full workflow: python -m dearpygui_controller.workflow_orchestrator")
        print()

    except Exception as e:
        print(f"\n❌ Demo Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
