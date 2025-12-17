# Memory Tool

> Source: [https://geminicli.com/docs/tools/memory](https://geminicli.com/docs/tools/memory)

## Overview

Save and recall information across sessions.

## save_memory

```
> Remember that our kick uses 120 BPM
[Saves to memory]
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `content` | string | Memory content |
| `tags` | array | Optional tags |

## Recall

Memories are automatically used in context:
```
> What BPM does our kick use?
[Recalls: 120 BPM]
```

## Memory Management

```
/memory list          # List all memories
/memory search kick   # Search memories
/memory delete id     # Remove memory
/memory clear         # Clear all
```

## ableton-mcp Memories

Useful project memories:
```
> Remember: Default tempo is 120 BPM
> Remember: All tracks sidechain from Kick
> Remember: Rumble uses Hybrid Reverb → Roar → EQ Eight → Compressor
> Remember: Tests require live Ableton connection
```

## Related Pages

- [Memport](memport.md) - Memory import
- [Tools](tools.md) - All tools
