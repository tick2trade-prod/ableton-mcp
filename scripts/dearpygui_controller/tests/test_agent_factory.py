"""Tests for AgentFactory."""

import pytest


class TestAgentFactory:
    """Test AgentFactory agent creation."""

    def test_create_known_agent(self):
        """Verify factory can create known agents."""
        from dearpygui_controller.agent_factory import AgentFactory

        agent = AgentFactory.create("composer", verbose=False)
        assert agent is not None
        assert agent.get_role() == "Rhythm Programmer"

    def test_create_unknown_agent_raises(self):
        """Verify factory raises for unknown agents."""
        from dearpygui_controller.agent_factory import AgentFactory

        with pytest.raises(ValueError) as exc_info:
            AgentFactory.create("nonexistent")

        assert "Unknown agent type" in str(exc_info.value)
        assert "nonexistent" in str(exc_info.value)

    def test_create_batch(self):
        """Verify batch creation."""
        from dearpygui_controller.agent_factory import AgentFactory

        agents = AgentFactory.create_batch(
            ["composer", "mixer", "verifier"],
            verbose=False,
        )

        assert len(agents) == 3
        assert "composer" in agents
        assert "mixer" in agents
        assert "verifier" in agents

    def test_list_agents(self):
        """Verify list_agents returns all agents."""
        from dearpygui_controller.agent_factory import AgentFactory

        agents_info = AgentFactory.list_agents()

        assert len(agents_info) > 0
        assert "composer" in agents_info
        assert "role" in agents_info["composer"]
        assert "goal" in agents_info["composer"]

    def test_get_agents_by_category(self):
        """Verify agents grouped by category."""
        from dearpygui_controller.agent_factory import AgentFactory

        categories = AgentFactory.get_agents_by_category()

        assert "foundation" in categories
        assert "synthesis" in categories
        assert "rhythm" in categories

        # Check some expected agents
        assert "composer" in categories["foundation"]
        assert "synthesizer" in categories["synthesis"]

    def test_create_production_workflow(self):
        """Verify production workflow creation."""
        from dearpygui_controller.agent_factory import AgentFactory

        agents = AgentFactory.create_production_workflow(verbose=False)

        assert len(agents) >= 10  # At least 10 agents
        assert "synthesizer" in agents
        assert "mastering" in agents
        assert "verifier" in agents

    def test_created_agents_are_instances(self):
        """Verify created agents are proper instances."""
        from dearpygui_controller.agent_factory import AgentFactory
        from dearpygui_controller.agents.base_agent import BaseAgent

        agent = AgentFactory.create("composer", verbose=False)
        assert isinstance(agent, BaseAgent)

    def test_create_with_kwargs(self):
        """Verify factory passes kwargs to agent constructor."""
        from dearpygui_controller.agent_factory import AgentFactory

        agent = AgentFactory.create(
            "composer",
            verbose=False,
            ollama_model="custom_model",
        )

        assert agent.ollama_model == "custom_model"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
