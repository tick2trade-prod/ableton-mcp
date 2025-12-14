# Agent Enhancement Pipeline

## Goal
Enhance all agents in `scripts/dearpygui_controller/agents/` using relevant sections from the 955-page Ableton 12 manual via token-efficient semantic search.

## Checklist

### Phase 1: Infrastructure Setup
- [ ] Check Redis status (required for vector embeddings)
- [ ] Verify Ableton Codegen MCP status
- [ ] Check if PDF is already embedded in Redis
- [ ] Embed PDF if needed (one-time operation)
- [ ] Verify embedding stats

### Phase 2: Agent Analysis
- [ ] List all agents in `/scripts/dearpygui_controller/agents/`
- [ ] Analyze each agent's purpose and functionality
- [ ] Map agents to relevant Ableton concepts

### Phase 3: Documentation Search
For each agent:
- [ ] `arranger_agent.py` - Search for arrangement/automation
- [ ] `arrangement_agent.py` - Search for clip/scene management
- [ ] `composer_agent.py` - Search for MIDI/note composition
- [ ] `effects_chain_agent.py` - Search for audio effects/racks
- [ ] `mastering_agent.py` - Search for mastering chain
- [ ] `mixer_agent.py` - Search for mixer/routing
- [ ] `modulation_agent.py` - Search for LFO/modulation
- [ ] `percussion_agent.py` - Search for drum racks
- [ ] `sound_design_agent.py` - Search for synthesis/devices
- [ ] `synthesizer_agent.py` - Search for synth devices
- [ ] `transition_agent.py` - Search for crossfades/transitions
- [ ] `vocals_agent.py` - Search for vocal processing
- [ ] `verifier_agent.py` - Search for quality metrics
- [ ] `research_agent.py` - (Meta agent, may skip)

### Phase 4: Enhancement Generation
- [ ] Create enhancement script that processes all agents
- [ ] Generate recommendations per agent
- [ ] Save results to artifact for review

### Phase 5: Review & Apply
- [ ] Review enhancement recommendations
- [ ] User approval for changes
- [ ] Apply approved enhancements
