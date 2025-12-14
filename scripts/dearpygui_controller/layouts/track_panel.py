"""Track panel layout for DearPyGUI controller."""

try:
    import dearpygui.dearpygui as dpg

    HAS_DPG = True
except ImportError:
    HAS_DPG = False
    dpg = None

from ..config import TRACKS


def create_track_panel(parent: int | str) -> dict[int, int]:
    """Create track status panel with progress bars.

    Args:
        parent: Parent window/group ID

    Returns:
        Dict mapping track_index to progress bar tag
    """
    if not HAS_DPG:
        return {}

    progress_bars = {}

    with dpg.child_window(label="Track Status", parent=parent, width=-1, height=300):
        dpg.add_text("Track Progress")
        dpg.add_separator()

        for track in TRACKS:
            with dpg.group(horizontal=True):
                # Track name label
                dpg.add_text(f"{track.name:20s}", tag=f"label_track_{track.index}")

                # Progress bar
                tag = dpg.add_progress_bar(
                    default_value=0.0,
                    overlay="0%",
                    width=-1,
                    tag=f"progress_track_{track.index}",
                )
                progress_bars[track.index] = tag

    return progress_bars


def update_track_progress(track_index: int, progress: float) -> None:
    """Update progress bar for a track.

    Args:
        track_index: Track index (0-15)
        progress: Progress value (0.0 - 1.0)
    """
    if not HAS_DPG:
        return

    tag = f"progress_track_{track_index}"
    if dpg.does_item_exist(tag):
        dpg.set_value(tag, progress)
        dpg.configure_item(tag, overlay=f"{int(progress * 100)}%")


def reset_all_progress() -> None:
    """Reset all track progress bars to 0."""
    for i in range(16):
        update_track_progress(i, 0.0)
