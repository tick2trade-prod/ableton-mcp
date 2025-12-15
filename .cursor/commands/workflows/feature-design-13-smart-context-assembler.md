# Feature Design: Smart Context Assembler

**Feature ID**: 13
**Priority**: P1 (High)
**Impact**: Token Reduction (30%), Latency Improvement (15%), Quality Improvement (10%)
**Complexity**: Medium-High (4-6 days)

---

## Problem Statement

Current context retrieval is inefficient:
- `ContextManager` retrieves ALL context for a query
- No filtering or relevance scoring
- Sends 5-10K tokens when only 1-2K are relevant
- Wastes tokens on irrelevant code/docs
- Increases latency due to larger prompts

### Current Inefficient Flow
```python
# app/server/services/context_manager.py
async def assemble_context(query: str) -> str:
    """Returns ALL research results, all code files, all docs."""
    research = await gam.research(query, max_iters=5)  # All 5 iterations
    code = await self._get_all_related_code(query)      # All matches
    docs = await self._get_all_docs(query)              # All docs

    # Concatenates everything - often 8-12K tokens
    return f"{research}\n\n{code}\n\n{docs}"
```

**Problem**: For a query like "implement user authentication":
- Retrieves 12 research articles (8K tokens)
- Includes 20 code files (4K tokens)
- Adds 15 doc pages (3K tokens)
- **Total: 15K tokens sent to LLM**
- **Only ~3K tokens are actually relevant**
- **80% token waste**

---

## Proposed Solution

Create a **Smart Context Assembler** that:
1. Computes relevance scores for each context chunk
2. Ranks chunks by relevance
3. Selects top N chunks that fit within budget
4. Returns minimal, highly relevant context
5. Tracks what was included/excluded for debugging

---

## Architecture

### New Agent: `SmartContextAssembler`

**Location**: `app/server/agents/context_assembler.py`

**Responsibilities**:
- Compute relevance scores using embeddings or TF-IDF
- Rank context chunks by score
- Apply token budget constraints
- Assemble minimal context within budget
- Track and log selection decisions

**Key Methods**:
```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class ContextChunk:
    """A piece of context with metadata."""
    content: str
    source: str  # "research", "code", "docs"
    relevance_score: float
    token_count: int
    metadata: dict[str, Any]

@dataclass
class ContextBudget:
    """Token budget allocation."""
    total: int = 8000
    research: int = 3000
    code: int = 3000
    docs: int = 2000

class SmartContextAssembler:
    def __init__(self, embedding_model: str = "text-embedding-ada-002"):
        self.embeddings = EmbeddingModel(embedding_model)
        self.cache = {}

    async def assemble_smart_context(
        self,
        query: str,
        budget: ContextBudget = ContextBudget(),
        min_relevance: float = 0.3
    ) -> tuple[str, dict[str, Any]]:
        """Assemble minimal, relevant context within budget.

        Returns:
            (context_str, metadata) where metadata includes:
            - selected_chunks: list of ContextChunk
            - excluded_chunks: list of ContextChunk
            - total_tokens_used: int
            - relevance_distribution: dict
        """
        # Step 1: Retrieve all candidate chunks
        candidates = await self._get_all_candidates(query)

        # Step 2: Compute relevance scores
        query_embedding = await self.embeddings.embed(query)
        for chunk in candidates:
            chunk.relevance_score = await self._compute_relevance(
                query_embedding,
                chunk
            )

        # Step 3: Filter by min relevance
        relevant = [c for c in candidates if c.relevance_score >= min_relevance]

        # Step 4: Rank by relevance
        ranked = sorted(relevant, key=lambda c: c.relevance_score, reverse=True)

        # Step 5: Select within budget
        selected = self._select_within_budget(ranked, budget)

        # Step 6: Assemble context string
        context = self._format_context(selected)

        # Step 7: Build metadata
        metadata = self._build_metadata(selected, candidates)

        return context, metadata

    async def _get_all_candidates(self, query: str) -> list[ContextChunk]:
        """Retrieve all potential context chunks."""
        chunks = []

        # Research chunks
        research_results = await gam.research(query, max_iters=3)
        chunks.extend(self._chunk_research(research_results))

        # Code chunks
        code_files = await self._find_relevant_code(query)
        chunks.extend(self._chunk_code(code_files))

        # Doc chunks
        docs = await self._find_relevant_docs(query)
        chunks.extend(self._chunk_docs(docs))

        return chunks

    async def _compute_relevance(
        self,
        query_embedding: list[float],
        chunk: ContextChunk
    ) -> float:
        """Compute cosine similarity between query and chunk."""
        # Cache chunk embeddings
        cache_key = hashlib.sha256(chunk.content.encode()).hexdigest()
        if cache_key in self.cache:
            chunk_embedding = self.cache[cache_key]
        else:
            chunk_embedding = await self.embeddings.embed(chunk.content)
            self.cache[cache_key] = chunk_embedding

        # Cosine similarity
        similarity = self._cosine_similarity(query_embedding, chunk_embedding)

        # Boost based on source type and metadata
        boosted = self._apply_boosts(similarity, chunk)

        return boosted

    def _select_within_budget(
        self,
        ranked: list[ContextChunk],
        budget: ContextBudget
    ) -> list[ContextChunk]:
        """Greedily select chunks within budget constraints."""
        selected = []
        used = {"research": 0, "code": 0, "docs": 0}

        for chunk in ranked:
            source = chunk.source
            if used[source] + chunk.token_count <= budget.__dict__[source]:
                selected.append(chunk)
                used[source] += chunk.token_count

        return selected
```

---

## Use Cases

### Use Case 1: User Authentication Implementation

**Before (Context Manager)**:
```python
context = await context_manager.assemble_context("implement user authentication")
# Returns: 15K tokens (all research, all code, all docs)
```

**After (Smart Context Assembler)**:
```python
assembler = SmartContextAssembler()
context, metadata = await assembler.assemble_smart_context(
    query="implement user authentication",
    budget=ContextBudget(total=5000, research=2000, code=2000, docs=1000)
)
# Returns: 5K tokens (top-ranked, highly relevant)
# metadata shows what was selected/excluded and why

print(f"Selected {len(metadata['selected_chunks'])} chunks")
print(f"Excluded {len(metadata['excluded_chunks'])} low-relevance chunks")
print(f"Token usage: {metadata['total_tokens_used']}/5000")
```

**Benefit**: 67% token reduction (15K → 5K), 40% latency reduction

### Use Case 2: Bug Fix with Minimal Context

**Problem**: Fixing a specific bug doesn't need entire codebase

**Before**:
```python
# Returns 10K tokens of loosely related code
context = await context_manager.assemble_context("fix null pointer in login")
```

**After**:
```python
context, metadata = await assembler.assemble_smart_context(
    query="fix null pointer in login",
    budget=ContextBudget(total=2000, code=1500, research=500),
    min_relevance=0.5  # Higher threshold for bug fixes
)
# Returns: 2K tokens (just the login module + relevant fixes)
```

**Benefit**: 80% token reduction (10K → 2K), faster response

### Use Case 3: Research-Heavy Task

**Problem**: Some tasks need more research, less code

**After**:
```python
# Allocate budget based on task type
context, metadata = await assembler.assemble_smart_context(
    query="research modern authentication patterns",
    budget=ContextBudget(total=8000, research=6000, code=1000, docs=1000)
)
# Prioritizes research over code
```

**Benefit**: Dynamic budget allocation based on task

### Use Case 4: Debugging Selection

**Problem**: Need to understand why certain context was/wasn't included

**After**:
```python
context, metadata = await assembler.assemble_smart_context(query)

# Inspect selection decisions
for chunk in metadata['selected_chunks']:
    print(f"✅ {chunk.source}: {chunk.relevance_score:.2f} - {chunk.metadata['title']}")

for chunk in metadata['excluded_chunks'][:10]:
    print(f"❌ {chunk.source}: {chunk.relevance_score:.2f} - {chunk.metadata['title']}")

# Output:
# ✅ research: 0.87 - JWT Authentication Best Practices
# ✅ code: 0.82 - app/server/auth/jwt_handler.py
# ✅ docs: 0.79 - Authentication Architecture
# ❌ research: 0.25 - Database Connection Pooling
# ❌ code: 0.22 - app/utils/string_helpers.py
```

---

## Relevance Scoring Strategy

### 1. Embedding-Based Similarity (Primary)

```python
async def _compute_embedding_relevance(
    query_embedding: list[float],
    chunk: ContextChunk
) -> float:
    """Cosine similarity between query and chunk embeddings."""
    chunk_embedding = await self.embeddings.embed(chunk.content)
    return cosine_similarity(query_embedding, chunk_embedding)
```

**Pros**:
- Captures semantic similarity
- Works with synonyms and related concepts
- Language model quality

**Cons**:
- Requires embedding API calls (cost/latency)
- Needs caching

### 2. TF-IDF Fallback (Fast)

```python
def _compute_tfidf_relevance(query: str, chunk: ContextChunk) -> float:
    """TF-IDF-based relevance for fast offline scoring."""
    query_terms = set(query.lower().split())
    chunk_terms = set(chunk.content.lower().split())

    intersection = query_terms & chunk_terms
    union = query_terms | chunk_terms

    return len(intersection) / len(union) if union else 0.0
```

**Pros**:
- No API calls
- Very fast
- No caching needed

**Cons**:
- Misses semantic relationships
- Keyword-based only

### 3. Hybrid Approach (Recommended)

```python
async def _compute_relevance(
    query_embedding: list[float],
    chunk: ContextChunk
) -> float:
    """Hybrid: embeddings + TF-IDF + boosts."""

    # Embedding similarity (0-1)
    embedding_score = await self._compute_embedding_relevance(
        query_embedding,
        chunk
    )

    # TF-IDF similarity (0-1)
    tfidf_score = self._compute_tfidf_relevance(query, chunk)

    # Weighted combination
    base_score = 0.7 * embedding_score + 0.3 * tfidf_score

    # Apply boosts
    boosted_score = self._apply_boosts(base_score, chunk)

    return boosted_score

def _apply_boosts(self, score: float, chunk: ContextChunk) -> float:
    """Apply heuristic boosts based on metadata."""
    multiplier = 1.0

    # Boost recent code changes
    if chunk.metadata.get("recently_modified"):
        multiplier *= 1.2

    # Boost code with matching keywords in filename
    if chunk.source == "code" and self._filename_matches_query(chunk):
        multiplier *= 1.15

    # Boost docs with "best practices" or "guide"
    if chunk.source == "docs" and any(
        kw in chunk.content.lower() for kw in ["best practice", "guide", "how to"]
    ):
        multiplier *= 1.1

    # Penalize very long chunks (likely less focused)
    if chunk.token_count > 2000:
        multiplier *= 0.9

    return min(score * multiplier, 1.0)
```

---

## Budget Management

### Dynamic Budget Allocation

```python
@dataclass
class TaskType:
    """Task type determines budget allocation."""
    name: str
    research_ratio: float
    code_ratio: float
    docs_ratio: float

TASK_TYPES = {
    "feature": TaskType("feature", research_ratio=0.3, code_ratio=0.5, docs_ratio=0.2),
    "bugfix": TaskType("bugfix", research_ratio=0.1, code_ratio=0.8, docs_ratio=0.1),
    "research": TaskType("research", research_ratio=0.7, code_ratio=0.1, docs_ratio=0.2),
    "refactor": TaskType("refactor", research_ratio=0.2, code_ratio=0.6, docs_ratio=0.2),
}

def create_budget_for_task(
    task_type: str,
    total_budget: int = 8000
) -> ContextBudget:
    """Create budget based on task type."""
    task = TASK_TYPES[task_type]
    return ContextBudget(
        total=total_budget,
        research=int(total_budget * task.research_ratio),
        code=int(total_budget * task.code_ratio),
        docs=int(total_budget * task.docs_ratio),
    )
```

### Usage:
```python
# Feature development - needs balanced context
budget = create_budget_for_task("feature", total_budget=8000)
# ContextBudget(total=8000, research=2400, code=4000, docs=1600)

# Bug fix - needs mostly code
budget = create_budget_for_task("bugfix", total_budget=5000)
# ContextBudget(total=5000, research=500, code=4000, docs=500)
```

---

## Integration Points

### 1. Update CodeGenerator

**Before**:
```python
# app/generation/code_generator.py
async def generate(self, prompt: str) -> str:
    context = await context_manager.assemble_context(prompt)  # 15K tokens
    return await self._generate_with_context(prompt, context)
```

**After**:
```python
async def generate(self, prompt: str) -> str:
    assembler = SmartContextAssembler()
    context, metadata = await assembler.assemble_smart_context(
        query=prompt,
        budget=create_budget_for_task("feature")
    )

    # Log selection for debugging
    logger.info(f"Selected {len(metadata['selected_chunks'])} chunks, "
                f"used {metadata['total_tokens_used']} tokens")

    return await self._generate_with_context(prompt, context)
```

### 2. Update ContextManager

**Make it use SmartContextAssembler by default**:
```python
# app/server/services/context_manager.py
class ContextManager:
    def __init__(self):
        self.assembler = SmartContextAssembler()

    async def assemble_context(
        self,
        query: str,
        smart: bool = True,  # New flag
        budget: ContextBudget | None = None
    ) -> str:
        if not smart:
            # Legacy behavior
            return await self._assemble_all_context(query)

        # Smart assembly
        context, metadata = await self.assembler.assemble_smart_context(
            query=query,
            budget=budget or ContextBudget()
        )
        return context
```

### 3. Add to Orchestrator

**New workflow parameter**:
```python
# app/server/orchestrator.py
async def execute_workflow(
    feature_name: str,
    task_type: str = "feature",  # New parameter
    context_budget: int = 8000    # New parameter
) -> WorkflowResult:
    budget = create_budget_for_task(task_type, context_budget)

    # Pass budget to all phases
    context = await context_manager.assemble_context(
        query=feature_name,
        smart=True,
        budget=budget
    )
```

---

## Caching Strategy

### Embedding Cache

```python
class EmbeddingCache:
    """LRU cache for chunk embeddings."""

    def __init__(self, max_size: int = 1000):
        self.cache: OrderedDict[str, list[float]] = OrderedDict()
        self.max_size = max_size

    def get(self, content_hash: str) -> list[float] | None:
        if content_hash in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(content_hash)
            return self.cache[content_hash]
        return None

    def put(self, content_hash: str, embedding: list[float]) -> None:
        if content_hash in self.cache:
            self.cache.move_to_end(content_hash)
        else:
            if len(self.cache) >= self.max_size:
                # Remove least recently used
                self.cache.popitem(last=False)
            self.cache[content_hash] = embedding
```

**Benefits**:
- Avoids re-embedding same chunks
- 90%+ hit rate for common queries
- Reduces embedding API calls by 80%

---

## Performance Metrics

### Expected Improvements

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Avg Context Tokens** | 12K | 5K | **58% reduction** |
| **Context Assembly Time** | 2.5s | 1.8s | **28% faster** |
| **LLM Response Time** | 8s | 5s | **37% faster** |
| **Total Latency** | 10.5s | 6.8s | **35% reduction** |
| **Cost per Query** | $0.12 | $0.05 | **58% reduction** |

### Token Distribution

**Before (Context Manager)**:
```
Total: 12,000 tokens
├─ Research: 6,000 tokens (50%)
├─ Code:     4,000 tokens (33%)
└─ Docs:     2,000 tokens (17%)

Relevance:
├─ High (>0.7):   2,000 tokens (17%)
├─ Medium (0.4-0.7): 4,000 tokens (33%)
└─ Low (<0.4):    6,000 tokens (50%) ← WASTED
```

**After (Smart Context Assembler)**:
```
Total: 5,000 tokens
├─ Research: 2,000 tokens (40%)
├─ Code:     2,000 tokens (40%)
└─ Docs:     1,000 tokens (20%)

Relevance:
├─ High (>0.7):   3,500 tokens (70%)
├─ Medium (0.4-0.7): 1,500 tokens (30%)
└─ Low (<0.4):        0 tokens (0%)
```

---

## Implementation Plan

### Phase 1: Core Assembler (2 days)
1. Create `SmartContextAssembler` class
2. Implement embedding-based relevance scoring
3. Add budget-constrained selection
4. Basic metadata tracking
5. Unit tests

### Phase 2: Chunking & Scoring (1.5 days)
1. Implement research chunking
2. Implement code chunking (by function/class)
3. Implement doc chunking (by section)
4. Add TF-IDF fallback
5. Add boost heuristics

### Phase 3: Integration (1.5 days)
1. Update `ContextManager` with smart mode
2. Update `CodeGenerator` to use smart assembly
3. Add task-type-based budgets
4. Integration tests

### Phase 4: Optimization (1 day)
1. Add embedding cache
2. Optimize chunking performance
3. Add observability (metrics, logging)
4. Performance benchmarks

---

## Testing Strategy

### Unit Tests

```python
def test_relevance_scoring():
    assembler = SmartContextAssembler()
    query_emb = [0.1, 0.2, 0.3]

    high_relevance = ContextChunk(
        content="JWT authentication implementation guide",
        source="docs",
        token_count=500,
        metadata={}
    )

    low_relevance = ContextChunk(
        content="Database connection pool configuration",
        source="code",
        token_count=300,
        metadata={}
    )

    high_score = await assembler._compute_relevance(query_emb, high_relevance)
    low_score = await assembler._compute_relevance(query_emb, low_relevance)

    assert high_score > 0.7
    assert low_score < 0.3
    assert high_score > low_score

def test_budget_constraints():
    assembler = SmartContextAssembler()

    chunks = [
        ContextChunk("chunk1", "research", 0.9, 1000, {}),
        ContextChunk("chunk2", "research", 0.8, 1500, {}),  # Should be skipped (exceeds budget)
        ContextChunk("chunk3", "code", 0.85, 1200, {}),
    ]

    budget = ContextBudget(total=5000, research=1000, code=2000)
    selected = assembler._select_within_budget(chunks, budget)

    assert len(selected) == 2
    assert selected[0].content == "chunk1"
    assert selected[1].content == "chunk3"
```

### Integration Tests

```python
@pytest.mark.integration
async def test_end_to_end_assembly():
    assembler = SmartContextAssembler()

    context, metadata = await assembler.assemble_smart_context(
        query="implement user authentication",
        budget=ContextBudget(total=5000)
    )

    # Verify token budget respected
    assert metadata['total_tokens_used'] <= 5000

    # Verify relevance threshold
    for chunk in metadata['selected_chunks']:
        assert chunk.relevance_score >= 0.3

    # Verify all sources represented
    sources = {c.source for c in metadata['selected_chunks']}
    assert "research" in sources
    assert "code" in sources
```

---

## Risks & Mitigations

### Risk 1: Embedding API Costs
**Problem**: Embedding every chunk is expensive
**Mitigation**:
- LRU cache with 90%+ hit rate
- TF-IDF fallback for quick scoring
- Batch embedding requests

### Risk 2: Relevance Scoring Accuracy
**Problem**: May exclude important context
**Mitigation**:
- Hybrid scoring (embeddings + TF-IDF + boosts)
- Metadata tracking for debugging
- Min relevance threshold tunable per task
- Fall back to Context Manager if quality degrades

### Risk 3: Chunking Overhead
**Problem**: Splitting content takes time
**Mitigation**:
- Cache chunks with content hash
- Parallel chunking
- Lazy chunking (on-demand)

---

## Success Metrics

**Must Have**:
- ✅ 30%+ token reduction vs Context Manager
- ✅ Maintains code quality (no degradation)
- ✅ 15%+ latency improvement
- ✅ Respects budget constraints

**Nice to Have**:
- 📊 Embedding cache hit rate >85%
- 🎯 Relevance scores correlate with human judgment
- 🔄 Automatic budget tuning based on task type

---

## Alternatives Considered

### Alternative 1: Rule-Based Filtering
**Pros**: Simple, no embeddings needed
**Cons**: Misses semantic relationships
**Decision**: Rejected - too brittle

### Alternative 2: LLM-Based Selection
**Pros**: Very accurate relevance
**Cons**: Slow, expensive (LLM call per chunk)
**Decision**: Rejected - defeats purpose of optimization

### Alternative 3: Pre-Computed Indexes
**Pros**: Very fast lookup
**Cons**: Requires offline indexing, stale data
**Decision**: Maybe later for read-heavy workloads

---

## Related Features

- Feature 11: Context Caching Agent (provides cached research)
- Feature 12: Batch Processing Agent (parallel chunking)
- Observability (track selection decisions)

---

**Status**: Ready for Implementation
**Assigned**: TBD
**Target Release**: v2.2
