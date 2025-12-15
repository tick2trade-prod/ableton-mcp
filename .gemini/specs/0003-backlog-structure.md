# Spec 0003: Project Structure Refactor

## Status: ✅ Phase 1 Complete | 🚧 Phase 2 In Progress

**Last Updated:** 2025-12-11  
**Commit:** `ea44cd3` - refactor: adopt redis-mcp project structure with src/ layout

---

## Objective
Adopt a standard project structure similar to `redis-mcp` to improve maintainability and discoverability, while supporting Antigravity agent workflows.

---

## ✅ Completed (Phase 1)

### Core Structure Migration
- [x] Created `src/` directory layout
- [x] Moved `MCP_Server/` → `src/ableton_mcp/`
- [x] Moved `AbletonMCP_Remote_Script/` → `src/remote_script/`
- [x] Added `src/__init__.py` and `src/ableton_mcp/version.py`
- [x] Removed old directories

### Build System
- [x] Updated `pyproject.toml` to use `uv_build` backend
- [x] Updated entry point: `src.ableton_mcp.server:main`
- [x] Added `build-docker-local` target to Makefile
- [x] Updated Dockerfile with OS/IDE/MODEL build arguments

### Configuration
- [x] Expanded `config.yaml` with comprehensive settings
- [x] Updated `tests/config.py` to load from YAML
- [x] Created `gemini-extension.json` for agent discovery

### Verification
- [x] All 27 tests passing (11.77s)
- [x] Package builds successfully with uv_build
- [x] Ableton connection verified (port 9877)
- [x] Pre-commit hooks passing

---

## 🚧 Remaining Tasks (Phase 2)

### Directory Structure Refinement

#### 1. Move Analysis Module
```bash
analysis/analyze_track.py → src/ableton_mcp/analysis/track.py
```
**Rationale:** Audio analysis is core functionality, should be in main package

#### 2. Create `examples/` Directory
```
examples/
  __init__.py
  explore_browser.py    # Move from scripts/
  techno/               # Consider moving from tests/techno/
    patterns.py
    README.md
```
**Rationale:** Separate example/demo code from DevOps scripts

#### 3. Create `app/` Layer (Optional)
```
app/
  __init__.py
  workflows/            # Agent orchestration
  visualizer/           # DearPyGui GUI (see below)
```
**Rationale:** Application layer for agent-facing logic and GUI tools

---

## 🔬 Research: DearPyGui for Audio Visualization & Asset Management

### Overview
**DearPyGui** is a GPU-accelerated Python GUI framework ideal for:
- Real-time audio waveform visualization
- Spectrogram display
- Asset browser/manager
- Integration with librosa and NumPy

### Key Capabilities

#### 1. Audio Visualization with Librosa
```python
import dearpygui.dearpygui as dpg
import librosa
import numpy as np

# Load audio with librosa
y, sr = librosa.load('audio.wav')

# Create waveform plot
dpg.add_line_series(x=np.arange(len(y)), y=y, parent="waveform_plot")

# Create spectrogram
D = librosa.stft(y)
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
dpg.add_heat_series(S_db, parent="spectrogram_plot")
```

**Features:**
- Real-time waveform updates via `dpg.set_value()`
- GPU-accelerated rendering for smooth playback
- Native NumPy array support
- Multiple plot types: line, scatter, heatmap

#### 2. File Browser & Asset Manager
```python
# Built-in file dialog
dpg.add_file_dialog(
    directory_selector=False,
    show=True,
    callback=load_audio_callback,
    file_filter="Audio Files (*.wav *.mp3){.wav,.mp3}",
    width=700,
    height=400
)

# Custom asset browser with thumbnails
dpg.add_child_window("asset_browser")
for asset in assets:
    dpg.add_image_button(asset.thumbnail)
    dpg.add_text(asset.name)
```

**Features:**
- Built-in file/directory dialogs
- Custom tree views for folder navigation
- Image thumbnails for visual assets
- Drag-and-drop support

#### 3. Proposed Implementation Structure

```
app/visualizer/
  __init__.py
  main.py              # DearPyGui app entry point
  audio_viewer.py      # Waveform/spectrogram display
  asset_browser.py     # File browser for assets/
  analysis_panel.py    # Librosa analysis results
  themes.py            # DPG themes/styling
```

### Integration with Current Codebase

#### Asset Organization
```
assets/
  audio/
    reference/         # Reference tracks
    samples/           # Audio samples
    exports/           # Rendered outputs
  midi/
    patterns/          # MIDI patterns
    templates/         # MIDI templates
  projects/            # Ableton project files
  analysis/            # Librosa analysis cache (JSON)
```

#### Workflow
1. **Browse Assets:** DearPyGui file browser shows `assets/` structure
2. **Select Audio:** Click file → loads with librosa
3. **Visualize:** Display waveform, spectrogram, chromagram
4. **Analyze:** Run librosa features (tempo, key, spectral)
5. **Export:** Save analysis to `assets/analysis/`
6. **Load to Ableton:** Send to MCP server via tools

### Example: Audio Analysis Viewer

```python
import dearpygui.dearpygui as dpg
import librosa
import numpy as np

class AudioAnalyzer:
    def __init__(self):
        dpg.create_context()
        
    def load_audio(self, filepath):
        y, sr = librosa.load(filepath)
        
        # Waveform
        dpg.set_value("waveform", [np.arange(len(y)), y])
        
        # Spectrogram
        D = librosa.stft(y)
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        dpg.set_value("spectrogram", S_db.tolist())
        
        # Features
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        
        dpg.set_value("tempo_text", f"Tempo: {tempo:.1f} BPM")
        dpg.set_value("chroma_plot", chroma.tolist())
        
    def create_ui(self):
        with dpg.window(label="Audio Analyzer", width=1200, height=800):
            # File browser
            dpg.add_button(label="Open Audio", callback=self.show_file_dialog)
            
            # Waveform plot
            with dpg.plot(label="Waveform", height=200):
                dpg.add_plot_axis(dpg.mvXAxis, label="Samples")
                dpg.add_plot_axis(dpg.mvYAxis, label="Amplitude", tag="y_axis")
                dpg.add_line_series([], [], tag="waveform", parent="y_axis")
            
            # Spectrogram
            with dpg.plot(label="Spectrogram", height=300):
                dpg.add_plot_axis(dpg.mvXAxis, label="Time")
                dpg.add_plot_axis(dpg.mvYAxis, label="Frequency")
                dpg.add_heat_series([], tag="spectrogram")
            
            # Analysis results
            dpg.add_text("", tag="tempo_text")
```

### Dependencies
```toml
[project.optional-dependencies]
gui = [
    "dearpygui>=1.11.0",
    "librosa>=0.10.0",
    "numpy>=1.24.0",
    "pillow>=10.0.0",  # For thumbnails
]
```

### Makefile Targets
```makefile
install-gui: ## Install GUI dependencies
	uv sync --group gui

run-visualizer: ## Launch audio visualizer
	.venv/bin/python -m app.visualizer.main

analyze-asset: ## Analyze audio file (usage: make analyze-asset FILE=path/to/audio.wav)
	.venv/bin/python -m app.visualizer.audio_viewer $(FILE)
```

---

## Proposed Final Structure

```
/
  src/
    ableton_mcp/            # Main MCP server package
      __init__.py
      server.py
      version.py
      analysis/             # ← MOVE analysis/ here
        __init__.py
        track.py            # Librosa integration
    remote_script/          # Ableton Remote Script
      __init__.py
  
  app/                      # ← NEW: Application layer
    __init__.py
    visualizer/             # DearPyGui GUI
      __init__.py
      main.py
      audio_viewer.py
      asset_browser.py
    workflows/              # Agent orchestration
  
  examples/                 # ← NEW: Example scripts
    __init__.py
    explore_browser.py      # ← MOVE from scripts/
    techno/                 # ← CONSIDER moving from tests/
      patterns.py
      README.md
  
  tests/                    # Test suite
    config.py
    conftest.py
    test_tools.py
    test_rack_chain_tools.py
    techno/                 # OR keep here if integration tests
  
  scripts/                  # DevOps scripts only
    deploy.py
    clear_tracks.py
    *.sh
  
  assets/                   # Binary assets
    audio/
      reference/
      samples/
      exports/
    midi/
    projects/
    analysis/               # ← NEW: Cached librosa analysis
  
  external/                 # Git submodules
  config.yaml
  pyproject.toml
  gemini-extension.json
  Makefile
```

---

## References
- [redis-mcp](https://github.com/redis/mcp-redis) - Structure reference
- [DearPyGui Docs](https://dearpygui.readthedocs.io/) - GUI framework
- [Librosa](https://librosa.org/) - Audio analysis
- [Antigravity MCP Docs](https://antigravity.google/docs/mcp)

