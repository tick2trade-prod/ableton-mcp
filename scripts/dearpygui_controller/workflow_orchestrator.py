"""Workflow Orchestrator for managing multi-agent production workflows."""

import asyncio
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Optional

from .agent_factory import AgentFactory
from .agents.base_agent import AgentResult, BaseAgent


@dataclass
class WorkflowStep:
    """A single step in a workflow."""

    name: str
    agent_type: str
    params: dict[str, Any] = field(default_factory=dict)
    required: bool = True  # If False, continue on failure
    timeout: Optional[float] = None  # Timeout in seconds


@dataclass
class WorkflowResult:
    """Result from a workflow execution."""

    success: bool
    duration: float  # Total duration in seconds
    steps_completed: int
    steps_failed: int
    step_results: dict[str, AgentResult]
    errors: list[str] = field(default_factory=list)


class WorkflowOrchestrator:
    """Orchestrates multi-agent workflows for I Am Machine production."""

    def __init__(self, verbose: bool = True):
        """Initialize the orchestrator.

        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        self.factory = AgentFactory()
        self._progress_callback: Optional[Callable] = None
        self._log_callback: Optional[Callable] = None

    def set_progress_callback(self, callback: Callable) -> None:
        """Set callback for progress updates."""
        self._progress_callback = callback

    def set_log_callback(self, callback: Callable) -> None:
        """Set callback for log messages."""
        self._log_callback = callback

    def log(self, message: str) -> None:
        """Log a message."""
        if self.verbose:
            print(f"[Orchestrator] {message}")
        if self._log_callback:
            self._log_callback(f"[Orchestrator] {message}")

    def update_progress(self, current: int, total: int, step_name: str) -> None:
        """Update workflow progress."""
        progress = current / total if total > 0 else 0
        if self._progress_callback:
            self._progress_callback(progress, step_name)

    async def execute_step(
        self,
        step: WorkflowStep,
        agent: BaseAgent,
    ) -> AgentResult:
        """Execute a single workflow step.

        Args:
            step: Workflow step to execute
            agent: Agent instance to use

        Returns:
            AgentResult from the step

        Raises:
            asyncio.TimeoutError: If step exceeds timeout
        """
        self.log(f"Executing step: {step.name}")

        # Set callbacks
        if self._progress_callback:
            agent.set_progress_callback(
                lambda idx, prog: self.update_progress(idx, 16, step.name)
            )
        if self._log_callback:
            agent.set_log_callback(self._log_callback)

        # Execute with optional timeout
        if step.timeout:
            try:
                result = await asyncio.wait_for(
                    agent.execute(**step.params),
                    timeout=step.timeout,
                )
            except asyncio.TimeoutError:
                self.log(f"Step timed out: {step.name}")
                return AgentResult(
                    success=False,
                    message=f"Timeout after {step.timeout}s",
                    errors=[f"Step exceeded timeout of {step.timeout}s"],
                )
        else:
            result = await agent.execute(**step.params)

        return result

    async def execute_workflow(
        self,
        steps: list[WorkflowStep],
        stop_on_error: bool = True,
    ) -> WorkflowResult:
        """Execute a workflow of agent steps.

        Args:
            steps: List of workflow steps to execute
            stop_on_error: Whether to stop on first error (default: True)

        Returns:
            WorkflowResult with execution summary
        """
        start_time = time.time()
        step_results = {}
        errors = []
        steps_completed = 0
        steps_failed = 0

        self.log(f"Starting workflow with {len(steps)} steps...")

        for i, step in enumerate(steps):
            self.update_progress(i, len(steps), step.name)

            try:
                # Create agent for this step
                agent = self.factory.create(step.agent_type, verbose=self.verbose)

                # Execute step
                result = await self.execute_step(step, agent)
                step_results[step.name] = result

                if result.success:
                    steps_completed += 1
                    self.log(f"✓ Step completed: {step.name}")
                else:
                    steps_failed += 1
                    error_msg = f"✗ Step failed: {step.name} - {result.message}"
                    self.log(error_msg)
                    errors.append(error_msg)
                    errors.extend(result.errors)

                    if step.required and stop_on_error:
                        self.log("Stopping workflow due to error")
                        break

            except Exception as e:
                steps_failed += 1
                error_msg = f"✗ Step exception: {step.name} - {str(e)}"
                self.log(error_msg)
                errors.append(error_msg)

                step_results[step.name] = AgentResult(
                    success=False,
                    message=str(e),
                    errors=[str(e)],
                )

                if step.required and stop_on_error:
                    self.log("Stopping workflow due to exception")
                    break

        duration = time.time() - start_time
        self.update_progress(len(steps), len(steps), "Complete")

        success = steps_failed == 0

        self.log(f"Workflow complete: {steps_completed}/{len(steps)} steps succeeded")
        self.log(f"Duration: {duration:.2f}s")

        return WorkflowResult(
            success=success,
            duration=duration,
            steps_completed=steps_completed,
            steps_failed=steps_failed,
            step_results=step_results,
            errors=errors,
        )

    @classmethod
    def get_full_production_workflow(cls) -> list[WorkflowStep]:
        """Get the complete I Am Machine production workflow.

        Returns:
            List of workflow steps for full production
        """
        return [
            # Phase 1: Research & Planning
            WorkflowStep(
                name="Research Production Techniques",
                agent_type="research",
                params={"topic": "peak time techno production"},
                required=False,  # Optional research step
            ),
            # Phase 2: Synthesis Programming
            WorkflowStep(
                name="Program Synthesizers",
                agent_type="synthesizer",
                required=True,
                timeout=60.0,
            ),
            # Phase 3: Rhythm & Composition
            WorkflowStep(
                name="Create Drum Patterns",
                agent_type="composer",
                params={"bars": 4},
                required=True,
            ),
            WorkflowStep(
                name="Create Percussion Patterns",
                agent_type="percussion",
                params={"bars": 4},
                required=True,
            ),
            # Phase 4: Vocals & Processing
            WorkflowStep(
                name="Process Vocals",
                agent_type="vocals",
                required=True,
            ),
            # Phase 5: Mixing
            WorkflowStep(
                name="Apply Effects Chains",
                agent_type="mixer",
                required=True,
            ),
            WorkflowStep(
                name="Configure Signal Routing",
                agent_type="effects_chain",
                params={"mode": "all"},
                required=True,
            ),
            # Phase 6: Transitions & Movement
            WorkflowStep(
                name="Create Transitions",
                agent_type="transition",
                required=True,
            ),
            WorkflowStep(
                name="Apply Modulation",
                agent_type="modulation",
                required=True,
            ),
            # Phase 7: Arrangement
            WorkflowStep(
                name="Structure Arrangement",
                agent_type="arrangement",
                params={"mode": "full"},
                required=True,
            ),
            # Phase 8: Mastering
            WorkflowStep(
                name="Master Final Mix",
                agent_type="mastering",
                params={"analyze_only": False},
                required=True,
            ),
            # Phase 9: Verification
            WorkflowStep(
                name="Verify Project Completion",
                agent_type="verifier",
                required=False,  # Optional verification
            ),
        ]

    @classmethod
    def get_quick_workflow(cls) -> list[WorkflowStep]:
        """Get a quick workflow for testing.

        Returns:
            List of workflow steps for quick production test
        """
        return [
            WorkflowStep(
                name="Create Basic Patterns",
                agent_type="composer",
                params={"bars": 2},
                required=True,
            ),
            WorkflowStep(
                name="Apply Basic Mixing",
                agent_type="mixer",
                required=True,
            ),
            WorkflowStep(
                name="Verify Setup",
                agent_type="verifier",
                required=False,
            ),
        ]


async def run_full_production(verbose: bool = True) -> WorkflowResult:
    """Run the complete I Am Machine production workflow.

    Args:
        verbose: Enable verbose logging

    Returns:
        WorkflowResult with execution summary
    """
    orchestrator = WorkflowOrchestrator(verbose=verbose)
    workflow = WorkflowOrchestrator.get_full_production_workflow()
    return await orchestrator.execute_workflow(workflow, stop_on_error=False)


if __name__ == "__main__":
    # Example usage
    result = asyncio.run(run_full_production())

    print("\n" + "=" * 70)
    print("  WORKFLOW SUMMARY")
    print("=" * 70)
    print(f"Success: {result.success}")
    print(f"Duration: {result.duration:.2f}s")
    print(f"Steps completed: {result.steps_completed}")
    print(f"Steps failed: {result.steps_failed}")

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  - {error}")
