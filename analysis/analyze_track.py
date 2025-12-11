
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
    # Mono, 22kHz is sufficient for tempo/key
    y, sr = librosa.load(file_path, sr=22050)
    duration = librosa.get_duration(y=y, sr=sr)
    print(f"  Duration: {duration:.2f}s")
    
    # 2. Tempo & Beats
    print("  Detecting Tempo...")
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    print(f"  BPM: {tempo:.2f}")
    
    # 3. Key Detection (Simple Chorma)
    print("  Estimating Key...")
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    key_idx = np.mean(chroma, axis=1).argmax()
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    print(f"  Estimated Key: {keys[key_idx]}")
    
    # 4. Low-End Energy (Techno Rumble check)
    # Filter for sub-bass < 100Hz
    # This is a placeholder for more advanced spectral analysis
    
    print("\n✅ Analysis Complete.")
    print("------------------------------------------------")
    print(f"To recreate in Ableton:")
    print(f"1. Set Global Tempo to {tempo:.2f}")
    print(f"2. Root Note: {keys[key_idx]}")
    print("------------------------------------------------")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run analysis/analyze_track.py <path_to_audio_file>")
        print("Example: uv run analysis/analyze_track.py ~/Downloads/techno.mp3")
    else:
        analyze_track(sys.argv[1])
