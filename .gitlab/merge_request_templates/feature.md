## Summary
<!-- Describe what this MR does -->


## Spec Reference
<!-- Link to the spec file, e.g., `.gemini/specs/0001-name.md` -->
- Spec: `.gemini/specs/____-____.md`

## Type
<!-- Check one -->
- [ ] `feat` - New feature
- [ ] `fix` - Bug fix
- [ ] `test` - Tests only
- [ ] `docs` - Documentation
- [ ] `refactor` - Code refactor

---

## Pre-Merge Checklist

### Required
- [ ] **Title follows format**: `<type>: <description> (#<id>)`
- [ ] **Spec file exists** and is updated
- [ ] **All tests pass**: `make test`
- [ ] **Pre-commit passed**: `make pre-commit`
- [ ] **Branch is rebased** on target

### Tests
- [ ] New/modified code has test coverage
- [ ] Tests run against **live Ableton** (no mocks)
- [ ] `make test-connection` passes

### Code Quality
- [ ] No lint errors
- [ ] Follows project conventions
- [ ] No hardcoded secrets

---

## Verification
```bash
# Run these before merging
make test           # All tests pass
make pre-commit     # Linting passes
make check-port     # Ableton connection ready
```
