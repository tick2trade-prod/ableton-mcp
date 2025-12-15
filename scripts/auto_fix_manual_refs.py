"""Auto-fix script: Add Ableton Manual references to all agent and test files.

Reads improvement plans and adds Manual references to module docstrings.
"""

import re
from pathlib import Path

# Manual reference mappings from improvement plans
AGENT_REFS = {
    "arrangement_agent.py": ("13.8", "Clip Launch Settings", 340),
    "arranger_agent.py": ("4.7", "Editing Breakpoint Envelopes", 122),
    "automation_agent.py": ("4.6", "Working with Automation", 116),
    "browser_agent.py": ("5", "Managing Files and Sets", 71),
    "composer_agent.py": ("13.1.4", "Groove Pool", 326),
    "effects_chain_agent.py": ("18.1", "Audio Effect Racks", 445),
    "groove_agent.py": ("13.1.4", "Groove Pool", 326),
    "mastering_agent.py": ("28.20", "Multiband Dynamics", 563),
    "mixer_agent.py": ("17.7", "Monitoring", 366),
    "modulation_agent.py": ("30.13.5", "Modulation Matrix", 748),
    "percussion_agent.py": ("30.5", "Drum Racks", 797),
    "research_agent.py": ("1", "General Documentation", 1),
    "return_track_agent.py": ("17.5", "Return Tracks", 357),
    "sampler_agent.py": ("30.10", "Sampler", 701),
    "sidechain_agent.py": ("28.14", "Sidechain Parameters", 535),
    "sound_design_agent.py": ("28.3", "Auto Filter", 511),
    "synthesizer_agent.py": ("30.13", "Wavetable", 742),
    "transition_agent.py": ("20.4.2", "Fade and Crossfade Editing", 396),
    "verifier_agent.py": ("28.51", "Spectrum", 620),
    "vocals_agent.py": ("28.13", "Corpus", 530),
}

TEST_REFS = {
    "test_arrangement_agent.py": ("13.8", "Clip Launch Settings", 340),
    "test_arranger_agent.py": ("4.7", "Editing Breakpoint Envelopes", 122),
    "test_automation_agent.py": ("4.6", "Working with Automation", 116),
    "test_browser_agent.py": ("5", "Managing Files and Sets", 71),
    "test_composer_agent.py": ("13.1.4", "Groove Pool", 326),
    "test_effects_chain_agent.py": ("18.1", "Audio Effect Racks", 445),
    "test_groove_agent.py": ("13.1.4", "Groove Pool", 326),
    "test_mastering_agent.py": ("28.20", "Multiband Dynamics", 563),
    "test_mixer_agent.py": ("17.7", "Monitoring", 366),
    "test_modulation_agent.py": ("30.13.5", "Modulation Matrix", 748),
    "test_percussion_agent.py": ("30.5", "Drum Racks", 797),
    "test_research_agent.py": ("1", "General Documentation", 1),
    "test_return_track_agent.py": ("17.5", "Return Tracks", 357),
    "test_sampler_agent.py": ("30.10", "Sampler", 701),
    "test_sidechain_agent.py": ("28.14", "Sidechain Parameters", 535),
    "test_sound_design_agent.py": ("28.3", "Auto Filter", 511),
    "test_synthesizer_agent.py": ("30.13", "Wavetable", 742),
    "test_transition_agent.py": ("20.4.2", "Fade and Crossfade Editing", 396),
    "test_verifier_agent.py": ("28.51", "Spectrum", 620),
    "test_vocals_agent.py": ("28.13", "Corpus", 530),
}


def add_manual_ref_to_file(filepath: Path, section: str, title: str, page: int) -> bool:
    """Add Manual reference to module docstring if not already present."""
    content = filepath.read_text()

    # Check if reference already exists
    if f"Reference: Ableton Manual Section {section}" in content:
        print(f"  ⏭️  {filepath.name} - already has reference")
        return False

    # Find module docstring
    match = re.search(r'(""".*?""")', content, re.DOTALL)
    if not match:
        print(f"  ❌ {filepath.name} - no module docstring found")
        return False

    old_docstring = match.group(1)

    # Create new docstring with reference
    lines = old_docstring.split("\n")
    if len(lines) < 2:
        print(f"  ❌ {filepath.name} - docstring too short")
        return False

    # Insert reference after first line
    new_lines = [lines[0], ""]
    new_lines.append(
        f'Reference: Ableton Manual Section {section} "{title}" (page {page})'
    )
    new_lines.append("")
    new_lines.extend(lines[1:])

    new_docstring = "\n".join(new_lines)
    new_content = content.replace(old_docstring, new_docstring, 1)

    filepath.write_text(new_content)
    print(f"  ✅ {filepath.name} - added reference")
    return True


def main():
    """Add Manual references to all agent and test files."""
    agent_dir = Path("scripts/dearpygui_controller/agents")
    test_dir = Path("tests/agents")

    print("Adding Manual References to Agent Files...")
    agent_count = 0
    for filename, (section, title, page) in AGENT_REFS.items():
        filepath = agent_dir / filename
        if filepath.exists():
            if add_manual_ref_to_file(filepath, section, title, page):
                agent_count += 1

    print("\n Adding Manual References to Test Files...")
    test_count = 0
    for filename, (section, title, page) in TEST_REFS.items():
        filepath = test_dir / filename
        if filepath.exists():
            if add_manual_ref_to_file(filepath, section, title, page):
                test_count += 1

    print(f"\n{'=' * 60}")
    print("Complete!")
    print(f"Agent files updated: {agent_count}/{len(AGENT_REFS)}")
    print(f"Test files updated: {test_count}/{len(TEST_REFS)}")
    print(f"Total: {agent_count + test_count}/40")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
