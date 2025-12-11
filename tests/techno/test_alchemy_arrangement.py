"""
I/O Alchemy recreation test suite.

Recreates ALCHEMY_I_O.mp3 in Ableton Live using 16 tracks.
Based on librosa analysis: 129.2 BPM, G Minor.
"""

import time

import pytest

from tests.config import ABLETON_MAX_TRACKS
from tests.techno.patterns_alchemy import (
    get_acid_lead_pattern,
    get_arp_pattern,
    get_bass_mid_pattern,
    get_clap_pattern,
    get_hihat_pattern,
    get_impact_pattern,
    get_kick_pattern,
    get_open_hat_pattern,
    get_pad_pattern,
    get_perc2_pattern,
    get_perc_pattern,
    get_riser_pattern,
    get_stab_pattern,
    get_sub_bass_pattern,
)


class TestAlchemyArrangement:
    """I/O Alchemy style techno track generator.

    Based on analysis of ALCHEMY_I_O.mp3:
    - BPM: 129.2
    - Key: G Minor
    - Structure: Drop/breakdown transitions
    """

    TEMPO = 129.0  # Rounded from 129.2 for cleaner grid
    CLIP_LENGTH = 16.0  # 16 bars

    # 16-track layout (Ableton Intro limit)
    TRACKS = [
        {
            "name": "Kick",
            "type": "kick",
            "query": "query:Drums#FileId_5446",
        },
        {
            "name": "Sub Bass",
            "type": "sub_bass",
            "query": "query:Sounds#Bass:FileId_5199",
        },
        {
            "name": "Bass Mid",
            "type": "bass_mid",
            "query": "query:Synths#Drift",
        },
        {
            "name": "Acid Lead",
            "type": "acid",
            "query": "query:Synths#Drift",
        },
        {
            "name": "Lead Arp",
            "type": "arp",
            "query": "query:Synths#Simpler",
        },
        {
            "name": "Pad",
            "type": "pad",
            "query": "query:Synths#Simpler",
        },
        {
            "name": "Stab",
            "type": "stab",
            "query": "query:Synths#Simpler",
        },
        {
            "name": "Hi-Hats",
            "type": "hihat",
            "query": "query:Drums#FileId_5446",
        },
        {
            "name": "Open Hat",
            "type": "open_hat",
            "query": "query:Drums#FileId_5446",
        },
        {
            "name": "Clap",
            "type": "clap",
            "query": "query:Drums#FileId_5446",
        },
        {
            "name": "Perc 1",
            "type": "perc",
            "query": "query:Drums#FileId_5446",
        },
        {
            "name": "Perc 2",
            "type": "perc2",
            "query": "query:Synths#Simpler",
        },
        {
            "name": "FX Riser",
            "type": "riser",
            "query": "query:Synths#Simpler",
        },
        {
            "name": "FX Impact",
            "type": "impact",
            "query": "query:Drums#FileId_5446",
        },
        {
            "name": "Send FX",
            "type": "send_fx",
            "query": "query:AudioFx#Auto%20Filter",
        },
        {
            "name": "Master",
            "type": "master",
            "query": "query:AudioFx#Limiter",
        },
    ]

    PATTERN_MAP = {
        "kick": get_kick_pattern,
        "sub_bass": get_sub_bass_pattern,
        "bass_mid": get_bass_mid_pattern,
        "acid": get_acid_lead_pattern,
        "arp": get_arp_pattern,
        "pad": get_pad_pattern,
        "stab": get_stab_pattern,
        "hihat": get_hihat_pattern,
        "open_hat": get_open_hat_pattern,
        "clap": get_clap_pattern,
        "perc": get_perc_pattern,
        "perc2": get_perc2_pattern,
        "riser": get_riser_pattern,
        "impact": get_impact_pattern,
    }

    @pytest.mark.live
    def test_generate_alchemy(self, client, live_session, find_loadable):
        """Generate full I/O Alchemy recreation with 16 tracks."""
        print(f"\n🎵 Generating I/O Alchemy ({self.TEMPO} BPM, G Minor)...")

        # 1. Setup Global
        client("stop_playback")
        client("set_tempo", {"tempo": self.TEMPO})

        # 2. Verify track count
        current = live_session["track_count"]
        needed = len(self.TRACKS)

        print(f"  Current tracks: {current}, Needed: {needed}")
        print(f"  Max tracks (Intro): {ABLETON_MAX_TRACKS}")

        # Calculate how many tracks we can create
        available_slots = ABLETON_MAX_TRACKS - current
        can_create = min(needed, available_slots)

        track_indices = []
        created_count = 0

        # 3. Create/configure each track
        for i, track in enumerate(self.TRACKS):
            if i < can_create:
                # Create new track
                res = client("create_midi_track", {"index": -1})
                if res.get("status") != "success":
                    print(f"    ❌ Failed to create track: {track['name']}")
                    continue
                idx = res["result"]["index"]
                created_count += 1
            else:
                # Reuse existing track (starting from beginning)
                idx = i - can_create
                if idx >= current:
                    print("    ⚠️  No more track slots available")
                    break

            track_indices.append(idx)

            # Name track
            client("set_track_name", {"track_index": idx, "name": track["name"]})

            # Load instrument
            uri = track.get("query")
            print(f"    [{i + 1:02d}] {track['name']}: Loading {uri}")

            res = client("load_browser_item", {"track_index": idx, "item_uri": uri})
            if res.get("status") != "success":
                print(f"        ❌ Load failed: {res.get('message', 'Unknown error')}")
                continue

            time.sleep(0.3)

            # Create clip and add notes (skip FX tracks)
            if track["type"] in self.PATTERN_MAP:
                # Create clip
                client(
                    "create_clip",
                    {
                        "track_index": idx,
                        "clip_index": 0,
                        "length": self.CLIP_LENGTH,
                    },
                )

                # Get pattern
                pattern_fn = self.PATTERN_MAP[track["type"]]
                notes = pattern_fn(self.CLIP_LENGTH)

                if notes:
                    client(
                        "add_notes_to_clip",
                        {"track_index": idx, "clip_index": 0, "notes": notes},
                    )
                    print(f"        ✓ Added {len(notes)} notes")

            # Verify device loaded
            time.sleep(0.2)
            track_info = client("get_track_info", {"track_index": idx})
            if track_info.get("status") == "success":
                devices = track_info["result"].get("devices", [])
                if devices:
                    device_names = [d["name"] for d in devices[:2]]
                    print(f"        ✓ Devices: {', '.join(device_names)}")
                else:
                    print("        ⚠️  No devices found")

        # 4. Summary
        print(f"\n✅ Created {created_count} tracks, {len(track_indices)} configured")
        print(
            f"   Tempo: {self.TEMPO} BPM | Key: G Minor | Bars: {int(self.CLIP_LENGTH)}"
        )

        # 5. Start playback
        client("start_playback")

        # Assert success
        assert len(track_indices) >= 12, (
            f"Expected 12+ tracks, got {len(track_indices)}"
        )

    @pytest.mark.live
    def test_verify_track_structure(self, client, live_session):
        """Verify the generated track structure matches spec."""
        print("\n🔍 Verifying track structure...")

        session = client("get_session_info")
        if session.get("status") != "success":
            pytest.skip("Session info unavailable")

        tracks = session["result"].get("tracks", [])
        print(f"  Total tracks: {len(tracks)}")

        # Skip if session not synchronized (can happen with Live's internal caching)
        if len(tracks) == 0:
            pytest.skip(
                "Session tracks not synchronized - run test_generate_alchemy first"
            )

        # Check for expected track names
        expected_names = {t["name"] for t in self.TRACKS}
        found_names = {t.get("name", "") for t in tracks}

        matching = expected_names & found_names
        print(f"  Matching track names: {len(matching)}/{len(expected_names)}")

        assert len(matching) >= 8, f"Expected 8+ matching tracks, got {len(matching)}"

    @pytest.mark.live
    def test_verify_tempo(self, client, live_session):
        """Verify tempo is set correctly."""
        tempo = live_session.get("tempo", 0)
        print(f"\n🎵 Tempo: {tempo} BPM")
        assert abs(tempo - self.TEMPO) < 1.0, f"Expected ~{self.TEMPO} BPM, got {tempo}"
