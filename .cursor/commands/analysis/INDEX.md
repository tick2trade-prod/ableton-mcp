# Analysis Commands Index

Debugging and performance analysis commands for diagnosing code issues.

---

## Commands

| Command | Purpose | Key Features |
|---------|---------|--------------|
| `debug-assistant.md` | AI-powered debugging | Auto-detect errors, suggest fixes, GAM learning |
| `performance-profiler.md` | Performance profiling | CPU, memory, I/O, database profiling |

---

## Usage Patterns

### Auto-Detect and Fix Errors
```
/debug-assistant
Auto Fix: true
Search GAM: true
```

### Debug Specific Error
```
/debug-assistant
Error: AttributeError: 'NoneType' object has no attribute 'email'
Context: Occurs when user not found in database
```

### Profile Performance
```
/performance-profiler
Target: app.services.user.get_user_profile
Profile Type: all
Duration: 10
Generate Flamegraph: true
```

### Database Performance
```
/performance-profiler
Target: POST /api/users/register
Profile Type: database
```

---

## Analysis Workflow

### Debug Assistant
1. **Error Detection** - Auto-detect from terminal
2. **Root Cause Analysis** - Examine code and context
3. **GAM Memory Search** - Find similar past issues
4. **Solution Generation** - Propose ranked fixes
5. **Apply Fix** - Optionally auto-apply solution

### Performance Profiler
1. **Setup Profiling** - Inject instrumentation
2. **Execute Target** - Run and collect data
3. **Analyze Results** - Identify bottlenecks
4. **Generate Report** - Metrics and suggestions
5. **Compare Baseline** - Detect regressions

---

## Common Issues Handled

### Debug Assistant
- **AttributeError**: None checks, object validation
- **KeyError**: Dictionary access, default values
- **TypeError**: Type validation, conversion
- **SQLAlchemyError**: Query issues, connections
- **ValidationError**: Pydantic validation

### Performance Profiler
- **N+1 Queries**: Database optimization
- **Memory Leaks**: Object lifecycle issues
- **Slow Functions**: CPU hotspots
- **I/O Bottlenecks**: File/network operations
- **Missing Indexes**: Database performance

---

## Integration

### Pre-commit Hooks
```bash
# Auto-debug before commit
uv run python -m app.tools.debug_assistant --auto-detect
```

### CI/CD Pipeline
```yaml
- name: Performance Regression Check
  run: uv run python -m app.tools.performance_profiler --compare-baseline
```

### Development Workflow
1. **Debug Assistant** → Fix errors immediately
2. **Performance Profiler** → Optimize bottlenecks
3. **Code Review** → Validate fixes
4. **Test Generator** → Add regression tests

---

## Related Directories

- `/qa/` - Code review and testing
- `/workflows/` - Complete development workflows
- `/operations/` - Apply fixes and optimizations
