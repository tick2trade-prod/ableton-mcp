# Memport (Memory Import Processor)

> Source: [https://geminicli.com/docs/core/memport](https://geminicli.com/docs/core/memport)

## Overview

Memport enables importing and processing memories for persistent context across sessions.

## Usage

### Save Memory
```
> Remember that our project uses 120 BPM for all tracks
[Saves to memory]
```

### Recall Memory
```
> What BPM do we use?
[Recalls from memory: 120 BPM]
```

### Import Memories
```
/memory import notes.md
```

## Memory Format

Memories are stored as structured data:
```json
{
  "memories": [
    {
      "id": "mem_123",
      "content": "Project uses 120 BPM",
      "timestamp": "2024-01-01T00:00:00Z",
      "tags": ["project", "settings"]
    }
  ]
}
```

## Configuration

```json
{
  "memory": {
    "enabled": true,
    "path": "~/.gemini/memories.json",
    "maxItems": 1000
  }
}
```

## ableton-mcp Memories

Useful memories for this project:
- Tempo: 120 BPM
- Time signature: 4/4
- Key conventions
- Device preferences

```
> Remember: Kick tracks use Drum Rack with 808 samples
> Remember: Rumble uses Hybrid Reverb → Roar → EQ Eight → Compressor
> Remember: All tracks use sidechain from Kick
```

## Related Pages

- [Memory Tool](memory.md) - Memory tool
- [Configuration](configuration.md) - Settings
