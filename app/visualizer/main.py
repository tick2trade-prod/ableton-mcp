"""Main entry point for the DearPyGui Audio Visualizer."""

import sys
from pathlib import Path

try:
    import dearpygui.dearpygui as dpg

    DPG_AVAILABLE = True
except ImportError:
    DPG_AVAILABLE = False
    print("Warning: DearPyGui not installed. Run: uv pip install dearpygui")


def run_visualizer(initial_file: str | None = None):
    """Run the complete audio visualizer application.

    Args:
        initial_file: Optional path to audio file to load on startup
    """
    if not DPG_AVAILABLE:
        print("Error: DearPyGui not installed.")
        print("Install with: uv pip install dearpygui")
        return 1

    from app.visualizer.analysis_panel import AnalysisPanel
    from app.visualizer.asset_browser import AssetBrowser
    from app.visualizer.audio_viewer import AudioViewer

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

    # Create custom theme
    with dpg.theme() as global_theme, dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(
            dpg.mvThemeCol_WindowBg, (15, 15, 15), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_ChildBg, (25, 25, 25), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_Border, (60, 60, 60), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_Button, (40, 40, 40), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_ButtonHovered, (60, 60, 60), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_ButtonActive, (80, 80, 80), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_TitleBg, (40, 40, 40), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_TitleBgActive, (60, 60, 60), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_style(
            dpg.mvStyleVar_WindowRounding, 5, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_style(
            dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core
        )

    dpg.bind_theme(global_theme)

    # Main window layout
    with (
        dpg.window(label="Audio Visualizer", tag="main_window"),
        dpg.group(horizontal=True),
    ):
        # Left panel - Asset Browser
        with dpg.child_window(width=300, height=-1, tag="left_panel", border=True):
            dpg.add_text("ASSET BROWSER", tag="browser_title")
            dpg.add_separator()
            browser.create_window(parent="left_panel")

        # Center panel - Audio Viewer
        with dpg.child_window(width=-350, height=-1, tag="center_panel", border=True):
            with dpg.group(horizontal=True):
                dpg.add_text("AUDIO ANALYSIS", tag="viewer_title")
                dpg.add_spacer(width=20)
                dpg.add_button(
                    label="Open File...",
                    callback=lambda: dpg.show_item("file_dialog"),
                    width=100,
                )
            dpg.add_separator()

            viewer.create_window(parent="center_panel")

        # Right panel - Analysis Results
        with dpg.child_window(width=340, height=-1, tag="right_panel", border=True):
            dpg.add_text("DETAILS", tag="panel_title")
            dpg.add_separator()
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
        dpg.add_file_extension(".wav", color=(100, 255, 100, 255))
        dpg.add_file_extension(".mp3", color=(100, 255, 100, 255))
        dpg.add_file_extension(".flac", color=(100, 200, 255, 255))
        dpg.add_file_extension(".aiff", color=(100, 200, 255, 255))

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
