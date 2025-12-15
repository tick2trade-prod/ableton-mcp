# Asset Organization

This directory contains binary assets for the project. For a clean Git history, we recommend using [Git Large File Storage (LFS)](https://git-lfs.github.com/).

## Directory Structure

- **`audio/`**: Audio files (samples, recordings).
    - **`reference/`**: Reference tracks for analysis/recreation.
        - *Place `YOURE_TOXIC.mp3` here.*
    - **`samples/`**: One-shot samples and loops.
- **`midi/`**: Exported MIDI clips and patterns.
- **`projects/`**: Ableton Live Project folders (`.als` files and associated samples).

## Git LFS Setup (Recommended)

To prevent repository bloat, track large binary files with LFS:

```bash
# Install LFS
git lfs install

# Track common audio formats
git lfs track "*.wav"
git lfs track "*.mp3"
git lfs track "*.aif"
git lfs track "*.als"
git lfs track "*.alp"

# Verify tracking
cat .gitattributes
```

## Usage in Scripts

- **Analysis**: Place reference tracks in `assets/audio/reference/`.
- **Tests**: Load samples from `assets/audio/samples/`.
