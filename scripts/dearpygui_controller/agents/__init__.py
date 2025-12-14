"""Agents package for I Am Machine recreation."""

from .arrangement_agent import ArrangementAgent
from .arranger_agent import ArrangerAgent
from .base_agent import BaseAgent
from .composer_agent import ComposerAgent
from .effects_chain_agent import EffectsChainAgent
from .mastering_agent import MasteringAgent
from .mixer_agent import MixerAgent
from .modulation_agent import ModulationAgent
from .percussion_agent import PercussionAgent
from .research_agent import ResearchAgent
from .sound_design_agent import SoundDesignAgent
from .synthesizer_agent import SynthesizerAgent
from .transition_agent import TransitionAgent
from .verifier_agent import VerifierAgent
from .vocals_agent import VocalsAgent

__all__ = [
    # Original agents
    "ArrangerAgent",
    "BaseAgent",
    "ResearchAgent",
    "ComposerAgent",
    "MixerAgent",
    "SoundDesignAgent",
    "VerifierAgent",
    # New specialized agents
    "ArrangementAgent",
    "EffectsChainAgent",
    "MasteringAgent",
    "ModulationAgent",
    "PercussionAgent",
    "SynthesizerAgent",
    "TransitionAgent",
    "VocalsAgent",
]
