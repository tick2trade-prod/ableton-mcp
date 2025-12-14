# Feature Design: Context Caching Agent

**Feature ID**: 11
**Priority**: P0 (Critical)
**Impact**: Token Reduction (50%), Latency Reduction (30%)
**Complexity**: Medium (3-5 days)

---

## Problem Statement

Current implementation has severe token waste due to redundant research operations:
- `GAMMemoryManager.research()` called 3-5 times per workflow
- Each call re-queries memory stores with overlapping queries
- `CodeGenerator.generate()` calls research() before every generation
- No caching between workflow phases
- Estimated waste: **50-70% of total tokens**

### Current Flow (Wasteful)
```
Research Phase: GAM research (500 tokens)
  ↓
Plan Phase: GAM research again (500 tokens) ← DUPLICATE
  ↓
Implementation: GAM research (500 tokens) ← DUPLICATE
  ↓
Code Generation: research() before gen (500 tokens) ← DUPLICATE

Total: 2000 tokens (should be 500)
```

---

## Proposed Solution

Create a **Context Caching Agent** that:
1. Intercepts all research operations
2. Caches results by content hash
3. Serves cached results for identical/similar queries
4. Invalidates cache when memory is updated
5. Tracks cache hits for observability

---

## Architecture

### New Agent: `ContextCachingAgent`

**Location**: `app/server/agents/context_cache_agent.py`

**Responsibilities**:
- Maintain in-memory LRU cache of research results
- Hash query text + parameters to generate cache keys
- Intercept `GAMMemoryManager.research()` calls
- Provide cache statistics and hit rate metrics

**Key Methods**:
```python
class ContextCachingAgent:
    async def get_or_research(
        self,
        query: str,
        max_iters: int = 5,
        cache_ttl: int = 3600
    ) -> ResearchResult:
        """Get cached result or perform research."""
        cache_key = self._hash_query(query, max_iters)

        if cached := self._get_from_cache(cache_key):
            return cached

        result = await self.gam.research(query, max_iters)
        self._put_in_cache(cache_key, result, ttl=cache_ttl)
        return result

    def invalidate_pattern(self, pattern: str):
        """Invalidate cache entries matching pattern."""
        # For when memory is updated

    def get_stats(self) -> CacheStats:
        """Return cache hit rate and savings."""
```

---

## Integration Points

### 1. Wrap `GAMMemoryManager`

**Current**: Direct calls to `gam.research()`
```python
# app/research/autonomous_research.py
gam = GAMMemoryManager()
result = gam.research(query, max_iters=5)
```

**New**: Through caching agent
```python
# app/research/autonomous_research.py
cache_agent = ContextCachingAgent()
result = await cache_agent.get_or_research(query, max_iters=5)
```

### 2. Intercept in Tools

**Update**: `app/server/tools/gam_tool.py`
```python
async def research_memory(query: str) -> str:
    cache_agent = get_cache_agent()  # Singleton
    result = await cache_agent.get_or_research(query)
    return result
```

### 3. Update CodeGenerator

**Update**: `app/generation/code_generator.py`
```python
def generate(self, prompt: str, context_query: str = None):
    if context_query:
        # Old: context = self.gam.research(context_query)
        context = await self.cache_agent.get_or_research(context_query)
```

---

## Cache Strategy

### Cache Key Generation
```python
def _hash_query(self, query: str, max_iters: int) -> str:
    """Generate deterministic cache key."""
    content = f"{query}::{max_iters}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]
```

### Cache Storage
```python
class CacheEntry:
    key: str
    result: ResearchResult
    timestamp: float
    ttl: int
    hit_count: int
```

**Storage Options**:
1. **In-Memory** (Phase 1): `dict` with LRU eviction
2. **Redis** (Phase 2): Persistent cache across restarts
3. **File-Based** (Fallback): JSON files in `.cursor/cache/context/`

### TTL Strategy
```python
# Different TTLs for different query types
CACHE_TTL_CONFIG = {
    "research": 3600,      # 1 hour
    "codebase": 1800,      # 30 minutes (code changes)
    "workflow": 7200,      # 2 hours (longer lived)
    "external_api": 300,   # 5 minutes (fresh data)
}
```

### Invalidation Rules
```python
# Invalidate when:
1. Memory is updated (new documents added)
2. TTL expires
3. Manual flush (testing)
4. Cache size exceeds limit (LRU eviction)
```

---

## Data Model

### CacheStats
```python
@dataclass
class CacheStats:
    total_requests: int
    cache_hits: int
    cache_misses: int
    hit_rate: float
    tokens_saved: int
    latency_saved_ms: float
```

### CacheMetrics (for observability)
```python
@dataclass
class CacheMetrics:
    timestamp: datetime
    cache_size: int
    memory_usage_mb: float
    avg_ttl_remaining: float
    top_queries: list[str]  # Most cached queries
```

---

## Performance Impact

### Token Savings
```
Without Cache:
- Research Phase: 500 tokens
- Plan Phase: 500 tokens
- Implementation: 500 tokens
- Code Gen: 500 tokens
Total: 2000 tokens

With Cache:
- Research Phase: 500 tokens (cache miss)
- Plan Phase: 0 tokens (cache hit)
- Implementation: 0 tokens (cache hit)
- Code Gen: 0 tokens (cache hit)
Total: 500 tokens

Savings: 75%
```

### Latency Savings
```
Without Cache:
- Each research: 2-5 seconds
- Total: 8-20 seconds

With Cache:
- First research: 2-5 seconds
- Cache hits: <10ms
- Total: 2-5 seconds

Savings: 60-75%
```

---

## Implementation Plan

### Phase 1: Core Caching (2 days)
1. Create `ContextCachingAgent` class
2. Implement in-memory LRU cache
3. Add cache key hashing
4. Basic TTL support
5. Unit tests

### Phase 2: Integration (1 day)
1. Update `GAMMemoryManager` wrapper
2. Update `gam_tool.py`
3. Update `CodeGenerator`
4. Update `AutonomousResearcher`
5. Integration tests

### Phase 3: Observability (1 day)
1. Add cache statistics
2. Telemetry integration
3. Cache hit rate metrics
4. Token savings tracking
5. Dashboard (optional)

### Phase 4: Advanced Features (1 day)
1. Redis backend (optional)
2. File-based persistence
3. Cache warming
4. Similarity-based caching
5. Pattern invalidation

---

## Dependencies

**Required**:
- `app/core/gam_memory.py` - To wrap
- `app/server/tools/gam_tool.py` - To update
- `app/generation/code_generator.py` - To update

**Optional**:
- `redis-py` - For persistent cache
- `cachetools` - For LRU implementation

---

## Testing Strategy

### Unit Tests
```python
def test_cache_miss_performs_research():
    agent = ContextCachingAgent()
    result = await agent.get_or_research("test query")
    assert result is not None
    assert agent.get_stats().cache_hits == 0

def test_cache_hit_reuses_result():
    agent = ContextCachingAgent()
    result1 = await agent.get_or_research("test query")
    result2 = await agent.get_or_research("test query")
    assert result1 == result2
    assert agent.get_stats().cache_hits == 1

def test_ttl_expiration():
    agent = ContextCachingAgent()
    await agent.get_or_research("query", cache_ttl=1)
    time.sleep(2)
    await agent.get_or_research("query")
    assert agent.get_stats().cache_misses == 2
```

### Integration Tests
```python
def test_workflow_uses_cache():
    stats_before = cache_agent.get_stats()
    orchestrator.execute_workflow("test feature")
    stats_after = cache_agent.get_stats()
    assert stats_after.tokens_saved > 1000
```

---

## Risks & Mitigations

### Risk 1: Stale Cache
**Mitigation**:
- Short TTLs (1 hour default)
- Invalidate on memory updates
- Manual flush command

### Risk 2: Memory Bloat
**Mitigation**:
- LRU eviction (max 1000 entries)
- Memory usage monitoring
- Configurable cache size limit

### Risk 3: Cache Key Collisions
**Mitigation**:
- SHA256 hashing
- Include all parameters in key
- Collision detection

---

## Success Metrics

**Must Have**:
- ✅ 50%+ token reduction in workflows
- ✅ 30%+ latency reduction
- ✅ 80%+ cache hit rate (after warmup)
- ✅ <10ms cache lookup time

**Nice to Have**:
- 📊 Dashboard showing cache stats
- 📈 Token cost savings over time
- 🎯 Per-query cache hit rates

---

## Alternatives Considered

### Alternative 1: Memoization Decorator
**Pros**: Simple, no new agent
**Cons**: No TTL, no invalidation, no observability
**Decision**: Rejected - insufficient control

### Alternative 2: Redis-Only Caching
**Pros**: Persistent, scalable
**Cons**: External dependency, overkill for single-user
**Decision**: Phase 2 feature

### Alternative 3: No Caching
**Pros**: Simple
**Cons**: 50% token waste, slow
**Decision**: Rejected - unacceptable performance

---

## Related Features

- Feature 13: Smart Context Assembler (uses this)
- Feature 14: Semantic Code Search (caches embeddings)
- Observability system (telemetry integration)

---

**Status**: Ready for Implementation
**Assigned**: TBD
**Target Release**: v2.1
