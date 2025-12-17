#!/usr/bin/env python3
"""Compare audio signals using librosa for similarity metrics."""

import json
import sys
from pathlib import Path

import librosa
import numpy as np


def load_audio(path: str, sr: int = 22050) -> tuple[np.ndarray, int]:
    """Load audio file."""
    y, sr = librosa.load(path, sr=sr, mono=True)
    return y, sr


def compute_mfcc(y: np.ndarray, sr: int, n_mfcc: int = 13) -> np.ndarray:
    """Compute MFCC features."""
    return librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)


def compute_similarity(ref_path: str, test_path: str) -> dict:
    """
    Compute similarity between reference and test audio.

    Returns dict with:
        - mfcc_similarity: Cosine similarity of MFCCs (0-1)
        - spectral_similarity: Spectral contrast similarity
        - overall: Weighted average
    """
    # Load audio
    ref_y, ref_sr = load_audio(ref_path)
    test_y, test_sr = load_audio(test_path)

    # Trim to match length (use shorter)
    min_len = min(len(ref_y), len(test_y))
    ref_y = ref_y[:min_len]
    test_y = test_y[:min_len]

    # MFCC similarity
    ref_mfcc = compute_mfcc(ref_y, ref_sr)
    test_mfcc = compute_mfcc(test_y, test_sr)

    # Pad/trim to same shape
    min_frames = min(ref_mfcc.shape[1], test_mfcc.shape[1])
    ref_mfcc = ref_mfcc[:, :min_frames]
    test_mfcc = test_mfcc[:, :min_frames]

    # Cosine similarity of mean MFCC
    ref_mean = ref_mfcc.mean(axis=1)
    test_mean = test_mfcc.mean(axis=1)
    mfcc_sim = np.dot(ref_mean, test_mean) / (
        np.linalg.norm(ref_mean) * np.linalg.norm(test_mean)
    )

    # Spectral contrast
    ref_contrast = librosa.feature.spectral_contrast(y=ref_y, sr=ref_sr)
    test_contrast = librosa.feature.spectral_contrast(y=test_y, sr=test_sr)
    min_frames = min(ref_contrast.shape[1], test_contrast.shape[1])
    ref_contrast = ref_contrast[:, :min_frames]
    test_contrast = test_contrast[:, :min_frames]
    contrast_diff = np.mean(np.abs(ref_contrast - test_contrast))
    spectral_sim = max(0, 1 - contrast_diff / 50)  # Normalize

    # Overall (weighted)
    overall = 0.6 * mfcc_sim + 0.4 * spectral_sim

    return {
        "mfcc_similarity": round(float(mfcc_sim) * 100, 1),
        "spectral_similarity": round(float(spectral_sim) * 100, 1),
        "overall": round(float(overall) * 100, 1),
    }


def compare_stems(
    ref_stems_dir: str,
    test_stems_dir: str,
    output_file: str | None = None,
) -> dict:
    """
    Compare all stems between reference and test directories.

    Expected structure:
        drums.wav, bass.wav, vocals.wav, other.wav
    """
    stem_names = ["drums", "bass", "vocals", "other"]
    results = {}

    ref_dir = Path(ref_stems_dir)
    test_dir = Path(test_stems_dir)

    for stem in stem_names:
        ref_file = ref_dir / f"{stem}.wav"
        test_file = test_dir / f"{stem}.wav"

        if not ref_file.exists():
            results[stem] = {"error": "Reference stem not found"}
            continue
        if not test_file.exists():
            results[stem] = {"error": "Test stem not found"}
            continue

        print(f"Comparing {stem}...")
        results[stem] = compute_similarity(str(ref_file), str(test_file))

    # Overall summary
    valid = [r for r in results.values() if "overall" in r]
    if valid:
        results["_summary"] = {
            "average_similarity": round(
                sum(r["overall"] for r in valid) / len(valid), 1
            ),
            "stems_compared": len(valid),
        }

    if output_file:
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {output_file}")

    return results


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: compare_signals.py <ref_stems_dir> <test_stems_dir> [output.json]"
        )
        sys.exit(1)

    ref_dir = sys.argv[1]
    test_dir = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else None

    results = compare_stems(ref_dir, test_dir, output)
    print(json.dumps(results, indent=2))
