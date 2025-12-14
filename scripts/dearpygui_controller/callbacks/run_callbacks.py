"""Run callbacks for DearPyGUI controller buttons."""

import asyncio
from threading import Thread

from ..agents import (
    ArrangerAgent,
    ComposerAgent,
    MixerAgent,
    ResearchAgent,
    SoundDesignAgent,
    VerifierAgent,
)
from ..config import TRACKS
from ..layouts.agent_panel import get_enabled_agents
from ..layouts.log_panel import clear_log, log_message
from ..layouts.track_panel import reset_all_progress, update_track_progress

# State
_running = False
_current_thread: Thread | None = None


def _make_progress_callback():
    """Create progress callback that updates the GUI."""

    def callback(track_index: int, progress: float):
        update_track_progress(track_index, progress)

    return callback


def _make_log_callback():
    """Create log callback that updates the GUI."""

    def callback(message: str):
        log_message(message)

    return callback


async def _run_pipeline():
    """Run the full agent pipeline."""
    global _running

    enabled = get_enabled_agents()
    log_message(f"Starting with agents: {', '.join(enabled)}")

    progress_cb = _make_progress_callback()
    log_cb = _make_log_callback()

    # Research phase
    if "research" in enabled and _running:
        log_message("=== Phase 1: Research ===")
        agent = ResearchAgent()
        agent.set_log_callback(log_cb)
        result = await agent.execute(topic="techno rumble kick production")
        log_message(f"Research: {result.message}")

    # Composition phase
    if "composer" in enabled and _running:
        log_message("=== Phase 2: Composition ===")
        agent = ComposerAgent()
        agent.set_progress_callback(progress_cb)
        agent.set_log_callback(log_cb)

        for track in TRACKS:
            if not _running:
                break
                result = await agent.execute(track_index=track.index)
                log_message(f"Compose {track.name}: {result.message}")

    # Sound Design phase
    if "sound_design" in enabled and _running:
        log_message("=== Phase 3: Sound Design ===")
        agent = SoundDesignAgent()
        agent.set_progress_callback(progress_cb)
        agent.set_log_callback(log_cb)

        # Configure all tracks
        result = await agent.execute()
        log_message(f"Sound Design: {result.message}")

    # Arrangement phase
    if "arranger" in enabled and _running:
        log_message("=== Phase 4: Arrangement ===")
        agent = ArrangerAgent()
        agent.set_log_callback(log_cb)
        result = await agent.execute(structure="techno_basic")
        log_message(f"Arrangement: {result.message}")

    # Mixing phase
    if "mixer" in enabled and _running:
        log_message("=== Phase 5: Mixing ===")
        agent = MixerAgent()
        agent.set_progress_callback(progress_cb)
        agent.set_log_callback(log_cb)

        for track in TRACKS:
            if not _running:
                break
            result = await agent.execute(track_index=track.index)
            log_message(f"Mix {track.name}: {result.message}")

    # Verification phase
    if "verifier" in enabled and _running:
        log_message("=== Phase 6: Verification ===")
        agent = VerifierAgent()
        agent.set_log_callback(log_cb)
        result = await agent.execute()
        log_message(f"Verify: {result.message}")

    if _running:
        log_message("=== Pipeline Complete ===")
    else:
        log_message("=== Pipeline Stopped ===")

    _running = False


def _run_async_pipeline():
    """Run pipeline in async context."""
    asyncio.run(_run_pipeline())


def on_run_all(sender=None, app_data=None):
    """Button callback: Run All."""
    global _running, _current_thread

    if _running:
        log_message("Already running!")
        return

    _running = True
    log_message("Starting I AM MACHINE recreation pipeline...")

    # Run in background thread to not block GUI
    _current_thread = Thread(target=_run_async_pipeline, daemon=True)
    _current_thread.start()


def on_stop(sender=None, app_data=None):
    """Button callback: Stop."""
    global _running

    if _running:
        log_message("Stopping pipeline...")
        _running = False
    else:
        log_message("Not running")


def on_reset(sender=None, app_data=None):
    """Button callback: Reset."""
    global _running

    _running = False
    reset_all_progress()
    clear_log()
    log_message("Reset complete - ready to start")


async def _run_verify_only():
    """Run verification only."""
    log_message("=== Running Verification ===")
    agent = VerifierAgent()
    agent.set_log_callback(_make_log_callback())
    result = await agent.execute()

    # Print the report
    report = result.data.get("report", "")
    for line in report.split("\n"):
        log_message(line)


def on_verify(sender=None, app_data=None):
    """Button callback: Verify."""
    log_message("Starting verification...")
    thread = Thread(target=lambda: asyncio.run(_run_verify_only()), daemon=True)
    thread.start()


def is_running() -> bool:
    """Check if pipeline is currently running."""
    return _running
