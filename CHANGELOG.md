# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Conventional Commits](https://www.conventionalcommits.org/).

## [Unreleased]

### Added
- **Rack Chain Tools**
  - `create_audio_effect_rack` - Create empty Audio Effect Rack on track
  - `create_rack_chain` - Add chain to rack
  - `load_effect_to_chain` - Load effect into specific chain
  - `load_effect_on_main` - Load effect on Master track
  - `get_browser_tree` - Get browser category hierarchy
  - `get_browser_items_at_path` - Navigate browser by path
  - `load_drum_kit` - Load drum rack with kit

- **Updated Tools**
  - `get_device_parameters` - Now supports devices in rack chains
  - `set_device_parameter` - Now supports devices in rack chains

- **Testing Infrastructure**
  - 38 integration tests (run against live Ableton DAW)
  - `tests/test_tools.py` - 27 general tool tests
  - `tests/test_rack_chain_tools.py` - 11 branch-specific tests
  - Pytest markers: `live`, `session`, `clip`, `device`, `browser`, `transport`

- **Development Tooling**
  - `Makefile` with test, verify, and deployment commands
  - `.pre-commit-config.yaml` for linting and conventional commits
  - GitLab MR templates with pre-merge checklists
  - `make verify` target for pre-merge validation

- **Documentation**
  - [TOOLS.md](./TOOLS.md) - Complete list of 27 available tools
  - `.gemini/` spec-driven development system
  - Conventional commit and branch naming conventions

### Changed
- Docstrings for `duplicate_clip`, `empty_clip_slot`, `relocate_clip` now explicitly state MIDI-only limitation
- `device_index` handling in `_create_audio_effect_rack` now validates rack loaded and returns actual position

### Fixed
- Removed redundant exception object from 33 `logger.exception()` calls
