"""
Analyze separated stems to extract musical patterns.
"""

import argparse
import json
from pathlib import Path

import librosa


def analyze_drums(audio_path):
    print(f"Analyzing drums: {audio_path}")
    y, sr = librosa.load(audio_path)

    # onset detection
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units="time")

    # simple low/high freq separation for kick vs hihat
    # This is a naive approximation, but a starting point
    # D = np.abs(librosa.stft(y))
    # Low freq energy (< 150Hz)
    # low_band = D[: int(150 / (sr / 2) * D.shape[0]), :]
    # low_energy = np.sum(low_band, axis=0)

    # High freq energy (> 5000Hz)
    # high_band = D[int(5000 / (sr / 2) * D.shape[0]) :, :]
    # high_energy = np.sum(high_band, axis=0)

    # Normalize
    # times = librosa.times_like(low_energy, sr=sr)

    return {
        "onsets": onsets.tolist(),
        # We'll refine kick/hat detection in future iterations
        # "kick_onsets": ...,
        # "hat_onsets": ...
    }


def analyze_bass(audio_path):
    print(f"Analyzing bass: {audio_path}")
    y, sr = librosa.load(audio_path)

    # Pitch tracking using PYIN
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y, fmin=librosa.note_to_hz("C1"), fmax=librosa.note_to_hz("C4")
    )

    times = librosa.times_like(f0, sr=sr)

    notes = []
    current_note = None

    for i, (f, v) in enumerate(zip(f0, voiced_flag, strict=False)):
        if v:
            pitch_midi = librosa.hz_to_midi(f)
            if current_note is None:
                current_note = {"start": times[i], "pitch": pitch_midi, "frames": 1}
            else:
                # If pitch is close, extend note
                if abs(current_note["pitch"] - pitch_midi) < 1.0:
                    current_note["frames"] += 1
                else:
                    # New note
                    current_note["duration"] = times[i] - current_note["start"]
                    notes.append(current_note)
                    current_note = {"start": times[i], "pitch": pitch_midi, "frames": 1}
        else:
            if current_note:
                current_note["duration"] = times[i] - current_note["start"]
                notes.append(current_note)
                current_note = None

    return {"notes": notes}


def main():
    parser = argparse.ArgumentParser(description="Analyze audio stems")
    parser.add_argument("stems_dir", type=Path, help="Directory containing stems")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("analysis_results.json"),
        help="Output JSON file",
    )

    args = parser.parse_args()

    if not args.stems_dir.exists():
        raise FileNotFoundError(f"Stems directory not found: {args.stems_dir}")

    results = {}

    drums_path = args.stems_dir / "drums.mp3"
    if drums_path.exists():
        results["drums"] = analyze_drums(drums_path)
    else:
        print(f"⚠️ Drums not found: {drums_path}")

    bass_path = args.stems_dir / "bass.mp3"
    if bass_path.exists():
        results["bass"] = analyze_bass(bass_path)
    else:
        print(f"⚠️ Bass not found: {bass_path}")

    if not results:
        raise FileNotFoundError("No analysis results generated (stems missing?)")

    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Analysis complete. Results saved to {args.output}")


if __name__ == "__main__":
    main()
