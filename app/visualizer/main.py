"""Main entry point for the DearPyGui Audio Visualizer."""

import sys
from pathlib import Path
from typing import Optional

try:
    import dearpygui.dearpygui as dpg

    DPG_AVAILABLE = True
except ImportError:
    DPG_AVAILABLE = False
    print("Warning: DearPyGui not installed. Run: uv pip install dearpygui")


def run_visualizer(initial_file: Optional[str] = None):
    """Run the complete audio visualizer application.

    Args:
        initial_file: Optional path to audio file to load on startup
    """
    if not DPG_AVAILABLE:
        print("Error: DearPyGui not installed.")
        print("Install with: uv pip install dearpygui")
        return 1

    from app.visualizer.audio_viewer import AudioViewer
    from app.visualizer.asset_browser import AssetBrowser
    from app.visualizer.analysis_panel import AnalysisPanel

    dpg.create_context()
    dpg.create_viewport(title="Ableton MCP - Audio Visualizer", width=1400, height=800)

    # Create components
    viewer = AudioViewer()
    browser = AssetBrowser()
    panel = AnalysisPanel()

    def on_file_selected(filepath: str):
        """Handle file selection from browser."""
        suffix = Path(filepath).suffix.lower()
        if suffix in {".wav", ".mp3", ".flac", ".aiff", ".ogg"}:
            analysis = viewer.load_audio(filepath)
            viewer.update_plots()
            panel.update(analysis)

    browser.on_file_selected = on_file_selected

    # Main window layout
    with dpg.window(label="Audio Visualizer", tag="main_window"):
        with dpg.group(horizontal=True):
            # Left panel - Asset Browser
            with dpg.child_window(width=350, height=-1, tag="left_panel"):
                dpg.add_text("Asset Browser", tag="browser_title")
                dpg.add_separator()
                browser.create_window(parent="left_panel")

            # Center panel - Audio Viewer
            with dpg.child_window(width=-350, height=-1, tag="center_panel"):
                dpg.add_text("Audio Analysis", tag="viewer_title")
                dpg.add_separator()

                # File dialog button
                dpg.add_button(
                    label="Open File...",
                    callback=lambda: dpg.show_item("file_dialog"),
                )
                dpg.add_separator()

                viewer.create_window(parent="center_panel")

            # Right panel - Analysis Results
            with dpg.child_window(width=300, height=-1, tag="right_panel"):
                panel.create_window(parent="right_panel")

    # File dialog
    def file_callback(sender, app_data):
        selections = app_data.get("selections", {})
        if selections:
            filepath = list(selections.values())[0]
            on_file_selected(filepath)

    with dpg.file_dialog(
        directory_selector=False,
        show=False,
        callback=file_callback,
        tag="file_dialog",
        width=700,
        height=400,
    ):
        dpg.add_file_extension(".wav", color=(0, 255, 0, 255))
        dpg.add_file_extension(".mp3", color=(0, 255, 0, 255))
        dpg.add_file_extension(".flac", color=(0, 200, 255, 255))
        dpg.add_file_extension(".aiff", color=(0, 200, 255, 255))

    # Load initial file if provided
    if initial_file and Path(initial_file).exists():
        on_file_selected(initial_file)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

    return 0


def main():
    """CLI entry point."""
    initial_file = sys.argv[1] if len(sys.argv) > 1 else None
    return run_visualizer(initial_file)


if __name__ == "__main__":
    sys.exit(main())
