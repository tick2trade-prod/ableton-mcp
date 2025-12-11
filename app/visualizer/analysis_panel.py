"""Analysis Panel - Display librosa analysis results using DearPyGui."""


try:
    import dearpygui.dearpygui as dpg

    DPG_AVAILABLE = True
except ImportError:
    DPG_AVAILABLE = False


class AnalysisPanel:
    """Panel for displaying audio analysis results."""

    KEY_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    def __init__(self):
        if not DPG_AVAILABLE:
            raise ImportError("DearPyGui not installed. Run: uv pip install dearpygui")
        self.analysis_data: dict = {}

    def update(self, analysis: dict):
        """Update panel with new analysis data."""
        self.analysis_data = analysis

        # Update text displays
        dpg.set_value("analysis_file", f"File: {analysis.get('file', 'N/A')}")
        dpg.set_value("analysis_tempo", f"Tempo: {analysis.get('tempo', 0):.1f} BPM")
        dpg.set_value("analysis_key", f"Key: {analysis.get('key', 'N/A')}")
        dpg.set_value(
            "analysis_duration", f"Duration: {analysis.get('duration', 0):.1f}s"
        )

        # Update recommendations
        tempo = analysis.get("tempo", 0)
        key = analysis.get("key", "C")

        rec_text = f"""
Ableton Recommendations:
------------------------
1. Set Global Tempo: {tempo:.1f} BPM
2. Root Note: {key}
3. Scale: {key} Minor (for techno)
"""
        dpg.set_value("recommendations", rec_text)

    def create_window(self, parent: str | None = None):
        """Create the analysis panel window."""
        container = parent if parent else "analysis_panel_window"

        if parent is None:
            dpg.add_window(
                label="Analysis Results", tag=container, width=300, height=400
            )

        with dpg.group(parent=container):
            dpg.add_text("Analysis Results", tag="analysis_header")
            dpg.add_separator()

            dpg.add_text("File: N/A", tag="analysis_file")
            dpg.add_text("Tempo: -- BPM", tag="analysis_tempo")
            dpg.add_text("Key: N/A", tag="analysis_key")
            dpg.add_text("Duration: --s", tag="analysis_duration")

            dpg.add_separator()
            dpg.add_text("", tag="recommendations", wrap=280)


if __name__ == "__main__":
    if not DPG_AVAILABLE:
        print("Error: DearPyGui not installed")
    else:
        dpg.create_context()
        dpg.create_viewport(title="Analysis Panel Test", width=350, height=450)

        panel = AnalysisPanel()
        panel.create_window()

        # Test data
        panel.update(
            {
                "file": "test_track.wav",
                "tempo": 128.5,
                "key": "E",
                "duration": 180.0,
            }
        )

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("analysis_panel_window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()
