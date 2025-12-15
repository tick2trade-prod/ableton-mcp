# Workflow: Schema Design

**Phase**: 3 - Feature Development
**ID**: 4014

## Overview

Design database schema changes with migrations.

## Usage

```
/workflow-schema-design feature="User profiles" migration_type="additive"
```

## Parameters

- `feature`: Feature requiring schema changes (required)
- `migration_type`: additive | breaking (default: "additive")
- `generate_migration`: Auto-generate migration (default: true)

## Workflow Steps

1. Design schema changes
2. Plan migration strategy
3. Generate migration scripts
4. Document rollback procedure
5. Review with DBA

## Output

```json
{
  "migration_file": "migrations/001_user_profiles.sql",
  "rollback_file": "migrations/001_rollback.sql",
  "status": "ready_for_review"
}
```
