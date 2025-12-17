# Installation

> Source: [https://geminicli.com/docs/get-started/installation](https://geminicli.com/docs/get-started/installation)

## Installation Methods

### NPM (Recommended)

```bash
npm install -g @google/gemini-cli
```

### Homebrew (macOS)

```bash
brew install gemini-cli
```

### Manual Installation

Download from [GitHub Releases](https://github.com/google-gemini/gemini-cli/releases).

## Verification

```bash
gemini --version
```

## System Requirements

- Node.js 18+ (for npm installation)
- macOS, Linux, or Windows
- Internet connection

## Post-Installation

### Authenticate
```bash
gemini auth login
```

### Configure
```bash
gemini settings
```

### Test
```bash
gemini "Hello, world!"
```

## Updating

### NPM
```bash
npm update -g @google/gemini-cli
```

### Homebrew
```bash
brew upgrade gemini-cli
```

## ableton-mcp Integration

After installation:

1. Configure MCP servers in `~/.gemini/settings.json`
2. Navigate to project directory
3. Start Gemini CLI

```bash
cd ~/ableton-mcp
gemini
```

## Related Pages

- [Get Started](get-started.md) - Quick start
- [Configuration](configuration.md) - Settings
- [Uninstall](uninstall.md) - Removal
