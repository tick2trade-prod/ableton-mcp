# Migration Option Analysis

## Decision Matrix: A vs B vs C

> Date: 2025-12-16

---

## Weighted Scoring

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| **Time to MVP** | 25% | 8 | 5 | 6 |
| **Code Quality** | 20% | 4 | 9 | 8 |
| **Risk Level** | 20% | 6 | 5 | 8 |
| **Maintainability** | 15% | 4 | 9 | 7 |
| **Learning Value** | 10% | 5 | 9 | 8 |
| **Rollback Safety** | 10% | 8 | 3 | 9 |

### Scores
- **Option A**: (0.25×8 + 0.20×4 + 0.20×6 + 0.15×4 + 0.10×5 + 0.10×8) = **5.9**
- **Option B**: (0.25×5 + 0.20×9 + 0.20×5 + 0.15×9 + 0.10×9 + 0.10×3) = **6.5**
- **Option C**: (0.25×6 + 0.20×8 + 0.20×8 + 0.15×7 + 0.10×8 + 0.10×9) = **7.4**

---

## Option A: Incremental Refactor

### What We Keep
```
ableton-mcp/
├── scripts/
│   ├── ableton_cache_ast_codegen_mcp/  ✓ Keep, refactor
│   ├── dearpygui_controller/agents/    ✓ Keep as-is
│   └── validators/                      ✓ Keep as-is
├── tests/                               ✓ Keep
├── live_set/                            ✓ Reference patterns
└── src/ableton_mcp/                     ✓ Refactor to FastMCP
```

### Effort Estimate
| Task | Hours |
|------|-------|
| Refactor MCP server to FastMCP patterns | 8 |
| Update imports across codebase | 4 |
| Fix broken tests | 8 |
| Add stem tools | 8 |
| **Total** | **28 hours** |

### Pros
- Fastest path to working code
- Preserve git history
- Tests already exist

### Cons
- Tech debt persists
- Complex dependency tree
- Hard to adopt clean patterns

---

## Option B: Clean Slate

### What We Create
```
ableton-fastmcp/
├── src/
│   ├── server.py             # New FastMCP server
│   ├── tools/                # Ported tools
│   └── resources/            # New resources
├── agents/                    # Ported from dearpygui_controller
├── tests/                     # New test suite
└── pyproject.toml            # Fresh dependencies
```

### Migration Effort
| Component | LOC | Hours |
|-----------|-----|-------|
| FastMCP server setup | ~200 | 4 |
| Port 27 MCP tools | ~1500 | 16 |
| Port 22 agents | ~6000 | 24 |
| Port validators | ~300 | 4 |
| New tests | ~1000 | 16 |
| **Total** | **~9000** | **64 hours** |

### Pros
- Clean architecture
- FastMCP best practices
- Modern uv tooling
- Smaller, focused repo

### Cons
- Lose git history
- Migration bugs
- Slower time to MVP

---

## Option C: Hybrid (Recommended)

### What We Create
```
ableton-fastmcp/
├── src/                       # New FastMCP code
├── agents/                    # Migrated incrementally
├── tests/
├── legacy/                    # Git submodule → ableton-mcp
│   └── (read-only reference)
├── migration/
│   ├── status.md              # Track progress
│   └── comparisons/           # A/B test results
└── pyproject.toml
```

### Migration Strategy

#### Phase 1: Foundation (Week 1)
- Create new repo with FastMCP
- Add old repo as submodule
- Copy documentation
- Set up CI

#### Phase 2: Core Tools (Week 2)
- Implement stem separation (NEW)
- Port session tools
- Port track tools
- Verify parity with legacy

#### Phase 3: Agents (Week 3)
- Port BaseAgent
- Port core agents (Percussion, Synth, Vocals, Effects)
- Add StemComparisonAgent (NEW)
- Integration test

#### Phase 4: MVP (Week 4)
- Run full I Am Machine workflow
- Iterate on quality
- Remove submodule when stable

### Effort Estimate
| Phase | Hours |
|-------|-------|
| Foundation | 4 |
| Core Tools | 16 |
| Agents | 24 |
| MVP | 16 |
| **Total** | **60 hours** |

### Pros
- Safety net of legacy code
- Gradual, validated migration
- Can reference working implementations
- Keep git history in submodule
- Flexible timeline

### Cons
- More complex setup initially
- Two repos to manage
- Need to keep in sync

---

## Recommendation

### Go with Option C (Hybrid)

**Rationale:**
1. **Lower risk**: Legacy code available for reference
2. **Validated migration**: Can A/B test new vs old
3. **Flexibility**: Can pause migration if issues arise
4. **Clean result**: Ends with clean new codebase

### First Steps

```bash
# 1. Create new project
cd ~/projects
uv init ableton-fastmcp --python 3.12
cd ableton-fastmcp

# 2. Add FastMCP
uv add "fastmcp[standard]"

# 3. Add legacy as submodule
git submodule add ../ableton-mcp legacy

# 4. Copy documentation
cp -r legacy/.antigravity .
cp -r legacy/.claude .
cp -r legacy/.gemini .

# 5. Create initial structure
mkdir -p src/tools src/resources agents tests
```

---

## Questions to Resolve Before Deciding

1. **How broken is current repo?**
   - Run full test suite
   - Count failing tests
   - Identify blocking issues

2. **What's the minimum viable FastMCP?**
   - Session tools only?
   - Full tool parity required?

3. **Agent migration priority?**
   - All 22 agents needed for MVP?
   - Which subset is sufficient?

4. **Timeline constraints?**
   - Hard deadline for MVP?
   - Learning priority vs delivery?
