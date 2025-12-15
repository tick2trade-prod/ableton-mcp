#!/usr/bin/env python3
"""
Evaluate SOTA Researcher v2 using RAGAS metrics and log to MLflow.

This script:
1. Creates a test dataset with research topics
2. Wraps the sota_researcher_v2 agent as a chain factory for LangSmith evaluation
3. Runs RAGAS evaluation via LangSmith
4. Logs all metrics to MLflow for tracking

Prerequisites:
- MLflow server running (docker-compose up -d mlflow) or local SQLite backend
- LangSmith API key set (LANGCHAIN_API_KEY environment variable)
- RAGAS dependencies installed
- DeepAgents and MCP tools configured
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from ragas.datasets import TestDataset

from app.evaluation.ragas_mlflow import RagasMLflowEvaluator

# Import sota_researcher_v2 functions
from scripts.deepagents.sota_researcher_v2 import research_and_plan


def create_research_chain_factory():
    """
    Create a chain factory for evaluating sota_researcher_v2.

    This wraps the async research_and_plan function to work with LangSmith evaluation.
    LangSmith expects a callable that takes inputs (dict) and returns outputs (dict).

    Returns:
        Callable chain factory compatible with LangSmith evaluation
    """

    async def research_chain_async(inputs: dict[str, Any]) -> dict[str, Any]:
        """
        Async chain function that invokes the research agent.

        Args:
            inputs: Dictionary with 'topic' and optionally 'research_questions'

        Returns:
            Dictionary with 'output' containing the research results
        """
        # Extract inputs from dataset
        topic = inputs.get("topic", "")
        research_questions = inputs.get("research_questions", None)
        output_path = inputs.get("output_path", None)

        # Validate topic
        if not topic or not topic.strip():
            return {"output": "Error: Topic cannot be empty", "error": "Empty topic provided"}

        # Run research
        try:
            result = await research_and_plan(
                topic=topic,
                research_questions=research_questions if research_questions else None,
                output_path=output_path if output_path else None,
            )

            # Extract output for evaluation
            # RAGAS expects 'output' key with the answer
            research_content = result.get("research_results", {}).get("agent_response", "")
            if not research_content:
                # Fallback to plan content
                research_content = result.get("plan", {}).get("content", "")

            return {
                "output": research_content,
                "success": result.get("success", False),
                "latency_ms": result.get("latency_ms", 0),
            }
        except Exception as e:
            return {
                "output": f"Error during research: {str(e)}",
                "error": str(e),
                "success": False,
            }

    # LangSmith can handle async functions, but we need to ensure it's properly awaited
    # For compatibility, we'll create a sync wrapper that runs the async function
    def research_chain_sync(inputs: dict[str, Any]) -> dict[str, Any]:
        """
        Sync wrapper for async research chain.

        Args:
            inputs: Dictionary with 'topic' and optionally 'research_questions'

        Returns:
            Dictionary with 'output' containing the research results
        """
        # Check if we're in an async context
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is running, we need to use a different approach
                # For LangSmith evaluation, this should be fine as it handles async
                return asyncio.run(research_chain_async(inputs))
            else:
                return loop.run_until_complete(research_chain_async(inputs))
        except RuntimeError:
            # No event loop, create one
            return asyncio.run(research_chain_async(inputs))

    # Return the async version - LangSmith should handle it
    # If not, we can use the sync wrapper
    return research_chain_async


def create_test_dataset() -> TestDataset:
    """
    Create a test dataset for evaluating SOTA Researcher v2.

    Returns:
        TestDataset with research topics and ground truth
    """
    test_data = {
        "topic": [
            "Vector search optimization techniques",
            "FastAPI best practices for production",
            "Python async patterns and performance",
        ],
        "research_questions": [
            ["What are the best vector search algorithms?", "How to optimize latency?"],
            ["What are production deployment best practices?", "How to handle errors?"],
            ["What are the performance implications?", "How to avoid common pitfalls?"],
        ],
        "ground_truth": [
            "Vector search optimization involves using efficient algorithms like HNSW, "
            "IVF, or product quantization. Latency can be optimized through indexing strategies, "
            "approximate search, and hardware acceleration.",
            "FastAPI production best practices include using async/await, proper error handling, "
            "request validation, logging, monitoring, and deployment with Docker/Kubernetes.",
            "Python async patterns require understanding of event loops, coroutines, and async/await. "
            "Performance can be improved by avoiding blocking operations and using async libraries.",
        ],
    }

    return TestDataset.from_dict(test_data)


def create_research_dataset() -> TestDataset:
    """
    Create a more comprehensive research dataset.

    Returns:
        TestDataset with diverse research topics
    """
    test_data = {
        "topic": [
            "LangGraph state management patterns",
            "RAGAS evaluation metrics for agent systems",
            "MCP server implementation best practices",
        ],
        "research_questions": [
            None,  # No specific questions
            ["What metrics are most relevant?", "How to interpret scores?"],
            ["What are the key patterns?", "How to handle errors?"],
        ],
        "ground_truth": [
            "LangGraph provides state management through state graphs with nodes and edges. "
            "State is passed between nodes and can be modified at each step.",
            "RAGAS metrics for agents include answer relevancy, context precision, context recall, "
            "and faithfulness. Scores range from 0-1 with higher being better.",
            "MCP servers should use stdio or SSE transport, handle errors gracefully, "
            "and provide clear tool descriptions.",
        ],
    }

    return TestDataset.from_dict(test_data)


async def evaluate_sota_researcher_v2(
    dataset_name: str = "sota-researcher-v2-test",
    experiment_name: str = "sota-researcher-v2-evaluations",
    mlflow_tracking_uri: str | None = None,
    run_name: str | None = None,
    use_comprehensive_dataset: bool = False,
    verbose: bool = True,
) -> dict[str, Any]:
    """
    Evaluate SOTA Researcher v2 agent using RAGAS metrics.

    Args:
        dataset_name: Name for the LangSmith dataset
        experiment_name: Name for the MLflow experiment
        mlflow_tracking_uri: MLflow tracking URI (defaults to env var or localhost:5000)
        run_name: Name for the evaluation run (auto-generated if None)
        use_comprehensive_dataset: Whether to use comprehensive dataset (default: False)
        verbose: Whether to print detailed progress

    Returns:
        Dictionary with evaluation results and MLflow run info
    """
    print("🚀 Evaluating SOTA Researcher v2 with RAGAS")
    print("=" * 60)

    # Check prerequisites
    if not os.environ.get("LANGCHAIN_API_KEY"):
        print("⚠️  Warning: LANGCHAIN_API_KEY not set.")
        print("   LangSmith features may not work. Set it with:")
        print("   export LANGCHAIN_API_KEY=your_key_here")
        print()

    # Create test dataset
    print("1. Creating test dataset...")
    if use_comprehensive_dataset:
        dataset = create_research_dataset()
    else:
        dataset = create_test_dataset()
    print(f"   ✅ Created dataset with {len(dataset.to_pandas())} examples")

    # Initialize evaluator
    print("2. Initializing RAGAS-MLflow evaluator...")
    evaluator = RagasMLflowEvaluator(
        mlflow_tracking_uri=mlflow_tracking_uri
        or os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5000"),
        experiment_name=experiment_name,
    )
    print(f"   ✅ Evaluator initialized (experiment: {experiment_name})")

    # Upload dataset to LangSmith
    print("3. Uploading dataset to LangSmith...")
    try:
        langsmith_dataset = evaluator.upload_dataset_to_langsmith(
            dataset=dataset,
            dataset_name=dataset_name,
            dataset_desc="Test dataset for SOTA Researcher v2 evaluation",
        )
        print(f"   ✅ Dataset uploaded: {langsmith_dataset.name}")
    except ValueError as e:
        if "already exists" in str(e):
            print(f"   ℹ️  Dataset already exists, using existing: {dataset_name}")
        else:
            raise

    # Create chain factory
    print("4. Creating chain factory for agent...")
    chain_factory = create_research_chain_factory()
    print("   ✅ Chain factory created")

    # Run evaluation
    print("5. Running RAGAS evaluation...")
    print("   This may take several minutes depending on the number of examples...")
    try:
        result = evaluator.evaluate_and_log(
            dataset_name=dataset_name,
            llm_or_chain_factory=chain_factory,
            run_name=run_name,
            verbose=verbose,
            tags={
                "version": "v2",
                "agent_type": "deepagents",
                "evaluator": "ragas",
            },
        )

        print("\n✅ Evaluation Complete!")
        print("=" * 60)
        print(f"MLflow Run ID: {result['mlflow_run_id']}")
        print(f"Experiment ID: {result['mlflow_experiment_id']}")
        print(f"Run Name: {result['run_name']}")
        print("\nMetrics logged:")
        for metric_name, metric_value in result.get("metrics", {}).items():
            print(
                f"  - {metric_name}: {metric_value:.4f}"
                if isinstance(metric_value, (int, float))
                else f"  - {metric_name}: {metric_value}"
            )

        mlflow_uri = mlflow_tracking_uri or os.environ.get(
            "MLFLOW_TRACKING_URI", "http://localhost:5000"
        )
        print(f"\n📊 View results in MLflow UI: {mlflow_uri}")
        print(f"   Experiment: {experiment_name}")
        print(f"   Run: {result['run_name']}")

        return result

    except Exception as e:
        print(f"\n❌ Error during evaluation: {e}")
        import traceback

        traceback.print_exc()
        raise


def main():
    """Main entry point for evaluation script."""
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate SOTA Researcher v2 with RAGAS")
    parser.add_argument(
        "--dataset-name",
        type=str,
        default="sota-researcher-v2-test",
        help="Name for the LangSmith dataset",
    )
    parser.add_argument(
        "--experiment-name",
        type=str,
        default="sota-researcher-v2-evaluations",
        help="Name for the MLflow experiment",
    )
    parser.add_argument(
        "--mlflow-tracking-uri",
        type=str,
        default=None,
        help="MLflow tracking URI (defaults to env var or http://localhost:5000)",
    )
    parser.add_argument(
        "--run-name",
        type=str,
        default=None,
        help="Name for the evaluation run (auto-generated if not provided)",
    )
    parser.add_argument(
        "--comprehensive",
        action="store_true",
        help="Use comprehensive research dataset",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress verbose output",
    )

    args = parser.parse_args()

    # Run evaluation
    result = asyncio.run(
        evaluate_sota_researcher_v2(
            dataset_name=args.dataset_name,
            experiment_name=args.experiment_name,
            mlflow_tracking_uri=args.mlflow_tracking_uri,
            run_name=args.run_name,
            use_comprehensive_dataset=args.comprehensive,
            verbose=not args.quiet,
        )
    )

    # Exit with appropriate code
    if result.get("metrics"):
        sys.exit(0)
    else:
        print("⚠️  Warning: No metrics were extracted from evaluation")
        sys.exit(1)


if __name__ == "__main__":
    main()
