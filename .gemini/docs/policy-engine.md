# Policy Engine

> Source: [https://geminicli.com/docs/core/policy-engine](https://geminicli.com/docs/core/policy-engine)

## Overview

The Policy Engine provides fine-grained control over tool execution.

## Policies

### Allow Policy
```json
{
  "policies": [
    {
      "type": "allow",
      "tools": ["read_file", "write_file"],
      "paths": ["./src/**", "./tests/**"]
    }
  ]
}
```

### Deny Policy
```json
{
  "policies": [
    {
      "type": "deny",
      "tools": ["run_shell_command"],
      "patterns": ["rm -rf *", "sudo *"]
    }
  ]
}
```

### Confirm Policy
```json
{
  "policies": [
    {
      "type": "confirm",
      "tools": ["write_file"],
      "paths": ["./src/**"]
    }
  ]
}
```

## Policy Evaluation

1. Check deny policies first (highest priority)
2. Check allow policies
3. Check confirm policies
4. Apply default behavior

## Configuration

```json
{
  "policyEngine": {
    "enabled": true,
    "policies": [...]
  }
}
```

## ableton-mcp Policies

```json
{
  "policies": [
    {
      "type": "allow",
      "tools": ["read_file"],
      "paths": ["**/*"]
    },
    {
      "type": "confirm",
      "tools": ["write_file"],
      "paths": ["./src/**", "./tests/**", "./live_set/**"]
    },
    {
      "type": "allow",
      "tools": ["run_shell_command"],
      "patterns": ["pytest *", "make check-*", "git status"]
    },
    {
      "type": "deny",
      "tools": ["run_shell_command"],
      "patterns": ["rm -rf *"]
    }
  ]
}
```

## Related Pages

- [Tools API](tools-api.md) - Tool management
- [Trusted Folders](trusted-folders.md) - Trust settings
- [Sandbox](sandbox.md) - Isolation
