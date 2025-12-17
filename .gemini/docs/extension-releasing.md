# Extension Releasing

> Source: [https://geminicli.com/docs/extensions/extension-releasing](https://geminicli.com/docs/extensions/extension-releasing)

## Publishing Process

### 1. Prepare Package
```json
{
  "name": "@yourname/extension",
  "version": "1.0.0",
  "main": "dist/index.js",
  "geminiCli": {
    "type": "extension"
  }
}
```

### 2. Build for Production
```bash
npm run build
npm test
```

### 3. Publish
```bash
npm publish --access public
```

## Versioning

Follow semver:
- MAJOR: Breaking changes
- MINOR: New features
- PATCH: Bug fixes

## Registry

Extensions are published to npm with the `gemini-cli-extension` keyword.

## Documentation

Include:
- README.md
- Usage examples
- Configuration options

## Related Pages

- [Extensions](extensions.md) - Overview
- [Getting Started with Extensions](extensions-getting-started.md) - Development
