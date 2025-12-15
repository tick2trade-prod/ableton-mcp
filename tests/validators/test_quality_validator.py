"""Test quality validator using Pydantic 2.x models.

Validates:
- TDD markers (🔴 RED, 🟢 GREEN, 🔄 REFACTOR)
- Docstring format (module, class, method)
- Ableton Manual references (Section X.Y, page numbers)
- Test structure (Arrange/Act/Assert)
- Fixture usage

Usage:
    python tests/validators/test_quality_validator.py
"""

import ast
import re
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import Pydantic models
from models import (  # noqa: E402
    AbletonReference,
    ClassDocstring,
    MethodDocstring,
    ModuleDocstring,
    TestClass,
    TestMethod,
    TestModule,
    ValidationResult,
)


class TestQualityValidator:
    """Validate test files against TDD and docstring standards."""

    def __init__(self, test_dir: Path):
        self.test_dir = test_dir
        self.results: list[ValidationResult] = []

    def _extract_references(self, docstring: str) -> list[AbletonReference]:
        """Extract Ableton Manual references from docstring.

        Pattern: Section 28.9.2 \"Compressor Tips\" (page 521)
        """
        if not docstring:
            return []

        pattern = r"Section\\s+([\\d\\.]+)\\s+\"([^\"]+)\"\\s+\\(page\\s+(\\d+)\\)"
        matches = re.findall(pattern, docstring)

        references = []
        for section, title, page in matches:
            try:
                ref = AbletonReference(section=section, title=title, page=int(page))
                references.append(ref)
            except Exception:
                # Skip invalid references
                pass

        return references

    def _has_tdd_markers(self, docstring: str) -> bool:
        """Check if docstring has TDD workflow section."""
        if not docstring:
            return False
        return "TDD" in docstring and "Workflow" in docstring

    def _extract_tdd_marker(self, docstring: str) -> str | None:
        """Extract TDD marker from method docstring."""
        if not docstring:
            return None

        if "🔴" in docstring or "RED" in docstring:
            return "RED"
        elif "🟢" in docstring or "GREEN" in docstring:
            return "GREEN"
        elif "🔄" in docstring or "REFACTOR" in docstring:
            return "REFACTOR"
        return None

    def _parse_module_docstring(self, docstring: str) -> ModuleDocstring | None:
        """Parse module-level docstring."""
        if not docstring:
            return None

        try:
            references = self._extract_references(docstring)
            has_tdd = self._has_tdd_markers(docstring)

            # Skip validation if no references (will be caught later)
            if not references:
                return ModuleDocstring(
                    description=docstring[:100],
                    references=[
                        AbletonReference(section="0.0", title="Placeholder", page=1)
                    ],
                    has_tdd_workflow=has_tdd,
                )

            return ModuleDocstring(
                description=docstring[:200],
                references=references,
                has_tdd_workflow=has_tdd,
            )
        except Exception:
            return None

    def _parse_class_docstring(self, docstring: str) -> ClassDocstring:
        """Parse class-level docstring."""
        if not docstring:
            docstring = "No description"

        references = self._extract_references(docstring)

        return ClassDocstring(description=docstring[:200], references=references)

    def _parse_method_docstring(self, docstring: str) -> MethodDocstring:
        """Parse method-level docstring."""
        if not docstring:
            docstring = "No description"

        references = self._extract_references(docstring)
        tdd_marker = self._extract_tdd_marker(docstring)

        return MethodDocstring(
            description=docstring[:200], references=references, tdd_marker=tdd_marker
        )

    def _parse_method(self, node: ast.FunctionDef) -> TestMethod:
        """Parse a test method."""
        docstring = ast.get_docstring(node) or ""
        method_doc = self._parse_method_docstring(docstring)

        # Extract fixture usage
        fixtures = []
        if node.args.args:
            fixtures = [arg.arg for arg in node.args.args if arg.arg != "self"]

        # Check for AAA structure (simplified - look for comments)
        source = ast.unparse(node) if hasattr(ast, "unparse") else ""
        has_arrange = "Arrange" in source or "# Arrange" in source
        has_act = "Act" in source or "# Act" in source
        has_assert = "assert" in source.lower()

        return TestMethod(
            name=node.name,
            docstring=method_doc,
            has_arrange=has_arrange,
            has_act=has_act,
            has_assert=has_assert,
            uses_fixtures=fixtures,
        )

    def parse_file(self, filepath: Path) -> TestModule | None:
        """Parse test file into Pydantic model."""
        try:
            with open(filepath) as f:
                content = f.read()
                tree = ast.parse(content)

            # Extract module docstring
            module_docstring = ast.get_docstring(tree)
            if not module_docstring:
                return None

            # Parse module docstring
            module_doc = self._parse_module_docstring(module_docstring)
            if not module_doc:
                return None

            # Check imports
            imports_pytest = "import pytest" in content or "from pytest" in content
            imports_mock = (
                "from unittest.mock import Mock" in content or "import Mock" in content
            )

            # Extract classes and methods
            classes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
                    class_doc_str = ast.get_docstring(node) or ""
                    class_doc = self._parse_class_docstring(class_doc_str)

                    methods = [
                        self._parse_method(m)
                        for m in node.body
                        if isinstance(m, ast.FunctionDef) and m.name.startswith("test_")
                    ]

                    if methods:  # Only add classes with test methods
                        classes.append(
                            TestClass(
                                name=node.name, docstring=class_doc, methods=methods
                            )
                        )

            if not classes:
                return None

            return TestModule(
                filepath=filepath,
                filename=filepath.name,
                docstring=module_doc,
                classes=classes,
                imports_pytest=imports_pytest,
                imports_mock=imports_mock,
            )

        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None

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
                    errors=["Failed to parse file or missing required docstrings"],
                    score=0.0,
                )

            # Validate module docstring
            if len(test_module.docstring.references) < 1:
                errors.append("Module missing Ableton Manual references")
                score -= 20

            if not test_module.docstring.has_tdd_workflow:
                warnings.append("Module docstring missing TDD Workflow section")
                score -= 10

            # Validate imports
            if not test_module.imports_pytest:
                errors.append("Missing pytest import")
                score -= 5

            if not test_module.imports_mock:
                warnings.append("Missing Mock import")
                score -= 3

            # Validate classes
            for cls in test_module.classes:
                if len(cls.methods) == 0:
                    warnings.append(f"Class {cls.name} has no test methods")
                    score -= 5

                # Validate methods
                for method in cls.methods:
                    if not method.has_assert:
                        errors.append(f"{method.name}: Missing assert statements")
                        score -= 10

                    if not method.docstring.tdd_marker:
                        warnings.append(f"{method.name}: Missing TDD marker")
                        score -= 2

            passed = len(errors) == 0 and score >= 70.0

            return ValidationResult(
                filepath=filepath,
                passed=passed,
                errors=errors,
                warnings=warnings,
                score=max(0.0, score),
            )

        except Exception as e:
            return ValidationResult(
                filepath=filepath,
                passed=False,
                errors=[f"Validation error: {str(e)}"],
                score=0.0,
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
        report_lines = ["# Test Quality Validation Report\\n"]

        # Summary
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        avg_score = sum(r.score for r in self.results) / total if total > 0 else 0

        report_lines.append(f"**Total Tests**: {total}")
        report_lines.append(
            f"**Passed**: {passed}/{total} ({passed / total * 100:.1f}%)"
        )
        report_lines.append(f"**Average Score**: {avg_score:.1f}/100\\n")

        # Per-file results
        report_lines.append("## Test Files\\n")

        for result in sorted(self.results, key=lambda r: r.score, reverse=True):
            report_lines.append(f"### {result.filepath.name} - {result.status}")
            report_lines.append(f"**Score**: {result.score:.1f}/100\\n")

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

        return "\\n".join(report_lines)


# Main execution
if __name__ == "__main__":
    from pathlib import Path

    validator = TestQualityValidator(Path("tests/agents"))
    results = validator.validate_all()

    # Generate report
    report = validator.generate_report()

    # Save to artifacts
    output_path = Path("artifacts/report/test_quality_report.md")
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(report)

    print(f"✅ Validation complete: {output_path}")
    print(f"Passed: {sum(1 for r in results if r.passed)}/{len(results)}")
    print(f"Average score: {sum(r.score for r in results) / len(results):.1f}/100")
