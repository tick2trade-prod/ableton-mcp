"""Audio Viewer - Waveform and Spectrogram display using DearPyGui."""

from pathlib import Path

import numpy as np

try:
    import dearpygui.dearpygui as dpg

    DPG_AVAILABLE = True
except ImportError:
    DPG_AVAILABLE = False

try:
    import librosa

    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False


class AudioViewer:
    """Audio visualization component with waveform and spectrogram display."""

    def __init__(self):
        if not DPG_AVAILABLE:
            raise ImportError("DearPyGui not installed. Run: uv pip install dearpygui")
        if not LIBROSA_AVAILABLE:
            raise ImportError("Librosa not installed. Run: uv pip install librosa")

        self.current_file: str | None = None
        self.audio_data: np.ndarray | None = None
        self.sample_rate: int = 22050
        self.analysis_result: dict = {}

    def load_audio(self, filepath: str, duration: float = 30.0) -> dict:
        """Load and analyze audio file."""
        self.current_file = filepath
        self.audio_data, self.sample_rate = librosa.load(
            filepath, sr=22050, duration=duration
        )

        # Get tempo
        onset_env = librosa.onset.onset_strength(y=self.audio_data, sr=self.sample_rate)
        tempo, beats = librosa.beat.beat_track(
            onset_envelope=onset_env, sr=self.sample_rate
        )
        tempo_val = float(tempo[0]) if hasattr(tempo, "__iter__") else float(tempo)

        # Get key
        chroma = librosa.feature.chroma_cqt(y=self.audio_data, sr=self.sample_rate)
        key_idx = int(np.mean(chroma, axis=1).argmax())
        keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

        # Spectrogram
        D = librosa.stft(self.audio_data)
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

        self.analysis_result = {
            "file": Path(filepath).name,
            "tempo": tempo_val,
            "key": keys[key_idx],
            "duration": len(self.audio_data) / self.sample_rate,
            "spectrogram": S_db,
            "chroma": chroma,
        }

        return self.analysis_result

    def update_plots(self):
        """Update DearPyGui plots with current audio data."""
        if self.audio_data is None:
            return

        # Downsample waveform for display (max 10000 points)
        samples = len(self.audio_data)
        step = max(1, samples // 10000)
        x_data = np.arange(0, samples, step) / self.sample_rate
        y_data = self.audio_data[::step]

        # Update waveform
        dpg.set_value("waveform_series", [x_data.tolist(), y_data.tolist()])

        # Update info text
        result = self.analysis_result
        dpg.set_value(
            "info_text",
            f"File: {result.get('file', 'N/A')}\n"
            f"Tempo: {result.get('tempo', 0):.1f} BPM\n"
            f"Key: {result.get('key', 'N/A')}\n"
            f"Duration: {result.get('duration', 0):.1f}s",
        )

        # Update chroma plot
        if "chroma" in result:
            chroma_mean = result["chroma"].mean(axis=1)
            dpg.set_value(
                "chroma_series",
                [list(range(12)), chroma_mean.tolist()],
            )

    def create_window(self, parent: str | None = None):
        """Create the audio viewer window/panel."""
        container = parent if parent else "audio_viewer_window"

        if parent is None:
            dpg.add_window(label="Audio Viewer", tag=container, width=800, height=600)

        with dpg.group(parent=container):
            # Info panel
            dpg.add_text("No file loaded", tag="info_text")
            dpg.add_separator()

            # Waveform plot
            with dpg.plot(label="Waveform", height=200, width=-1):
                dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)", tag="waveform_x")
                dpg.add_plot_axis(dpg.mvYAxis, label="Amplitude", tag="waveform_y")
                dpg.add_line_series(
                    [], [], label="Audio", parent="waveform_y", tag="waveform_series"
                )

            dpg.add_separator()

            # Chroma plot
            with dpg.plot(label="Chroma (Key Distribution)", height=150, width=-1):
                dpg.add_plot_axis(dpg.mvXAxis, label="Note", tag="chroma_x")
                dpg.add_plot_axis(dpg.mvYAxis, label="Intensity", tag="chroma_y")
                dpg.add_bar_series(
                    list(range(12)),
                    [0] * 12,
                    label="Chroma",
                    parent="chroma_y",
                    tag="chroma_series",
                )


def standalone_viewer(filepath: str | None = None):
    """Run audio viewer as standalone application."""
    if not DPG_AVAILABLE:
        print("Error: DearPyGui not installed. Run: uv pip install dearpygui")
        return

    dpg.create_context()
    dpg.create_viewport(title="Ableton MCP - Audio Viewer", width=900, height=700)

    viewer = AudioViewer()

    def file_callback(sender, app_data):
        selections = app_data.get("selections", {})
        if selections:
            filepath = list(selections.values())[0]
            viewer.load_audio(filepath)
            viewer.update_plots()

    # Main window
    with dpg.window(label="Audio Analysis", tag="main_window"):
        dpg.add_button(
            label="Open Audio File",
            callback=lambda: dpg.show_item("file_dialog"),
        )
        dpg.add_separator()
        viewer.create_window(parent="main_window")

    # File dialog
    with dpg.file_dialog(
        directory_selector=False,
        show=False,
        callback=file_callback,
        tag="file_dialog",
        width=700,
        height=400,
    ):
        dpg.add_file_extension(".wav")
        dpg.add_file_extension(".mp3")
        dpg.add_file_extension(".flac")
        dpg.add_file_extension(".aiff")

    # Load file if provided
    if filepath:
        viewer.load_audio(filepath)
        viewer.update_plots()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    import sys

    filepath = sys.argv[1] if len(sys.argv) > 1 else None
    standalone_viewer(filepath)
