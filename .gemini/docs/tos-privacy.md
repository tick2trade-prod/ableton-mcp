# Terms of Service and Privacy

> Source: [https://geminicli.com/docs/tos-privacy](https://geminicli.com/docs/tos-privacy)

## Terms of Service

Usage of Gemini CLI is subject to:
- [Google Cloud Terms](https://cloud.google.com/terms)
- [Gemini API Terms](https://ai.google.dev/terms)

## Privacy

### Data Collection
- Anonymous telemetry (can be disabled)
- No conversation content stored
- No file contents transmitted beyond API

### Disabling Telemetry
```json
{
  "telemetry": false
}
```

### API Data
Data sent to Gemini API:
- Your prompts
- File context (when requested)

Subject to:
- [Gemini API Privacy Policy](https://ai.google.dev/terms)

## Security

### Credentials
- Stored locally
- Encrypted where possible
- Use environment variables for keys

### Tool Execution
- Confirmation required by default
- Sandbox available for isolation

## Related Pages

- [Telemetry](telemetry.md) - Data collection settings
- [Sandbox](sandbox.md) - Isolation
- [Trusted Folders](trusted-folders.md) - Security
