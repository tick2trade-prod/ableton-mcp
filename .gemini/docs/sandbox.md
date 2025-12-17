# Sandbox

> Source: [https://geminicli.com/docs/cli/sandbox](https://geminicli.com/docs/cli/sandbox)

## Overview

Sandbox mode isolates tool execution in a secure, containerized environment.

## Enabling Sandbox

### Configuration
```json
{
  "sandbox": true
}
```

### Command Line
```bash
gemini --sandbox
```

## How It Works

1. Tools execute in isolated container
2. Limited file system access
3. Network restrictions
4. Process isolation

## Sandbox Features

### File System
- Read-only access to project
- Write to designated areas only
- No access to system files

### Network
- Limited outbound connections
- No inbound connections
- Allowed hosts configurable

### Processes
- No spawning arbitrary processes
- Controlled resource usage

## Configuration

```json
{
  "sandbox": {
    "enabled": true,
    "allowedPaths": [
      "./src",
      "./tests"
    ],
    "allowedHosts": [
      "api.example.com"
    ],
    "readOnly": false
  }
}
```

## When to Use Sandbox

### Recommended
- Untrusted code execution
- Sensitive environments
- Shared systems

### Not Needed
- Local development
- Trusted projects
- Full access required

## Limitations

- MCP servers may not work
- Docker required
- Performance overhead
- Some tools unavailable

## ableton-mcp Considerations

For this project, sandbox is generally not needed as:
- Local development environment
- Trusted codebase
- MCP servers need full access

## Related Pages

- [Security](secure-mode.md) - Security features
- [Trusted Folders](trusted-folders.md) - Trust settings
