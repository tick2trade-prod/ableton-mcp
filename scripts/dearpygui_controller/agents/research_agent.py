"""Research Agent for sound design research."""

from .base_agent import AgentResult, BaseAgent


class ResearchAgent(BaseAgent):
    """ResearchAgent - Research production techniques using documentation.

    Reference: Ableton Manual Section 1 "General Documentation" (page 1)

    Searches embedded Ableton documentation and web for techniques.
    """

    def __init__(self, **kwargs):
        super().__init__(name="ResearchAgent", **kwargs)

    def get_role(self) -> str:
        return "Sound Research Engineer"

    def get_goal(self) -> str:
        return "Find production techniques for Peak Time Techno"

    async def execute(
        self,
        topic: str = "techno rumble kick",
        **kwargs,
    ) -> AgentResult:
        """Research a production topic.

        Args:
            topic: Topic to research (e.g., "techno rumble kick")

        Returns:
            AgentResult with research findings
        """
        self.log(f"Researching: {topic}")

        findings = {
            "topic": topic,
            "techniques": [],
            "signal_chains": [],
            "parameters": {},
        }

        try:
            # Try to use MCP research tools
            from scripts.ableton_cache_ast_codegen_mcp.mcp_server import (
                search_ableton_docs,
                search_production_technique,
            )

            # Search embedded docs
            self.log("Searching Ableton documentation...")
            docs_result = await search_ableton_docs(topic, top_k=3)
            if docs_result.get("success"):
                findings["techniques"].extend(
                    [r.get("text", "")[:200] for r in docs_result.get("results", [])]
                )

            # Search production techniques
            self.log("Searching production techniques...")
            tech_result = await search_production_technique(topic, genre="techno")
            if tech_result.get("success"):
                findings["signal_chains"].extend(
                    [r.get("title", "") for r in tech_result.get("results", [])[:3]]
                )

            self.log(f"Found {len(findings['techniques'])} techniques")
            return AgentResult(
                success=True,
                message=f"Research complete for '{topic}'",
                data=findings,
            )

        except ImportError:
            # Fallback with hardcoded knowledge
            self.log("MCP tools not available, using built-in knowledge")
            findings["techniques"] = [
                "Rumble Kick: Reverb tail → Distortion → Low-pass filter",
                "Sidechain compression for pumping effect",
                "909 kick as the foundation",
            ]
            findings["signal_chains"] = [
                "Kick → Reverb → Roar → EQ Eight → Compressor",
            ]
            findings["parameters"] = {
                "reverb_decay": 0.6,
                "roar_drive": 6.0,
                "eq_high_cut": 150,
            }
            return AgentResult(
                success=True,
                message=f"Research complete (built-in) for '{topic}'",
                data=findings,
            )
        except Exception as e:
            self.log(f"Research error: {e}")
            return AgentResult(
                success=False,
                message=f"Research failed: {e}",
                errors=[str(e)],
            )
