# Exec: Skill

**Rank**: 5 - Hybrid Registry + Execution Commands

## Overview

Execute any skill from the 2000_INDEX_SKILLS registry by ID.

## Usage

```
/exec-skill skill_id="2001" params='{"feature_name": "User auth"}'
```

## Parameters

- `skill_id`: Skill ID from registry (required)
- `params`: Skill-specific parameters as JSON (required)

## Available Skills

See `.cursor/commands/app/registry/2000_INDEX_SKILLS.md`

## Implementation

```python
from app.server.skills import get_skill

skill = get_skill(skill_id)
result = await skill.execute(**params)
```

## Output

```json
{"skill_id": "2001", "result": {...}}
```
