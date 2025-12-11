"""Audio track analysis using librosa.

Extract musical features for techno reproduction including
tempo, key, and beat mapping.
"""

import json
import os
from pathlib import Path
from typing import Optional

import librosa
import numpy as np


def analyze_track(file_path: str, duration: float = 10.0) -> dict:
    """Analyze an audio file to extract musical features.

    Args:
        file_path: Path to audio file (.wav, .mp3, etc)
        duration: Duration in seconds to analyze (default: 10s)

    Returns:
        dict with analysis results including tempo, key, duration
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    try:
        y, sr = librosa.load(file_path, sr=22050, duration=duration)
    except Exception as e:
        return {"error": f"Error loading audio: {e}"}

    full_duration = librosa.get_duration(path=file_path)

    # Tempo & Beats
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    tempo_val = float(tempo[0]) if hasattr(tempo, "__iter__") else float(tempo)

    # Key Detection
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    key_idx = int(np.mean(chroma, axis=1).argmax())
    keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    # Spectral features
    spectral_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
    spectral_bandwidth = float(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)))

    return {
        "file": os.path.basename(file_path),
        "path": file_path,
        "duration": full_duration,
        "analyzed_duration": min(duration, full_duration),
        "sample_rate": sr,
        "tempo": tempo_val,
        "key": keys[key_idx],
        "key_index": key_idx,
        "spectral_centroid": spectral_centroid,
        "spectral_bandwidth": spectral_bandwidth,
        "beat_frames": beat_frames.tolist(),
        "waveform": y.tolist(),
        "chroma": chroma.mean(axis=1).tolist(),
    }


def get_analysis_result(file_path: str, cache_dir: Optional[str] = None) -> dict:
    """Get analysis result, using cache if available.

    Args:
        file_path: Path to audio file
        cache_dir: Optional cache directory (defaults to assets/analysis/)

    Returns:
        dict with analysis results
    """
    if cache_dir is None:
        cache_dir = (
            Path(__file__).parent.parent.parent.parent.parent / "assets/analysis"
        )
    else:
        cache_dir = Path(cache_dir)

    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{Path(file_path).stem}_analysis.json"

    if cache_file.exists():
        with open(cache_file) as f:
            return json.load(f)

    result = analyze_track(file_path)

    if "error" not in result:
        # Remove large arrays before caching
        cache_result = {k: v for k, v in result.items() if k not in ["waveform"]}
        with open(cache_file, "w") as f:
            json.dump(cache_result, f, indent=2)

    return result


def print_analysis(file_path: str) -> None:
    """Print analysis results to console."""
    result = analyze_track(file_path)

    if "error" in result:
        print(f"❌ {result['error']}")
        return

    print(f"\n🔍 Analyzing: {result['file']}...")
    print(f"  Duration: {result['duration']:.2f}s")
    print(f"  BPM: {result['tempo']:.2f}")
    print(f"  Estimated Key: {result['key']}")
    print("\n✅ Analysis Complete.")
    print("------------------------------------------------")
    print("To recreate in Ableton:")
    print(f"1. Set Global Tempo to {result['tempo']:.2f}")
    print(f"2. Root Note: {result['key']}")
    print("------------------------------------------------")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m src.ableton_mcp.analysis.track <path_to_audio_file>")
    else:
        print_analysis(sys.argv[1])
