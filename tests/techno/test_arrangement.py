
import pytest
from tests.config import ABLETON_MAX_TRACKS

class TestTechnoArrangement:
    """i_o style techno track generator."""
    
    TEMPO = 130.0
    CLIP_LENGTH = 16.0
    
    TRACKS = [
        {"name": "Kick Heavy", "type": "kick"},
        {"name": "Sub Bass", "type": "bass"},
        {"name": "Acid Lead", "type": "acid"},
        {"name": "Stab", "type": "stab"},
        {"name": "Hi-Hats", "type": "hats"},
        {"name": "Perc", "type": "perc"},
    ]
    
    @pytest.mark.live
    def test_generate_track(self, client, live_session, find_loadable):
        """Generate full track with instruments."""
        print(f"\n🎵 Generating i_o Techno ({self.TEMPO} BPM)...")
        
        # 1. Setup Global
        client("stop_playback")
        client("set_tempo", {"tempo": self.TEMPO})
        
        # 2. Find Sounds
        drum_uri = find_loadable("Drums") or "query:Synths#Drum%20Rack"
        bass_uri = find_loadable("Sounds/Bass") or "query:Synths#Simpler"
        lead_uri = "query:Synths#Simpler"
        
        print(f"  Sounds: \n    Drums: {drum_uri}\n    Bass: {bass_uri}")
        
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
                if res["status"] != "success": continue
                idx = res["result"]["index"]
            else:
                idx = max(0, current - needed) + i
                if idx >= current: break
            
            track_indices.append(idx)
            client("set_track_name", {"track_index": idx, "name": track["name"]})
            
            # Load Instrument
            uri = drum_uri if track["type"] in ["kick", "hats", "perc"] else (bass_uri if track["type"] == "bass" else lead_uri)
            client("load_browser_item", {"track_index": idx, "item_uri": uri})
            
            # Create Clip & Notes
            client("create_clip", {"track_index": idx, "clip_index": 0, "length": self.CLIP_LENGTH})
            notes = self._get_notes(track["type"])
            if notes:
                client("add_notes_to_clip", {"track_index": idx, "clip_index": 0, "notes": notes})
                
        # 4. Play
        client("start_playback")
        assert len(track_indices) > 0

    def _get_notes(self, type_enc):
        """Generate notes based on type."""
        notes = []
        if type_enc == "kick":
            for i in range(16):
                notes.append({"pitch": 36, "start_time": i, "duration": 0.5, "velocity": 127 if i%4==0 else 110, "mute": False})
        elif type_enc == "bass":
             # Offbeat bass (simplified)
            for i in range(16):
                notes.append({"pitch": 28, "start_time": i+0.5, "duration": 0.5, "velocity": 120, "mute": False})
        elif type_enc == "hats":
            for i in range(16):
                notes.append({"pitch": 42, "start_time": i+0.5, "duration": 0.25, "velocity": 90, "mute": False})
        return notes
