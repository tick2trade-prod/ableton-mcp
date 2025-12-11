import argparse
import json
import os

import librosa
import numpy as np


def detect_key_and_mode(y, sr):
    """
    Detect musical key and mode (major/minor) using chroma features.

    Returns:
        tuple: (key_name, mode) where mode is 'Major' or 'Minor'
    """
    # Separate harmonic and percussive components
    y_harmonic = librosa.effects.harmonic(y)

    # Compute chroma features from harmonic component
    chroma = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)

    # Average chroma across time
    chroma_mean = np.mean(chroma, axis=1)

    # Detect root note
    key_idx = chroma_mean.argmax()
    keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    key_name = keys[key_idx]

    # Simple major/minor detection based on chroma profile
    # Major has strong 3rd and 5th, minor has flat 3rd
    major_profile = np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0])
    minor_profile = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0])

    # Rotate profiles to match detected key
    major_rotated = np.roll(major_profile, key_idx)
    minor_rotated = np.roll(minor_profile, key_idx)

    # Normalize chroma
    chroma_norm = chroma_mean / (np.sum(chroma_mean) + 1e-8)

    # Calculate correlation
    major_corr = np.corrcoef(chroma_norm, major_rotated)[0, 1]
    minor_corr = np.corrcoef(chroma_norm, minor_rotated)[0, 1]

    mode = "Major" if major_corr > minor_corr else "Minor"

    return key_name, mode


def detect_sections(y, sr):
    """
    Detect musical sections using RMS energy analysis.

    Returns:
        dict: Section markers with timestamps
    """
    # Compute RMS energy
    rms = librosa.feature.rms(y=y)[0]

    # Normalize
    rms_norm = (rms - np.min(rms)) / (np.max(rms) - np.min(rms) + 1e-8)

    # Simple threshold-based detection
    high_energy_threshold = 0.7
    low_energy_threshold = 0.3

    # Find transitions
    sections = []
    current_section = None

    for i, energy in enumerate(rms_norm):
        time = librosa.frames_to_time(i, sr=sr)

        if energy > high_energy_threshold and current_section != "drop":
            sections.append({"type": "drop", "time": time})
            current_section = "drop"
        elif energy < low_energy_threshold and current_section != "breakdown":
            sections.append({"type": "breakdown", "time": time})
            current_section = "breakdown"

    return sections


def analyze_track(file_path, full_track=False, json_output=False):
    """
    Analyze an audio file to extract musical features for techno reproduction.

    Extracts:
    1. BPM (Tempo)
    2. Key and Mode (Major/Minor)
    3. Beat Map
    4. Section Detection (Intro/Drop/Breakdown)

    Args:
        file_path (str): Path to audio file (.wav, .mp3, etc)
        full_track (bool): Analyze full track instead of first 10s
        json_output (bool): Output as JSON instead of human-readable

    Returns:
        dict: Analysis results if json_output=True, None otherwise
    """
    if not os.path.exists(file_path):
        error_msg = f"Error: File not found: {file_path}"
        if json_output:
            print(json.dumps({"error": error_msg}))
        else:
            print(error_msg)
        return None

    if not json_output:
        print(f"\n🔍 Analyzing: {os.path.basename(file_path)}...")

    # 1. Load Audio
    try:
        duration = None if full_track else 10.0
        y, sr = librosa.load(file_path, sr=22050, duration=duration)
    except Exception as e:
        error_msg = f"Error loading audio: {e}"
        hint = (
            "You may need to install ffmpeg for mp3 support "
            "(macOS: brew install ffmpeg)"
        )
        if json_output:
            print(json.dumps({"error": error_msg, "hint": hint}))
        else:
            print(f"❌ {error_msg}")
            print(f"💡 Hint: {hint}")
        return None

    full_duration = librosa.get_duration(path=file_path)
    analyzed_duration = librosa.get_duration(y=y, sr=sr)

    if not json_output:
        print(f"  Duration: {full_duration:.2f}s (analyzing {analyzed_duration:.2f}s)")

    # 2. Tempo & Beats
    if not json_output:
        print("  Detecting Tempo...")
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    tempo_val = float(tempo[0]) if hasattr(tempo, "__iter__") else float(tempo)

    # 3. Key and Mode Detection
    if not json_output:
        print("  Estimating Key and Mode...")
    key_name, mode = detect_key_and_mode(y, sr)

    # 4. Section Detection
    if not json_output:
        print("  Detecting Sections...")
    sections = detect_sections(y, sr)

    # Prepare results
    results = {
        "file": os.path.basename(file_path),
        "duration_total": round(full_duration, 2),
        "duration_analyzed": round(analyzed_duration, 2),
        "bpm": round(tempo_val, 2),
        "key": key_name,
        "mode": mode,
        "sections": sections,
    }

    # Output
    if json_output:
        print(json.dumps(results, indent=2))
    else:
        print("\n✅ Analysis Complete.")
        print("------------------------------------------------")
        print(f"BPM: {results['bpm']}")
        print(f"Key: {results['key']} {results['mode']}")
        if sections:
            print(f"Sections detected: {len(sections)}")
            for section in sections[:3]:  # Show first 3
                print(f"  - {section['type'].capitalize()} at {section['time']:.2f}s")
        print("------------------------------------------------")
        print("To recreate in Ableton:")
        print(f"1. Set Global Tempo to {results['bpm']}")
        print(f"2. Root Note: {results['key']} {results['mode']}")
        print("------------------------------------------------")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Analyze audio tracks for musical features (BPM, key, structure)"
    )
    parser.add_argument("file_path", help="Path to audio file (.wav, .mp3, .aif, etc.)")
    parser.add_argument(
        "--full",
        action="store_true",
        help="Analyze full track instead of first 10 seconds",
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()
    analyze_track(args.file_path, full_track=args.full, json_output=args.json)


if __name__ == "__main__":
    main()
