# tools/separator.py
import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TechnoSeparator")


@mcp.tool()
def separate_stems(mp3_path: str, output_dir: str = "./stems"):
    """
    Uses Demucs to split a song into 4 stems (Drums, Bass, Vocal, Other).
    """
    # This runs the standard demucs command line tool
    # pip install demucs
    command = [
        "demucs",
        "--two-stems=drums",  # Optional: Focus only on drums if you want
        "-o",
        output_dir,
        mp3_path,
    ]
    subprocess.run(command, check=True)
    return f"Separated {mp3_path}. Check {output_dir} for the 4 wav files."
