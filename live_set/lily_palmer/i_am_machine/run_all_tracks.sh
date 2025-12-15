#!/bin/bash
# Run all track scripts incrementally with verification
#
# This script creates all 16 tracks for "I Am Machine" recreation:
# - Rhythm section: Kick, Rumble, Bass, Acid
# - Hi-hats: Closed, Open
# - Percussion: Clap, Tom, Glitch, Ride
# - Synths: Stab, Drone
# - Vocals: Main, FX
# - Transitions: Riser, Impact
#
# Usage: ./run_all_tracks.sh
# Prerequisites:
#   - Ableton Live running with AbletonMCP control surface
#   - Port 9877 accessible

set -e  # Exit on first error

cd "$(dirname "$0")"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     I Am Machine - 16 Track Techno Setup                 ║"
echo "║     Using optimized scripts with AbletonMCPClient        ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Test connection first
echo "Testing Ableton connection..."
python3 -c "from ableton_client import AbletonMCPClient; c = AbletonMCPClient(); r = c.get_session_info(); print(f'Connected: {r.data.get(\"tempo\")} BPM') if r.success else exit(1)" || {
    echo "ERROR: Cannot connect to Ableton. Ensure:"
    echo "  1. Ableton Live is running"
    echo "  2. AbletonMCP control surface is enabled"
    echo "  3. Port 9877 is accessible"
    exit 1
}
echo ""

DELAY=1.5  # Delay between tracks

for i in $(seq -w 01 16); do
    script=$(ls track_${i}_*.py 2>/dev/null | head -1)
    if [ -f "$script" ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Running $script..."
        echo ""

        uv run python "$script"

        if [ $? -ne 0 ]; then
            echo ""
            echo "!!! FAILED on $script !!!"
            echo "Check the error above and fix before continuing."
            exit 1
        fi

        echo ""
        sleep $DELAY
    fi
done

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  ✓ All 16 tracks created successfully!                   ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  Next steps:                                             ║"
echo "║  1. Load samples into Drum Samplers                      ║"
echo "║  2. Configure audio routing for Rumble/Vocal FX          ║"
echo "║  3. Set up sidechain compression from Kick               ║"
echo "║  4. Automate filter sweeps on Acid, Riser                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
