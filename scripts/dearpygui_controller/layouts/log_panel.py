"""Log panel layout for DearPyGUI controller."""

from datetime import datetime

try:
    import dearpygui.dearpygui as dpg

    HAS_DPG = True
except ImportError:
    HAS_DPG = False
    dpg = None


LOG_TAG = "log_output"
_log_buffer: list[str] = []


def create_log_panel(parent: int | str) -> int | None:
    """Create log output panel.

    Args:
        parent: Parent window/group ID

    Returns:
        Log text widget tag
    """
    if not HAS_DPG:
        return None

    with dpg.child_window(label="Logs", parent=parent, width=-1, height=150):
        dpg.add_text("Activity Log")
        dpg.add_separator()

        tag = dpg.add_input_text(
            multiline=True,
            readonly=True,
            width=-1,
            height=-1,
            tag=LOG_TAG,
        )
        return tag

    return None


def log_message(message: str) -> None:
    """Append a timestamped message to the log.

    Args:
        message: Message to log
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {message}"
    _log_buffer.append(line)

    # Keep buffer size reasonable
    if len(_log_buffer) > 500:
        _log_buffer.pop(0)

    if HAS_DPG and dpg.does_item_exist(LOG_TAG):
        dpg.set_value(LOG_TAG, "\n".join(_log_buffer))


def clear_log() -> None:
    """Clear the log buffer and display."""
    _log_buffer.clear()
    if HAS_DPG and dpg.does_item_exist(LOG_TAG):
        dpg.set_value(LOG_TAG, "")


def get_log_buffer() -> list[str]:
    """Get the current log buffer."""
    return _log_buffer.copy()
