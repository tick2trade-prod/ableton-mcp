# Claude Installation

> Source: [Claude Platform Docs](https://platform.claude.com/docs)

## Installation Methods

### NPM (Recommended)
```bash
npm install -g @anthropic-ai/claude-code
```

### Homebrew (macOS)
```bash
brew install claude-code
```

## Prerequisites

- Node.js 18+
- Anthropic API key

## Post-Installation

### Set API Key
```bash
export ANTHROPIC_API_KEY=your_api_key
```

### Verify Installation
```bash
claude --version
```

### Test
```bash
claude "Hello, world!"
```

## Configuration

Create `.claude/` directory for project settings:
```bash
mkdir -p .claude
```

## ableton-mcp Setup

1. Install Claude CLI
2. Set API key
3. Configure permissions in `.claude/settings.local.json`
4. Run `claude` in project directory

## Related Pages

- [Intro](intro.md) - Overview
- [Configuration](configuration.md) - Settings
- [Permissions](permissions.md) - Command permissions
