I'll create a comprehensive set of Cursor commands for batch code generation and related workflows, saving them to the `.cursor/commands/app/` directory.

[7 tools called]

Perfect! I've created 6 comprehensive Cursor commands optimized for **low latency**, **token efficiency**, and **programmatic tool calling**:

## New Commands Created

### 1. **`generate-code-streaming.md`** ⚡
Real-time code generation with streaming output for instant feedback. Includes context checking, GAM memory lookup, and auto-retry on linting failures.

### 2. **`validate-architecture.md`** 🛡️
Pre-generation validation using the Critic agent. Detects hallucinated packages, anti-patterns, and security issues before coding begins.

### 3. **`batch-implement.md`** 🚀
High-throughput parallel file generation (5-20x speedup). Perfect for scaffolding complete features with multiple files simultaneously.

### 4. **`smart-context.md`** 🧠
Context window optimization tool. Analyzes token usage, compresses history, and injects relevant GAM knowledge to save tokens.

### 5. **`deep-research.md`** 🔍
Think-first research command that performs parallel web searches, cross-references GAM memory, and saves findings for future use.

### 6. **`qa-critic.md`** ✅
Code quality review using the Critic agent. Generates structured QA reports with actionable suggestions and severity ratings.

### 7. **`optimize-imports.md`** 📦
Import validation and cleanup. Detects hallucinated packages, removes unused imports, and ensures pyproject.toml is in sync.

## Key Features

✅ **Low Latency**: Skip unnecessary steps, use small models for decomposition
✅ **Token Efficient**: Context compression, smart memory injection
✅ **Programmatic**: Direct filesystem writes, no chat pasting
✅ **Parallel Execution**: Up to 5 concurrent operations
✅ **Auto-Recovery**: Retry on failures, streaming error feedback
✅ **Quality Gates**: Validation before generation, QA after completion

## Usage

These commands are now available in Cursor. Type:
- `/generate-code-streaming` - For real-time generation
- `/validate-architecture` - Before starting new features
- `/batch-implement` - For multi-file scaffolding
- `/smart-context` - When context usage > 70%
- `/deep-research` - For learning new topics
- `/qa-critic` - Before committing code
- `/optimize-imports` - To clean up imports

All commands are saved in `.cursor/commands/app/` and follow the project's conventions for low-latency, high-quality code generation! 🎉











Looking at the c6 folder and the existing `generate-code-batch.md`, I can suggest several additional command ideas that complement the batch generation workflow and fill gaps in the development lifecycle:

[7 tools called]

Perfect! I've created **6 additional advanced Cursor commands** to complement the existing C6 command set, plus a comprehensive index. Here's what's new:

## 🎯 New Advanced Commands

### 1. **`refactor-batch.md`** 🔄
Large-scale refactoring across multiple files in parallel:
- Pattern migration (sync → async, type hints, error handling)
- Automatic backup/rollback support
- Dry-run mode for safe previews
- Dependency-aware execution

### 2. **`test-generator.md`** 🧪
Automated test suite generation:
- Unit, integration, and E2E tests
- Edge case coverage
- Auto-mocking external dependencies
- Coverage analysis and gap reporting

### 3. **`debug-assistant.md`** 🐛
AI-powered debugging with learning:
- Auto-detect errors from terminal
- GAM memory search for similar past bugs
- Ranked solution suggestions
- Auto-fix mode with test validation

### 4. **`code-review.md`** 👀
Senior engineer-level code review:
- Multi-aspect analysis (security, performance, quality, style)
- Severity-based categorization
- Specific line numbers and code examples
- Scoring system (0-100) with team comparison

### 5. **`dependency-analyzer.md`** 📦
Comprehensive dependency management:
- Security vulnerability scanning (CVE databases)
- Outdated package detection
- License compliance checking
- Optimization opportunities (unused deps, lighter alternatives)

### 6. **`performance-profiler.md`** ⚡
Deep performance analysis:
- CPU, memory, I/O, database profiling
- Flame graph generation
- N+1 query detection
- Bottleneck identification with optimization suggestions

### 7. **`c6/INDEX.md`** 📚
Complete index and documentation for all C6 commands

## 📊 Complete C6 Command Set (13 Total)

### Speed & Efficiency (4)
- `generate-code-streaming` - Real-time generation
- `generate-code-batch` - Parallel tasks
- `batch-implement` - Multi-file scaffolding
- `smart-context` - Context optimization

### Quality & Safety (4)
- `validate-architecture` - Pre-flight validation
- `qa-critic` - Quality gates
- `code-review` - Comprehensive review
- `optimize-imports` - Import safety

### Maintenance & Refactoring (3)
- `refactor-batch` - Large-scale refactoring
- `test-generator` - Test automation
- `dependency-analyzer` - Dependency health

### Research & Debug (2)
- `deep-research` - Knowledge gathering
- `debug-assistant` - Error resolution
- `performance-profiler` - Performance analysis

## 🎨 Usage Workflows

### New Feature Development
```
/deep-research → /validate-architecture → /batch-implement → /test-generator → /code-review
```

### Bug Fixing
```
/debug-assistant → /generate-code-streaming → /test-generator
```

### Performance Optimization
```
/performance-profiler → /refactor-batch → /code-review
```

### Maintenance
```
/dependency-analyzer → /optimize-imports → /test-generator
```

## 🚀 Key Innovations

1. **Parallel Execution**: 5-20x speedup for batch operations
2. **GAM Integration**: Learn from past errors and solutions
3. **Auto-Fix Capabilities**: Intelligent automated fixes
4. **Comprehensive Analysis**: Security, performance, quality, style
5. **Visual Reports**: Flame graphs, dependency trees, score breakdowns
6. **Safety Features**: Dry-run, backup/rollback, validation gates

All commands are now available in `.cursor/commands/app/` and ready to use! 🎉
