#!/usr/bin/env python3
"""
Agent Enhancement Pipeline using Ableton Manual Embeddings.

Completes Phases 2-5 of the enhancement pipeline:
- Phase 2: Agent Analysis
- Phase 3: Documentation Search
- Phase 4: Enhancement Generation
- Phase 5: Review & Apply
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.ableton_cache_ast_codegen_mcp.pdf_embeddings import AbletonDocEmbeddings
from scripts.ableton_cache_ast_codegen_mcp.settings import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Agent metadata mapping
AGENT_SEARCH_QUERIES = {
    "arranger_agent.py": {
        "purpose": "Arranging clips on timeline, creating song structure",
        "queries": [
            "arrangement view automation timeline",
            "song structure intro verse chorus",
            "automation envelopes breakpoints",
        ],
    },
    "arrangement_agent.py": {
        "purpose": "Clip and scene management in session view",
        "queries": [
            "session view clip launching",
            "scene management follow actions",
            "clip properties loop settings",
        ],
    },
    "composer_agent.py": {
        "purpose": "Creating MIDI patterns and note composition",
        "queries": [
            "MIDI note composition piano roll",
            "velocity duration note editing",
            "MIDI clip quantization groove",
        ],
    },
    "effects_chain_agent.py": {
        "purpose": "Audio effects and rack configuration",
        "queries": [
            "audio effects racks chains",
            "parallel processing macro controls",
            "effect rack routing signal flow",
        ],
    },
    "mastering_agent.py": {
        "purpose": "Mastering chain and final processing",
        "queries": [
            "mastering chain limiter",
            "multiband compression dynamics",
            "master track processing EQ",
        ],
    },
    "mixer_agent.py": {
        "purpose": "Mixer routing and level management",
        "queries": [
            "mixer routing sends returns",
            "track volume panning",
            "group tracks submixing",
        ],
    },
    "modulation_agent.py": {
        "purpose": "LFO and modulation configuration",
        "queries": [
            "LFO modulation envelope",
            "parameter modulation mapping",
            "modulation sources destinations",
        ],
    },
    "percussion_agent.py": {
        "purpose": "Drum rack and percussion setup",
        "queries": [
            "drum rack pad configuration",
            "drum sampler trigger mode",
            "percussion MIDI mapping",
        ],
    },
    "sound_design_agent.py": {
        "purpose": "Synthesis and device parameter configuration",
        "queries": [
            "synthesis oscillator filter",
            "device parameter automation",
            "Wavetable Operator Drift synthesis",
        ],
    },
    "synthesizer_agent.py": {
        "purpose": "Synthesizer device configuration",
        "queries": [
            "synthesizer devices Wavetable",
            "Operator FM synthesis",
            "Drift Meld synthesis parameters",
        ],
    },
    "transition_agent.py": {
        "purpose": "Crossfades and transition effects",
        "queries": [
            "crossfade automation transitions",
            "fade in fade out curves",
            "transition effects risers",
        ],
    },
    "vocals_agent.py": {
        "purpose": "Vocal processing and effects",
        "queries": [
            "vocal processing effects chain",
            "vocal EQ compression",
            "vocal reverb delay effects",
        ],
    },
    "verifier_agent.py": {
        "purpose": "Quality metrics and validation",
        "queries": [
            "spectrum analyzer metering",
            "loudness LUFS measurement",
            "audio quality analysis",
        ],
    },
}


class AgentEnhancer:
    """Enhance agents using Ableton manual documentation."""

    def __init__(self):
        """Initialize enhancer with embeddings."""
        settings = get_settings()
        self.embeddings = AbletonDocEmbeddings(
            pdf_path=settings.pdf_path,
            redis_url=settings.redis_url,
            index_name=settings.redis_index_name,
            embedding_model=settings.embedding_model,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        self.agents_dir = Path("scripts/dearpygui_controller/agents")
        self.results = {}

    async def phase_2_analyze_agents(self) -> dict[str, Any]:
        """Phase 2: Analyze all agents."""
        logger.info("=" * 60)
        logger.info("PHASE 2: Agent Analysis")
        logger.info("=" * 60)

        agent_files = list(self.agents_dir.glob("*_agent.py"))
        agent_files = [f for f in agent_files if f.name != "base_agent.py"]

        logger.info(f"Found {len(agent_files)} agents to analyze")

        analysis = {}
        for agent_file in agent_files:
            metadata = AGENT_SEARCH_QUERIES.get(agent_file.name, {})
            analysis[agent_file.name] = {
                "path": str(agent_file),
                "purpose": metadata.get("purpose", "Unknown"),
                "queries": metadata.get("queries", []),
            }
            logger.info(f"  ✓ {agent_file.name}: {metadata.get('purpose', 'Unknown')}")

        return analysis

    async def phase_3_search_documentation(
        self, agent_analysis: dict[str, Any]
    ) -> dict[str, Any]:
        """Phase 3: Search documentation for each agent."""
        logger.info("=" * 60)
        logger.info("PHASE 3: Documentation Search")
        logger.info("=" * 60)

        search_results = {}

        for agent_name, metadata in agent_analysis.items():
            logger.info(f"\nSearching docs for: {agent_name}")
            agent_results = []

            for query in metadata["queries"]:
                logger.info(f"  Query: {query}")
                try:
                    result = await self.embeddings.search_docs(query, top_k=2)
                    if result["success"]:
                        agent_results.append(
                            {
                                "query": query,
                                "results": result["results"],
                                "latency_ms": result["latency_ms"],
                            }
                        )
                        logger.info(
                            f"    ✓ Found {len(result['results'])} results "
                            f"({result['latency_ms']:.1f}ms)"
                        )
                    else:
                        logger.warning(f"    ✗ Search failed: {result.get('error')}")
                except Exception as e:
                    logger.error(f"    ✗ Error: {e}")

            search_results[agent_name] = {
                "purpose": metadata["purpose"],
                "search_results": agent_results,
                "total_results": sum(len(r["results"]) for r in agent_results),
            }

        return search_results

    async def phase_4_generate_enhancements(
        self, search_results: dict[str, Any]
    ) -> dict[str, Any]:
        """Phase 4: Generate enhancement recommendations."""
        logger.info("=" * 60)
        logger.info("PHASE 4: Enhancement Generation")
        logger.info("=" * 60)

        enhancements = {}

        for agent_name, data in search_results.items():
            logger.info(f"\nGenerating enhancements for: {agent_name}")

            recommendations = []

            # Analyze search results and generate recommendations
            for search_result in data["search_results"]:
                query = search_result["query"]
                results = search_result["results"]

                if not results:
                    continue

                # Get top result
                top_result = results[0]

                recommendation = {
                    "query": query,
                    "relevance": top_result["similarity"],
                    "page": top_result["page_num"],
                    "section": top_result["section"],
                    "excerpt": top_result["text"][:300] + "...",
                    "suggestion": self._generate_suggestion(
                        agent_name, query, top_result
                    ),
                }
                recommendations.append(recommendation)

            enhancements[agent_name] = {
                "purpose": data["purpose"],
                "total_docs_found": data["total_results"],
                "recommendations": recommendations,
                "priority": self._calculate_priority(recommendations),
            }

            logger.info(
                f"  ✓ Generated {len(recommendations)} recommendations "
                f"(Priority: {enhancements[agent_name]['priority']})"
            )

        return enhancements

    def _generate_suggestion(self, agent_name: str, query: str, result: dict) -> str:
        """Generate enhancement suggestion based on search result."""
        similarity = result["similarity"]
        section = result["section"]
        page = result["page_num"]

        if similarity > 0.7:
            return (
                f"HIGH RELEVANCE: Review '{section}' (page {page}) for detailed "
                f"implementation guidance on {query}"
            )
        elif similarity > 0.5:
            return (
                f"MEDIUM RELEVANCE: Consider '{section}' (page {page}) for "
                f"additional context on {query}"
            )
        else:
            return (
                f"LOW RELEVANCE: '{section}' (page {page}) may provide "
                f"background information"
            )

    def _calculate_priority(self, recommendations: list[dict]) -> str:
        """Calculate priority based on recommendations."""
        if not recommendations:
            return "LOW"

        avg_relevance = sum(r["relevance"] for r in recommendations) / len(
            recommendations
        )

        if avg_relevance > 0.7:
            return "HIGH"
        elif avg_relevance > 0.5:
            return "MEDIUM"
        else:
            return "LOW"

    async def phase_5_save_results(self, enhancements: dict[str, Any]) -> Path:
        """Phase 5: Save enhancement results for review."""
        logger.info("=" * 60)
        logger.info("PHASE 5: Save Results")
        logger.info("=" * 60)

        output_file = Path("artifacts/agent_enhancements.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Save as JSON
        with open(output_file, "w") as f:
            json.dump(enhancements, f, indent=2)

        logger.info(f"✓ Saved enhancement results to: {output_file}")

        # Generate summary report
        summary_file = Path("artifacts/agent_enhancements_summary.md")
        self._generate_summary_report(enhancements, summary_file)

        logger.info(f"✓ Saved summary report to: {summary_file}")

        return output_file

    def _generate_summary_report(
        self, enhancements: dict[str, Any], output_file: Path
    ) -> None:
        """Generate markdown summary report."""
        with open(output_file, "w") as f:
            f.write("# Agent Enhancement Report\n\n")
            f.write(
                f"Generated: {Path(__file__).name} using Ableton Live 12 Manual\n\n"
            )

            # Summary statistics
            total_agents = len(enhancements)
            total_recommendations = sum(
                len(e["recommendations"]) for e in enhancements.values()
            )
            high_priority = sum(
                1 for e in enhancements.values() if e["priority"] == "HIGH"
            )

            f.write("## Summary\n\n")
            f.write(f"- **Total Agents Analyzed**: {total_agents}\n")
            f.write(f"- **Total Recommendations**: {total_recommendations}\n")
            f.write(f"- **High Priority Agents**: {high_priority}\n\n")

            # Per-agent details
            f.write("## Agent Details\n\n")

            # Sort by priority
            sorted_agents = sorted(
                enhancements.items(),
                key=lambda x: {"HIGH": 3, "MEDIUM": 2, "LOW": 1}[x[1]["priority"]],
                reverse=True,
            )

            for agent_name, data in sorted_agents:
                f.write(f"### {agent_name}\n\n")
                f.write(f"**Purpose**: {data['purpose']}\n\n")
                f.write(f"**Priority**: {data['priority']}\n\n")
                f.write(
                    f"**Documentation Found**: {data['total_docs_found']} chunks\n\n"
                )

                if data["recommendations"]:
                    f.write("**Recommendations**:\n\n")
                    for i, rec in enumerate(data["recommendations"], 1):
                        f.write(f"{i}. **{rec['query']}**\n")
                        f.write(f"   - Relevance: {rec['relevance']:.2f}\n")
                        f.write(f"   - Section: {rec['section']}\n")
                        f.write(f"   - Page: {rec['page']}\n")
                        f.write(f"   - Suggestion: {rec['suggestion']}\n")
                        f.write(f"   - Excerpt: {rec['excerpt']}\n\n")
                else:
                    f.write("*No recommendations generated*\n\n")

                f.write("---\n\n")

    async def run_pipeline(self) -> None:
        """Run the complete enhancement pipeline."""
        logger.info("Starting Agent Enhancement Pipeline")
        logger.info("=" * 60)

        try:
            # Phase 2: Analyze agents
            agent_analysis = await self.phase_2_analyze_agents()

            # Phase 3: Search documentation
            search_results = await self.phase_3_search_documentation(agent_analysis)

            # Phase 4: Generate enhancements
            enhancements = await self.phase_4_generate_enhancements(search_results)

            # Phase 5: Save results
            output_file = await self.phase_5_save_results(enhancements)

            logger.info("=" * 60)
            logger.info("Pipeline Complete!")
            logger.info(f"Results saved to: {output_file}")
            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            raise


async def main():
    """Main entry point."""
    enhancer = AgentEnhancer()
    await enhancer.run_pipeline()


if __name__ == "__main__":
    asyncio.run(main())
