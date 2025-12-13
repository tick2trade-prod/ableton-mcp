"""Asset Browser - File browser for assets/ directory using DearPyGui."""

from collections.abc import Callable
from pathlib import Path

try:
    import dearpygui.dearpygui as dpg

    DPG_AVAILABLE = True
except ImportError:
    DPG_AVAILABLE = False


class AssetBrowser:
    """File browser component for navigating the assets/ directory."""

    AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".aiff", ".ogg"}
    MIDI_EXTENSIONS = {".mid", ".midi"}

    def __init__(self, root_path: str | None = None):
        if not DPG_AVAILABLE:
            raise ImportError("DearPyGui not installed. Run: uv pip install dearpygui")

        if root_path is None:
            self.root_path = Path(__file__).parent.parent.parent / "assets"
        else:
            self.root_path = Path(root_path)

        self.current_path = self.root_path
        self.on_file_selected: Callable[[str], None] | None = None

    def get_directory_contents(self, path: Path) -> tuple[list[Path], list[Path]]:
        """Get sorted directories and files from a path."""
        if not path.exists():
            return [], []

        dirs = sorted([p for p in path.iterdir() if p.is_dir()])
        files = sorted([p for p in path.iterdir() if p.is_file()])
        return dirs, files

    def get_file_icon(self, path: Path) -> str:
        """Get emoji icon based on file type."""
        suffix = path.suffix.lower()
        if suffix in self.AUDIO_EXTENSIONS:
            return "🎵"
        elif suffix in self.MIDI_EXTENSIONS:
            return "🎹"
        elif suffix == ".json":
            return "📄"
        elif suffix == ".als":
            return "🎛️"
        else:
            return "📁" if path.is_dir() else "📄"

    def refresh_browser(self):
        """Refresh the file browser display."""
        dpg.delete_item("file_list", children_only=True)

        dirs, files = self.get_directory_contents(self.current_path)

        # Update path display
        rel_path = self.current_path.relative_to(self.root_path)
        dpg.set_value("path_display", f"📂 assets/{rel_path}")

        # Add parent directory option if not at root
        if self.current_path != self.root_path:
            with dpg.group(parent="file_list", horizontal=True):
                dpg.add_button(
                    label="⬆️ ..",
                    callback=lambda: self.navigate_to(self.current_path.parent),
                )

        # Add directories
        for d in dirs:
            with dpg.group(parent="file_list", horizontal=True):
                dpg.add_button(
                    label=f"📁 {d.name}",
                    callback=lambda s, a, u=d: self.navigate_to(u),
                )

        # Add files
        for f in files:
            icon = self.get_file_icon(f)
            with dpg.group(parent="file_list", horizontal=True):
                dpg.add_button(
                    label=f"{icon} {f.name}",
                    callback=lambda s, a, u=f: self.select_file(u),
                )

    def navigate_to(self, path: Path):
        """Navigate to a directory."""
        self.current_path = path
        self.refresh_browser()

    def select_file(self, path: Path):
        """Handle file selection."""
        if self.on_file_selected:
            self.on_file_selected(str(path))
        dpg.set_value("selected_file", f"Selected: {path.name}")

    def create_window(self, parent: str | None = None):
        """Create the asset browser window/panel."""
        container = parent if parent else "asset_browser_window"

        if parent is None:
            dpg.add_window(label="Asset Browser", tag=container, width=400, height=500)

        with dpg.group(parent=container):
            dpg.add_text("📂 assets/", tag="path_display")
            dpg.add_separator()

            with dpg.child_window(tag="file_list", height=-50):
                pass  # Will be populated by refresh_browser

            dpg.add_separator()
            dpg.add_text("No file selected", tag="selected_file")

        self.refresh_browser()


def standalone_browser(root_path: str | None = None):
    """Run asset browser as standalone application."""
    if not DPG_AVAILABLE:
        print("Error: DearPyGui not installed. Run: uv pip install dearpygui")
        return

    dpg.create_context()
    dpg.create_viewport(title="Ableton MCP - Asset Browser", width=500, height=600)

    browser = AssetBrowser(root_path)

    def on_select(filepath: str):
        print(f"Selected: {filepath}")

    browser.on_file_selected = on_select
    browser.create_window()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("asset_browser_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else None
    standalone_browser(root)
