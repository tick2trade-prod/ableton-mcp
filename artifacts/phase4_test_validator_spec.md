# Phase 4: Test Quality Validation - Pydantic Validator Specification

## Overview

Create a Pydantic-based validator to enforce TDD standards and docstring quality across `tests/agents/` to maintain high code standards using Ableton Manual references.

## Task 1: Create Pydantic Test Validator (1 day)

### File: `tests/validators/test_quality_validator.py`

### Pydantic Models

```python
"""Test quality validator using Pydantic models.

Validates:
- TDD markers (🔴 RED, 🟢 GREEN, 🔄 REFACTOR)
- Docstring format (module, class, method)
- Ableton Manual references (Section X.Y, page numbers)
- Test structure (Arrange/Act/Assert)
- Fixture usage
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional
import ast
import re
from pathlib import Path


class AbletonReference(BaseModel):
    """Ableton Manual reference validation."""
    
    section: str = Field(..., pattern=r"^\d+\.\d+(\.\d+)?$")  # e.g., "28.9.2"
    title: str = Field(..., min_length=1)
    page: int = Field(..., gt=0, lt=1000)
    
    @validator("section")
    def validate_section_format(cls, v):
        """Ensure section follows X.Y or X.Y.Z format."""
        parts = v.split(".")
        if not (2 <= len(parts) <= 3):
            raise ValueError(f"Section must be X.Y or X.Y.Z format, got: {v}")
        return v
    
    @property
    def reference_string(self) -> str:
        """Format as: 'Section 28.9.2 "Title" (page 521)'"""
        return f'Section {self.section} "{self.title}" (page {self.page})'


class ModuleDocstring(BaseModel):
    """Module-level docstring validation."""
    
    description: str = Field(..., min_length=10)
    references: list[AbletonReference] = Field(..., min_items=1, max_items=3)
    has_tdd_workflow: bool = Field(default=True)
    tdd_markers: list[Literal["RED", "GREEN", "REFACTOR"]] = Field(
        default_factory=lambda: ["RED", "GREEN", "REFACTOR"]
    )
    
    @validator("has_tdd_workflow")
    def validate_tdd_section(cls, v, values):
        """Ensure TDD workflow section exists."""
        if not v:
            raise ValueError("Module docstring must include TDD Workflow section")
        return v


class ClassDocstring(BaseModel):
    """Class-level docstring validation."""
    
    description: str = Field(..., min_length=10)
    references: list[AbletonReference] = Field(default_factory=list, max_items=2)
    excerpt: Optional[str] = Field(None, min_length=20)


class MethodDocstring(BaseModel):
    """Method-level docstring validation."""
    
    description: str = Field(..., min_length=10)
    references: list[AbletonReference] = Field(default_factory=list, max_items=2)
    tdd_marker: Optional[Literal["RED", "GREEN", "REFACTOR"]] = None
    
    @validator("tdd_marker")
    def validate_marker_in_docstring(cls, v, values):
        """Check if TDD marker emoji present."""
        if v and v not in ["RED", "GREEN", "REFACTOR"]:
            raise ValueError(f"Invalid TDD marker: {v}")
        return v


class TestMethod(BaseModel):
    """Individual test method validation."""
    
    name: str = Field(..., pattern=r"^test_[a-z_]+$")
    docstring: MethodDocstring
    has_arrange: bool = Field(default=True)
    has_act: bool = Field(default=True)
    has_assert: bool = Field(default=True)
    uses_fixtures: list[str] = Field(default_factory=list)
    
    @validator("uses_fixtures")
    def validate_fixture_names(cls, v):
        """Ensure only valid fixtures used."""
        valid_fixtures = {"mock_mcp_client", "mock_agent_logger"}
        invalid = set(v) - valid_fixtures
        if invalid:
            raise ValueError(f"Invalid fixtures: {invalid}")
        return v


class TestClass(BaseModel):
    """Test class validation."""
    
    name: str = Field(..., pattern=r"^Test[A-Za-z]+$")
    docstring: ClassDocstring
    methods: list[TestMethod] = Field(..., min_items=1)


class TestModule(BaseModel):
    """Entire test module validation."""
    
    filepath: Path
    filename: str = Field(..., pattern=r"^test_[a-z_]+_agent\.py$")
    docstring: ModuleDocstring
    classes: list[TestClass] = Field(..., min_items=1)
    imports_pytest: bool = Field(default=True)
    imports_mock: bool = Field(default=True)
    
    @validator("imports_pytest")
    def validate_pytest_import(cls, v):
        """Ensure pytest is imported."""
        if not v:
            raise ValueError("Must import pytest")
        return v


class ValidationResult(BaseModel):
    """Validation result for a test file."""
    
    filepath: Path
    passed: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    score: float = Field(ge=0.0, le=100.0)
    
    @property
    def status(self) -> str:
        """Return PASS/FAIL status."""
        return "✅ PASS" if self.passed else "❌ FAIL"
```

### Validator Class

```python
class TestQualityValidator:
    """Validate test files against TDD and docstring standards."""
    
    def __init__(self, test_dir: Path):
        self.test_dir = test_dir
        self.results: list[ValidationResult] = []
    
    def parse_file(self, filepath: Path) -> Optional[TestModule]:
        """Parse test file into Pydantic model."""
        try:
            with open(filepath, "r") as f:
                tree = ast.parse(f.read())
            
            # Extract module docstring
            module_docstring = ast.get_docstring(tree)
            if not module_docstring:
                raise ValueError("Missing module docstring")
            
            # Parse docstring for references
            references = self._extract_references(module_docstring)
            
            # Extract classes and methods
            classes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_doc = ast.get_docstring(node)
                    methods = [
                        self._parse_method(m)
                        for m in node.body
                        if isinstance(m, ast.FunctionDef) and m.name.startswith("test_")
                    ]
                    classes.append(
                        TestClass(
                            name=node.name,
                            docstring=self._parse_class_docstring(class_doc),
                            methods=methods
                        )
                    )
            
            return TestModule(
                filepath=filepath,
                filename=filepath.name,
                docstring=self._parse_module_docstring(module_docstring),
                classes=classes,
            )
        
        except Exception as e:
            return None
    
    def _extract_references(self, docstring: str) -> list[AbletonReference]:
        """Extract Ableton Manual references from docstring."""
        # Pattern: Section 28.9.2 "Compressor Tips" (page 521)
        pattern = r'Section\s+([\d\.]+)\s+"([^"]+)"\s+\(page\s+(\d+)\)'
        matches = re.findall(pattern, docstring)
        
        return [
            AbletonReference(section=section, title=title, page=int(page))
            for section, title, page in matches
        ]
    
    def validate_file(self, filepath: Path) -> ValidationResult:
        """Validate a single test file."""
        errors = []
        warnings = []
        score = 100.0
        
        try:
            test_module = self.parse_file(filepath)
            
            if not test_module:
                return ValidationResult(
                    filepath=filepath,
                    passed=False,
                    errors=["Failed to parse file"],
                    score=0.0
                )
            
            # Validate module docstring
            if len(test_module.docstring.references) < 1:
                errors.append("Module missing Ableton Manual references")
                score -= 20
            
            # Validate classes
            for cls in test_module.classes:
                if len(cls.methods) == 0:
                    warnings.append(f"Class {cls.name} has no test methods")
                    score -= 5
                
                # Validate methods
                for method in cls.methods:
                    if not method.has_arrange:
                        errors.append(f"{method.name}: Missing Arrange section")
                        score -= 10
                    
                    if not method.has_act:
                        errors.append(f"{method.name}: Missing Act section")
                        score -= 10
                    
                    if not method.has_assert:
                        errors.append(f"{method.name}: Missing Assert section")
                        score -= 10
                    
                    if not method.docstring.tdd_marker:
                        warnings.append(f"{method.name}: Missing TDD marker")
                        score -= 5
            
            passed = len(errors) == 0 and score >= 70.0
            
            return ValidationResult(
                filepath=filepath,
                passed=passed,
                errors=errors,
                warnings=warnings,
                score=max(0.0, score)
            )
        
        except Exception as e:
            return ValidationResult(
                filepath=filepath,
                passed=False,
                errors=[str(e)],
                score=0.0
            )
    
    def validate_all(self) -> list[ValidationResult]:
        """Validate all test files in directory."""
        test_files = sorted(self.test_dir.glob("test_*_agent.py"))
        
        for filepath in test_files:
            result = self.validate_file(filepath)
            self.results.append(result)
        
        return self.results
    
    def generate_report(self) -> str:
        """Generate markdown report."""
        report_lines = ["# Test Quality Validation Report\n"]
        
        # Summary
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        avg_score = sum(r.score for r in self.results) / total if total > 0 else 0
        
        report_lines.append(f"**Total Tests**: {total}")
        report_lines.append(f"**Passed**: {passed}/{total} ({passed/total*100:.1f}%)")
        report_lines.append(f"**Average Score**: {avg_score:.1f}/100\n")
        
        # Per-file results
        report_lines.append("## Test Files\n")
        
        for result in sorted(self.results, key=lambda r: r.score, reverse=True):
            report_lines.append(f"### {result.filepath.name} - {result.status}")
            report_lines.append(f"**Score**: {result.score:.1f}/100\n")
            
            if result.errors:
                report_lines.append("**Errors**:")
                for error in result.errors:
                    report_lines.append(f"- ❌ {error}")
                report_lines.append("")
            
            if result.warnings:
                report_lines.append("**Warnings**:")
                for warning in result.warnings:
                    report_lines.append(f"- ⚠️ {warning}")
                report_lines.append("")
        
        return "\n".join(report_lines)


# Main execution
if __name__ == "__main__":
    from pathlib import Path
    
    validator = TestQualityValidator(Path("tests/agents"))
    results = validator.validate_all()
    
    # Generate report
    report = validator.generate_report()
    
    # Save to artifacts
    output_path = Path("artifacts/test_quality_report.md")
    output_path.write_text(report)
    
    print(f"✅ Validation complete: {output_path}")
    print(f"Passed: {sum(1 for r in results if r.passed)}/{len(results)}")
```

---

## Task 2: Run Validator (0.5 day)

### Command
```bash
uv run python tests/validators/test_quality_validator.py
```

### Expected Output Files
1. `artifacts/test_quality_report.md` - Detailed pass/fail per test file
2. Console output with summary statistics

### Report Format
```markdown
# Test Quality Validation Report

**Total Tests**: 15
**Passed**: 10/15 (66.7%)
**Average Score**: 78.3/100

## Test Files

### test_effects_chain_agent.py - ✅ PASS
**Score**: 95.0/100

**Warnings**:
- ⚠️ test_create_effect_rack_no_mcp_client: Missing TDD marker

### test_composer_agent.py - ❌ FAIL
**Score**: 65.0/100

**Errors**:
- ❌ Module missing Ableton Manual references
- ❌ test_create_midi_pattern: Missing Arrange section

**Warnings**:
- ⚠️ Class TestComposerAgent has no excerpt in docstring
```

---

## Task 3: Create Recommendations (0.5 day)

### Analysis Criteria
1. **Common Issues**: Most frequent errors/warnings
2. **Priority**: HIGH (blocking), MEDIUM (important), LOW (nice-to-have)
3. **Effort**: Estimated time to fix
4. **Impact**: Effect on code quality

### Output: `artifacts/test_improvement_plan.md`

```markdown
# Test Improvement Action Plan

## Summary
- **Total Issues**: 47
- **HIGH Priority**: 12
- **MEDIUM Priority**: 23
- **LOW Priority**: 12

## Common Issues

### 1. Missing Ableton Manual References (HIGH)
**Affected Files**: 5
- test_composer_agent.py
- test_mixer_agent.py
- test_modulation_agent.py
- test_verifier_agent.py
- test_vocals_agent.py

**Action**: Add module-level references using pattern from test_percussion_agent.py
**Estimated Time**: 2 hours
**Priority**: HIGH

### 2. Missing TDD Markers in Method Docstrings (MEDIUM)
**Affected Files**: 8
**Example**:
```python
def test_example(self, mock_mcp_client):
    """Test description.
    
    🔴 RED: This test should fail - method doesn't exist yet
    """
```

**Action**: Add 🔴/🟢/🔄 markers to all test method docstrings
**Estimated Time**: 1 hour
**Priority**: MEDIUM

### 3. Missing Arrange/Act/Assert Comments (MEDIUM)
**Affected Files**: 6

**Action**: Add AAA comments in test bodies
**Estimated Time**: 1.5 hours
**Priority**: MEDIUM

## Implementation Order

### Phase 1: Critical (Week 1)
1. Add Ableton Manual references to all modules
2. Fix missing docstrings

### Phase 2: Important (Week 2)
1. Add TDD markers to methods
2. Add AAA comments to test bodies

### Phase 3: Polish (Week 3)
1. Add excerpts to class docstrings
2. Improve reference specificity
```

---

## Integration with ableton_codegen MCP

### Verify Manual References
```python
def verify_reference_with_mcp(reference: AbletonReference) -> bool:
    """Verify reference exists in Ableton Manual using MCP."""
    from mcp_ableton_codegen import search_ableton_docs
    
    query = f"{reference.title} page {reference.page}"
    results = search_ableton_docs(query, top_k=3)
    
    # Check if any result matches page number
    for result in results.get("results", []):
        if result.get("page_num") == reference.page:
            return True
    
    return False
```

---

## Success Criteria

✅ Validator runs without errors  
✅ All 15 existing test files validated  
✅ Quality report generated  
✅ Improvement plan created  
✅ At least 70% of tests pass validation  
✅ Clear action items for failing tests

**Total Time**: 2 days (1 day validator + 0.5 day run + 0.5 day recommendations)
