"""Tests for WorkflowOrchestrator."""

import pytest


class TestWorkflowStep:
    """Test WorkflowStep dataclass."""

    def test_workflow_step_creation(self):
        """Verify workflow step can be created."""
        from dearpygui_controller.workflow_orchestrator import WorkflowStep

        step = WorkflowStep(
            name="Test Step",
            agent_type="composer",
            params={"bars": 4},
            required=True,
            timeout=30.0,
        )

        assert step.name == "Test Step"
        assert step.agent_type == "composer"
        assert step.params == {"bars": 4}
        assert step.required is True
        assert step.timeout == 30.0

    def test_workflow_step_defaults(self):
        """Verify workflow step defaults."""
        from dearpygui_controller.workflow_orchestrator import WorkflowStep

        step = WorkflowStep(
            name="Test",
            agent_type="composer",
        )

        assert step.params == {}
        assert step.required is True
        assert step.timeout is None


class TestWorkflowOrchestrator:
    """Test WorkflowOrchestrator."""

    def test_orchestrator_creation(self):
        """Verify orchestrator can be created."""
        from dearpygui_controller.workflow_orchestrator import WorkflowOrchestrator

        orch = WorkflowOrchestrator(verbose=False)
        assert orch is not None
        assert orch.factory is not None

    def test_log_callback(self):
        """Verify log callback works."""
        from dearpygui_controller.workflow_orchestrator import WorkflowOrchestrator

        logs = []
        orch = WorkflowOrchestrator(verbose=False)
        orch.set_log_callback(lambda msg: logs.append(msg))
        orch.log("Test message")

        assert len(logs) > 0
        assert any("Test message" in log for log in logs)

    def test_progress_callback(self):
        """Verify progress callback works."""
        from dearpygui_controller.workflow_orchestrator import WorkflowOrchestrator

        progress_updates = []
        orch = WorkflowOrchestrator(verbose=False)
        orch.set_progress_callback(
            lambda prog, name: progress_updates.append((prog, name))
        )
        orch.update_progress(5, 10, "Test Step")

        assert len(progress_updates) > 0
        assert progress_updates[0][0] == 0.5
        assert progress_updates[0][1] == "Test Step"

    @pytest.mark.asyncio
    async def test_execute_simple_workflow(self):
        """Verify simple workflow execution."""
        from dearpygui_controller.workflow_orchestrator import (
            WorkflowOrchestrator,
            WorkflowStep,
        )

        orch = WorkflowOrchestrator(verbose=False)
        steps = [
            WorkflowStep(
                name="Compose",
                agent_type="composer",
                params={"bars": 2},
            ),
        ]

        result = await orch.execute_workflow(steps)

        assert result is not None
        assert result.duration >= 0
        assert "Compose" in result.step_results

    @pytest.mark.asyncio
    async def test_workflow_with_multiple_steps(self):
        """Verify multi-step workflow."""
        from dearpygui_controller.workflow_orchestrator import (
            WorkflowOrchestrator,
            WorkflowStep,
        )

        orch = WorkflowOrchestrator(verbose=False)
        steps = [
            WorkflowStep(name="Step 1", agent_type="composer", params={"bars": 1}),
            WorkflowStep(name="Step 2", agent_type="mixer"),
        ]

        result = await orch.execute_workflow(steps)

        assert len(result.step_results) == 2
        assert "Step 1" in result.step_results
        assert "Step 2" in result.step_results

    @pytest.mark.asyncio
    async def test_workflow_stop_on_error(self):
        """Verify workflow stops on error when configured."""
        from dearpygui_controller.workflow_orchestrator import (
            WorkflowOrchestrator,
            WorkflowStep,
        )

        orch = WorkflowOrchestrator(verbose=False)
        steps = [
            WorkflowStep(
                name="Invalid Step",
                agent_type="nonexistent",  # This will fail
                required=True,
            ),
            WorkflowStep(name="Should Not Run", agent_type="composer"),
        ]

        result = await orch.execute_workflow(steps, stop_on_error=True)

        assert result.success is False
        assert result.steps_failed > 0
        # Second step should not have run
        assert "Should Not Run" not in result.step_results

    @pytest.mark.asyncio
    async def test_workflow_continue_on_error(self):
        """Verify workflow continues on non-required failures."""
        from dearpygui_controller.workflow_orchestrator import (
            WorkflowOrchestrator,
            WorkflowStep,
        )

        orch = WorkflowOrchestrator(verbose=False)
        steps = [
            WorkflowStep(
                name="Optional Step",
                agent_type="research",  # Might fail in mock mode
                required=False,
            ),
            WorkflowStep(name="Required Step", agent_type="composer", params={"bars": 1}),
        ]

        result = await orch.execute_workflow(steps, stop_on_error=True)

        # Both steps should have run
        assert "Optional Step" in result.step_results
        assert "Required Step" in result.step_results

    def test_get_full_production_workflow(self):
        """Verify full production workflow definition."""
        from dearpygui_controller.workflow_orchestrator import WorkflowOrchestrator

        workflow = WorkflowOrchestrator.get_full_production_workflow()

        assert len(workflow) > 0
        step_names = [step.name for step in workflow]

        # Check key phases are present
        assert any("Synthesizer" in name for name in step_names)
        assert any("Arrangement" in name for name in step_names)
        assert any("Master" in name for name in step_names)
        assert any("Verify" in name for name in step_names)

    def test_get_quick_workflow(self):
        """Verify quick workflow definition."""
        from dearpygui_controller.workflow_orchestrator import WorkflowOrchestrator

        workflow = WorkflowOrchestrator.get_quick_workflow()

        assert len(workflow) > 0
        assert len(workflow) < 10  # Should be shorter than full

        step_names = [step.name for step in workflow]
        assert any("Pattern" in name for name in step_names)

    @pytest.mark.asyncio
    async def test_execute_quick_workflow(self):
        """Verify quick workflow executes."""
        from dearpygui_controller.workflow_orchestrator import WorkflowOrchestrator

        orch = WorkflowOrchestrator(verbose=False)
        workflow = WorkflowOrchestrator.get_quick_workflow()

        result = await orch.execute_workflow(workflow, stop_on_error=False)

        assert result is not None
        assert result.steps_completed > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
