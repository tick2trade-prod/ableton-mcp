"""Agent Factory for creating agents with standardized configuration."""

from typing import Any

from .agents import (
    ArrangementAgent,
    BaseAgent,
    ComposerAgent,
    EffectsChainAgent,
    MasteringAgent,
    MixerAgent,
    ModulationAgent,
    PercussionAgent,
    ResearchAgent,
    SynthesizerAgent,
    TransitionAgent,
    VerifierAgent,
    VocalsAgent,
)


class AgentFactory:
    """Factory for creating and configuring agents."""

    # Registry of available agents
    AGENTS = {
        "research": ResearchAgent,
        "composer": ComposerAgent,
        "mixer": MixerAgent,
        "verifier": VerifierAgent,
        "arrangement": ArrangementAgent,
        "synthesizer": SynthesizerAgent,
        "percussion": PercussionAgent,
        "vocals": VocalsAgent,
        "transition": TransitionAgent,
        "modulation": ModulationAgent,
        "effects_chain": EffectsChainAgent,
        "mastering": MasteringAgent,
    }

    @classmethod
    def create(
        cls,
        agent_type: str,
        verbose: bool = True,
        **kwargs: Any,
    ) -> BaseAgent:
        """Create an agent by type.

        Args:
            agent_type: Type of agent to create
            verbose: Enable verbose logging
            **kwargs: Additional arguments passed to agent constructor

        Returns:
            Configured agent instance

        Raises:
            ValueError: If agent_type is not recognized
        """
        if agent_type not in cls.AGENTS:
            available = ", ".join(cls.AGENTS.keys())
            raise ValueError(
                f"Unknown agent type: {agent_type}. Available: {available}"
            )

        agent_class = cls.AGENTS[agent_type]
        return agent_class(verbose=verbose, **kwargs)

    @classmethod
    def create_batch(
        cls,
        agent_types: list,
        verbose: bool = True,
        **kwargs: Any,
    ) -> dict[str, BaseAgent]:
        """Create multiple agents at once.

        Args:
            agent_types: List of agent type strings
            verbose: Enable verbose logging
            **kwargs: Additional arguments passed to all agent constructors

        Returns:
            Dictionary mapping agent type to agent instance
        """
        return {
            agent_type: cls.create(agent_type, verbose=verbose, **kwargs)
            for agent_type in agent_types
        }

    @classmethod
    def list_agents(cls) -> dict[str, dict[str, str]]:
        """List all available agents with their roles and goals.

        Returns:
            Dictionary mapping agent type to role/goal info
        """
        agents_info = {}

        for agent_type, agent_class in cls.AGENTS.items():
            # Create temporary instance to get role/goal
            agent = agent_class(verbose=False)
            agents_info[agent_type] = {
                "role": agent.get_role(),
                "goal": agent.get_goal(),
                "class": agent_class.__name__,
            }

        return agents_info

    @classmethod
    def get_agents_by_category(cls) -> dict[str, list]:
        """Get agents grouped by category.

        Returns:
            Dictionary mapping category to list of agent types
        """
        return {
            "foundation": ["research", "composer", "mixer", "verifier"],
            "synthesis": ["synthesizer"],
            "rhythm": ["percussion"],
            "vocals": ["vocals"],
            "effects": ["transition", "modulation", "effects_chain"],
            "arrangement": ["arrangement", "mastering"],
        }

    @classmethod
    def create_production_workflow(
        cls,
        verbose: bool = True,
    ) -> dict[str, BaseAgent]:
        """Create a complete production workflow with all agents.

        Returns:
            Dictionary of all agents needed for full production
        """
        workflow_agents = [
            "research",
            "synthesizer",
            "composer",
            "percussion",
            "vocals",
            "mixer",
            "transition",
            "modulation",
            "effects_chain",
            "arrangement",
            "mastering",
            "verifier",
        ]

        return cls.create_batch(workflow_agents, verbose=verbose)
