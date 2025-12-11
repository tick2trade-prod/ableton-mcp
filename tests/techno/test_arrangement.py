
import pytest
from tests.config import ABLETON_MAX_TRACKS
from tests.techno.patterns import (
    get_kick_pattern,
    get_bass_pattern,
    get_lead_pattern,
    get_hihat_pattern,
    get_stab_pattern,
    get_perc_pattern
)

class TestTechnoArrangement:
    """i_o style techno track generator."""

    TEMPO = 130.0
    CLIP_LENGTH = 16.0

    TRACKS = [
        {"name": "Kick Heavy", "type": "kick", "query": "query:Drums#Kit-Core 909"},
        {"name": "Sub Bass", "type": "bass", "query": "query:Sounds#Bass#Basic Sine"},
        {"name": "Acid Lead", "type": "acid", "query": "query:Sounds#Lead#Acid"},
        {"name": "Stab", "type": "stab", "query": "query:Sounds#Synth Keys#Stab"},
        {"name": "Hi-Hats", "type": "hats", "query": "query:Drums#Kit-Core 909"},
        {"name": "Perc", "type": "perc", "query": "query:Drums#Kit-Core 909"},
        {"name": "Rumble", "type": "rumble", "query": "query:Sounds#Bass#Sub"},
        {"name": "Master Chain", "type": "master", "query": "query:Audio Effects#Limiter"},
    ]

    @pytest.mark.live
    def test_generate_track(self, client, live_session, find_loadable):
        """Generate full track with instruments."""
        print(f"\\n🎵 Generating i_o Techno ({self.TEMPO} BPM)...")

        # 1. Setup Global
        client("stop_playback")
        client("set_tempo", {"tempo": self.TEMPO})

        # 2. Find Sounds
        drum_uri = find_loadable("Drums") or "query:Synths#Drum%20Rack"
        bass_uri = find_loadable("Sounds/Bass") or "query:Synths#Simpler"
        lead_uri = "query:Synths#Simpler"

        print(f"  Sounds: \\n    Drums: {drum_uri}\\n    Bass: {bass_uri}")

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

            # Load Instrument (Use defined query or fallback to generic search)
            uri = track.get("query")

            # Fallback logic if explicit query fails (simulated here by checking for URI)
            if not uri:
                if track["type"] in ["kick", "hats", "perc"]:
                    uri = drum_uri
                elif track["type"] == "bass":
                    uri = bass_uri
                elif track["type"] == "rumble":
                    uri = bass_uri  # Fallback to bass for rumble
                else:
                    uri = lead_uri

            print(f"    Loading: {uri}")
            res = client("load_browser_item", {"track_index": idx, "item_uri": uri})

            # Retry with fallback if failed
            if res["status"] != "success":
                print(f"    ⚠️ Failed to load {uri}, trying fallback...")
                if track["type"] in ["kick", "hats", "perc"]:
                    fallback_uri = drum_uri
                elif track["type"] == "bass":
                    fallback_uri = bass_uri
                elif track["type"] == "rumble":
                    fallback_uri = bass_uri
                else:
                    fallback_uri = lead_uri

                print(f"    Loading Fallback: {fallback_uri}")
                res = client("load_browser_item", {"track_index": idx, "item_uri": fallback_uri})

                if res["status"] != "success":
                     print(f"    ❌ Failed to load fallback {fallback_uri}")

            # Small delay to let device load (basic wait)
            import time
            time.sleep(0.5)

            # Create Clip & Notes
            client("create_clip", {"track_index": idx, "clip_index": 0, "length": self.CLIP_LENGTH})

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
                client("add_notes_to_clip", {"track_index": idx, "clip_index": 0, "notes": notes})
            elif track["type"] == "rumble":
                 # Rumble often mirrors the kick pattern
                 notes = get_kick_pattern(self.CLIP_LENGTH)
                 client("add_notes_to_clip", {"track_index": idx, "clip_index": 0, "notes": notes})
            elif track["type"] in ["fx", "master"]:
                 # Just effect loading, no notes needed
                 pass

        # 4. Play
        client("start_playback")
        assert len(track_indices) > 0
