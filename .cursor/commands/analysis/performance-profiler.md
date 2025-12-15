# Performance Profiler

## Overview

Profile code performance, identify bottlenecks, and suggest optimizations. Analyzes CPU, memory, I/O, and database query performance.

## Usage

Type `/performance-profiler` to profile current code or specify target.

## Parameters

- `target`: What to profile (function, file, endpoint, test) (required)
- `profile_type`: Type of profiling (cpu, memory, io, database, all) (default: all)
- `duration`: Profiling duration in seconds (default: 10)
- `generate_flamegraph`: Generate flame graph visualization (default: true)

## Example Usage

### Profile Function

```
/performance-profiler
Target: app.services.user.get_user_profile
Profile Type: all
Duration: 10
```

### Profile API Endpoint

```
/performance-profiler
Target: POST /api/users/register
Profile Type: database
```

### Memory Profiling

```
/performance-profiler
Target: app.utils.data_processor.process_large_file
Profile Type: memory
Generate Flamegraph: true
```

### Profile Tests

```
/performance-profiler
Target: tests/integration/test_api.py::test_user_flow
Profile Type: all
```

## Workflow

1. **Setup Profiling**:
   - Inject profiling instrumentation
   - Configure profilers (cProfile, memory_profiler, py-spy)
   - Set sampling rate and duration

2. **Execute Target**:
   - Run function/endpoint/test
   - Collect profiling data
   - Monitor resource usage

3. **Analyze Results**:
   - Identify hotspots (>10% time)
   - Find memory leaks
   - Detect N+1 queries
   - Analyze I/O bottlenecks

4. **Generate Report**:
   - Performance metrics
   - Bottleneck analysis
   - Optimization suggestions
   - Flame graphs

5. **Compare Baseline**:
   - Load previous profile from GAM
   - Calculate performance delta
   - Detect regressions

## Profile Types

### CPU Profiling
- Function call times
- Call counts
- Hotspot identification
- Flame graph generation

### Memory Profiling
- Memory allocation
- Memory leaks
- Peak memory usage
- Object lifecycle

### I/O Profiling
- File operations
- Network requests
- Database queries
- Blocking operations

### Database Profiling
- Query execution time
- N+1 query detection
- Missing indexes
- Query optimization

## Performance Report Format

```markdown
# Performance Profile Report

## Summary
**Target**: `app.services.user.get_user_profile`
**Duration**: 10.0 seconds
**Total Calls**: 1,247
**Total Time**: 8.3 seconds
**Peak Memory**: 145 MB

## 🔥 Hotspots (Top 5)

### 1. Database Query (45.2% of time)
**Function**: `sqlalchemy.engine.execute`
**Time**: 3.75s (45.2%)
**Calls**: 1,247
**Avg**: 3.0ms per call

**Issue**: N+1 query problem
**Current Code**:
```python
for user in users:
    user.posts  # Lazy load - triggers query per user
```

**Optimized**:
```python
users = db.query(User).options(selectinload(User.posts)).all()
# Single query with JOIN
```

**Expected Improvement**: 95% faster (3.75s → 0.2s)

### 2. JSON Serialization (18.3% of time)
**Function**: `json.dumps`
**Time**: 1.52s (18.3%)
**Calls**: 1,247

**Issue**: Serializing large objects repeatedly
**Optimization**: Use `orjson` (5-10x faster)

### 3. Password Hashing (12.1% of time)
**Function**: `bcrypt.hashpw`
**Time**: 1.00s (12.1%)
**Calls**: 89

**Issue**: Using max rounds (15)
**Optimization**: Reduce to 12 rounds (still secure, 2x faster)

## 💾 Memory Analysis

**Peak Usage**: 145 MB
**Baseline**: 45 MB
**Growth**: +100 MB

### Memory Hotspots

1. **Large List Accumulation** (85 MB)
   - Line 42: `results = [process(item) for item in large_list]`
   - **Fix**: Use generator: `(process(item) for item in large_list)`

2. **Cached Objects** (15 MB)
   - Line 67: Cache never expires
   - **Fix**: Add TTL or LRU eviction

## 🗄️ Database Performance

**Total Queries**: 1,258
**Total Time**: 3.85s
**Slowest Query**: 250ms

### Query Analysis

| Query | Count | Total Time | Avg Time | Issue |
|-------|-------|------------|----------|-------|
| SELECT users | 1,247 | 3.75s | 3.0ms | N+1 problem |
| SELECT posts | 1 | 0.08s | 80ms | Missing index |
| UPDATE user | 10 | 0.02s | 2ms | OK |

### Recommendations

1. **Add Index**:
   ```sql
   CREATE INDEX idx_posts_user_id ON posts(user_id);
   ```
   Expected: 80ms → 5ms

2. **Use Eager Loading**:
   ```python
   .options(selectinload(User.posts))
   ```
   Expected: 1,247 queries → 2 queries

## 🔧 Optimization Opportunities

### High Impact (>20% improvement)

1. **Fix N+1 Queries** → 45% faster
2. **Use orjson** → 15% faster
3. **Add Database Index** → 10% faster

**Total Expected Improvement**: 70% faster (8.3s → 2.5s)

### Medium Impact (5-20% improvement)

4. **Reduce bcrypt rounds** → 6% faster
5. **Use generators** → 5% faster

### Low Impact (<5% improvement)

6. **Cache repeated calculations** → 2% faster

## 📊 Flame Graph

[Flame graph visualization would be embedded here]

## 📈 Performance Comparison

| Metric | Before | After (Projected) | Improvement |
|--------|--------|-------------------|-------------|
| Total Time | 8.3s | 2.5s | 70% faster |
| Memory | 145 MB | 60 MB | 59% less |
| Queries | 1,258 | 11 | 99% fewer |
| Throughput | 150 req/s | 500 req/s | 233% more |

## 🎯 Action Plan

1. **Immediate** (High Impact):
   ```bash
   # Add database index
   uv run alembic revision --autogenerate -m "Add posts user_id index"

   # Fix N+1 queries
   # Apply code changes from Hotspot #1
   ```

2. **Short-term** (Medium Impact):
   ```bash
   # Switch to orjson
   uv add orjson

   # Reduce bcrypt rounds
   # Update config: BCRYPT_ROUNDS = 12
   ```

3. **Long-term** (Optimization):
   - Implement caching layer (Redis)
   - Consider pagination for large result sets
   - Add query result caching

## 📝 Notes

- Profile saved to GAM for future comparison
- Re-run after optimizations to measure improvement
- Consider load testing with realistic data volumes
```

## Best Practices

- Profile before optimizing
- Focus on high-impact bottlenecks first
- Measure after each optimization
- Compare against baseline
- Profile with realistic data
- Consider production workloads
- Save profiles for regression detection

## Integration

### Pytest Plugin
```python
@pytest.mark.profile
def test_expensive_operation():
    # Automatically profiled
    pass
```

### API Middleware
```python
# Auto-profile slow endpoints (>1s)
app.add_middleware(ProfilerMiddleware, threshold=1.0)
```

### CI/CD Performance Tests
```yaml
- name: Performance Regression Check
  run: uv run python -m app.tools.performance_profiler --compare-baseline
```

## Related Commands

- `/debug-assistant` - Debug performance issues
- `/code-review` - Review for performance anti-patterns
- `/refactor-batch` - Apply performance optimizations
