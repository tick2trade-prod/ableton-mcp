# Authentication

> Source: [https://geminicli.com/docs/get-started/authentication](https://geminicli.com/docs/get-started/authentication)

## Authentication Methods

### Google Account Login

```bash
gemini auth login
```

Opens browser for Google OAuth authentication.

### API Key

```bash
export GOOGLE_API_KEY=your_api_key
```

Or in settings:
```json
{
  "apiKey": "your_api_key"
}
```

### Application Default Credentials (ADC)

For Google Cloud environments:
```bash
gcloud auth application-default login
```

## Verifying Authentication

```bash
gemini auth status
```

## Managing Credentials

### View Current Auth
```bash
gemini auth whoami
```

### Logout
```bash
gemini auth logout
```

### Switch Accounts
```bash
gemini auth logout
gemini auth login
```

## Secure Key Storage

### Environment Variables (Recommended)
```bash
# ~/.bashrc or ~/.zshrc
export GOOGLE_API_KEY=your_key
```

### Keychain (macOS)
Gemini CLI can use system keychain for secure storage.

## ableton-mcp Setup

```bash
# Set API key
export GOOGLE_API_KEY=your_key

# Verify
gemini auth status

# Test
gemini "Hello, world!"
```

## Related Pages

- [Installation](installation.md) - Setup steps
- [Configuration](configuration.md) - All settings
