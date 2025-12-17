# Uninstall

> Source: [https://geminicli.com/docs/cli/uninstall](https://geminicli.com/docs/cli/uninstall)

## Uninstall Methods

### NPM
```bash
npm uninstall -g @google/gemini-cli
```

### Homebrew
```bash
brew uninstall gemini-cli
```

## Cleanup

### Remove Configuration
```bash
rm -rf ~/.gemini
```

### Remove Credentials
```bash
# Credentials stored via OAuth
rm -rf ~/.gemini/credentials.json

# Environment variables
# Remove from ~/.bashrc or ~/.zshrc:
# export GOOGLE_API_KEY=...
```

### Remove Project Settings
```bash
rm -rf .gemini/
```

## Verify Removal

```bash
which gemini  # Should return nothing
gemini --version  # Should show command not found
```

## Related Pages

- [Installation](installation.md) - Reinstallation
