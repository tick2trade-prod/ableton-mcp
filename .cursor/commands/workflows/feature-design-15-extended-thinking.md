# Feature Design: Extended Thinking Integration

**Feature ID**: 15
**Priority**: P2 (Medium)
**Impact**: Quality Improvement (25%), Debugging Improvement (40%), Token Efficiency (10%)
**Complexity**: Medium (3-5 days)

---

## Problem Statement

Current thinking tool is stubbed and agents lack visible reasoning:
- `thinking_tool.py` has placeholder implementation
- Agents make decisions without showing thought process
- No way to debug agent reasoning
- Complex decisions lack justification
- Users can't understand why agent chose a solution

### Current Stubbed Implementation

```python
# app/server/tools/thinking_tool.py (258 lines, but mostly empty)
async def think(prompt: str) -> str:
    """Extended thinking - STUBBED.

    TODO: Integrate with Claude's extended thinking mode or implement
    structured reasoning blocks.
    """
    # Just returns empty string - no actual thinking
    return ""
```

**Problems**:

1. **No Visible Reasoning**:
   - Agent generates code without explanation
   - Users don't know why agent made choices
   - Hard to trust agent decisions

2. **Debugging Nightmare**:
   - When agent fails, no way to see thought process
   - Can't identify where reasoning went wrong
   - Requires re-running entire workflow to debug

3. **Lost Insights**:
   - Agent may have considered multiple approaches
   - Trade-off analysis not visible
   - Alternative solutions not documented

4. **Quality Issues**:
   - Without structured reasoning, agents skip important considerations
   - No verification step before acting
   - Miss edge cases due to hasty decisions

---

## Proposed Solution

Integrate **Extended Thinking** properly to:
1. Enable Claude's extended thinking mode for complex tasks
2. Capture reasoning blocks in structured format
3. Display thinking process to users
4. Use thinking for plan validation and debugging
5. Improve decision quality through explicit reasoning

---

## Architecture

### Updated Tool: `ExtendedThinkingTool`

**Location**: `app/server/tools/thinking_tool.py` (replace stub)

**Responsibilities**:
- Invoke Claude's extended thinking mode
- Structure thinking into phases (analyze, evaluate, decide)
- Format thinking blocks for display
- Cache thinking for debugging
- Integrate with planning and code generation

**Key Methods**:

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class ThinkingBlock:
    """Structured thinking output."""
    phase: Literal["analyze", "evaluate", "decide", "verify"]
    content: str
    duration_ms: int
    confidence: float  # 0-1

@dataclass
class ThinkingResult:
    """Complete thinking session."""
    blocks: list[ThinkingBlock]
    conclusion: str
    alternatives_considered: list[str]
    risks_identified: list[str]
    total_thinking_time_ms: int

class ExtendedThinkingTool:
    """Extended thinking for complex reasoning tasks."""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.thinking_cache = {}

    async def think(
        self,
        task: str,
        context: str = "",
        thinking_budget: int = 10000,  # Max thinking tokens
        require_phases: list[str] | None = None
    ) -> ThinkingResult:
        """Perform extended thinking on a task.

        Args:
            task: The problem/question to think about
            context: Additional context for reasoning
            thinking_budget: Max tokens for thinking (default 10K)
            require_phases: Force specific thinking phases

        Returns:
            Structured thinking result with conclusion
        """
        prompt = self._create_thinking_prompt(task, context, require_phases)

        # Call Claude with extended thinking enabled
        response = await self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=thinking_budget,
            thinking={
                "type": "enabled",
                "budget_tokens": thinking_budget
            },
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Parse thinking blocks from response
        result = self._parse_thinking_response(response)

        # Cache for debugging
        cache_key = hashlib.sha256(task.encode()).hexdigest()
        self.thinking_cache[cache_key] = result

        return result

    def _create_thinking_prompt(
        self,
        task: str,
        context: str,
        require_phases: list[str] | None
    ) -> str:
        """Create structured prompt for thinking."""

        phases_instruction = ""
        if require_phases:
            phases_instruction = f"""
Required thinking phases:
{chr(10).join(f'- {phase}' for phase in require_phases)}
"""

        return f"""You are working on this task:

{task}

Context:
{context}

{phases_instruction}

Think through this carefully before providing your conclusion. Consider:

1. **Analyze**: Break down the problem
   - What are the key components?
   - What constraints exist?
   - What information is missing?

2. **Evaluate**: Consider different approaches
   - What are 2-3 viable solutions?
   - What are the trade-offs of each?
   - What are the risks?

3. **Decide**: Choose the best approach
   - Which solution best meets requirements?
   - Why is this better than alternatives?
   - What edge cases need handling?

4. **Verify**: Sanity check your decision
   - Does this solve the original problem?
   - Are there any obvious flaws?
   - What could go wrong?

After thinking, provide your conclusion with a clear recommendation.
"""

    def _parse_thinking_response(self, response) -> ThinkingResult:
        """Parse Claude's response into structured thinking."""

        blocks = []
        alternatives = []
        risks = []
        total_time = 0

        # Extract thinking blocks (Claude returns these in response)
        for content_block in response.content:
            if content_block.type == "thinking":
                # Parse thinking text into phases
                thinking_text = content_block.thinking

                # Heuristic: split by phase keywords
                phase_blocks = self._split_into_phases(thinking_text)

                for phase, text in phase_blocks:
                    block = ThinkingBlock(
                        phase=phase,
                        content=text,
                        duration_ms=0,  # Not exposed by API
                        confidence=self._estimate_confidence(text)
                    )
                    blocks.append(block)

                    # Extract alternatives and risks
                    if phase == "evaluate":
                        alternatives.extend(self._extract_alternatives(text))
                    elif phase == "decide":
                        risks.extend(self._extract_risks(text))

            elif content_block.type == "text":
                conclusion = content_block.text

        return ThinkingResult(
            blocks=blocks,
            conclusion=conclusion,
            alternatives_considered=alternatives,
            risks_identified=risks,
            total_thinking_time_ms=total_time
        )

    def _split_into_phases(self, thinking_text: str) -> list[tuple[str, str]]:
        """Split thinking text into phases."""
        phases = []

        # Look for phase markers
        markers = {
            "analyze": ["analyzing", "break down", "understanding"],
            "evaluate": ["evaluating", "considering", "comparing", "alternatives"],
            "decide": ["deciding", "choosing", "best approach", "solution"],
            "verify": ["verifying", "checking", "sanity check", "validation"]
        }

        current_phase = "analyze"
        current_text = []

        for line in thinking_text.split("\n"):
            line_lower = line.lower()

            # Check if line indicates phase transition
            new_phase = None
            for phase, keywords in markers.items():
                if any(kw in line_lower for kw in keywords):
                    new_phase = phase
                    break

            if new_phase and new_phase != current_phase:
                # Save current phase
                if current_text:
                    phases.append((current_phase, "\n".join(current_text)))

                # Start new phase
                current_phase = new_phase
                current_text = [line]
            else:
                current_text.append(line)

        # Save final phase
        if current_text:
            phases.append((current_phase, "\n".join(current_text)))

        return phases

    def format_for_display(self, result: ThinkingResult) -> str:
        """Format thinking result for user display."""

        output = ["## 🧠 Extended Thinking Process\n"]

        for i, block in enumerate(result.blocks, 1):
            phase_emoji = {
                "analyze": "🔍",
                "evaluate": "⚖️",
                "decide": "✅",
                "verify": "🔎"
            }

            emoji = phase_emoji.get(block.phase, "💭")
            output.append(f"### {emoji} Phase {i}: {block.phase.title()}\n")
            output.append(f"**Confidence:** {block.confidence:.0%}\n")
            output.append(block.content)
            output.append("\n---\n")

        if result.alternatives_considered:
            output.append("### 🔀 Alternatives Considered\n")
            for alt in result.alternatives_considered:
                output.append(f"- {alt}")
            output.append("\n")

        if result.risks_identified:
            output.append("### ⚠️ Risks Identified\n")
            for risk in result.risks_identified:
                output.append(f"- {risk}")
            output.append("\n")

        output.append("### 🎯 Conclusion\n")
        output.append(result.conclusion)

        return "\n".join(output)
```

---

## Use Cases

### Use Case 1: Plan Validation

**Problem**: Need to validate implementation plan before executing

**Before (No Thinking)**:
```python
# Just executes plan without validation
plan = await planner.create_plan(feature_request)
result = await executor.execute(plan)  # Hope it works!
```

**After (With Thinking)**:
```python
thinking_tool = ExtendedThinkingTool(api_key)

# Think through the plan
thinking_result = await thinking_tool.think(
    task=f"Validate this implementation plan: {plan}",
    context=f"Feature request: {feature_request}",
    require_phases=["analyze", "evaluate", "verify"]
)

# Display thinking process
print(thinking_tool.format_for_display(thinking_result))

# Check if plan is sound
if "major risk" in thinking_result.conclusion.lower():
    print("⚠️  Plan has risks, revising...")
    plan = await planner.revise_plan(plan, thinking_result.risks_identified)

# Execute validated plan
result = await executor.execute(plan)
```

**Output Example**:
```
## 🧠 Extended Thinking Process

### 🔍 Phase 1: Analyze
**Confidence:** 85%

The plan proposes implementing user authentication with JWT tokens.
Key components:
- JWT generation and validation
- Login/logout endpoints
- Middleware for protected routes
- User model with password hashing

Missing considerations:
- Token refresh strategy not specified
- Password reset flow absent
- Rate limiting not mentioned

---

### ⚖️ Phase 2: Evaluate
**Confidence:** 75%

Alternative 1: Session-based auth
- Pros: Simpler, no token management
- Cons: Less scalable, requires shared session store

Alternative 2: OAuth2 with external provider
- Pros: No password storage, proven security
- Cons: Dependency on third party, more complex

Alternative 3: JWT (proposed)
- Pros: Stateless, scalable, flexible
- Cons: Token revocation tricky, needs refresh strategy

---

### ✅ Phase 3: Decide
**Confidence:** 80%

JWT approach is appropriate given requirements. However, plan needs:
1. Add token refresh mechanism
2. Add password reset flow
3. Add rate limiting on auth endpoints

---

### 🔎 Phase 4: Verify
**Confidence:** 90%

With additions, plan will work. Edge cases to handle:
- Concurrent logins from same user
- Token expiration during active session
- Password complexity requirements

---

### 🔀 Alternatives Considered
- Session-based authentication
- OAuth2 delegation

### ⚠️ Risks Identified
- Token revocation strategy missing
- No mention of rate limiting
- Password reset flow absent

### 🎯 Conclusion

Plan is solid but incomplete. Add token refresh, password reset, and rate
limiting before proceeding. Estimated additions: +2 hours.
```

**Benefit**: Catch plan issues before wasting time implementing

### Use Case 2: Code Generation Decision

**Problem**: Agent needs to choose between multiple implementation approaches

**Before**:
```python
# Agent silently picks first approach that comes to mind
code = await code_gen.generate("implement caching")
```

**After**:
```python
thinking_tool = ExtendedThinkingTool(api_key)

# Think through implementation approaches
thinking = await thinking_tool.think(
    task="Choose best caching implementation for this use case",
    context=f"""
    Use case: Cache API responses for 5 minutes
    Traffic: 1000 req/min
    Budget: Low
    Existing stack: Python, FastAPI
    """,
    require_phases=["analyze", "evaluate", "decide"]
)

# Show reasoning to user
print(thinking_tool.format_for_display(thinking))

# Generate code based on decision
code = await code_gen.generate(
    f"Implement caching using approach: {thinking.conclusion}"
)
```

**Output**:
```
### ⚖️ Phase 2: Evaluate

Option 1: Redis
- Pros: Fast, distributed, feature-rich
- Cons: External dependency, hosting cost, overkill for simple case

Option 2: In-memory LRU cache
- Pros: No dependencies, free, fast for single instance
- Cons: Not distributed, lost on restart

Option 3: File-based cache
- Pros: Persistent, no dependencies
- Cons: Slower, file I/O overhead

### 🎯 Conclusion

For this use case, in-memory LRU cache (functools.lru_cache) is best:
- Low traffic (1000 req/min is manageable in-memory)
- Low budget (no external service)
- Simple to implement
- Sufficient for 5-minute TTL

Use Redis only if traffic grows >10K req/min or need distributed caching.
```

**Benefit**: Better implementation choices, documented reasoning

### Use Case 3: Debugging Failed Workflow

**Problem**: Workflow failed, need to understand where reasoning went wrong

**After**:
```python
# Retrieve cached thinking from failed workflow
thinking_cache = thinking_tool.thinking_cache

for cache_key, thinking_result in thinking_cache.items():
    print(f"\n=== Task: {cache_key[:8]} ===")
    print(thinking_tool.format_for_display(thinking_result))

# Output shows exact reasoning at each decision point
# Can identify where logic failed
```

**Benefit**: Faster debugging, understand agent decisions

### Use Case 4: Learning from Agent

**Problem**: New developer wants to understand how agent approaches problems

**After**:
```python
# Enable thinking display for educational purposes
thinking_result = await thinking_tool.think(
    task="Design a REST API for blog posts",
    context="FastAPI, PostgreSQL, JWT auth"
)

# Student sees expert-level reasoning process
print(thinking_tool.format_for_display(thinking_result))

# Learn from agent's thought process:
# - How to break down design problems
# - Trade-offs to consider
# - Edge cases to think about
```

**Benefit**: Educational value, learn agent's reasoning patterns

---

## Integration Points

### 1. Update Planner Agent

**Add thinking before planning**:
```python
# app/server/agents/planner.py
class PlannerAgent:
    def __init__(self):
        self.thinking_tool = ExtendedThinkingTool(api_key)

    async def create_plan(self, feature_request: str) -> Plan:
        # Think through planning approach
        thinking = await self.thinking_tool.think(
            task=f"Plan how to implement: {feature_request}",
            context=await self._get_context(feature_request),
            require_phases=["analyze", "evaluate", "decide"]
        )

        # Use thinking to guide plan creation
        plan = await self._generate_plan_from_thinking(
            feature_request,
            thinking
        )

        # Attach thinking for debugging
        plan.reasoning = thinking

        return plan
```

### 2. Update Code Generator

**Add thinking for complex generation**:
```python
# app/generation/code_generator.py
async def generate_complex(self, prompt: str, complexity: str = "high") -> str:
    if complexity == "high":
        # Use thinking for complex tasks
        thinking = await thinking_tool.think(
            task=f"Design implementation approach for: {prompt}",
            require_phases=["analyze", "evaluate", "decide", "verify"]
        )

        # Generate based on thinking
        context = f"""
        Thinking process:
        {thinking.conclusion}

        Implementation requirements:
        {prompt}
        """

        return await self._generate_with_context(prompt, context)
    else:
        # Simple generation without thinking
        return await self._generate(prompt)
```

### 3. New Skill: Plan Validation

**Create skill that validates plans using thinking**:
```python
# app/server/skills/plan_validation.py
async def validate_plan_with_thinking(plan: Plan) -> ValidationResult:
    """Validate plan using extended thinking."""

    thinking_tool = ExtendedThinkingTool(api_key)

    thinking = await thinking_tool.think(
        task=f"Validate this implementation plan:\n{plan.to_markdown()}",
        require_phases=["analyze", "evaluate", "verify"]
    )

    # Extract validation result
    issues = thinking.risks_identified
    suggestions = thinking.alternatives_considered

    is_valid = "approved" in thinking.conclusion.lower()

    return ValidationResult(
        is_valid=is_valid,
        issues=issues,
        suggestions=suggestions,
        thinking_process=thinking
    )
```

### 4. Update Orchestrator

**Add thinking display to workflow**:
```python
# app/server/orchestrator.py
async def execute_workflow(
    feature_name: str,
    show_thinking: bool = True  # New parameter
) -> WorkflowResult:

    if show_thinking:
        # Display thinking at key decision points
        print("🧠 Planning approach...")
        planning_thinking = await get_cached_thinking("plan")
        print(thinking_tool.format_for_display(planning_thinking))

        print("\n🧠 Implementation design...")
        impl_thinking = await get_cached_thinking("implement")
        print(thinking_tool.format_for_display(impl_thinking))

    result = await self._execute_workflow_impl(feature_name)
    return result
```

---

## Performance Considerations

### Thinking Budget Management

```python
# Different tasks need different thinking budgets

THINKING_BUDGETS = {
    "simple": 1000,      # Simple yes/no decisions
    "medium": 5000,      # Standard tasks
    "complex": 10000,    # Architecture decisions
    "critical": 20000,   # Mission-critical decisions
}

async def think_with_budget(task: str, complexity: str = "medium") -> ThinkingResult:
    budget = THINKING_BUDGETS[complexity]

    return await thinking_tool.think(
        task=task,
        thinking_budget=budget
    )
```

### Caching Thinking Results

```python
# Cache thinking for repeated queries

def get_cached_thinking(task: str) -> ThinkingResult | None:
    cache_key = hashlib.sha256(task.encode()).hexdigest()

    if cache_key in thinking_tool.thinking_cache:
        return thinking_tool.thinking_cache[cache_key]

    return None

async def think_with_cache(task: str) -> ThinkingResult:
    cached = get_cached_thinking(task)
    if cached:
        return cached

    result = await thinking_tool.think(task)
    return result
```

---

## Implementation Plan

### Phase 1: Core Integration (2 days)
1. Update `thinking_tool.py` with extended thinking API
2. Implement `ThinkingResult` dataclass
3. Add phase parsing logic
4. Basic formatting for display
5. Unit tests

### Phase 2: Structured Reasoning (1.5 days)
1. Implement required phases
2. Add alternative extraction
3. Add risk extraction
4. Add confidence estimation
5. Integration tests

### Phase 3: Agent Integration (1 day)
1. Update Planner agent
2. Update Code Generator
3. Add to Orchestrator
4. Display thinking in workflows

### Phase 4: Caching & Optimization (0.5 days)
1. Add thinking cache
2. Add budget management
3. Performance tests
4. Documentation

---

## Testing Strategy

### Unit Tests

```python
def test_thinking_phases():
    thinking_tool = ExtendedThinkingTool(api_key)

    result = await thinking_tool.think(
        task="Should we use Redis or in-memory cache?",
        require_phases=["analyze", "evaluate", "decide"]
    )

    # Verify all required phases present
    phases = {block.phase for block in result.blocks}
    assert "analyze" in phases
    assert "evaluate" in phases
    assert "decide" in phases

def test_alternative_extraction():
    thinking_text = """
    Evaluating options:
    1. Use Redis for caching
    2. Use in-memory LRU cache
    3. Use file-based cache
    """

    alternatives = thinking_tool._extract_alternatives(thinking_text)

    assert len(alternatives) >= 2
    assert "Redis" in alternatives[0]
    assert "LRU" in alternatives[1]
```

### Integration Tests

```python
@pytest.mark.integration
async def test_plan_validation_with_thinking():
    plan = Plan(
        steps=[
            "Create user model",
            "Implement JWT auth",
            "Add login endpoint"
        ]
    )

    validation = await validate_plan_with_thinking(plan)

    # Should identify missing steps
    assert len(validation.issues) > 0
    assert any("password reset" in issue.lower() for issue in validation.issues)
```

---

## Success Metrics

**Must Have**:
- ✅ 25% quality improvement (catch issues before implementation)
- ✅ 40% faster debugging (visible reasoning)
- ✅ Thinking cache hit rate >60%
- ✅ Phases correctly identified >90% of time

**Nice to Have**:
- 📊 User satisfaction with reasoning quality
- 🎯 Reduction in "why did agent do X?" questions
- 🔄 Educational value for junior developers

---

## Risks & Mitigations

### Risk 1: Thinking Token Cost
**Problem**: Extended thinking uses tokens
**Mitigation**:
- Cache thinking results
- Use thinking only for complex tasks
- Configurable budgets

### Risk 2: Slower Response
**Problem**: Thinking adds latency
**Mitigation**:
- Make thinking optional (default off for simple tasks)
- Show thinking progress to user
- Async thinking (don't block generation)

### Risk 3: Poor Phase Detection
**Problem**: May not correctly split thinking into phases
**Mitigation**:
- Improve prompt to guide phase structure
- Add phase markers in prompt
- Manual phase extraction as fallback

---

## Related Features

- Feature 11: Context Caching (cache thinking results)
- Feature 12: Batch Processing (parallel thinking for multiple tasks)
- Plan Feedback System (use thinking to validate plans)

---

**Status**: Ready for Implementation
**Assigned**: TBD
**Target Release**: v2.2
