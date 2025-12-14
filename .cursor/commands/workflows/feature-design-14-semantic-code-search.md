# Feature Design: Semantic Code Search Agent

**Feature ID**: 14
**Priority**: P1 (High)
**Impact**: Quality Improvement (30%), Latency Reduction (20%), Token Efficiency (15%)
**Complexity**: High (6-8 days)

---

## Problem Statement

Current code search is text-based and inefficient:
- Uses simple `grep` and `glob` for code discovery
- Misses semantic relationships between code
- Returns many false positives (keyword matches)
- Requires multiple search iterations
- Wastes tokens on irrelevant code files

### Current Text-Based Search Flow

```python
# app/server/tools/coder_tool.py
async def find_relevant_code(query: str) -> list[Path]:
    """Text-based search - misses semantics."""

    # Keyword search - literal matches only
    files = subprocess.check_output(
        ["grep", "-r", "-l", query, "app/"],
        text=True
    ).split()

    return [Path(f) for f in files]
```

**Problems**:

1. **Misses Semantic Matches**:
   - Query: "authentication handler"
   - Misses: `verify_user_credentials()` (semantically related but no keyword match)
   - Returns: `auth_handler.py` but not functionally similar `jwt_validator.py`

2. **Too Many False Positives**:
   - Query: "cache"
   - Returns: 47 files (comments, variable names, actual cache implementations)
   - Only 3-5 are actually relevant
   - Wastes time reviewing 40+ false positives

3. **Requires Multiple Iterations**:
   - First search: too broad or too narrow
   - Manual refinement: adjust keywords
   - Second search: still not right
   - Typical: 3-5 search iterations per task

4. **No Code Understanding**:
   - Searches text, not structure
   - Can't find "similar functions"
   - Can't understand "what this does"
   - No AST awareness

---

## Proposed Solution

Create a **Semantic Code Search Agent** that:
1. Indexes codebase with AST parsing
2. Generates embeddings for code chunks
3. Supports semantic queries ("functions that validate input")
4. Returns ranked results by relevance
5. Provides code structure metadata

---

## Architecture

### New Agent: `SemanticCodeSearchAgent`

**Location**: `app/server/agents/semantic_search.py`

**Responsibilities**:
- Build and maintain code index (AST + embeddings)
- Parse semantic queries
- Rank results by semantic similarity
- Extract code metadata (signatures, docstrings)
- Provide explanations for why code matched

**Key Components**:

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class CodeChunk:
    """A searchable code element."""
    file_path: Path
    chunk_type: Literal["function", "class", "method", "module"]
    name: str
    signature: str
    docstring: str | None
    code: str
    start_line: int
    end_line: int
    imports: list[str]
    calls: list[str]
    embedding: list[float] | None = None

@dataclass
class SearchResult:
    """A search result with relevance score."""
    chunk: CodeChunk
    relevance_score: float
    explanation: str
    snippet: str

class SemanticCodeSearchAgent:
    """Semantic code search with AST parsing and embeddings."""

    def __init__(
        self,
        project_root: Path,
        embedding_model: str = "text-embedding-ada-002",
        index_cache_dir: Path | None = None
    ):
        self.project_root = project_root
        self.embeddings = EmbeddingModel(embedding_model)
        self.cache_dir = index_cache_dir or (project_root / ".cursor" / "cache" / "code_index")
        self.index: dict[str, CodeChunk] = {}

    async def search(
        self,
        query: str,
        limit: int = 10,
        min_relevance: float = 0.3,
        chunk_types: list[str] | None = None
    ) -> list[SearchResult]:
        """Semantic search for code.

        Args:
            query: Natural language or keyword query
            limit: Max results to return
            min_relevance: Minimum similarity score (0-1)
            chunk_types: Filter by ["function", "class", "method", "module"]

        Returns:
            Ranked list of search results with explanations
        """
        # Build index if not exists
        if not self.index:
            await self.build_index()

        # Embed query
        query_embedding = await self.embeddings.embed(query)

        # Compute relevance scores
        candidates = []
        for chunk_id, chunk in self.index.items():
            # Apply filters
            if chunk_types and chunk.chunk_type not in chunk_types:
                continue

            # Compute semantic similarity
            if chunk.embedding is None:
                chunk.embedding = await self.embeddings.embed(
                    self._chunk_to_text(chunk)
                )

            similarity = self._cosine_similarity(query_embedding, chunk.embedding)

            # Apply boosts
            boosted_score = self._apply_boosts(similarity, chunk, query)

            if boosted_score >= min_relevance:
                candidates.append((chunk, boosted_score))

        # Sort by relevance
        candidates.sort(key=lambda x: x[1], reverse=True)

        # Build results with explanations
        results = []
        for chunk, score in candidates[:limit]:
            explanation = self._generate_explanation(chunk, query, score)
            snippet = self._extract_snippet(chunk)

            results.append(SearchResult(
                chunk=chunk,
                relevance_score=score,
                explanation=explanation,
                snippet=snippet
            ))

        return results

    async def build_index(self, force_rebuild: bool = False) -> None:
        """Build code index with AST parsing and embeddings."""

        # Check cache
        cache_file = self.cache_dir / "index.json"
        if cache_file.exists() and not force_rebuild:
            self.index = self._load_index_from_cache(cache_file)
            return

        print("Building code index...")
        chunks = []

        # Find all Python files
        py_files = list(self.project_root.glob("**/*.py"))

        # Parse each file
        for py_file in py_files:
            if self._should_skip(py_file):
                continue

            try:
                file_chunks = await self._parse_file(py_file)
                chunks.extend(file_chunks)
            except Exception as e:
                print(f"Warning: Failed to parse {py_file}: {e}")

        # Generate embeddings in batch
        print(f"Generating embeddings for {len(chunks)} code chunks...")
        chunk_texts = [self._chunk_to_text(c) for c in chunks]
        embeddings = await self.embeddings.embed_batch(chunk_texts)

        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding

        # Build index
        self.index = {self._chunk_id(c): c for c in chunks}

        # Save to cache
        self._save_index_to_cache(cache_file)

        print(f"Index built: {len(self.index)} code chunks")

    async def _parse_file(self, file_path: Path) -> list[CodeChunk]:
        """Parse a Python file into searchable chunks using AST."""
        import ast

        source = file_path.read_text()
        tree = ast.parse(source)

        chunks = []

        # Extract module-level docstring
        module_doc = ast.get_docstring(tree)
        if module_doc:
            chunks.append(CodeChunk(
                file_path=file_path,
                chunk_type="module",
                name=file_path.stem,
                signature="",
                docstring=module_doc,
                code=source[:500],  # First 500 chars
                start_line=1,
                end_line=len(source.split("\n")),
                imports=self._extract_imports(tree),
                calls=[]
            ))

        # Extract classes and functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                chunks.append(self._parse_function(node, file_path, source))

            elif isinstance(node, ast.ClassDef):
                chunks.append(self._parse_class(node, file_path, source))

                # Extract methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        chunks.append(self._parse_method(
                            item, node.name, file_path, source
                        ))

        return chunks

    def _parse_function(
        self,
        node: ast.FunctionDef,
        file_path: Path,
        source: str
    ) -> CodeChunk:
        """Parse function node into CodeChunk."""
        import ast

        signature = self._extract_signature(node)
        docstring = ast.get_docstring(node)
        code = self._extract_source(node, source)
        calls = self._extract_function_calls(node)

        return CodeChunk(
            file_path=file_path,
            chunk_type="function",
            name=node.name,
            signature=signature,
            docstring=docstring,
            code=code,
            start_line=node.lineno,
            end_line=node.end_lineno or node.lineno,
            imports=[],
            calls=calls
        )

    def _apply_boosts(
        self,
        base_score: float,
        chunk: CodeChunk,
        query: str
    ) -> float:
        """Apply heuristic boosts to improve ranking."""
        multiplier = 1.0

        # Boost if name matches query keywords
        query_words = set(query.lower().split())
        name_words = set(chunk.name.lower().replace("_", " ").split())
        if query_words & name_words:
            multiplier *= 1.3

        # Boost if docstring contains query keywords
        if chunk.docstring:
            doc_words = set(chunk.docstring.lower().split())
            if query_words & doc_words:
                multiplier *= 1.2

        # Boost public APIs (no leading underscore)
        if not chunk.name.startswith("_"):
            multiplier *= 1.1

        # Boost recently modified files
        if self._is_recently_modified(chunk.file_path):
            multiplier *= 1.15

        # Penalize test files (unless query mentions "test")
        if "test" in str(chunk.file_path) and "test" not in query.lower():
            multiplier *= 0.7

        return min(base_score * multiplier, 1.0)

    def _generate_explanation(
        self,
        chunk: CodeChunk,
        query: str,
        score: float
    ) -> str:
        """Generate human-readable explanation for why this matched."""
        reasons = []

        # Semantic similarity
        if score > 0.8:
            reasons.append("Strong semantic match")
        elif score > 0.6:
            reasons.append("Good semantic match")
        else:
            reasons.append("Moderate semantic match")

        # Name match
        query_words = set(query.lower().split())
        name_words = set(chunk.name.lower().replace("_", " ").split())
        if query_words & name_words:
            reasons.append(f"Name contains '{' '.join(query_words & name_words)}'")

        # Docstring match
        if chunk.docstring:
            doc_words = set(chunk.docstring.lower().split())
            matches = query_words & doc_words
            if matches:
                reasons.append(f"Docstring mentions {len(matches)} query keywords")

        # Type info
        reasons.append(f"{chunk.chunk_type} in {chunk.file_path.name}")

        return " | ".join(reasons)
```

---

## Use Cases

### Use Case 1: Find Authentication Code

**Before (Text Search)**:
```python
# Keyword search
files = grep -r "auth" app/
# Returns: 47 files (too many, mostly false positives)

# Refine
files = grep -r "authenticate" app/
# Returns: 12 files (still too broad)

# Manual review of 12 files to find 2 relevant ones
```

**After (Semantic Search)**:
```python
search_agent = SemanticCodeSearchAgent(Path("."))

results = await search_agent.search(
    query="authentication and user verification",
    limit=10
)

for result in results:
    print(f"[{result.relevance_score:.2f}] {result.chunk.name} - {result.explanation}")
    print(f"  {result.snippet}\n")

# Output:
# [0.89] verify_user_credentials - Strong semantic match | Name contains 'user' | function in auth.py
#   async def verify_user_credentials(username: str, password: str) -> bool:
#       """Verify user credentials against database."""
#
# [0.85] authenticate_request - Strong semantic match | Name contains 'authenticate' | method in middleware.py
#   async def authenticate_request(self, request: Request) -> User | None:
#       """Authenticate incoming request using JWT token."""
#
# [0.78] validate_jwt_token - Good semantic match | Docstring mentions 3 query keywords | function in jwt.py
#   def validate_jwt_token(token: str) -> dict[str, Any] | None:
#       """Validate JWT token and return payload."""
```

**Benefit**: 1 search instead of 3, 3 relevant results immediately, no manual filtering

### Use Case 2: Find Similar Functions

**Query**: "Find functions similar to `send_email()`"

```python
# First, get the target function
target_code = """
async def send_email(to: str, subject: str, body: str) -> bool:
    '''Send email via SMTP.'''
    # Implementation
"""

results = await search_agent.search(
    query=f"functions that send notifications or messages: {target_code}",
    chunk_types=["function"]
)

# Returns:
# - send_sms()
# - send_slack_notification()
# - send_webhook()
# - push_notification()
```

**Benefit**: Discover similar functionality for refactoring or consistency

### Use Case 3: Find Usage Examples

**Query**: "Show me how to use GAMMemoryManager"

```python
results = await search_agent.search(
    query="code that uses GAMMemoryManager to memorize or research",
    limit=5
)

# Returns functions that:
# - Import GAMMemoryManager
# - Call .memorize() or .research()
# - Show actual usage patterns
```

**Benefit**: Learn API usage from real examples in codebase

### Use Case 4: Architecture Discovery

**Query**: "What are the main orchestration workflows?"

```python
results = await search_agent.search(
    query="high-level workflow orchestration and coordination",
    chunk_types=["class", "function"],
    limit=10
)

# Returns:
# - AutonomousWorkflow
# - TaskOrchestrator
# - execute_workflow()
# - coordinate_agents()
```

**Benefit**: Understand codebase architecture quickly

---

## Advanced Features

### 1. Multi-Query Search

```python
async def search_with_refinement(
    initial_query: str,
    refinement_queries: list[str]
) -> list[SearchResult]:
    """Combine multiple queries for better results."""

    # Get initial results
    results = await search_agent.search(initial_query, limit=20)

    # Refine by filtering with additional queries
    for refinement in refinement_queries:
        refinement_emb = await embeddings.embed(refinement)

        # Re-rank based on refinement
        for result in results:
            refinement_score = cosine_similarity(
                refinement_emb,
                result.chunk.embedding
            )
            # Boost if matches refinement
            if refinement_score > 0.6:
                result.relevance_score *= 1.2

        results.sort(key=lambda r: r.relevance_score, reverse=True)

    return results[:10]

# Usage
results = await search_with_refinement(
    initial_query="authentication",
    refinement_queries=["JWT tokens", "async functions"]
)
# Returns: async functions related to JWT authentication
```

### 2. Code Similarity Clustering

```python
async def find_duplicates(threshold: float = 0.85) -> list[tuple[CodeChunk, CodeChunk]]:
    """Find similar/duplicate code chunks."""

    duplicates = []

    chunks = list(search_agent.index.values())
    for i, chunk1 in enumerate(chunks):
        for chunk2 in chunks[i+1:]:
            similarity = cosine_similarity(chunk1.embedding, chunk2.embedding)

            if similarity > threshold:
                duplicates.append((chunk1, chunk2, similarity))

    return sorted(duplicates, key=lambda x: x[2], reverse=True)

# Usage
dupes = await find_duplicates(threshold=0.90)
for chunk1, chunk2, score in dupes[:5]:
    print(f"[{score:.2f}] {chunk1.name} <-> {chunk2.name}")
    # Suggests refactoring opportunities
```

### 3. Dependency Graph

```python
async def build_dependency_graph(
    target_function: str
) -> dict[str, list[str]]:
    """Build call graph for a function."""

    results = await search_agent.search(target_function, limit=1)
    if not results:
        return {}

    target = results[0].chunk

    graph = {target.name: target.calls}

    # Recursively find dependencies
    for call in target.calls:
        call_results = await search_agent.search(call, limit=1)
        if call_results:
            graph[call] = call_results[0].chunk.calls

    return graph

# Usage
graph = await build_dependency_graph("execute_workflow")
# Returns:
# {
#   "execute_workflow": ["plan_feature", "generate_code", "run_tests"],
#   "plan_feature": ["research_topic", "create_plan"],
#   "generate_code": ["get_context", "call_llm"],
#   ...
# }
```

---

## Integration Points

### 1. Update Coder Tool

**Before**:
```python
# app/server/tools/coder_tool.py
async def find_relevant_code(query: str) -> list[Path]:
    # grep-based search
    ...
```

**After**:
```python
async def find_relevant_code(query: str) -> list[Path]:
    """Use semantic search instead of grep."""
    search_agent = get_semantic_search_agent()

    results = await search_agent.search(query, limit=10)

    # Return unique file paths
    files = list({r.chunk.file_path for r in results})

    return files
```

### 2. Update Code Generator

**Use semantic search to find similar code**:
```python
# app/generation/code_generator.py
async def generate_with_examples(prompt: str) -> str:
    # Find similar code for context
    search_agent = get_semantic_search_agent()

    examples = await search_agent.search(
        f"code examples similar to: {prompt}",
        limit=3
    )

    context = "\n\n".join([
        f"# Example from {ex.chunk.file_path}\n{ex.snippet}"
        for ex in examples
    ])

    return await self._generate_with_context(prompt, context)
```

### 3. New Skill: Code Discovery

```python
# app/server/skills/code_discovery.py
async def discover_codebase_structure() -> dict[str, Any]:
    """Automatically discover codebase architecture."""

    search_agent = get_semantic_search_agent()

    structure = {
        "entry_points": await search_agent.search("main entry points", limit=5),
        "apis": await search_agent.search("API endpoints and routes", limit=10),
        "models": await search_agent.search("data models and schemas", limit=10),
        "services": await search_agent.search("business logic services", limit=10),
        "utils": await search_agent.search("utility functions", limit=10),
    }

    return structure
```

---

## Performance Optimization

### 1. Incremental Indexing

```python
async def update_index_incremental(changed_files: list[Path]) -> None:
    """Update index for changed files only."""

    for file_path in changed_files:
        # Remove old chunks for this file
        old_chunks = [
            cid for cid, chunk in self.index.items()
            if chunk.file_path == file_path
        ]
        for cid in old_chunks:
            del self.index[cid]

        # Parse and add new chunks
        new_chunks = await self._parse_file(file_path)
        for chunk in new_chunks:
            chunk.embedding = await self.embeddings.embed(
                self._chunk_to_text(chunk)
            )
            self.index[self._chunk_id(chunk)] = chunk

    # Save updated index
    self._save_index_to_cache()
```

### 2. Embedding Batching

```python
async def embed_batch(self, texts: list[str], batch_size: int = 100) -> list[list[float]]:
    """Batch embedding requests for efficiency."""

    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]

        # Single API call for batch
        batch_embeddings = await self.embedding_api.embed_batch(batch)

        all_embeddings.extend(batch_embeddings)

    return all_embeddings
```

### 3. Index Persistence

```python
def _save_index_to_cache(self, cache_file: Path) -> None:
    """Save index to disk for fast loading."""

    cache_file.parent.mkdir(parents=True, exist_ok=True)

    # Serialize index
    index_data = {
        "version": "1.0",
        "created_at": datetime.now().isoformat(),
        "chunks": [
            {
                "id": chunk_id,
                "file_path": str(chunk.file_path),
                "chunk_type": chunk.chunk_type,
                "name": chunk.name,
                "signature": chunk.signature,
                "docstring": chunk.docstring,
                "code": chunk.code,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "imports": chunk.imports,
                "calls": chunk.calls,
                "embedding": chunk.embedding,
            }
            for chunk_id, chunk in self.index.items()
        ]
    }

    # Compress and save
    import gzip
    with gzip.open(cache_file, "wt", encoding="utf-8") as f:
        json.dump(index_data, f)
```

---

## Implementation Plan

### Phase 1: AST Parser (2 days)
1. Implement file parsing with `ast` module
2. Extract functions, classes, methods, modules
3. Build `CodeChunk` dataclass
4. Extract signatures, docstrings, calls
5. Unit tests for parsing

### Phase 2: Indexing (2 days)
1. Build index from codebase
2. Generate embeddings for chunks
3. Implement caching (save/load index)
4. Add incremental indexing
5. Performance tests

### Phase 3: Search (2 days)
1. Implement semantic search
2. Add relevance scoring with boosts
3. Generate explanations
4. Support filters (chunk types, file patterns)
5. Integration tests

### Phase 4: Integration (2 days)
1. Update `coder_tool.py`
2. Update `code_generator.py`
3. Add code discovery skill
4. CLI tool for manual searches
5. End-to-end tests

---

## Testing Strategy

### Unit Tests

```python
def test_parse_function():
    source = '''
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b
    '''

    chunks = parse_file_from_source(source)

    assert len(chunks) == 1
    assert chunks[0].name == "add"
    assert chunks[0].signature == "def add(a: int, b: int) -> int"
    assert "Add two numbers" in chunks[0].docstring

def test_semantic_search():
    search_agent = SemanticCodeSearchAgent(Path("."))
    await search_agent.build_index()

    results = await search_agent.search("authentication", limit=5)

    assert len(results) > 0
    assert all(r.relevance_score >= 0.3 for r in results)
    assert results[0].relevance_score >= results[-1].relevance_score
```

### Performance Tests

```python
@pytest.mark.benchmark
async def test_index_build_time():
    search_agent = SemanticCodeSearchAgent(Path("."))

    start = time.time()
    await search_agent.build_index()
    duration = time.time() - start

    # Should index 100 files in < 30 seconds
    assert duration < 30

@pytest.mark.benchmark
async def test_search_latency():
    search_agent = SemanticCodeSearchAgent(Path("."))
    await search_agent.build_index()

    start = time.time()
    results = await search_agent.search("authentication")
    duration = time.time() - start

    # Should search in < 500ms
    assert duration < 0.5
```

---

## Success Metrics

**Must Have**:
- ✅ 80%+ accuracy vs manual code review
- ✅ < 1s search latency
- ✅ 30% quality improvement (better code discovery)
- ✅ 50% reduction in search iterations

**Nice to Have**:
- 📊 Index 1000 files in < 1 minute
- 🎯 Relevance scores correlate with developer judgment
- 🔄 Auto-rebuild index on file changes

---

## Risks & Mitigations

### Risk 1: Embedding Costs
**Problem**: Embedding entire codebase is expensive
**Mitigation**:
- Cache embeddings indefinitely
- Incremental updates (only changed files)
- Batch API calls

### Risk 2: Index Staleness
**Problem**: Index out of sync with code changes
**Mitigation**:
- File watcher for auto-rebuild
- Timestamp checking on search
- Manual rebuild command

### Risk 3: Large Codebases
**Problem**: 10K+ files slow to index
**Mitigation**:
- Parallel parsing
- Progressive indexing (index on-demand)
- Filter out vendored/generated code

---

## Related Features

- Feature 11: Context Caching (cache search results)
- Feature 13: Smart Context Assembler (use search for context)
- Observability (track search quality)

---

**Status**: Ready for Implementation
**Assigned**: TBD
**Target Release**: v2.3
