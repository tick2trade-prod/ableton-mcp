"""Agent quality validator using Pydantic 2.x models.

Validates:
- Manual references in docstrings
- Type hints on all parameters
- Error handling with AgentResult
- Mock MCP client support
- Naming conventions
- Code structure

Usage:
    python scripts/validators/agent_quality_validator.py
"""

import ast
import re
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models.v1.agent_models import (  # noqa: E402
    AgentClass,
    AgentMethod,
    AgentModule,
    AgentValidationResult,
)
from models.v1.test_models import AbletonReference  # noqa: E402


class AgentQualityValidator:
    """Validate agent files against code quality standards."""

    def __init__(self, agent_dir: Path):
        self.agent_dir = agent_dir
        self.results: list[AgentValidationResult] = []

    def _extract_references(self, docstring: str) -> list[AbletonReference]:
        """Extract Ableton Manual references from docstring."""
        if not docstring:
            return []

        pattern = r'Section\\s+([\\d\\.]+)\\s+"([^"]+)"\\s+\\(page\\s+(\\d+)\\)'
        matches = re.findall(pattern, docstring)

        references = []
        for section, title, page in matches:
            try:
                ref = AbletonReference(section=section, title=title, page=int(page))
                references.append(ref)
            except Exception:
                pass

        return references

    def _has_type_hints(self, node: ast.FunctionDef) -> bool:
        """Check if function has type hints on parameters."""
        if not node.args.args:
            return True  # No args to type hint

        # Check if at least one arg (excluding self) has annotation
        for arg in node.args.args:
            if arg.arg != "self" and not arg.annotation:
                return False
        return True

    def _returns_agent_result(self, node: ast.FunctionDef) -> bool:
        """Check if function returns AgentResult."""
        if not node.returns:
            return False

        # Check return annotation
        if isinstance(node.returns, ast.Name):
            return node.returns.id == "AgentResult"
        return False

    def _has_error_handling(self, node: ast.FunctionDef) -> bool:
        """Check if function has try/except."""
        for child in ast.walk(node):
            if isinstance(child, ast.Try):
                return True
        return False

    def _handles_none_mcp(self, node: ast.FunctionDef) -> bool:
        """Check if function handles None MCP client."""
        source = ast.unparse(node) if hasattr(ast, "unparse") else ""
        return "if not mcp" in source or "mcp is None" in source

    def _parse_method(self, node: ast.FunctionDef) -> AgentMethod | None:
        """Parse an agent method."""
        try:
            docstring = ast.get_docstring(node) or ""
            references = self._extract_references(docstring)

            return AgentMethod(
                name=node.name,
                has_docstring=bool(docstring),
                has_type_hints=self._has_type_hints(node),
                returns_agent_result=self._returns_agent_result(node),
                is_async=isinstance(node, ast.AsyncFunctionDef),
                references=references,
                handles_none_mcp=self._handles_none_mcp(node),
                has_error_handling=self._has_error_handling(node),
            )
        except Exception:
            return None

    def parse_file(self, filepath: Path) -> AgentModule | None:
        """Parse agent file into Pydantic model."""
        try:
            with open(filepath) as f:
                content = f.read()
                tree = ast.parse(content)

            # Extract module docstring
            module_docstring = ast.get_docstring(tree) or ""
            module_refs = self._extract_references(module_docstring)

            # Check imports
            imports_base = (
                "from .base_agent import" in content or "import BaseAgent" in content
            )

            # Find agent class
            agent_class = None
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name.endswith("Agent"):
                    class_doc = ast.get_docstring(node) or ""
                    class_refs = self._extract_references(class_doc)

                    # Check inheritance
                    inherits_base = any(
                        base.id == "BaseAgent" if isinstance(base, ast.Name) else False
                        for base in node.bases
                    )

                    # Find required methods
                    has_get_role = False
                    has_get_goal = False
                    has_execute = False
                    methods = []

                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            if item.name == "get_role":
                                has_get_role = True
                            elif item.name == "get_goal":
                                has_get_goal = True
                            elif item.name == "execute":
                                has_execute = True

                            # Parse method (skip special methods)
                            if not item.name.startswith("_") and item.name not in [
                                "get_role",
                                "get_goal",
                                "__init__",
                            ]:
                                method = self._parse_method(item)
                                if method:
                                    methods.append(method)

                    agent_class = AgentClass(
                        name=node.name,
                        inherits_base_agent=inherits_base,
                        has_get_role=has_get_role,
                        has_get_goal=has_get_goal,
                        has_execute=has_execute,
                        methods=methods,
                        manual_references=class_refs,
                        has_docstring=bool(class_doc),
                    )
                    break

            if not agent_class:
                return None

            return AgentModule(
                filepath=filepath,
                filename=filepath.name,
                has_docstring=bool(module_docstring),
                manual_references=module_refs,
                imports_base_agent=imports_base,
                agent_class=agent_class,
            )

        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None

    def validate_file(self, filepath: Path) -> AgentValidationResult:
        """Validate a single agent file with weighted scoring."""
        errors = []
        warnings = []

        # Weighted scores (out of 100)
        documentation_score = 30.0
        type_safety_score = 25.0
        error_handling_score = 20.0
        structure_score = 15.0
        code_quality_score = 10.0

        try:
            agent_module = self.parse_file(filepath)

            if not agent_module:
                return AgentValidationResult(
                    filepath=filepath,
                    passed=False,
                    score=0.0,
                    errors=["Failed to parse agent file or missing agent class"],
                )

            # Documentation (30%)
            if not agent_module.has_docstring:
                errors.append("Missing module docstring")
                documentation_score -= 10

            if len(agent_module.manual_references) < 1:
                errors.append("Missing Ableton Manual references in module docstring")
                documentation_score -= 15

            if not agent_module.agent_class.has_docstring:
                warnings.append(
                    f"Class {agent_module.agent_class.name} missing docstring"
                )
                documentation_score -= 5

            # Structure (15%)
            if not agent_module.imports_base_agent:
                errors.append("Missing BaseAgent import")
                structure_score -= 5

            if not agent_module.agent_class.inherits_base_agent:
                errors.append(
                    f"{agent_module.agent_class.name} doesn't inherit from BaseAgent"
                )
                structure_score -= 5

            if not agent_module.agent_class.has_get_role:
                errors.append("Missing get_role() method")
                structure_score -= 2

            if not agent_module.agent_class.has_get_goal:
                errors.append("Missing get_goal() method")
                structure_score -= 2

            if not agent_module.agent_class.has_execute:
                errors.append("Missing execute() method")
                structure_score -= 5

            # Type Safety (25%)
            methods_without_types = 0
            for method in agent_module.agent_class.methods:
                if not method.has_type_hints:
                    methods_without_types += 1

            if methods_without_types > 0:
                warnings.append(f"{methods_without_types} methods missing type hints")
                type_safety_score -= min(methods_without_types * 5, 25)

            # Error Handling (20%)
            methods_without_error_handling = 0
            for method in agent_module.agent_class.methods:
                if not method.has_error_handling:
                    methods_without_error_handling += 1

            if methods_without_error_handling > 0:
                warnings.append(
                    f"{methods_without_error_handling} methods missing try/except"
                )
                error_handling_score -= min(methods_without_error_handling * 4, 20)

            # Code Quality (10%)
            methods_without_mcp_handling = 0
            for method in agent_module.agent_class.methods:
                if not method.handles_none_mcp:
                    methods_without_mcp_handling += 1

            if methods_without_mcp_handling > 0:
                warnings.append(
                    f"{methods_without_mcp_handling} methods don't handle None MCP"
                )
                code_quality_score -= min(methods_without_mcp_handling * 2, 10)

            # Calculate final score
            total_score = (
                max(0, documentation_score)
                + max(0, type_safety_score)
                + max(0, error_handling_score)
                + max(0, structure_score)
                + max(0, code_quality_score)
            )

            passed = len(errors) == 0 and total_score >= 70.0

            return AgentValidationResult(
                filepath=filepath,
                passed=passed,
                score=total_score,
                documentation_score=max(0, documentation_score),
                type_safety_score=max(0, type_safety_score),
                error_handling_score=max(0, error_handling_score),
                structure_score=max(0, structure_score),
                code_quality_score=max(0, code_quality_score),
                errors=errors,
                warnings=warnings,
            )

        except Exception as e:
            return AgentValidationResult(
                filepath=filepath,
                passed=False,
                score=0.0,
                errors=[f"Validation error: {str(e)}"],
            )

    def validate_all(self) -> list[AgentValidationResult]:
        """Validate all agent files in directory."""
        agent_files = sorted(self.agent_dir.glob("*_agent.py"))

        # Exclude base_agent.py
        agent_files = [f for f in agent_files if f.name != "base_agent.py"]

        for filepath in agent_files:
            result = self.validate_file(filepath)
            self.results.append(result)

        return self.results

    def generate_report(self) -> str:
        """Generate markdown report."""
        lines = ["# Agent Quality Validation Report\\n"]

        # Summary
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        avg_score = sum(r.score for r in self.results) / total if total > 0 else 0

        lines.append(f"**Total Agents**: {total}")
        lines.append(f"**Passed**: {passed}/{total} ({passed / total * 100:.1f}%)")
        lines.append(f"**Average Score**: {avg_score:.1f}/100\\n")

        # Score breakdown
        if self.results:
            avg_doc = sum(r.documentation_score for r in self.results) / total
            avg_type = sum(r.type_safety_score for r in self.results) / total
            avg_error = sum(r.error_handling_score for r in self.results) / total
            avg_struct = sum(r.structure_score for r in self.results) / total
            avg_quality = sum(r.code_quality_score for r in self.results) / total

            lines.append("## Average Scores by Category\\n")
            lines.append(f"- **Documentation** (30%): {avg_doc:.1f}/30")
            lines.append(f"- **Type Safety** (25%): {avg_type:.1f}/25")
            lines.append(f"- **Error Handling** (20%): {avg_error:.1f}/20")
            lines.append(f"- **Structure** (15%): {avg_struct:.1f}/15")
            lines.append(f"- **Code Quality** (10%): {avg_quality:.1f}/10\\n")

        # Per-file results
        lines.append("## Agent Files\\n")

        for result in sorted(self.results, key=lambda r: r.score, reverse=True):
            lines.append(f"### {result.filepath.name} - {result.status}")
            lines.append(f"**Score**: {result.score:.1f}/100\\n")

            lines.append("**Category Scores**:")
            lines.append(f"- Documentation: {result.documentation_score:.1f}/30")
            lines.append(f"- Type Safety: {result.type_safety_score:.1f}/25")
            lines.append(f"- Error Handling: {result.error_handling_score:.1f}/20")
            lines.append(f"- Structure: {result.structure_score:.1f}/15")
            lines.append(f"- Code Quality: {result.code_quality_score:.1f}/10\\n")

            if result.errors:
                lines.append("**Errors**:")
                for error in result.errors:
                    lines.append(f"- ❌ {error}")
                lines.append("")

            if result.warnings:
                lines.append("**Warnings**:")
                for warning in result.warnings:
                    lines.append(f"- ⚠️ {warning}")
                lines.append("")

        return "\\n".join(lines)


# Main execution
if __name__ == "__main__":
    validator = AgentQualityValidator(Path("scripts/dearpygui_controller/agents"))
    results = validator.validate_all()

    # Generate report
    report = validator.generate_report()

    # Save to artifacts
    output_path = Path("artifacts/agent_quality_report.md")
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(report)

    print(f"✅ Agent validation complete: {output_path}")
    print(f"Passed: {sum(1 for r in results if r.passed)}/{len(results)}")
    print(f"Average score: {sum(r.score for r in results) / len(results):.1f}/100")
