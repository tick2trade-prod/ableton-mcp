#!/usr/bin/env python3
"""
Ableton MCP Agent Controller GUI
A Dear PyGui interface for managing multi-agent workflows across Claude, Gemini, Ollama, and Codex.

Usage:
    uv python agent_gui.py
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

import dearpygui.dearpygui as dpg

# Configuration
CONTEXT_DIR = Path(".context")
OLLAMA_LOG = Path("../ollama_crewai_lab/ollama.log")

# Agent configurations
AGENTS = {
    "claude": {
        "command": "claude",
        "color": (100, 150, 255),
        "description": "Architect & Orchestrator - Best for system design and complex refactoring"
    },
    "gemini": {
        "command": "gemini",
        "color": (255, 100, 100),
        "description": "Researcher & Context Specialist - Best for exploration and multi-modal analysis"
    },
    "ollama": {
        "command": "ollama run",
        "color": (100, 255, 100),
        "description": "Local & Fast - Best for rapid iteration and privacy-sensitive code",
        "models": ["deepseek-coder-v2", "qwen2.5-coder", "codellama", "mixtral", "llama3.3"]
    },
    "codex": {
        "command": "codex",
        "color": (255, 255, 100),
        "description": "Code Generator - Best for boilerplate and test generation"
    }
}

# Context files
CONTEXT_FILES = [
    "current-session.md",
    "decisions.md",
    "research-notes.md",
    "todos.md"
]

# Global state
command_history = []
current_agent = "claude"
ollama_model = "deepseek-coder-v2"


def log_message(message, level="INFO"):
    """Add a timestamped message to the log."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"

    current_log = dpg.get_value("activity_log")
    dpg.set_value("activity_log", current_log + log_entry)

    # Auto-scroll to bottom
    dpg.set_y_scroll("activity_log", -1.0)


def run_agent_command(agent_name, prompt, model=None):
    """Executes an agent command via the shell."""
    log_message(f"Executing {agent_name} with prompt: {prompt[:50]}...")

    # Build command based on agent type
    if agent_name == "ollama" and model:
        command = f'ollama run {model} "{prompt}"'
    elif agent_name in AGENTS:
        command = f'{AGENTS[agent_name]["command"]} "{prompt}"'
    else:
        return f"Unknown agent: {agent_name}"

    try:
        # Use subprocess to run the command and capture output
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120  # 2 minute timeout
        )

        log_message(f"{agent_name} completed successfully", "SUCCESS")
        return result.stdout

    except subprocess.TimeoutExpired:
        error_msg = "Command timed out after 120 seconds"
        log_message(error_msg, "ERROR")
        return f"ERROR: {error_msg}"

    except subprocess.CalledProcessError as e:
        error_msg = f"Error running agent: {e.stderr}"
        log_message(error_msg, "ERROR")
        return f"ERROR: {error_msg}"

    except FileNotFoundError:
        error_msg = f"Agent command '{agent_name}' not found. Ensure your shell environment is correctly configured."
        log_message(error_msg, "ERROR")
        return f"ERROR: {error_msg}"


def read_context_file(filename):
    """Read a context file from the .context/ directory."""
    path = CONTEXT_DIR / filename
    try:
        with open(path) as f:
            content = f.read()
        log_message(f"Loaded context file: {filename}")
        return content
    except FileNotFoundError:
        error_msg = f"Context file not found at {path}"
        log_message(error_msg, "WARNING")
        return f"File not found: {path}\n\nPlease ensure the .context/ directory exists."
    except Exception as e:
        error_msg = f"Error reading {filename}: {str(e)}"
        log_message(error_msg, "ERROR")
        return f"ERROR: {error_msg}"


def update_context_file(filename, content):
    """Write updated content to a context file."""
    path = CONTEXT_DIR / filename
    try:
        # Ensure directory exists
        CONTEXT_DIR.mkdir(exist_ok=True)

        with open(path, 'w') as f:
            f.write(content)
        log_message(f"Updated context file: {filename}", "SUCCESS")
        return True
    except Exception as e:
        error_msg = f"Error writing {filename}: {str(e)}"
        log_message(error_msg, "ERROR")
        return False


def read_ollama_log():
    """Read the last 100 lines of ollama.log."""
    try:
        with open(OLLAMA_LOG) as f:
            lines = f.readlines()
            # Get last 100 lines
            return ''.join(lines[-100:])
    except FileNotFoundError:
        return f"Ollama log not found at {OLLAMA_LOG}"
    except Exception as e:
        return f"Error reading ollama log: {str(e)}"


def save_to_history(agent, prompt, response):
    """Save command to history."""
    history_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent,
        "prompt": prompt,
        "response": response[:200] + "..." if len(response) > 200 else response
    }
    command_history.append(history_entry)

    # Update history display
    update_history_display()


def update_history_display():
    """Update the command history display."""
    history_text = ""
    for i, entry in enumerate(reversed(command_history[-10:])):  # Show last 10
        history_text += f"[{entry['timestamp'][-8:]}] {entry['agent']}: {entry['prompt'][:40]}...\n"

    dpg.set_value("history_display", history_text)


# ========== GUI CALLBACKS ==========

def send_prompt_callback():
    """Handles the 'Send Prompt' button click."""
    agent_name = dpg.get_value("agent_selector")
    prompt_text = dpg.get_value("prompt_input")

    if not prompt_text.strip():
        dpg.set_value("output_log", "ERROR: Please enter a prompt.")
        log_message("Empty prompt submitted", "WARNING")
        return

    # Get ollama model if ollama is selected
    model = None
    if agent_name == "ollama":
        model = dpg.get_value("ollama_model_selector")

    # Clear output and show loading message
    dpg.set_value("output_log", f"Sending prompt to {agent_name}...\n")
    dpg.set_value("send_button", label="Processing...")
    dpg.configure_item("send_button", enabled=False)

    # Run the agent and update the output log
    output = run_agent_command(agent_name, prompt_text, model)
    dpg.set_value("output_log", output)

    # Save to history
    save_to_history(agent_name, prompt_text, output)

    # Re-enable button
    dpg.set_value("send_button", label="Send Prompt")
    dpg.configure_item("send_button", enabled=True)

    # Clear input for next command
    dpg.set_value("prompt_input", "")


def view_context_callback():
    """Updates the context viewer when a file is selected."""
    filename = dpg.get_value("context_selector")
    content = read_context_file(filename)
    dpg.set_value("context_viewer_text", content)


def save_context_callback():
    """Save edited context file."""
    filename = dpg.get_value("context_selector")
    content = dpg.get_value("context_viewer_text")

    if update_context_file(filename, content):
        dpg.set_value("context_status", f"Saved {filename}")
    else:
        dpg.set_value("context_status", f"Failed to save {filename}")


def view_ollama_log_callback():
    """Display ollama log in the output window."""
    log_content = read_ollama_log()
    dpg.set_value("output_log", log_content)
    log_message("Ollama log loaded")


def agent_changed_callback(sender, app_data):
    """Handle agent selection change."""
    global current_agent
    current_agent = app_data

    # Show/hide ollama model selector
    if app_data == "ollama":
        dpg.show_item("ollama_model_group")
    else:
        dpg.hide_item("ollama_model_group")

    # Update agent info
    agent_info = AGENTS[app_data]
    dpg.set_value("agent_info_text", agent_info["description"])
    log_message(f"Selected agent: {app_data}")


def clear_output_callback():
    """Clear the output log."""
    dpg.set_value("output_log", "")
    log_message("Output cleared")


def export_session_callback():
    """Export current session to a file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"session_{timestamp}.json"

    session_data = {
        "timestamp": datetime.now().isoformat(),
        "agent": current_agent,
        "history": command_history,
        "context_files": {
            f: read_context_file(f) for f in CONTEXT_FILES
        }
    }

    try:
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        log_message(f"Session exported to {filename}", "SUCCESS")
        dpg.set_value("output_log", f"Session exported to {filename}")
    except Exception as e:
        log_message(f"Failed to export session: {e}", "ERROR")


# ========== GUI LAYOUT ==========

def create_gui():
    """Create the main GUI layout."""
    dpg.create_context()

    # Set theme
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (20, 20, 30))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (40, 40, 50))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 80, 120))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 90, 140))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (50, 70, 110))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 10, 10)

    dpg.bind_theme(global_theme)

    # Main window
    with dpg.window(label="Ableton MCP Agent Controller", tag="primary_window", width=1200, height=800):

        # Header
        dpg.add_text("Multi-Agent Control Panel", color=(100, 200, 255))
        dpg.add_text("Workspace: ableton-mcp | Guide: WS-guide.md", color=(150, 150, 150))
        dpg.add_separator()
        dpg.add_spacer(height=5)

        # Left panel (Agent control)
        with dpg.group(horizontal=True):
            # Left column - Agent controls
            with dpg.child_window(width=700, height=700):
                dpg.add_text("Agent Selection", color=(100, 200, 255))
                dpg.add_spacer(height=5)

                # Agent selector
                with dpg.group(horizontal=True):
                    dpg.add_combo(
                        label="Agent",
                        items=list(AGENTS.keys()),
                        default_value="claude",
                        tag="agent_selector",
                        callback=agent_changed_callback,
                        width=150
                    )

                    # Ollama model selector (hidden by default)
                    with dpg.group(horizontal=True, tag="ollama_model_group", show=False):
                        dpg.add_text("Model:")
                        dpg.add_combo(
                            items=AGENTS["ollama"]["models"],
                            default_value="deepseek-coder-v2",
                            tag="ollama_model_selector",
                            width=200
                        )

                dpg.add_text("", tag="agent_info_text", wrap=650, color=(200, 200, 100))
                dpg.set_value("agent_info_text", AGENTS["claude"]["description"])

                dpg.add_spacer(height=10)
                dpg.add_separator()
                dpg.add_spacer(height=10)

                # Prompt input
                dpg.add_text("Prompt / Task", color=(100, 200, 255))
                dpg.add_input_text(
                    hint="Enter your task or question...",
                    multiline=True,
                    width=-1,
                    height=100,
                    tag="prompt_input"
                )

                # Action buttons
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Send Prompt",
                        callback=send_prompt_callback,
                        tag="send_button",
                        width=150
                    )
                    dpg.add_button(
                        label="Clear Output",
                        callback=clear_output_callback,
                        width=120
                    )
                    dpg.add_button(
                        label="View Ollama Log",
                        callback=view_ollama_log_callback,
                        width=150
                    )
                    dpg.add_button(
                        label="Export Session",
                        callback=export_session_callback,
                        width=120
                    )

                dpg.add_spacer(height=10)
                dpg.add_separator()
                dpg.add_spacer(height=10)

                # Output log
                dpg.add_text("Agent Output", color=(100, 200, 255))
                dpg.add_input_text(
                    multiline=True,
                    width=-1,
                    height=380,
                    tag="output_log",
                    default_value="Agent responses will appear here...\n\nTips:\n- Select an agent from the dropdown\n- Enter your prompt in the text box above\n- Click 'Send Prompt' to execute\n- View context files in the right panel",
                    readonly=True
                )

            # Right column - Context & Activity
            with dpg.child_window(width=470, height=700):
                # Context viewer
                dpg.add_text("Context Files", color=(100, 200, 255))
                dpg.add_spacer(height=5)

                with dpg.group(horizontal=True):
                    dpg.add_combo(
                        label="File",
                        items=CONTEXT_FILES,
                        default_value="current-session.md",
                        tag="context_selector",
                        callback=view_context_callback,
                        width=200
                    )
                    dpg.add_button(
                        label="Refresh",
                        callback=view_context_callback,
                        width=80
                    )
                    dpg.add_button(
                        label="Save",
                        callback=save_context_callback,
                        width=80
                    )

                dpg.add_text("", tag="context_status", color=(100, 255, 100))

                dpg.add_input_text(
                    multiline=True,
                    width=-1,
                    height=250,
                    tag="context_viewer_text",
                    readonly=False  # Allow editing
                )

                dpg.add_spacer(height=10)
                dpg.add_separator()
                dpg.add_spacer(height=10)

                # Command history
                dpg.add_text("Command History", color=(100, 200, 255))
                dpg.add_input_text(
                    multiline=True,
                    width=-1,
                    height=120,
                    tag="history_display",
                    readonly=True,
                    default_value="Command history will appear here..."
                )

                dpg.add_spacer(height=10)
                dpg.add_separator()
                dpg.add_spacer(height=10)

                # Activity log
                dpg.add_text("Activity Log", color=(100, 200, 255))
                dpg.add_input_text(
                    multiline=True,
                    width=-1,
                    height=150,
                    tag="activity_log",
                    readonly=True,
                    default_value=""
                )

        # Initialize context view
        dpg.set_value("context_viewer_text", read_context_file("current-session.md"))

    # Initial log message
    log_message("Agent Controller initialized")
    log_message(f"Context directory: {CONTEXT_DIR.absolute()}")
    log_message(f"Ollama log: {OLLAMA_LOG.absolute()}")

    # Set primary window
    dpg.set_primary_window("primary_window", True)


def main():
    """Main entry point."""
    create_gui()

    # Setup and run Dear PyGui
    dpg.create_viewport(title='Ableton MCP Agent Controller', width=1200, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
