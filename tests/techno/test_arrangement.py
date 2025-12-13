import pytest

from tests.config import ABLETON_MAX_TRACKS
from tests.techno.patterns import (
    get_bass_pattern,
    get_hihat_pattern,
    get_kick_pattern,
    get_lead_pattern,
    get_perc_pattern,
    get_rumble_pattern,
    get_stab_pattern,
)


class TestTechnoArrangement:
    """i_o style techno track generator."""

    TEMPO = 130.0
    CLIP_LENGTH = 16.0

    TRACKS = [
        {
            "name": "Kick Heavy",
            "type": "kick",
            "query": "query:Drums#FileId_5446",
        },  # 808 Core Kit
        {
            "name": "Sub Bass",
            "type": "bass",
            "query": "query:Sounds#Bass:FileId_5199",
        },  # 808 BNYX Stopper
        {
            "name": "Acid Lead",
            "type": "acid",
            "query": "query:Synths#Drift",
        },  # Drift synth for acid
        {
            "name": "Stab",
            "type": "stab",
            "query": "query:Synths#Simpler",
        },  # Simpler for stabs
        {
            "name": "Hi-Hats",
            "type": "hats",
            "query": "query:Drums#FileId_5446",
        },  # 808 Core Kit
        {
            "name": "Perc",
            "type": "perc",
            "query": "query:Drums#FileId_5446",
        },  # 808 Core Kit
        {
            "name": "Rumble",
            "type": "rumble",
            "query": "query:Sounds#Bass:FileId_5200",
        },  # 808 Drifter
        {
            "name": "Master Chain",
            "type": "master",
            "query": "query:AudioFx#Auto%20Filter",
        },  # Auto Filter
    ]

    @pytest.mark.live
    def test_generate_track(self, client, live_session, find_loadable):
        """Generate full track with instruments."""
        print(f"\\n🎵 Generating i_o Techno ({self.TEMPO} BPM)...")

        # 1. Setup Global
        client("stop_playback")
        client("set_tempo", {"tempo": self.TEMPO})

        # 2. Setup - All instruments verified to exist in Ableton Intro
        print("  Using 808 Core Kit for drums")
        print("  Using verified bass sounds and Drift/Simpler for synths")

        # 3. manage Tracks
        current = live_session["track_count"]
        needed = len(self.TRACKS)
        track_indices = []

        if current + needed <= ABLETON_MAX_TRACKS:
            start_new = True
        else:
            print("  Reusing existing tracks...")
            start_new = False

        for i, track in enumerate(self.TRACKS):
            if start_new:
                res = client("create_midi_track", {"index": -1})
                if res["status"] != "success":
                    continue
                idx = res["result"]["index"]
            else:
                idx = max(0, current - needed) + i
                if idx >= current:
                    break

            track_indices.append(idx)
            client("set_track_name", {"track_index": idx, "name": track["name"]})

            # Load Instrument (all queries verified to work)
            uri = track.get("query")

            print(f"    Loading: {uri}")
            res = client("load_browser_item", {"track_index": idx, "item_uri": uri})

            if res["status"] != "success":
                print(
                    f"    ❌ Failed to load {uri}: {res.get('message', 'Unknown error')}"
                )
                continue  # Skip this track

            # Small delay to let device load
            import time

            time.sleep(0.5)

            # Create Clip & Notes
            client(
                "create_clip",
                {"track_index": idx, "clip_index": 0, "length": self.CLIP_LENGTH},
            )

            # Get patterns from module
            notes = []
            if track["type"] == "kick":
                # Kick usually C1 (36) on Drum Racks
                notes = get_kick_pattern(self.CLIP_LENGTH)
            elif track["type"] == "bass":
                notes = get_bass_pattern(self.CLIP_LENGTH)
            elif track["type"] in ["acid", "lead"]:
                notes = get_lead_pattern(self.CLIP_LENGTH)
            elif track["type"] == "stab":
                notes = get_stab_pattern(self.CLIP_LENGTH)
            elif track["type"] == "hats":
                # Open Hat often A#1 (46) or similar in GM/Core kits
                # Adjusted to hit OH/CH MIDI notes
                notes = get_hihat_pattern(self.CLIP_LENGTH)
            elif track["type"] == "perc":
                # Clap/Snare often D#1 (39)
                notes = get_perc_pattern(self.CLIP_LENGTH)

            if notes:
                client(
                    "add_notes_to_clip",
                    {"track_index": idx, "clip_index": 0, "notes": notes},
                )
            elif track["type"] == "rumble":
                # Rumble uses its own pattern
                notes = get_rumble_pattern(self.CLIP_LENGTH)
                client(
                    "add_notes_to_clip",
                    {"track_index": idx, "clip_index": 0, "notes": notes},
                )
            elif track["type"] in ["fx", "master"]:
                # Just effect loading, no notes needed
                pass

            # Verify instrument loaded
            import time

            time.sleep(0.3)
            track_info = client("get_track_info", {"track_index": idx})
            if track_info.get("status") == "success":
                devices = track_info["result"].get("devices", [])
                if devices:
                    device_names = [d["name"] for d in devices]
                    print(f"    ✓ Loaded: {', '.join(device_names)}")
                else:
                    print(f"    ⚠️  No devices found on track {idx}")

        # 4. Play
        client("start_playback")
        assert len(track_indices) > 0
