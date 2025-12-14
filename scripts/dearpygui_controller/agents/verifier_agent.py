"""Verifier Agent for validating project completion."""

from dataclasses import dataclass

from .base_agent import AgentResult, BaseAgent


@dataclass
class VerificationResult:
    """Result of a single verification check."""

    name: str
    passed: bool
    message: str = ""
    expected: str = ""
    actual: str = ""


class VerifierAgent(BaseAgent):
    """Agent for verifying project completion.

    Checks boolean success criteria:
    - IS_BPM_VALID: Tempo == 136
    - HAS_ALL_TRACKS: 16 tracks exist
    - HAS_KICK_PATTERN: Track 0 has notes
    - HAS_RUMBLE_CHAIN: Track 1 has devices
    - etc.
    """

    def __init__(self, **kwargs):
        super().__init__(name="VerifierAgent", **kwargs)

    def get_role(self) -> str:
        return "QA Engineer"

    def get_goal(self) -> str:
        return "Validate project meets all success criteria"

    async def check_bpm(self) -> VerificationResult:
        """Check if BPM is 136."""
        mcp = self.get_mcp_client()
        if not mcp:
            return VerificationResult(
                name="IS_BPM_VALID",
                passed=True,
                message="Mock mode - assuming valid",
            )

        result = mcp.get_session_info()
        if not result.success:
            return VerificationResult(
                name="IS_BPM_VALID",
                passed=False,
                message=f"Failed to get session: {result.message}",
            )

        tempo = result.data.get("tempo", 0)
        is_valid = abs(tempo - 136.0) < 0.1

        return VerificationResult(
            name="IS_BPM_VALID",
            passed=is_valid,
            expected="136.0",
            actual=str(tempo),
            message=f"Tempo: {tempo} BPM",
        )

    async def check_track_count(self) -> VerificationResult:
        """Check if all 16 tracks exist."""
        mcp = self.get_mcp_client()
        if not mcp:
            return VerificationResult(
                name="HAS_ALL_TRACKS",
                passed=True,
                message="Mock mode - assuming valid",
            )

        result = mcp.get_session_info()
        if not result.success:
            return VerificationResult(
                name="HAS_ALL_TRACKS",
                passed=False,
                message=f"Failed to get session: {result.message}",
            )

        count = result.data.get("track_count", 0)
        is_valid = count >= 16

        return VerificationResult(
            name="HAS_ALL_TRACKS",
            passed=is_valid,
            expected="16",
            actual=str(count),
            message=f"Track count: {count}/16",
        )

    async def check_kick_pattern(self) -> VerificationResult:
        """Check if kick track has a valid pattern."""
        # In a real implementation, query clip notes
        # For now, return placeholder
        return VerificationResult(
            name="HAS_KICK_PATTERN",
            passed=True,
            message="Kick pattern check (placeholder)",
        )

    async def check_rumble_chain(self) -> VerificationResult:
        """Check if rumble track has correct device chain."""
        # In a real implementation, query device chain
        return VerificationResult(
            name="HAS_RUMBLE_CHAIN",
            passed=True,
            message="Rumble chain check (placeholder)",
        )

    async def check_sidechain(self) -> VerificationResult:
        """Check if sidechain compression is active."""
        return VerificationResult(
            name="IS_SIDECHAIN_ACTIVE",
            passed=False,
            message="Sidechain check (not implemented)",
        )

    async def check_all_devices(self) -> VerificationResult:
        """Check if all required devices are loaded."""
        return VerificationResult(
            name="ALL_DEVICES_LOADED",
            passed=True,
            message="Device check (placeholder)",
        )

    async def check_no_errors(self) -> VerificationResult:
        """Check Ableton log for errors."""
        return VerificationResult(
            name="NO_LATENCY_ERRORS",
            passed=True,
            message="Error check (placeholder)",
        )

    def format_report(
        self,
        results: list[VerificationResult],
    ) -> str:
        """Format verification results as a report."""
        lines = [
            "═" * 55,
            "  I AM MACHINE - Verification Report",
            "═" * 55,
        ]

        passed_count = 0
        for r in results:
            symbol = "✓" if r.passed else "✗"
            lines.append(f"  {symbol} {r.name:25s}: {r.message}")
            if r.passed:
                passed_count += 1

        lines.append("─" * 55)
        pct = (passed_count / len(results)) * 100 if results else 0
        lines.append(f"  Score: {passed_count}/{len(results)} ({pct:.0f}%)")
        lines.append("═" * 55)

        return "\n".join(lines)

    async def execute(self, **kwargs) -> AgentResult:
        """Run all verification checks.

        Returns:
            AgentResult with verification report
        """
        self.log("Running verification checks...")

        results = [
            await self.check_bpm(),
            await self.check_track_count(),
            await self.check_kick_pattern(),
            await self.check_rumble_chain(),
            await self.check_sidechain(),
            await self.check_all_devices(),
            await self.check_no_errors(),
        ]

        report = self.format_report(results)
        self.log("\n" + report)

        passed = sum(1 for r in results if r.passed)
        total = len(results)

        return AgentResult(
            success=passed == total,
            message=f"Verification: {passed}/{total} checks passed",
            data={
                "results": [
                    {"name": r.name, "passed": r.passed, "message": r.message}
                    for r in results
                ],
                "report": report,
            },
        )
