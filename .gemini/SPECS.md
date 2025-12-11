# Spec Index

Automatically tracked specifications tied to branches.

## Format
```
NNNN-<slug>.md
```
- `NNNN`: Monotonically increasing ID (0001, 0002, ...)
- `<slug>`: Branch name slug

## Specs

| ID | Branch | PR | Status |
|----|--------|----| -------|
| [0001](specs/0001-rack-chain-tools.md) | `feature/rack-chain-tools` | #50 | ✅ Tests Passing |
| [0002](specs/0002-io-alchemy-techno.md) | `feature/0001-rack-chain-tools` | - | ✅ macOS Working |

## Conventions

### Branch Naming
```
<type>/<id>-<slug>
```
Examples:
- `feature/0001-rack-chain-tools`
- `fix/0002-connection-timeout`
- `test/0003-integration-tests`

Types: `feature`, `fix`, `test`, `docs`, `refactor`

### PR Title Format
```
<type>: <description> (#<pr_number>)
```
Examples:
- `feat: add rack chain tools (#50)`
- `fix: resolve timeout issue (#51)`

### Commit Format
```
<type>: <description>
```
Types: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`
