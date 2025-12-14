# Feature Design: Batch Processing Agent

**Feature ID**: 12
**Priority**: P1 (High)
**Impact**: Latency Reduction (70%), Quality Improvement (20%)
**Complexity**: High (5-7 days)

---

## Problem Statement

Current implementation processes tasks sequentially:
- Code generation for multiple files: one at a time
- Test execution: run tests sequentially
- Multiple research queries: processed in order
- Workflow phases: strictly sequential

### Current Sequential Flow (Slow)
```
Generate file1.py (3s) → Generate file2.py (3s) → Generate file3.py (3s)
Total: 9 seconds

Run test1 (2s) → Run test2 (2s) → Run test3 (2s)
Total: 6 seconds

Overall: 15 seconds
```

**Problem**: For independent tasks, **70% of time is wasted waiting**

---

## Proposed Solution

Create a **Batch Processing Agent** that:
1. Identifies parallelizable tasks
2. Executes them concurrently
3. Aggregates results
4. Handles partial failures gracefully
5. Provides progress tracking

---

## Architecture

### New Agent: `BatchProcessingAgent`

**Location**: `app/server/agents/batch_agent.py`

**Responsibilities**:
- Detect task dependencies (DAG analysis)
- Execute independent tasks in parallel
- Aggregate and merge results
- Handle errors and retries
- Track progress and metrics

**Key Methods**:
```python
class BatchProcessingAgent:
    async def process_batch(
        self,
        tasks: list[Task],
        max_concurrency: int = 5
    ) -> BatchResult:
        """Process tasks in parallel with dependency management."""
        dag = self._build_dependency_graph(tasks)
        execution_plan = self._topological_sort(dag)

        results = []
        for level in execution_plan:
            # Execute all tasks in same level concurrently
            level_results = await asyncio.gather(
                *[self._execute_task(task) for task in level],
                return_exceptions=True
            )
            results.extend(level_results)

        return self._aggregate_results(results)

    async def parallel_code_generation(
        self,
        file_specs: list[FileSpec]
    ) -> list[GeneratedFile]:
        """Generate multiple files in parallel."""
        tasks = [
            self._create_gen_task(spec)
            for spec in file_specs
        ]
        return await self.process_batch(tasks)

    async def parallel_test_execution(
        self,
        test_files: list[Path]
    ) -> TestResults:
        """Run multiple test files in parallel."""
        tasks = [
            self._create_test_task(test_file)
            for test_file in test_files
        ]
        return await self.process_batch(tasks)
```

---

## Use Cases

### Use Case 1: Multi-File Code Generation
```python
# Before: Sequential (9 seconds)
for file_spec in file_specs:
    code = await code_gen.generate(file_spec)
    write_file(file_spec.path, code)

# After: Parallel (3 seconds)
batch_agent = BatchProcessingAgent()
results = await batch_agent.parallel_code_generation(file_specs)
for result in results:
    write_file(result.path, result.code)
```

**Speedup**: 3x (9s → 3s)

### Use Case 2: Exploratory Generation
```python
# Generate multiple approaches and pick best
approaches = [
    "Object-oriented design",
    "Functional approach",
    "Data-driven architecture"
]

batch_agent = BatchProcessingAgent()
implementations = await batch_agent.generate_alternatives(
    prompt=feature_description,
    approaches=approaches
)

best = batch_agent.rank_by_quality(implementations)
return best[0]
```

**Benefit**: Better quality through exploration

### Use Case 3: Parallel Testing
```python
# Before: Sequential (6 seconds)
for test_file in test_files:
    result = run_test(test_file)
    results.append(result)

# After: Parallel (2 seconds)
batch_agent = BatchProcessingAgent()
results = await batch_agent.parallel_test_execution(test_files)
```

**Speedup**: 3x (6s → 2s)

### Use Case 4: Multi-Query Research
```python
# Research multiple topics concurrently
queries = [
    "FastAPI async patterns",
    "PostgreSQL connection pooling",
    "Redis caching best practices"
]

batch_agent = BatchProcessingAgent()
research_results = await batch_agent.parallel_research(queries)
```

**Speedup**: 3x

---

## Task Dependency Management

### Dependency Graph (DAG)
```python
@dataclass
class Task:
    id: str
    function: Callable
    args: tuple
    kwargs: dict
    dependencies: list[str]  # IDs of tasks that must complete first

class DependencyGraph:
    def build(self, tasks: list[Task]) -> dict[str, list[Task]]:
        """Build DAG from task dependencies."""
        graph = {}
        for task in tasks:
            graph[task.id] = [
                t for t in tasks if t.id in task.dependencies
            ]
        return graph

    def topological_sort(self, graph: dict) -> list[list[Task]]:
        """Group tasks by execution level (parallelizable)."""
        levels = []
        completed = set()

        while len(completed) < len(graph):
            # Find tasks with no incomplete dependencies
            current_level = [
                task for task_id, task in graph.items()
                if task_id not in completed
                and all(dep_id in completed for dep_id in task.dependencies)
            ]
            levels.append(current_level)
            completed.update(task.id for task in current_level)

        return levels
```

### Example: Complex Workflow
```python
tasks = [
    Task(id="research", func=research, dependencies=[]),
    Task(id="plan", func=plan, dependencies=["research"]),
    Task(id="gen_model", func=gen_model, dependencies=["plan"]),
    Task(id="gen_api", func=gen_api, dependencies=["plan"]),  # Parallel with gen_model
    Task(id="gen_tests", func=gen_tests, dependencies=["gen_model", "gen_api"]),
]

# Execution plan:
# Level 0: [research]                    ← 1 task
# Level 1: [plan]                        ← 1 task
# Level 2: [gen_model, gen_api]          ← 2 parallel tasks
# Level 3: [gen_tests]                   ← 1 task
```

---

## Error Handling

### Partial Failure Strategy
```python
class BatchResult:
    successful: list[TaskResult]
    failed: list[TaskFailure]
    partial: bool

    def is_success(self) -> bool:
        return len(self.failed) == 0

    def retry_failed(self) -> BatchResult:
        """Retry only failed tasks."""
        failed_tasks = [f.task for f in self.failed]
        return batch_agent.process_batch(failed_tasks)
```

### Error Isolation
```python
# Don't let one failure crash all tasks
results = await asyncio.gather(
    *[self._execute_task(task) for task in tasks],
    return_exceptions=True  # ← Catch exceptions
)

# Process results
for i, result in enumerate(results):
    if isinstance(result, Exception):
        failures.append(TaskFailure(task=tasks[i], error=result))
    else:
        successes.append(result)
```

### Retry Logic
```python
async def _execute_task_with_retry(
    self,
    task: Task,
    max_retries: int = 3
) -> TaskResult:
    """Execute task with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return await self._execute_task(task)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

---

## Performance Metrics

### Concurrency Limits
```python
# Configurable based on workload
CONCURRENCY_LIMITS = {
    "code_generation": 3,  # LLM rate limits
    "test_execution": 5,   # CPU-bound
    "research": 3,         # API rate limits
    "file_io": 10,         # IO-bound
}
```

### Progress Tracking
```python
@dataclass
class BatchProgress:
    total_tasks: int
    completed: int
    failed: int
    in_progress: int

    @property
    def percent_complete(self) -> float:
        return (self.completed + self.failed) / self.total_tasks * 100

# Usage
async for progress in batch_agent.process_batch_streaming(tasks):
    print(f"Progress: {progress.percent_complete}%")
```

---

## Integration Points

### 1. Update CodeGenerator

**Add batch generation method**:
```python
# app/generation/code_generator.py
class CodeGenerator:
    async def generate_batch(
        self,
        file_specs: list[FileSpec]
    ) -> list[GeneratedFile]:
        """Generate multiple files in parallel."""
        batch_agent = get_batch_agent()
        return await batch_agent.parallel_code_generation(file_specs)
```

### 2. Update Orchestrator

**Add parallel execution mode**:
```python
# app/server/orchestrator.py
async def execute_workflow(
    feature_name: str,
    parallel: bool = True  # New parameter
) -> WorkflowResult:
    if parallel:
        batch_agent = get_batch_agent()
        # Identify parallelizable phases
        tasks = _extract_parallel_tasks(feature_name)
        await batch_agent.process_batch(tasks)
```

### 3. New Skill: Batch Implementation

**Create**: `app/server/skills/batch_implementation.py`
```python
async def execute_batch_implementation(
    feature_plans: list[FeaturePlan]
) -> list[ImplementationResult]:
    """Implement multiple features in parallel."""
    batch_agent = get_batch_agent()
    tasks = [
        Task(
            id=f"impl_{i}",
            func=generate_and_implement,
            args=(plan.prompt, plan.language),
            dependencies=[]
        )
        for i, plan in enumerate(feature_plans)
    ]
    return await batch_agent.process_batch(tasks)
```

---

## Configuration

### Config File: `batch_config.yaml`
```yaml
batch_processing:
  max_concurrency:
    code_generation: 3
    test_execution: 5
    research: 3
    default: 5

  retry:
    max_attempts: 3
    backoff_multiplier: 2
    max_backoff_seconds: 30

  timeouts:
    per_task_seconds: 60
    total_batch_seconds: 300

  features:
    enable_progress_tracking: true
    enable_result_caching: true
    enable_dependency_analysis: true
```

---

## Implementation Plan

### Phase 1: Core Batch Engine (2 days)
1. Create `BatchProcessingAgent` class
2. Implement `asyncio.gather` orchestration
3. Add progress tracking
4. Basic error handling
5. Unit tests

### Phase 2: Dependency Management (2 days)
1. Implement DAG builder
2. Topological sort algorithm
3. Level-based parallel execution
4. Dependency validation
5. Integration tests

### Phase 3: Integration (2 days)
1. Update `CodeGenerator.generate_batch()`
2. Add batch skill
3. Update orchestrator
4. Update tools for parallelism
5. End-to-end tests

### Phase 4: Advanced Features (1 day)
1. Retry logic with backoff
2. Partial failure handling
3. Resource limit management
4. Performance metrics
5. Configuration system

---

## Testing Strategy

### Unit Tests
```python
def test_independent_tasks_run_parallel():
    tasks = [Task(..., dependencies=[]) for _ in range(3)]
    start = time.time()
    await batch_agent.process_batch(tasks)
    duration = time.time() - start
    assert duration < 4  # Should be ~3s, not 9s

def test_dependent_tasks_run_sequentially():
    tasks = [
        Task(id="t1", dependencies=[]),
        Task(id="t2", dependencies=["t1"])
    ]
    result = await batch_agent.process_batch(tasks)
    assert result.is_success()

def test_partial_failure_continues():
    tasks = [
        Task(id="t1", func=lambda: "success"),
        Task(id="t2", func=lambda: raise_error()),
        Task(id="t3", func=lambda: "success")
    ]
    result = await batch_agent.process_batch(tasks)
    assert len(result.successful) == 2
    assert len(result.failed) == 1
```

### Performance Tests
```python
@pytest.mark.benchmark
def test_batch_speedup():
    # Measure sequential
    start = time.time()
    for i in range(3):
        await slow_operation()
    sequential_time = time.time() - start

    # Measure parallel
    start = time.time()
    await batch_agent.process_batch([
        Task(func=slow_operation) for _ in range(3)
    ])
    parallel_time = time.time() - start

    speedup = sequential_time / parallel_time
    assert speedup >= 2.5  # At least 2.5x speedup
```

---

## Risks & Mitigations

### Risk 1: Rate Limiting
**Problem**: LLM APIs have rate limits
**Mitigation**:
- Configurable concurrency limits per operation type
- Exponential backoff on rate limit errors
- Queue management

### Risk 2: Resource Exhaustion
**Problem**: Too many parallel tasks → OOM
**Mitigation**:
- Max concurrency limits
- Memory monitoring
- Task prioritization

### Risk 3: Dependency Bugs
**Problem**: Incorrect DAG → wrong execution order
**Mitigation**:
- Extensive DAG testing
- Dependency validation
- Dry-run mode

---

## Success Metrics

**Must Have**:
- ✅ 3x speedup for multi-file generation
- ✅ 3x speedup for test execution
- ✅ 100% correctness (dependency order)
- ✅ Graceful partial failure handling

**Nice to Have**:
- 📊 Real-time progress tracking
- 🎯 Auto-detect parallelizable tasks
- 🔄 Smart retry with circuit breaker

---

## Alternatives Considered

### Alternative 1: ThreadPoolExecutor
**Pros**: Built-in, simple
**Cons**: No async support, GIL limits
**Decision**: Rejected

### Alternative 2: Celery/Dramatiq
**Pros**: Production-ready, distributed
**Cons**: Overkill, external dependency
**Decision**: Use for background tasks only

### Alternative 3: Manual asyncio.gather
**Pros**: Simple
**Cons**: No dependency management, no error handling
**Decision**: Too limited

---

## Related Features

- Feature 11: Context Caching (parallel cache warming)
- Feature 13: Smart Context Assembler (parallel context retrieval)
- Observability (parallel metrics collection)

---

**Status**: Ready for Implementation
**Assigned**: TBD
**Target Release**: v2.2
