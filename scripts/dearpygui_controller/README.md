# DearPyGUI Controller - I Am Machine Recreation

A comprehensive multi-agent system for recreating Lilly Palmer's "I Am Machine" peak-time techno track in Ableton Live 12.

## Overview

This project uses specialized AI agents to automate the production workflow for recreating a professional techno track. Each agent focuses on a specific aspect of production, from synthesis programming to mastering.

## Features

### 🎛️ 16-Track Template
- **Low-End Engine** (Tracks 1-4): Kick, Rumble, Rolling Bass, Acid Line
- **Rhythmic Core** (Tracks 5-10): Hi-hats, Claps, Toms, Glitch, Ride
- **Harmonics** (Tracks 11-14): Synth Stabs, Drone, Vocals, Vocal FX
- **FX & Transitions** (Tracks 15-16): Risers, Impacts

### 🤖 Specialized Agents

#### Foundation Agents
- **ResearchAgent**: Production technique research and documentation search
- **ComposerAgent**: MIDI pattern generation (4-on-floor, 16ths, bass lines)
- **MixerAgent**: Device chain loading and volume balancing
- **VerifierAgent**: Quality assurance and project validation

#### New Synthesis & Sound Design Agents
- **SynthesizerAgent**: Advanced synth programming
  - FM synthesis (Operator) for bass
  - 303 Acid lines with Drift
  - Wavetable programming for stabs
  - Meld configuration for drones

- **PercussionAgent**: Advanced percussion patterns
  - Syncopated tribal toms
  - Random glitch percussion
  - Continuous ride cymbals

- **VocalsAgent**: Vocal processing chains
  - Telephone EQ curves for robotic quality
  - Vocoder effects with drum modulation
  - Granular synthesis for glitches
  - Reverse sweeps and frequency shifting

#### Effects & Processing Agents
- **TransitionAgent**: Energy transitions
  - 16-bar risers with filter automation
  - Impacts with Roar processing
  - Stereo width expansion

- **ModulationAgent**: Automation and movement
  - Filter cutoff automation
  - LFO routing
  - Reverb send automation
  - Parameter modulation

- **EffectsChainAgent**: Signal routing
  - Sidechain compression (Kick → Rumble, Bass, Acid, Ride)
  - Bass mono below 120Hz
  - Send/Return configuration
  - Mid/Side processing

#### Arrangement & Mastering Agents
- **ArrangementAgent**: Timeline structure
  - 7-section arrangement (Intro → Development → Breakdown → Drops → Outro)
  - 16-bar phrasing blocks
  - Track automation and muting
  - DJ-friendly intro/outro

- **MasteringAgent**: Master bus processing
  - Glue Compressor for cohesion
  - Mid/Side EQ for stereo control
  - Roar saturation for warmth
  - Limiting for -6 to -8 LUFS

### 🏭 Agent Factory

Create agents easily with the AgentFactory:

```python
from dearpygui_controller.agent_factory import AgentFactory

# Create single agent
agent = AgentFactory.create("synthesizer", verbose=True)

# Create batch
agents = AgentFactory.create_batch(["composer", "mixer", "mastering"])

# List all available agents
agents_info = AgentFactory.list_agents()

# Create full production workflow
workflow_agents = AgentFactory.create_production_workflow()
```

### 🎼 Workflow Orchestrator

Execute multi-agent workflows with error handling and progress tracking:

```python
from dearpygui_controller.workflow_orchestrator import (
    WorkflowOrchestrator,
    WorkflowStep,
)

# Create orchestrator
orch = WorkflowOrchestrator(verbose=True)

# Define workflow
workflow = [
    WorkflowStep("Program Synths", "synthesizer", timeout=60.0),
    WorkflowStep("Create Patterns", "composer", params={"bars": 4}),
    WorkflowStep("Apply Mixing", "mixer"),
    WorkflowStep("Master Track", "mastering"),
]

# Execute
result = await orch.execute_workflow(workflow)

# Or use predefined workflows
full_workflow = WorkflowOrchestrator.get_full_production_workflow()
result = await orch.execute_workflow(full_workflow)
```

## Installation

```bash
# Install dependencies
pip install pytest pytest-asyncio dearpygui

# Run tests
pytest scripts/dearpygui_controller/tests/ -v
```

## Usage

### Quick Start

```python
import asyncio
from dearpygui_controller.workflow_orchestrator import run_full_production

# Run complete production workflow
result = asyncio.run(run_full_production(verbose=True))

print(f"Success: {result.success}")
print(f"Duration: {result.duration:.2f}s")
print(f"Steps completed: {result.steps_completed}/{result.steps_completed + result.steps_failed}")
```

### Individual Agents

```python
from dearpygui_controller.agents import SynthesizerAgent, PercussionAgent

# Program synthesizers
synth_agent = SynthesizerAgent(verbose=True)
result = await synth_agent.execute()

# Create percussion patterns
perc_agent = PercussionAgent(verbose=True)
result = await perc_agent.execute(bars=4)
```

### Custom Workflows

```python
from dearpygui_controller.workflow_orchestrator import (
    WorkflowOrchestrator,
    WorkflowStep,
)

# Create custom workflow
custom_workflow = [
    WorkflowStep(
        name="Research Acid Techno",
        agent_type="research",
        params={"topic": "303 acid bass programming"},
        required=False,  # Optional step
    ),
    WorkflowStep(
        name="Program Acid Line",
        agent_type="synthesizer",
        params={"track_index": 3},  # Track 4: Acid Line
        required=True,
        timeout=30.0,
    ),
    WorkflowStep(
        name="Apply Modulation",
        agent_type="modulation",
        params={"track_index": 3},
        required=True,
    ),
]

orch = WorkflowOrchestrator(verbose=True)
result = await orch.execute_workflow(custom_workflow)
```

## Testing

The project includes comprehensive tests for all agents and utilities:

```bash
# Run all tests
pytest scripts/dearpygui_controller/tests/ -v

# Run specific test file
pytest scripts/dearpygui_controller/tests/test_new_agents.py -v

# Run tests with coverage
pytest scripts/dearpygui_controller/tests/ --cov=dearpygui_controller
```

### Test Coverage

- ✅ Base agent functionality (callbacks, logging, MCP integration)
- ✅ All 12 agents (foundation + new specialized agents)
- ✅ Agent factory (creation, batching, categorization)
- ✅ Workflow orchestrator (execution, error handling, timeouts)
- ✅ Configuration (tracks, parameters, singleton)
- ✅ UI components (panels, callbacks)

## Project Structure

```
dearpygui_controller/
├── agents/                  # Agent implementations
│   ├── base_agent.py       # Base agent class
│   ├── composer_agent.py   # Pattern generation
│   ├── mixer_agent.py      # Device chains
│   ├── verifier_agent.py   # QA validation
│   ├── synthesizer_agent.py    # NEW: Synth programming
│   ├── percussion_agent.py     # NEW: Percussion patterns
│   ├── vocals_agent.py         # NEW: Vocal processing
│   ├── transition_agent.py     # NEW: Risers/impacts
│   ├── modulation_agent.py     # NEW: Automation
│   ├── effects_chain_agent.py  # NEW: Signal routing
│   ├── arrangement_agent.py    # NEW: Timeline structure
│   └── mastering_agent.py      # NEW: Master bus
├── callbacks/              # GUI callbacks
├── layouts/                # GUI layouts
├── tests/                  # Comprehensive test suite
│   ├── test_agents.py          # Foundation agent tests
│   ├── test_new_agents.py      # NEW: Specialized agent tests
│   ├── test_agent_factory.py   # NEW: Factory tests
│   └── test_workflow_orchestrator.py  # NEW: Workflow tests
├── agent_factory.py        # NEW: Agent creation factory
├── workflow_orchestrator.py # NEW: Multi-agent workflows
├── config.py               # Configuration
└── main.py                 # GUI entry point
```

## Technical Specifications

### Target Output
- **BPM**: 136
- **Key**: F Minor
- **Style**: Peak-time Techno (Spannung)
- **LUFS**: -6 to -8 (integrated)
- **Duration**: ~6 minutes (140 bars)
- **Track Count**: 16

### Arrangement Structure
1. **Intro** (0-16 bars): Kick, Rumble, Hats
2. **Development** (16-48 bars): Add Bass, Percussion
3. **Breakdown 1** (48-64 bars): Filter, build tension
4. **Drop 1** (64-96 bars): Full energy
5. **Bridge** (96-112 bars): Minimal, Acid focus
6. **Main Drop** (112-128 bars): Maximum intensity
7. **Outro** (128-140 bars): Strip to Kick/Rumble

### Device Usage
- **Live 12 Specific**: Roar, Meld, Drum Sampler, Drift
- **Classic**: Operator, Wavetable, Reverb, Echo, EQ Eight
- **Processing**: Glue Compressor, Limiter, Vocoder

## Agent Workflow

The recommended production workflow:

1. **Research** (optional): Gather production techniques
2. **Synthesis**: Program all synths (Bass, Acid, Stabs, Drone)
3. **Composition**: Create drum and bass patterns
4. **Percussion**: Add toms, glitches, rides
5. **Vocals**: Process main vocal and FX
6. **Mixing**: Load devices and set levels
7. **Effects**: Configure sidechain and routing
8. **Transitions**: Create risers and impacts
9. **Modulation**: Apply automation
10. **Arrangement**: Structure timeline
11. **Mastering**: Final processing
12. **Verification**: QA checks

## Contributing

Contributions welcome! Please ensure:
- All new agents extend `BaseAgent`
- Comprehensive tests included
- Follows existing code style
- Documentation updated

## License

MIT License - See LICENSE file

## Acknowledgments

Based on the comprehensive technical analysis of Lilly Palmer's "I Am Machine" track in collaboration with Thomas Schumacher.
