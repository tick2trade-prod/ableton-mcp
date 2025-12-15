"""Agent panel layout for DearPyGUI controller."""

try:
    import dearpygui.dearpygui as dpg

    HAS_DPG = True
except ImportError:
    HAS_DPG = False
    dpg = None


AGENTS = [
    ("research", "Research Agent", "Searches docs and web"),
    ("arranger", "Arranger Agent", "Structures timeline"),
    ("composer", "Composer Agent", "Creates MIDI patterns"),
    ("sound_design", "Sound Design Agent", "Sculpts parameters"),
    ("mixer", "Mixer Agent", "Applies effects chains"),
    ("verifier", "Verifier Agent", "Validates completion"),
]


def create_agent_panel(parent: int | str) -> dict[str, int]:
    """Create agent control panel with checkboxes.

    Args:
        parent: Parent window/group ID

    Returns:
        Dict mapping agent_name to checkbox tag
    """
    if not HAS_DPG:
        return {}

    checkboxes = {}

    with dpg.child_window(label="Agents", parent=parent, width=200, height=150):
        dpg.add_text("Agent Selection")
        dpg.add_separator()

        for agent_id, name, tooltip in AGENTS:
            tag = dpg.add_checkbox(
                label=name,
                default_value=True,
                tag=f"agent_{agent_id}",
            )
            if dpg.does_item_exist(tag):
                dpg.bind_item_handler_registry(tag, "tooltip_handler")
            checkboxes[agent_id] = tag

    return checkboxes


def get_enabled_agents() -> list[str]:
    """Get list of enabled agent IDs."""
    if not HAS_DPG:
        return ["research", "composer", "mixer", "verifier"]

    enabled = []
    for agent_id, _, _ in AGENTS:
        tag = f"agent_{agent_id}"
        if dpg.does_item_exist(tag) and dpg.get_value(tag):
            enabled.append(agent_id)
    return enabled
