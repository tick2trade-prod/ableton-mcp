# Pydantic Models Changelog

All notable changes to validation models will be documented in this file.

Format: [Semantic Versioning](https://semver.org/)
- **MAJOR**: Breaking schema changes
- **MINOR**: New fields/validators (backward compatible)
- **PATCH**: Bug fixes, documentation

## [Unreleased]

## [1.1.0] - 2025-12-14
### Added
- Track validation models in `models/v1/track_models.py`
- `TrackType`, `MIDINote`, `DeviceConfig`, `TrackConfig`, `ProjectConfig` models
- Track configuration validator with JSON support
- Example track configuration and validation
- Modern Pydantic 2.x patterns throughout

## [1.0.0] - 2025-12-14
### Added
- Initial release with test validation models
- `AbletonReference` for manual section validation
- `ModuleDocstring`, `ClassDocstring`, `MethodDocstring` models
- `TestMethod`, `TestClass`, `TestModule` models
- `ValidationResult` for test file validation results
- Modern Pydantic 2.x patterns:
  - `model_config = ConfigDict(...)`
  - `@field_validator` decorators
  - `typing_extensions.Annotated` for field metadata
  - Future-proof for Pydantic 3.0
