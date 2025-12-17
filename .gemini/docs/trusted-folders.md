# Trusted Folders

> Source: [https://geminicli.com/docs/cli/trusted-folders](https://geminicli.com/docs/cli/trusted-folders)

## Overview

Trusted folders allow tools to execute without confirmation in specific directories.

## Configuration

```json
{
  "trustedFolders": [
    "~/projects/ableton-mcp",
    "~/projects/trusted-project"
  ]
}
```

## Trust Levels

### Folder Trust
All tools run without confirmation in trusted folders.

### Server Trust
MCP servers can be individually trusted:
```json
{
  "mcpServers": {
    "my-server": {
      "trust": true
    }
  }
}
```

## Security Considerations

### When to Trust
- Personal development folders
- Controlled environments
- Frequently used projects

### When NOT to Trust
- Unknown projects
- Downloaded code
- Shared environments

## ableton-mcp Setup

```json
{
  "trustedFolders": [
    "~/ableton-mcp"
  ],
  "mcpServers": {
    "ableton_codegen": {
      "trust": true
    }
  }
}
```

## Verification

Check trust status:
```
/trust status
```

## Related Pages

- [Sandbox](sandbox.md) - Isolation
- [Settings](settings.md) - Configuration
- [MCP](mcp.md) - Server trust
