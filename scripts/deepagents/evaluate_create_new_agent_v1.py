#!/usr/bin/env python3
"""Evaluate create_new_agent_v1 and log results to MLflow.

This script evaluates the create_new_agent_v1 agent and logs metrics to MLflow
for tracking performance over time.

Usage:
    uv run python scripts/deepagents/evaluate_create_new_agent_v1.py
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
    """Create test data for create_new_agent evaluation.

    Returns list of test cases with:
    - agent_name: Name of agent to create
    - description: What the agent should do
    - requirements: Optional requirements
    - ground_truth: Expected outcome
    """
    return [
        {
            "agent_name": "code_generator",
            "description": "Generates Python code based on requirements",
            "requirements": "Should use filesystem MCP and support validation",
            "ground_truth": "Agent should generate code generation agent with filesystem tools",
        },
        {
            "agent_name": "test_runner",
            "description": "Runs tests and reports results",
            "requirements": None,
            "ground_truth": "Agent should generate test runner agent",
        },
        {
            "agent_name": "documentation_generator",
            "description": "Generates documentation from code",
            "requirements": "Should use indexing-semantic-search-v2 for code analysis",
            "ground_truth": "Agent should generate documentation agent with semantic search",
        },
    ]


async def evaluate_create_new_agent() -> dict[str, Any]:
    """Evaluate create_new_agent_v1 and log results to MLflow.

    Returns:
        Dictionary with evaluation results and MLflow run info
    """
    from scripts.deepagents.create_new_agent_v1 import (
        create_agent_spec,
        generate_agent_files,
        validate_agent_files,
    )

    # Create test data
    test_data = create_test_data()

    # Use MLflowEvaluationContext for standardized tracking
    with MLflowEvaluationContext(
        experiment_name="create-new-agent-evaluations",
        run_name="create_new_agent_v1_evaluation",
        agent="create-new-agent-v1",
        version="1.0",
        evaluation_type="agent_creation",
        additional_params={"dataset_size": len(test_data)},
    ) as ctx:
        # Run agent on test data
        logger.info("Running agent on test data...")
        results = []

        for i, test_case in enumerate(test_data):
            agent_name = test_case["agent_name"]
            description = test_case["description"]
            requirements = test_case.get("requirements")
            ground_truth = test_case.get("ground_truth")

            logger.info(f"Evaluating test case {i + 1}/{len(test_data)}: {agent_name}...")

            try:
                # Step 1: Create agent spec
                spec_result = await create_agent_spec(
                    agent_name=agent_name,
                    description=description,
                    requirements=requirements,
                )

                if not spec_result.get("success"):
                    logger.warning(
                        f"Test case {i + 1} failed at spec creation: {spec_result.get('error')}"
                    )
                    ctx.log_test_case_metric(i, "success", 0)
                    results.append(
                        {
                            "agent_name": agent_name,
                            "success": False,
                            "error": spec_result.get("error"),
                        }
                    )
                    continue

                spec = spec_result.get("spec", {})
                spec_latency = spec_result.get("latency_ms", 0.0)

                # Step 2: Generate files
                files_result = await generate_agent_files(spec=spec)

                if not files_result.get("success"):
                    logger.warning(
                        f"Test case {i + 1} failed at file generation: {files_result.get('error')}"
                    )
                    ctx.log_test_case_metric(i, "success", 0)
                    results.append(
                        {
                            "agent_name": agent_name,
                            "success": False,
                            "error": files_result.get("error"),
                        }
                    )
                    continue

                files = files_result.get("files", {})
                files_latency = files_result.get("latency_ms", 0.0)

                # Step 3: Validate files
                validation_result = await validate_agent_files(files=files)

                validation_latency = validation_result.get("latency_ms", 0.0)
                is_valid = validation_result.get("valid", False)
                errors = validation_result.get("errors", [])
                warnings = validation_result.get("warnings", [])

                total_latency = spec_latency + files_latency + validation_latency

                if is_valid and len(files) == 5:
                    # Log per-test-case metrics (including step-specific metrics)
                    ctx.log_test_case_metric(i, "success", 1)
                    ctx.log_test_case_metric(i, "latency_ms", total_latency)
                    ctx.log_test_case_metric(i, "spec_latency_ms", spec_latency)
                    ctx.log_test_case_metric(i, "files_latency_ms", files_latency)
                    ctx.log_test_case_metric(i, "validation_latency_ms", validation_latency)
                    ctx.log_test_case_metric(i, "num_files", len(files))
                    ctx.log_test_case_metric(i, "num_errors", len(errors))
                    ctx.log_test_case_metric(i, "num_warnings", len(warnings))

                    results.append(
                        {
                            "agent_name": agent_name,
                            "success": True,
                            "latency_ms": total_latency,
                            "num_files": len(files),
                            "num_errors": len(errors),
                            "num_warnings": len(warnings),
                            "has_ground_truth": ground_truth is not None,
                        }
                    )
                else:
                    logger.warning(
                        f"Test case {i + 1} validation failed: {len(errors)} errors, {len(warnings)} warnings"
                    )
                    ctx.log_test_case_metric(i, "success", 0)
                    results.append(
                        {
                            "agent_name": agent_name,
                            "success": False,
                            "errors": errors,
                            "warnings": warnings,
                        }
                    )

            except Exception as e:
                logger.error(f"Error evaluating test case {i + 1}: {e}", exc_info=True)
                ctx.log_test_case_metric(i, "success", 0)
                results.append(
                    {
                        "agent_name": agent_name,
                        "success": False,
                        "error": str(e),
                    }
                )

        # Log aggregated results (automatically calculates metrics)
        summary = ctx.log_evaluation_results(results)

        logger.info(f"Evaluation complete. MLflow run ID: {summary['mlflow_run_id']}")
        logger.info(f"Average latency: {summary['metrics']['avg_latency_ms']:.2f}ms")
        logger.info(f"Success rate: {summary['metrics']['success_rate']:.2%}")

        return summary


def main():
    """Main entry point."""
    logger.info("Starting Create New Agent V1 evaluation")
    logger.info("=" * 60)

    try:
        result = asyncio.run(evaluate_create_new_agent())
        logger.info("\n" + "=" * 60)
        logger.info("Evaluation completed successfully!")
        logger.info(f"MLflow run ID: {result['mlflow_run_id']}")
        import mlflow

        logger.info(f"View results at: {mlflow.get_tracking_uri()}")
        return 0
    except Exception as e:
        logger.error(f"Evaluation failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
