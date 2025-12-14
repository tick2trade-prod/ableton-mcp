#!/usr/bin/env python3
"""DearPyGUI Controller for I Am Machine recreation.

Main entry point for the GUI application.

Usage:
    cd /Users/alexzh/ableton-mcp/scripts
    uv run python dearpygui_controller/main.py
"""

import sys
from pathlib import Path

# Ensure package is importable
scripts_dir = Path(__file__).parent.parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

try:
    import dearpygui.dearpygui as dpg

    HAS_DPG = True
except ImportError:
    HAS_DPG = False
    print("ERROR: DearPyGUI not installed. Run: uv sync --extra gui-controller")
    sys.exit(1)

from dearpygui_controller.callbacks import on_reset, on_run_all, on_stop, on_verify
from dearpygui_controller.config import TRACKS, get_config
from dearpygui_controller.layouts import (
    create_agent_panel,
    create_log_panel,
    create_track_panel,
)
from dearpygui_controller.layouts.log_panel import log_message


def create_main_window():
    """Create the main application window."""
    with dpg.window(label="I AM MACHINE Controller", tag="main_window"):
        # Header
        dpg.add_text("I AM MACHINE - Lily Palmer Recreation", color=(100, 200, 255))
        dpg.add_text("16 Tracks | 136 BPM | F Minor", color=(150, 150, 150))
        dpg.add_separator()

        # Main layout: Agent panel (left) + Track panel (right)
        with dpg.group(horizontal=True):
            # Left column - Agent panel
            create_agent_panel("main_window")

            # Right column - Track panel
            with dpg.child_window(width=-1, height=300):
                create_track_panel("main_window")

        dpg.add_separator()

        # Log panel
        create_log_panel("main_window")

        dpg.add_separator()

        # Control buttons
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="▶ RUN ALL",
                callback=on_run_all,
                width=120,
            )
            dpg.add_button(
                label="⏹ STOP",
                callback=on_stop,
                width=80,
            )
            dpg.add_button(
                label="🔄 RESET",
                callback=on_reset,
                width=80,
            )
            dpg.add_button(
                label="📊 VERIFY",
                callback=on_verify,
                width=100,
            )

        # Status bar
        dpg.add_separator()
        config = get_config()
        dpg.add_text(
            f"Ableton: {config.ableton.host}:{config.ableton.port} | "
            f"Ollama: {config.ollama.model}",
            color=(100, 100, 100),
        )


def setup_theme():
    """Configure the application theme."""
    with dpg.theme() as global_theme, dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 4)
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 40))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (50, 50, 60))

    dpg.bind_theme(global_theme)


def main():
    """Main entry point."""
    dpg.create_context()

    # Setup theme
    setup_theme()

    # Create main window
    create_main_window()

    # Viewport setup
    dpg.create_viewport(
        title="I AM MACHINE - DearPyGUI Controller",
        width=800,
        height=700,
    )
    dpg.setup_dearpygui()

    # Set main window as primary
    dpg.set_primary_window("main_window", True)

    # Initial log message
    log_message("Controller initialized")
    log_message(f"Ready to create {len(TRACKS)} tracks")

    # Show and start
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
