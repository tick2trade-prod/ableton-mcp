---
description: Run full CI validation locally
---
// turbo-all

## CI Workflow

1. Quick check (no Ableton):
   ```bash
   just ci
   ```

2. With live Ableton connection:
   ```bash
   just ci-live
   ```

3. Pre-merge validation:
   ```bash
   just pre-merge
   ```

4. Full doctor with edition detection:
   ```bash
   just doctor
   ```

## Expected Result
- Lint passes
- Tests pass
- Doctor passes (4/4)
- Ready to merge
