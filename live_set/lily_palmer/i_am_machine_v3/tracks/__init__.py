"""Track implementations for I Am Machine V3.

This module exports all track classes used in the 16-bar intro loop.
"""

# Low-end tracks from subdirectory
# Remaining tracks in main directory
from .base_track import BaseTrack
from .low_end.kick_track import KickTrack as Track01Kick
from .low_end.rumble_track import RumbleTrack as Track02Rumble
from .track_03_sub_bass import Track03SubBass
from .track_04_acid import Track04Acid
from .track_05_closed_hat import Track05ClosedHat
from .track_06_open_hat import Track06OpenHat
from .track_07_clap import Track07Clap
from .track_08_tom import Track08Tom
from .track_09_glitch import Track09Glitch
from .track_10_ride import Track10Ride
from .track_11_stab import Track11Stab
from .track_12_drone import Track12Drone
from .track_13_vocal import Track13Vocal
from .track_14_vocal_fx import Track14VocalFx
from .track_15_riser import Track15Riser
from .track_16_impact import Track16Impact

__all__ = [
    "BaseTrack",
    "Track01Kick",
    "Track02Rumble",
    "Track03SubBass",
    "Track04Acid",
    "Track05ClosedHat",
    "Track06OpenHat",
    "Track07Clap",
    "Track08Tom",
    "Track09Glitch",
    "Track10Ride",
    "Track11Stab",
    "Track12Drone",
    "Track13Vocal",
    "Track14VocalFx",
    "Track15Riser",
    "Track16Impact",
]
