# Run Priority: Kick + Rumble

Execute the priority tracks for Intro section recreation.

## Priority Tracks

1. **Track 01: Kick** - Foundation of the groove
2. **Track 07: Rumble** - Sub bass with sidechain pumping

These two tracks form the core groove of "I Am Machine" and should be created first.

## Quick Execution

### Option 1: Run Existing Scripts

```bash
# From project root
cd /Users/alexzh/ableton-mcp

# Run drums script (creates Kick + 5 other drum tracks)
python scripts/workflows/create_intro_drums.py

# Run bass script (creates Rumble + 2 other bass tracks)
python scripts/workflows/create_intro_bass.py
```

### Option 2: Kick Only (Minimal Test)

```python
# Direct MCP calls for kick only
import socket
import json

def send_command(cmd_type, params=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 9877))
    command = {"type": cmd_type, "params": params or {}}
    sock.sendall(json.dumps(command).encode())
    sock.settimeout(10)
    response = sock.recv(8192)
    sock.close()
    return json.loads(response)

# Create kick track
send_command("create_midi_track", {"index": 0})
send_command("set_track_name", {"track_index": 0, "name": "Kick"})
send_command("load_browser_item", {
    "track_index": 0,
    "item_uri": "query:Drums#FileId_14946"  # 909 Core Kit
})
```

## Validation Checklist

### After Kick Creation
- [ ] Port 9877 responding (`just check-port`)
- [ ] Track "Kick" visible in Ableton
- [ ] 909 Core Kit loaded
- [ ] 16-bar clip with 4-on-floor pattern
- [ ] Punchy, saturated kick sound

### After Rumble Creation
- [ ] Track "Rumble" visible at index 6
- [ ] Operator synth loaded
- [ ] Compressor with sidechain from Kick
- [ ] Pumping effect audible
- [ ] Sub doesn't clash with kick

## Reference Comparison

**File**: `/Users/alexzh/ableton-mcp/assets/audio/reference/I_AM_MACHINE_LILLY_PALMER.mp3`

1. Play the reference (first 16 bars = ~28 seconds at 136 BPM)
2. Solo your Kick + Rumble tracks
3. Compare:
   - [ ] Kick punch matches
   - [ ] Sub weight matches
   - [ ] Pump rhythm matches
   - [ ] Overall groove feel

## Troubleshooting

### No Sound from Drums
```bash
# Check if 909 kit is loaded properly
python -c "
import socket, json
s = socket.socket()
s.connect(('localhost', 9877))
s.sendall(json.dumps({'type': 'get_track_info', 'params': {'track_index': 0}}).encode())
print(s.recv(8192).decode())
"
```

### No Sidechain Pump
- Verify compressor is on Rumble track
- Check sidechain input is set to Track 0
- Lower threshold to -30dB

## Log Files

- `scripts/workflows/intro_drums.log`
- `scripts/workflows/intro_bass.log`

## Next Steps

After validating Kick + Rumble:
1. Complete remaining drum tracks (Snare, Hi-hats, Toms, Glitch, Ride)
2. Complete remaining bass tracks (Rolling Bass, Acid)
3. Move to Synths lane
4. Move to Vocals/FX lane

## Related Commands

- `/track-01-kick` - Detailed kick track guide
- `/track-07-rumble` - Detailed rumble track guide
- `/project-status` - Overall project progress
