#!/usr/bin/env python3
"""Evaluate autonomous_code_streaming_refactor_orchestrator_v1 and log results to MLflow.

This script evaluates the autonomous code streaming refactor orchestrator agent and logs metrics to MLflow
for tracking performance over time.

Usage:
    uv run python scripts/deepagents/evaluate_autonomous_code_streaming_refactor_orchestrator_v1.py
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.mcp.mlflow_evaluation import MLflowEvaluationContext

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def create_test_data() -> list[dict[str, Any]]:
    """Create test data for refactor orchestrator evaluation.

    Returns list of test cases with:
    - target_path: Path to refactor (file or directory)
    - refactoring_goals: List of refactoring goals
    - ground_truth: Expected refactoring outcome
    """
    return [
        {
            "target_path": "scripts/deepagents/",
            "refactoring_goals": [
                "Improve error handling",
                "Add type hints",
                "Extract common patterns",
            ],
            "ground_truth": "Refactoring should improve code quality, add type hints, and extract common patterns.",
        },
        {
            "target_path": "scripts/deepagents/create_new_agent_v1.py",
            "refactoring_goals": [
                "Extract streaming codegen into separate module",
                "Improve error handling",
            ],
            "ground_truth": "Refactoring should extract streaming codegen and improve error handling.",
        },
        {
            "target_path": "app/mcp/",
            "refactoring_goals": ["Add type hints", "Improve documentation"],
            "ground_truth": "Refactoring should add type hints and improve documentation.",
        },
    ]


async def evaluate_refactor_orchestrator() -> dict[str, Any]:
    """Evaluate autonomous_code_streaming_refactor_orchestrator_v1 and log results to MLflow.

    Returns:
        Dictionary with evaluation results and MLflow run info
    """
    from scripts.deepagents.autonomous_code_streaming_refactor_orchestrator_v1 import (
        analyze_codebase_for_refactoring,
        stream_refactor_code,
    )

    # Create test data
    test_data = create_test_data()

    # Use MLflowEvaluationContext for standardized tracking
    with MLflowEvaluationContext(
        experiment_name="refactor-orchestrator-evaluations",
        run_name="refactor_orchestrator_v1_evaluation",
        agent="autonomous-code-refactor-orchestrator-v1",
        version="1.0",
        evaluation_type="basic",
        additional_params={"dataset_size": len(test_data)},
    ) as ctx:
        # Run agent on test data
        logger.info("Running agent on test data...")
        results = []

        for i, test_case in enumerate(test_data):
            target_path = test_case["target_path"]
            refactoring_goals = test_case.get("refactoring_goals")
            ground_truth = test_case.get("ground_truth")

            logger.info(f"Evaluating test case {i + 1}/{len(test_data)}: {target_path}...")

            try:
                # Run analysis
                result = await analyze_codebase_for_refactoring(
                    target_path=target_path,
                    refactoring_goals=refactoring_goals if refactoring_goals else None,
                )

                # Extract metrics
                success = result.get("success", False)
                latency_ms = result.get("latency_ms", 0.0)
                analysis = result.get("analysis", {})
                content = analysis.get("content", "") if isinstance(analysis, dict) else ""

                # Prepare result for logging
                result_for_logging = {
                    "target_path": target_path,
                    "success": success,
                    "latency_ms": latency_ms,
                    "content_length": len(content) if success else 0,
                    "has_ground_truth": ground_truth is not None,
                }

                # Log per-test-case metrics
                if success:
                    ctx.log_test_case_metric(i, "success", 1)
                    ctx.log_test_case_metric(i, "latency_ms", latency_ms)
                    ctx.log_test_case_metric(i, "content_length", len(content))
                else:
                    error = result.get("error", "Unknown error")
                    logger.warning(f"Test case {i + 1} failed: {error}")
                    ctx.log_test_case_metric(i, "success", 0)
                    result_for_logging["error"] = error

                results.append(result_for_logging)

            except Exception as e:
                logger.error(f"Error evaluating test case {i + 1}: {e}", exc_info=True)
                ctx.log_test_case_metric(i, "success", 0)
                results.append(
                    {
                        "target_path": target_path,
                        "success": False,
                        "error": str(e),
                    }
                )

        # Test streaming code generation
        logger.info("Testing streaming code generation...")
        test_code = """
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
"""
        try:
            stream_result = await stream_refactor_code(
                code=test_code,
                refactoring_type="improve_error_handling",
                model="codellama",
            )
            stream_success = stream_result.get("success", False)
            stream_latency = stream_result.get("latency_ms", 0.0)
            ctx.log_metric("streaming_codegen_success", 1 if stream_success else 0)
            ctx.log_metric("streaming_codegen_latency_ms", stream_latency)
        except Exception as e:
            logger.warning(f"Streaming code generation test failed: {e}")
            ctx.log_metric("streaming_codegen_success", 0)

        # Log aggregated results (automatically calculates metrics)
        summary = ctx.log_evaluation_results(results)

        logger.info(f"Evaluation complete. MLflow run ID: {summary['mlflow_run_id']}")
        logger.info(f"Average latency: {summary['metrics']['avg_latency_ms']:.2f}ms")
        logger.info(f"Success rate: {summary['metrics']['success_rate']:.2%}")

        return summary


def main():
    """Main entry point."""
    logger.info("Starting Autonomous Code Streaming Refactor Orchestrator V1 evaluation")
    logger.info("=" * 60)

    try:
        result = asyncio.run(evaluate_refactor_orchestrator())
        logger.info("\n" + "=" * 60)
        logger.info("Evaluation completed successfully!")
        logger.info(f"MLflow run ID: {result['mlflow_run_id']}")
        # Get tracking URI from context if available
        try:
            import mlflow

            tracking_uri = mlflow.get_tracking_uri()
            logger.info(f"View results at: {tracking_uri}")
        except Exception:
            logger.info("MLflow tracking URI not available")
        return 0
    except Exception as e:
        logger.error(f"Evaluation failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
