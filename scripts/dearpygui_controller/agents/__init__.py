"""Agents package for I Am Machine recreation."""

from .arrangement_agent import ArrangementAgent
from .arranger_agent import ArrangerAgent
from .automation_agent import AutomationAgent
from .base_agent import BaseAgent
from .browser_agent import BrowserAgent
from .composer_agent import ComposerAgent
from .effects_chain_agent import EffectsChainAgent
from .groove_agent import GrooveAgent
from .mastering_agent import MasteringAgent
from .mixer_agent import MixerAgent
from .modulation_agent import ModulationAgent
from .percussion_agent import PercussionAgent
from .research_agent import ResearchAgent
from .return_track_agent import ReturnTrackAgent
from .sampler_agent import SamplerAgent
from .sidechain_agent import SidechainAgent
from .sound_design_agent import SoundDesignAgent
from .synthesizer_agent import SynthesizerAgent
from .transition_agent import TransitionAgent
from .verifier_agent import VerifierAgent
from .vocals_agent import VocalsAgent

__all__ = [
    # Original agents
    "ArrangerAgent",
    "AutomationAgent",
    "BaseAgent",
    "BrowserAgent",
    "ResearchAgent",
    "ComposerAgent",
    "MixerAgent",
    "SoundDesignAgent",
    "VerifierAgent",
    # New specialized agents
    "ArrangementAgent",
    "EffectsChainAgent",
    "GrooveAgent",
    "MasteringAgent",
    "ModulationAgent",
    "PercussionAgent",
    "ReturnTrackAgent",
    "SamplerAgent",
    "SidechainAgent",
    "SynthesizerAgent",
    "TransitionAgent",
    "VocalsAgent",
]
