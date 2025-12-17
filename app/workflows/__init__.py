"""Agent workflow orchestration for TDD-based track creation.

This module provides workflow orchestration for creating Ableton Live tracks
using Test-Driven Development (TDD) patterns. Each workflow corresponds to
a lane in the production pipeline.

Workflows:
- intro_drums: Create drum tracks (Kick, Snare, Hi-hats, Toms, Glitch, Ride)
- intro_bass: Create bass tracks (Rumble, Rolling Bass, Acid)
- intro_synths: Create synth tracks (Stabs, Drone)
- intro_vocals: Create vocal/FX tracks (Main Vocal, Vocal FX, Risers, Returns)

Usage:
    from app.workflows import IntroDrumsWorkflow

    workflow = IntroDrumsWorkflow()
    result = await workflow.execute()
"""

from .base import BaseWorkflow, TDDPhase, TrackSpec, TrackStatus, WorkflowResult
from .intro_bass import IntroBassWorkflow
from .intro_drums import IntroDrumsWorkflow
from .intro_synths import IntroSynthsWorkflow
from .intro_vocals import IntroVocalsWorkflow

__all__ = [
    # Base classes
    "BaseWorkflow",
    "TDDPhase",
    "TrackSpec",
    "TrackStatus",
    "WorkflowResult",
    # Workflows
    "IntroDrumsWorkflow",
    "IntroBassWorkflow",
    "IntroSynthsWorkflow",
    "IntroVocalsWorkflow",
]
