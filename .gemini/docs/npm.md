# NPM Packages

> Source: [https://geminicli.com/docs/npm](https://geminicli.com/docs/npm)

## Package Structure

```
gemini-cli/
├── packages/
│   ├── cli/          # Main CLI application
│   ├── core/         # Core functionality
│   └── sdk/          # Extension SDK
```

## Main Packages

### @google/gemini-cli
The main CLI tool:
```bash
npm install -g @google/gemini-cli
```

### @google/gemini-cli-core
Core library (for extensions):
```bash
npm install @google/gemini-cli-core
```

### @google/gemini-cli-sdk
SDK for building extensions:
```bash
npm install @google/gemini-cli-sdk
```

## Versioning

All packages follow semver and are released together.

## Related Pages

- [Installation](installation.md) - Install guide
- [Extensions](extensions.md) - Extension development
- [Releases](releases.md) - Release info
