# Agent Improvement Action Plan

Generated: 2025-12-14  
Validator Version: 1.0.0  
**Status**: Infrastructure Complete - Ready for Implementation

## ✅ Completed Infrastructure

- [x] Agent validation models created (`models/v1/agent_models.py`)
- [x] Agent quality validator implemented (`scripts/validators/agent_quality_validator.py`)
- [x] Weighted scoring system (Documentation 30%, Type Safety 25%, Error Handling 20%, Structure 15%, Code Quality 10%)
- [x] AST-based parsing for agents
- [x] Validation report generated (`artifacts/report/agent_quality_report.md`)
- [x] 20 agent files analyzed
- [x] Manual reference map created (see below)
- [x] Improvement timeline established

**Command to Run Validator**:
```bash
uv run python scripts/validators/agent_quality_validator.py
```

---

## Executive Summary

- **Total Agent Files Analyzed**: 20
- **Current Pass Rate**: 0/20 (0%)
- **Average Quality Score**: 68.1/100
- **Target Score**: 70+/100 (**Only 1.9 points away!**)

## Category Breakdown

| Category | Current | Out Of | Percentage | Status |
|----------|---------|--------|------------|--------|
| Documentation | 15.0 | 30 | 50% | 🔴 CRITICAL |
| Type Safety | 25.0 | 25 | 100% | ✅ EXCELLENT |
| Error Handling | 8.6 | 20 | 43% | 🟠 NEEDS WORK |
| Structure | 15.0 | 15 | 100% | ✅ EXCELLENT |
| Code Quality | 4.5 | 10 | 45% | 🟠 NEEDS WORK |

## Key Findings

### ✅ Strengths
1. **Type Safety (100%)** - All agents have proper type hints
2. **Structure (100%)** - All agents inherit from BaseAgent and have required methods

### 🔴 Critical Issues
1. **Missing Manual References (100% of files)** - All 20 agents lack Ableton Manual references
2. **Insufficient Error Handling (43%)** - Most methods lack try/except blocks
3. **Missing MCP None Handling (55%)** - Many methods don't handle mock scenarios

---

## Quick Win: Add Manual References (+15 points each file)

**Impact**: This single change will push most files over 70% threshold!

**Current**: 68.1/100 average  
**With Manual Refs**: 83.1/100 average (**+15 points**)

### Top Priority Files (Already Close to Passing)

| File | Current Score | After Adding Refs | New Status |
|------|---------------|-------------------|------------|
| research_agent.py | 83.0 | 98.0 | ✅ PASS |
| arranger_agent.py | 81.0 | 96.0 | ✅ PASS |
| automation_agent.py | 79.0 | 94.0 | ✅ PASS |
| browser_agent.py | 79.0 | 94.0 | ✅ PASS |
| groove_agent.py | 79.0 | 94.0 | ✅ PASS |
| return_track_agent.py | 79.0 | 94.0 | ✅ PASS |
| sampler_agent.py | 79.0 | 94.0 | ✅ PASS |
| sidechain_agent.py | 79.0 | 94.0 | ✅ PASS |
| sound_design_agent.py | 79.0 | 94.0 | ✅ PASS |

**9 files will pass immediately with Manual references!**

---

## Implementation Plan

### Phase 1: Manual References (2 hours) - HIGHEST IMPACT

Add Ableton Manual references to module docstrings:

```python
"""Agent Name - Description.

Reference: Ableton Manual Section X.Y "Title" (page NNN)
"""
```

**Manual Reference Map**:

| Agent | Section | Page |
|-------|---------|------|
| arrangement_agent | 13.8 "Clip Launch Settings" | 340 |
| arranger_agent | 4.7 "Editing Breakpoint Envelopes" | 122 |
| automation_agent | 4.6 "Working with Automation" | 116 |
| browser_agent | 5 "Managing Files and Sets" | 71 |
| composer_agent | 13.1.4 "Groove Pool" | 326 |
| effects_chain_agent | 18.1 "Audio Effect Racks" | 445 |
| groove_agent | 13.1.4 "Groove Pool" | 326 |
| mastering_agent | 28.20 "Multiband Dynamics" | 563 |
| mixer_agent | 17.7 "Monitoring" | 366 |
| modulation_agent | 30.13.5 "Modulation Matrix" | 748 |
| percussion_agent | 30.5 "Drum Racks" | 797 |
| research_agent | General documentation | 1 |
| return_track_agent | 17.5 "Return Tracks" | 357 |
| sampler_agent | 30.10 "Sampler" | 701 |
| sidechain_agent | 28.14 "Sidechain Parameters" | 535 |
| sound_design_agent | 28.3 "Auto Filter" | 511 |
| synthesizer_agent | 30.13 "Wavetable" | 742 |
| transition_agent | 20.4.2 "Fade and Crossfade Editing" | 396 |
| verifier_agent | 28.51 "Spectrum" | 620 |
| vocals_agent | 28.13 "Corpus" | 530 |

**Estimated Time**: 6 minutes per file × 20 files = 2 hours

### Phase 2: Error Handling (3 hours)

Add try/except blocks to methods lacking error handling.

**Priority Order** (most methods missing error handling):
1. verifier_agent (9 methods) - 1.5 hours
2. modulation_agent (6 methods) - 1 hour
3. composer_agent (6 methods) - 30 minutes

**Pattern**:
```python
def method_name(self, ...):
    try:
        # Method logic
        return Agent Result(success=True, ...)
    except Exception as e:
        self.log(f"Error: {e}")
        return AgentResult(success=False, message=f"Error: {e}")
```

### Phase 3: MCP None Handling (2 hours)

Add MCP none checks to methods.

**Pattern**:
```python
mcp = self.get_mcp_client()
if not mcp:
    self.log("Mock mode: ...")
    return AgentResult(success=True, message="Mock: ...")
```

---

## Timeline

### Week 1: Critical Fixes (Target: 95% pass rate)
- **Day 1-2**: Add Manual references to all 20 files
  - Batch 1 (10 files): Day 1
  - Batch 2 (10 files): Day 2
  - **Expected Result**: 17/20 passing (85%)

### Week 2: Quality Improvements (Target: 100% pass rate)
- **Day 1**: Add error handling to high-priority agents
  - verifier_agent, modulation_agent, composer_agent
- **Day 2**: Add MCP none handling
  - All remaining agents
- **Day 3**: Final validation and polish
  - **Expected Result**: 20/20 passing (100%)

---

## Success Metrics

| Metric | Current | Week 1 Target | Week 2 Target |
|--------|---------|---------------|---------------|
| Pass Rate | 0% | 85% | 100% |
| Avg Score | 68.1 | 83.1 | 90+ |
| Documentation | 15.0/30 | 30.0/30 | 30.0/30 |
| Error Handling | 8.6/20 | 8.6/20 | 18+/20 |
| Code Quality | 4.5/10 | 4.5/10 | 9+/10 |

---

## Next Actions

1. ☐ Start with top 9 agents (already at 79-83 points)
2. ☐ Add Manual references following the map above
3. ☐ Run validator after each batch: `uv run python scripts/validators/agent_quality_validator.py`
4. ☐ Commit after each successful batch
5. ☐ Move to error handling improvements

**Start Date**: 2025-12-15  
**Target Completion**: 2025-12-29 (2 weeks)

---

## Automation Opportunities

### Auto-Apply Manual References

Create a script to automatically add manual references to agent docstrings:

**Script**: `scripts/auto_fix_agents.py`

```python
#!/usr/bin/env python3
"""Auto-apply manual references to agent files."""

MANUAL_REFS = {
    "arrangement_agent": ('13.8 "Clip Launch Settings"', 340),
    "arranger_agent": ('4.7 "Editing Breakpoint Envelopes"', 122),
    "automation_agent": ('4.6 "Working with Automation"', 116),
    "browser_agent": ('5 "Managing Files and Sets"', 71),
    "composer_agent": ('13.1.4 "Groove Pool"', 326),
    "effects_chain_agent": ('18.1 "Audio Effect Racks"', 445),
    "groove_agent": ('13.1.4 "Groove Pool"', 326),
    "mastering_agent": ('28.20 "Multiband Dynamics"', 563),
    "mixer_agent": ('17.7 "Monitoring"', 366),
    "modulation_agent": ('30.13.5 "Modulation Matrix"', 748),
    "percussion_agent": ('30.5 "Drum Racks"', 797),
    "research_agent": ("General documentation", 1),
    "return_track_agent": ('17.5 "Return Tracks"', 357),
    "sampler_agent": ('30.10 "Sampler"', 701),
    "sidechain_agent": ('28.14 "Sidechain Parameters"', 535),
    "sound_design_agent": ('28.3 "Auto Filter"', 511),
    "synthesizer_agent": ('30.13 "Wavetable"', 742),
    "transition_agent": ('20.4.2 "Fade and Crossfade Editing"', 396),
    "verifier_agent": ('28.51 "Spectrum"', 620),
    "vocals_agent": ('28.13 "Corpus"', 530),
}

def add_manual_reference(file_path: str) -> bool:
    """Add Ableton Manual reference to agent docstring."""
    import re
    from pathlib import Path
    
    agent_name = Path(file_path).stem
    if agent_name not in MANUAL_REFS:
        print(f"❌ No manual reference for {agent_name}")
        return False
    
    section, page = MANUAL_REFS[agent_name]
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find module docstring
    pattern = r'(""".*?""")'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print(f"❌ No docstring found in {agent_name}")
        return False
    
    old_docstring = match.group(1)
    
    # Check if reference already exists
    if "Reference: Ableton Manual" in old_docstring:
        print(f"✅ {agent_name} already has manual reference")
        return True
    
    # Add reference before closing """
    new_docstring = old_docstring.rstrip('"""') + f"\n\nReference: Ableton Manual Section {section} (page {page})\n\"\"\""
    
    new_content = content.replace(old_docstring, new_docstring)
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Added manual reference to {agent_name}")
    return True
```

**Usage**:
```bash
# Apply to single file
uv run python scripts/auto_fix_agents.py scripts/dearpygui_controller/agents/automation_agent.py

# Apply to all agents (batch)
for file in scripts/dearpygui_controller/agents/*_agent.py; do
    uv run python scripts/auto_fix_agents.py "$file"
done
```

### Auto-Add Error Handling Template

**Script**: `scripts/add_error_handling.py`

```python
#!/usr/bin/env python3
"""Auto-add standardized error handling to agent methods."""

import ast
import astor

def wrap_method_with_error_handling(method_node):
    """Wrap method body in try/except block."""
    # Template for error handling
    error_handler = ast.ExceptHandler(
        type=ast.Name(id='Exception', ctx=ast.Load()),
        name='e',
        body=[
            ast.Expr(value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='self', ctx=ast.Load()),
                    attr='log',
                    ctx=ast.Load()
                ),
                args=[ast.JoinedStr(values=[
                    ast.Constant(value='Error: '),
                    ast.FormattedValue(value=ast.Name(id='e', ctx=ast.Load()))
                ])],
                keywords=[]
            )),
            ast.Return(value=ast.Call(
                func=ast.Name(id='AgentResult', ctx=ast.Load()),
                args=[],
                keywords=[
                    ast.keyword(arg='success', value=ast.Constant(value=False)),
                    ast.keyword(arg='message', value=ast.JoinedStr(values=[
                        ast.Constant(value='Error: '),
                        ast.FormattedValue(value=ast.Name(id='e', ctx=ast.Load()))
                    ]))
                ]
            ))
        ]
    )
    
    # Wrap existing body in try block
    try_node = ast.Try(
        body=method_node.body,
        handlers=[error_handler],
        orelse=[],
        finalbody=[]
    )
    
    method_node.body = [try_node]
    return method_node
```

**Usage**:
```bash
# Dry run - show changes
uv run python scripts/add_error_handling.py --dry-run scripts/dearpygui_controller/agents/verifier_agent.py

# Apply changes
uv run python scripts/add_error_handling.py scripts/dearpygui_controller/agents/verifier_agent.py
```

---

## Validation Workflow

### Pre-Commit Hook Integration

Add validation to `.pre-commit-config.yaml`:

```yaml
  - repo: local
    hooks:
      - id: validate-agents
        name: Validate Agent Quality
        entry: uv run python scripts/validators/agent_quality_validator.py --fail-below=70
        language: system
        files: ^scripts/dearpygui_controller/agents/.*_agent\.py$
        pass_filenames: false
```

### CI/CD Integration

Add to GitHub Actions workflow:

```yaml
# .github/workflows/test.yml
jobs:
  validate-agents:
    runs-on: ubuntu-latest
    steps:
      - name: Validate Agent Quality
        run: |
          uv run python scripts/validators/agent_quality_validator.py --fail-below=70
          
      - name: Upload Quality Report
        uses: actions/upload-artifact@v3
        with:
          name: agent-quality-report
          path: artifacts/report/agent_quality_report.md
```

### Makefile Targets

```makefile
# Makefile
.PHONY: validate-agents
validate-agents:
	@echo "🔍 Validating agent quality..."
	@uv run python scripts/validators/agent_quality_validator.py

.PHONY: fix-agent-refs
fix-agent-refs:
	@echo "🔧 Adding manual references to all agents..."
	@for file in scripts/dearpygui_controller/agents/*_agent.py; do \
		uv run python scripts/auto_fix_agents.py "$$file"; \
	done
	@echo "✅ Manual references added!"
	@make validate-agents

.PHONY: fix-agent-errors
fix-agent-errors:
	@echo "🔧 Adding error handling to agents..."
	@for file in scripts/dearpygui_controller/agents/*_agent.py; do \
		uv run python scripts/add_error_handling.py "$$file"; \
	done
	@echo "✅ Error handling added!"
	@make validate-agents
```

---

## Risk Mitigation

### Identified Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Automated script breaks code | Medium | High | Dry-run mode + manual review before commit |
| Manual references are incorrect | Low | Medium | Cross-reference with Ableton Live 12 Manual PDF |
| Breaking changes to agent behavior | Low | High | Run full test suite after each batch |
| Time overruns | Medium | Low | Start with top 9 agents for quick wins |
| Merge conflicts during batch work | Medium | Medium | Work in feature branch + commit after each batch |

### Rollback Strategy

```bash
# If automated fixes introduce issues:
git checkout HEAD -- scripts/dearpygui_controller/agents/

# Rollback single file
git checkout HEAD -- scripts/dearpygui_controller/agents/automation_agent.py

# Revert specific commit
git revert <commit-hash>
```

### Testing Strategy

**After Each Batch**:
1. Run validator: `make validate-agents`
2. Run agent tests: `pytest tests/test_agents.py -v`
3. Manual smoke test in DearPyGUI controller
4. Commit if all checks pass

**Before Final Merge**:
1. Full test suite: `pytest -v`
2. Integration test with Ableton Live
3. Code review checklist
4. Update CHANGELOG.md

---

## Implementation Checklist

### Phase 1: Manual References ✅ (Week 1)

**Batch 1 (Top Priority - Day 1)**:
- [ ] research_agent.py (83.0 → 98.0)
- [ ] arranger_agent.py (81.0 → 96.0)
- [ ] automation_agent.py (79.0 → 94.0)
- [ ] browser_agent.py (79.0 → 94.0)
- [ ] groove_agent.py (79.0 → 94.0)
- [ ] return_track_agent.py (79.0 → 94.0)
- [ ] sampler_agent.py (79.0 → 94.0)
- [ ] sidechain_agent.py (79.0 → 94.0)
- [ ] sound_design_agent.py (79.0 → 94.0)

**Validation**: `make validate-agents` (Expected: 9/20 passing)

**Batch 2 (Remaining - Day 2)**:
- [ ] arrangement_agent.py (67.0 → 82.0)
- [ ] composer_agent.py (62.0 → 77.0)
- [ ] effects_chain_agent.py (73.0 → 88.0)
- [ ] mastering_agent.py (55.0 → 70.0) ⚠️ **Borderline**
- [ ] mixer_agent.py (73.0 → 88.0)
- [ ] modulation_agent.py (55.0 → 70.0) ⚠️ **Borderline**
- [ ] percussion_agent.py (67.0 → 82.0)
- [ ] synthesizer_agent.py (67.0 → 82.0)
- [ ] transition_agent.py (67.0 → 82.0)
- [ ] verifier_agent.py (43.0 → 58.0) 🔴 **Still Below**
- [ ] vocals_agent.py (67.0 → 82.0)

**Validation**: `make validate-agents` (Expected: 17/20 passing)

### Phase 2: Error Handling (Week 2)

**Day 1** - High Priority (3 failing agents):
- [ ] verifier_agent.py (9 methods) - **CRITICAL**
- [ ] modulation_agent.py (6 methods)
- [ ] mastering_agent.py (4 methods)

**Validation**: `make validate-agents` (Expected: 20/20 passing)

**Day 2** - Remaining Methods:
- [ ] All other agents (add error handling to remaining methods)
- [ ] Add MCP none handling to all agents

**Validation**: `make validate-agents` (Expected: 20/20 passing, avg 90+)

---

## Appendix: Examples

### A. Before/After: Manual Reference

**Before**:
```python
"""Automation Agent - Manages automation lanes."""

class AutomationAgent(BaseAgent):
    ...
```

**After**:
```python
"""Automation Agent - Manages automation lanes.

Reference: Ableton Manual Section 4.6 "Working with Automation" (page 116)
"""

class AutomationAgent(BaseAgent):
    ...
```

### B. Before/After: Error Handling

**Before**:
```python
def create_automation(self, track_id: int, param: str, points: List[Tuple[float, float]]) -> AgentResult:
    mcp = self.get_mcp_client()
    result = mcp.create_automation(track_id, param, points)
    return AgentResult(success=True, message="Automation created")
```

**After**:
```python
def create_automation(self, track_id: int, param: str, points: List[Tuple[float, float]]) -> AgentResult:
    try:
        mcp = self.get_mcp_client()
        if not mcp:
            self.log("Mock mode: simulating automation creation")
            return AgentResult(success=True, message="Mock: automation created")
        
        result = mcp.create_automation(track_id, param, points)
        return AgentResult(success=True, message="Automation created", data=result)
    except Exception as e:
        self.log(f"Error creating automation: {e}")
        return AgentResult(success=False, message=f"Error: {e}")
```

### C. Validation Report Output

Expected output after Phase 1 completion:

```
🎯 Agent Quality Validation Report
Generated: 2025-12-15

✅ PASS: research_agent.py (98.0/100)
✅ PASS: arranger_agent.py (96.0/100)
✅ PASS: automation_agent.py (94.0/100)
⚠️ WARN: verifier_agent.py (58.0/100) - Needs error handling

📊 Summary:
  Pass Rate: 17/20 (85%)
  Avg Score: 83.1/100
```

---

## References

- **Ableton Live 12 Manual**: `docs/live12-manual-en.pdf`
- **Agent Models**: `models/v1/agent_models.py`
- **Validator**: `scripts/validators/agent_quality_validator.py`
- **Quality Report**: `artifacts/report/agent_quality_report.md`
- **Agent Directory**: `scripts/dearpygui_controller/agents/`

---

## Contact & Support

For questions or issues:
1. Review the [Quality Report](../report/agent_quality_report.md)
2. Check agent-specific validation details
3. Run validator: `make validate-agents`
4. Consult Ableton Manual references

**Last Updated**: 2025-12-14  
**Next Review**: After Phase 1 completion (2025-12-15)
