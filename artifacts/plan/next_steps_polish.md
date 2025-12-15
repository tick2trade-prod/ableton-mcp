# Next Steps - Remaining Polish & Integration

Generated: 2025-12-14
Status: Optional Improvements
**Estimated Total**: 3-5 hours

---

## Overview

All core functionality is complete. These are polish and integration improvements to maximize the value of the implemented system.

---

## Phase 1: Validator Updates & 100% Pass Rates (2-3 hours)

**Objective**: Update validator paths AND achieve 100% pass rates for all agents and tests

### Step 1: Update Validator Output Paths (30 min)

1. **Update Agent Validator Output Path**
   - File: `scripts/validators/agent_quality_validator.py`
   - Change: `artifacts/agent_quality_report.md` → `artifacts/report/agent_quality_report.md`
   - Line: ~391

2. **Update Test Validator Output Path**
   - File: `tests/validators/test_quality_validator.py`
   - Change: `artifacts/test_quality_report.md` → `artifacts/report/test_quality_report.md`
   - Estimated: Line ~300

3. **Re-run Validators to Get Baseline**
   ```bash
   uv run python scripts/validators/agent_quality_validator.py
   uv run python tests/validators/test_quality_validator.py
   ```

### Step 2: Fix Remaining 3 Agents to Reach 20/20 (1 hour)

**Current**: 17/20 agents passing (85%)
**Target**: 20/20 agents passing (100%)

Based on the agent improvement plan, the remaining 3 agents likely need:

1. **Add TDD Workflow Sections** (if missing)
   - Pattern:
   ```python
   """
   TDD Workflow:
   - 🔴 RED: Write failing test
   - 🟢 GREEN: Implement minimum code to pass
   - 🔄 REFACTOR: Clean up with tests as safety net
   """
   ```

2. **Add Missing Error Handling** (Phase 2 from agent improvement plan)
   - Add try/except blocks to methods
   - Priority: verifier_agent (9 methods), modulation_agent (6 methods), composer_agent (6 methods)
   - Pattern:
   ```python
   try:
       # Method logic
       return AgentResult(success=True, ...)
   except Exception as e:
       self.log(f"Error: {e}")
       return AgentResult(success=False, message=f"Error: {e}")
   ```

3. **Add MCP None Handling** (Phase 3 from agent improvement plan)
   - Add checks for mock scenarios
   - Pattern:
   ```python
   mcp = self.get_mcp_client()
   if not mcp:
       self.log("Mock mode: ...")
       return AgentResult(success=True, message="Mock: ...")
   ```

**Script Approach**:
```bash
# Create automated fix script
uv run python scripts/auto_add_error_handling.py --agents verifier modulation composer
```

### Step 3: Fix Remaining 6 Tests to Reach 20/20 (1 hour)

**Current**: 14/20 tests passing (70%)
**Target**: 20/20 tests passing (100%)

Based on the test improvement plan, the remaining 6 tests need:

1. **Add TDD Workflow Sections** (Phase 1 from test improvement plan)
   - Add to module docstrings:
   ```python
   """
   TDD Workflow:
   - 🔴 RED: Write failing test
   - 🟢 GREEN: Implement minimum code to pass
   - 🔄 REFACTOR: Clean up with tests as safety net
   """
   ```

2. **Add TDD Markers to Method Docstrings** (Phase 2 from test improvement plan)
   - Pattern for each test method:
   ```python
   def test_method(self):
       """Test description.

       🟢 GREEN: This test should pass with implemented method.
       """
   ```

3. **Add AAA Comments** (Phase 3 from test improvement plan - optional but helps)
   ```python
   # Arrange
   agent = Agent()

   # Act
   result = agent.method()

   # Assert
   assert result.success is True
   ```

**Script Approach**:
```bash
# Create automated fix script
uv run python scripts/auto_add_test_tdd_sections.py
```

### Step 4: Verify 100% Pass Rates (30 min)

1. **Re-run Both Validators**
   ```bash
   uv run python scripts/validators/agent_quality_validator.py
   uv run python tests/validators/test_quality_validator.py
   ```

2. **Check Reports**
   - `artifacts/report/agent_quality_report.md` → Expect 20/20 passing
   - `artifacts/report/test_quality_report.md` → Expect 20/20 passing

3. **Fix Any Remaining Issues**
   - Review errors/warnings in reports
   - Address manually if automated scripts missed anything

**Success Metrics**:
- ✅ Agent pass rate: 20/20 (100%)
- ✅ Test pass rate: 20/20 (100%)
- ✅ Average agent score: 90+/100
- ✅ Average test score: 90+/100
- ✅ All reports in correct artifact paths

---

## Phase 2: Track Generator MCP Integration (2 hours)

**Objective**: Connect track generator to live Ableton instance via MCP

### Prerequisites
- Ableton Live running
- AbletonMCP control surface enabled
- Port 9877 listening: `make check-port`

### Tasks

1. **Create MCP Client Wrapper** (30 min)
   - File: `live_set/lily_palmer/i_am_machine_v2/generators/mcp_client.py`
   - Wrap existing MCP tools for track generator use
   - Handle connection errors gracefully

2. **Update Track Generator** (30 min)
   - File: `live_set/lily_palmer/i_am_machine_v2/generators/track_generator.py`
   - Add real MCP client initialization
   - Test with simple 1-track config first

3. **Create Live Test Script** (30 min)
   - File: `live_set/lily_palmer/i_am_machine_v2/test_live_generation.py`
   - Generate example.json to Ableton
   - Verify track created with devices

4. **Generate Full Project** (30 min)
   - Use `i_am_machine_full.json` (16 tracks)
   - Monitor Ableton during generation
   - Document any issues

**Success Metric**: Full 16-track project generated successfully in Ableton

---

## Phase 3: TDD Markers for Tests (1-2 hours)

**Objective**: Add TDD workflow markers to test method docstrings

### Pattern

```python
def test_configure_wavetable_basic(self, mock_mcp_client):
    """Test basic wavetable configuration.

    🟢 GREEN: This test should pass with implemented method.

    Verifies that wavetable parameters are set correctly.
    """
```

### Implementation Strategy

1. **Create Auto-marker Script** (30 min)
   - File: `scripts/auto_add_tdd_markers.py`
   - Analyze test methods
   - Insert appropriate markers (🔴/🟢/🔄)

2. **Apply to High-Priority Tests** (30 min)
   - Start with tests that have complex logic
   - Focus on recently added tests
   - Target: 20+ methods marked

3. **Validate with Test Validator** (15 min)
   - Run test validator
   - Confirm marker detection works
   - Expect score improvement

**Success Metric**: 20+ test methods with TDD markers, validator confirms

---

## Phase 4: Error Handling Improvements (1-2 hours)

**Objective**: Add comprehensive error handling to agent methods

### Priority Agents (from improvement plan)

1. **verifier_agent.py** (9 methods) - 1 hour
2. **modulation_agent.py** (6 methods) - 30 min
3. **composer_agent.py** (6 methods) - 30 min

### Pattern

```python
async def method_name(self, track_index: int, **kwargs) -> AgentResult:
    """Method description."""
    try:
        mcp = self.get_mcp_client()
        if not mcp:
            self.log("Mock mode: skipping actual MCP call")
            return AgentResult(
                success=True,
                message="Mock: operation would succeed"
            )

        # Method logic
        result = await mcp.do_something(track_index, **kwargs)

        return AgentResult(
            success=True,
            message="Operation completed",
            data=result
        )

    except Exception as e:
        self.log(f"Error in method_name: {e}")
        return AgentResult(
            success=False,
            message=f"Failed: {e}"
        )
```

### Implementation

1. **Create Auto-fix Script** (30 min)
   - File: `scripts/auto_add_error_handling.py`
   - Detect methods without try/except
   - Wrap method bodies

2. **Apply to Priority Agents** (1 hour)
   - Start with verifier_agent
   - Then modulation_agent
   - Finally composer_agent

3. **Re-run Agent Validator** (15 min)
   - Expect error handling score improvement
   - Target: 18+/20 error handling score

**Success Metric**: 3 priority agents at 90+ overall score

---

## Phase 5: Documentation & Polish (30 min)

**Objective**: Final documentation updates

### Tasks

1. **Update Main README.md**
   - Add "Quality Validation" section
   - Document validator commands
   - Link to improvement plans

2. **Create VALIDATOR_GUIDE.md**
   - How to run validators
   - How to interpret results
   - How to fix common issues

3. **Update CHANGELOG.md**
   - Document all Phase 1-5 changes
   - Note quick wins completion
   - Version bump considerations

**Success Metric**: Clear documentation for future contributors

---

## Timeline

| Phase | Task | Time | Running Total |
|-------|------|------|---------------|
| 1a | Validator Paths | 30 min | 30 min |
| 1b | Fix 3 Remaining Agents | 1 hour | 1.5 hours |
| 1c | Fix 6 Remaining Tests | 1 hour | 2.5 hours |
| 1d | Verify 100% Pass Rates | 30 min | **3 hours** |
| 2 | MCP Integration | 2 hours | 5 hours |
| 3 | TDD Markers (Advanced) | 1-2 hours | 7 hours |
| 4 | Error Handling (Advanced) | 1-2 hours | 9 hours |
| 5 | Documentation | 30 min | 9.5 hours |

**Phase 1 Only (Recommended)**: 3 hours → 100% pass rates achieved
**Phase 1-2 (MCP Integration)**: 5 hours → Production ready
**Complete Polish**: 9.5 hours → All optional improvements

---

## Success Criteria

**Phase 1 Complete (3 hours)**:
- ✅ Validators report to correct paths
- ✅ 20/20 agents passing (100%)
- ✅ 20/20 tests passing (100%)
- ✅ Average scores 90+/100

**Phases 1-2 Complete (5 hours)**:
- ✅ All Phase 1 criteria
- ✅ Track generator works with live Ableton
- ✅ Full 16-track project generated successfully

**Full Polish (9.5 hours)**:
- ✅ All Phases 1-2 criteria
- ✅ Advanced TDD markers
- ✅ Advanced error handling
- ✅ Complete documentation

---

## High-Value Quick Wins

**Recommended Path**: Complete Phase 1 (3 hours) for maximum value

This achieves:
- 100% validator pass rates (industry standard)
- Production-ready code quality
- Clear baseline for future work

**If extremely time-limited**, focus on:

1. **Validator Path Update** (30 min) - Must have
2. **Fix 3 Failing Agents** (1 hour) - High impact
3. **Fix 6 Failing Tests** (1 hour) - High impact

**Total**: 2.5 hours for 95% of Phase 1 value

---

## Commands

```bash
# Phase 1
uv run python scripts/validators/agent_quality_validator.py
uv run python tests/validators/test_quality_validator.py

# Phase 2
make check-port
uv run python live_set/lily_palmer/i_am_machine_v2/test_live_generation.py

# Phase 3
uv run python scripts/auto_add_tdd_markers.py

# Phase 4
uv run python scripts/auto_add_error_handling.py
```

---

## Notes

- All these phases are **optional** - the core system is complete
- Phases can be done independently
- Focus on high-value quick wins if time constrained
- Document any issues encountered for future improvement
