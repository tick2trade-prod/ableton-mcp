import librosa
import numpy as np
import sys
import os


def analyze_track(file_path):
    """
    Analyze an audio file to extract musical features for techno reproduction.

    Extracts:
    1. BPM (Tempo)
    2. Beat Map
    3. Key (Chromagram)
    4. Onset Strength (Energy)

    Args:
        file_path (str): Path to audio file (.wav, .mp3, etc)
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return

    print(f"\n🔍 Analyzing: {os.path.basename(file_path)}...")

    # 1. Load Audio
    try:
        # Load only 10s to avoid memory issues and speed up
        y, sr = librosa.load(file_path, sr=22050, duration=10.0)
    except Exception as e:
        print(f"❌ Error loading audio: {e}")
        print("💡 Hint: You may need to install ffmpeg for mp3 support.")
        print("   macOS: brew install ffmpeg")
        return

    full_duration = librosa.get_duration(path=file_path)
    print(f"  Duration: {full_duration:.2f}s (analyzing first 10s)")

    # 2. Tempo & Beats
    print("  Detecting Tempo...")
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    # tempo may be array in newer librosa versions
    tempo_val = float(tempo[0]) if hasattr(tempo, "__iter__") else float(tempo)
    print(f"  BPM: {tempo_val:.2f}")

    # 3. Key Detection (Simple Chorma)
    print("  Estimating Key...")
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    key_idx = np.mean(chroma, axis=1).argmax()
    keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    print(f"  Estimated Key: {keys[key_idx]}")

    # 4. Low-End Energy (Techno Rumble check)
    # Filter for sub-bass < 100Hz
    # This is a placeholder for more advanced spectral analysis

    print("\n✅ Analysis Complete.")
    print("------------------------------------------------")
    print("To recreate in Ableton:")
    print(f"1. Set Global Tempo to {tempo_val:.2f}")
    print(f"2. Root Note: {keys[key_idx]}")
    print("------------------------------------------------")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run analysis/analyze_track.py <path_to_audio_file>")
        print("Example: uv run analysis/analyze_track.py ~/Downloads/techno.mp3")
    else:
        analyze_track(sys.argv[1])
