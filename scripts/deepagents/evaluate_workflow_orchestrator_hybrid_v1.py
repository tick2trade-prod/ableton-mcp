#!/usr/bin/env python3
"""Evaluate workflow_orchestrator_hybrid_v1 and log results to MLflow.

This script evaluates the workflow orchestrator agent and logs metrics to MLflow
for tracking performance over time.

Usage:
    uv run python scripts/deepagents/evaluate_workflow_orchestrator_hybrid_v1.py
    uv run python scripts/deepagents/evaluate_workflow_orchestrator_hybrid_v1.py --cycle 2 --feature prompt_caching
"""

import argparse
import asyncio
import logging
import os
import shutil
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.mcp.mlflow_evaluation import MLflowEvaluationContext

# Token counting support
try:
    from scripts.deepagents.token_counter import TokenCounter, get_token_counter

    TOKEN_COUNTER_AVAILABLE = True
except ImportError:
    TOKEN_COUNTER_AVAILABLE = False
    TokenCounter = None
    get_token_counter = None

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def observe_execution(operation_name: str, **context):
    """Context manager for observing operation execution with structured logging.

    Args:
        operation_name: Name of the operation being observed
        **context: Additional context to log
    """
    start_time = time.perf_counter()
    logger.info(f"Starting {operation_name}", extra={"context": context})

    try:
        yield
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            f"Completed {operation_name}",
            extra={"context": {**context, "elapsed_ms": elapsed_ms, "status": "success"}},
        )
    except Exception as e:
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        logger.error(
            f"Failed {operation_name}",
            extra={
                "context": {**context, "elapsed_ms": elapsed_ms, "status": "error", "error": str(e)}
            },
            exc_info=True,
        )
        raise


async def execute_with_timeout(coro: Any, timeout: float, operation_name: str) -> Any:
    """Execute coroutine with timeout and observability.

    Args:
        coro: Coroutine to execute
        timeout: Timeout in seconds
        operation_name: Name for logging

    Returns:
        Result from coroutine

    Raises:
        TimeoutError: If timeout is exceeded
    """
    async with observe_execution(f"{operation_name}_timeout", timeout=timeout):
        try:
            result = await asyncio.wait_for(coro, timeout=timeout)
            logger.debug(f"{operation_name} completed within timeout")
            return result
        except TimeoutError:
            logger.warning(f"{operation_name} timed out after {timeout}s")
            raise TimeoutError(f"{operation_name} timed out after {timeout} seconds")


def validate_prerequisites() -> tuple[bool, list[str]]:
    """Validate prerequisites for evaluation.

    Returns:
        Tuple of (is_valid, list of error messages)
    """
    errors = []
    uv_path = shutil.which("uv")
    if not uv_path:
        errors.append(
            "uv binary not found in PATH. "
            "Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
        )
    return len(errors) == 0, errors


def create_test_data() -> list[dict[str, Any]]:
    """Create test data for workflow orchestrator evaluation.

    Returns list of test cases with:
    - feature_name: Feature to implement
    - workflow_steps: Steps to execute
    - expected_result: Expected outcome
    """
    return [
        {
            "feature_name": "eval_test_simple",
            "workflow_steps": ["setup"],
            "expected_result": "Workflow should complete setup step",
        },
        {
            "feature_name": "eval_test_planning",
            "workflow_steps": ["setup", "planning"],
            "expected_result": "Workflow should complete setup and planning steps",
        },
    ]


async def evaluate_workflow_orchestrator(
    cycle: int | None = None,
    feature_name: str | None = None,
    baseline_run_id: str | None = None,
) -> dict[str, Any]:
    """Evaluate workflow_orchestrator_hybrid_v1 and log results to MLflow.

    Args:
        cycle: Cycle number (optional, for TCEL cycles)
        feature_name: Feature name (optional, for TCEL cycles)
        baseline_run_id: Baseline run ID for comparison (optional)

    Returns:
        Dictionary with evaluation results and MLflow run info

    Raises:
        RuntimeError: If prerequisites are not met or evaluation fails
    """
    async with observe_execution(
        "evaluate_workflow_orchestrator", cycle=cycle, feature_name=feature_name
    ):
        # Validate prerequisites
        is_valid, errors = validate_prerequisites()
        if not is_valid:
            error_msg = "Prerequisites validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        from scripts.deepagents.workflow_orchestrator_hybrid_v1 import (
            orchestrate_workflow,
        )

        # Create test data
        test_data = create_test_data()
        logger.info(f"Created {len(test_data)} test cases")

        # Determine run name
        if cycle is not None and feature_name:
            run_name = f"workflow_orchestrator_hybrid_v1_cycle_{cycle}_{feature_name}"
        elif cycle == 0:
            run_name = "workflow_orchestrator_hybrid_v1_baseline"
        else:
            run_name = "workflow_orchestrator_hybrid_v1_evaluation"

        # Get model configuration
        ollama_model = os.environ.get("OLLAMA_MODEL", "llama3.1:8b-optimized")
        workflow_model = os.environ.get("WORKFLOW_ORCHESTRATOR_MODEL", ollama_model)

        additional_params = {
            "dataset_size": len(test_data),
            "ollama_integration": True,
            "ollama_model": ollama_model,
            "workflow_model": workflow_model,
            "cost": 0.0,
        }

        if cycle is not None:
            additional_params["cycle"] = cycle
        if feature_name:
            additional_params["feature"] = feature_name
        if baseline_run_id:
            additional_params["baseline_run_id"] = baseline_run_id

        # Initialize token counter if available
        token_counter = None
        if TOKEN_COUNTER_AVAILABLE:
            try:
                token_counter = get_token_counter()
                logger.info("Token counting enabled")
            except Exception as e:
                logger.warning(f"Token counter initialization failed: {e}")

        # Use MLflowEvaluationContext for standardized tracking
        with MLflowEvaluationContext(
            experiment_name="workflow-orchestrator-hybrid-evaluations",
            run_name=run_name,
            agent="workflow-orchestrator-hybrid-v1",
            version="1.0",
            evaluation_type="basic",
            additional_params=additional_params,
        ) as ctx:
            results = []
            total_tokens = 0

            # Evaluate each test case
            for i, test_case in enumerate(test_data):
                test_feature_name = test_case["feature_name"]
                workflow_steps = test_case.get("workflow_steps")

                async with observe_execution(
                    f"test_case_{i + 1}",
                    feature_name=test_feature_name,
                    workflow_steps=workflow_steps,
                ):
                    logger.info(
                        f"Evaluating test case {i + 1}/{len(test_data)}: {test_feature_name}"
                    )

                    try:
                        if not test_feature_name:
                            raise ValueError("feature_name cannot be None")

                        # Execute workflow with timeout (60s per test case to allow for setup + planning)
                        workflow_result = await execute_with_timeout(
                            orchestrate_workflow(
                                feature_name=test_feature_name,
                                workflow_steps=workflow_steps,
                            ),
                            timeout=60.0,  # Increased from 30s to allow workflows to complete
                            operation_name=f"test_case_{i + 1}_workflow",
                        )

                        # Extract result from workflow response
                        # Log the actual workflow result structure for debugging
                        logger.info(
                            f"Workflow result for test case {i + 1}",
                            extra={
                                "context": {
                                    "workflow_result_keys": list(workflow_result.keys())
                                    if isinstance(workflow_result, dict)
                                    else "not_a_dict",
                                    "workflow_result_type": type(workflow_result).__name__,
                                    "has_success": "success" in workflow_result
                                    if isinstance(workflow_result, dict)
                                    else False,
                                    "success_value": workflow_result.get("success")
                                    if isinstance(workflow_result, dict)
                                    else None,
                                }
                            },
                        )

                        # Extract result from workflow response
                        if isinstance(workflow_result, dict):
                            result = {
                                "success": workflow_result.get("success", False),
                                "latency_ms": workflow_result.get("latency_ms", 0.0),
                                "results": workflow_result.get("results", {}),
                            }
                            if not result["success"]:
                                result["error"] = workflow_result.get("error", "Unknown error")
                        else:
                            # Fallback if result is not a dict
                            logger.warning(
                                f"Unexpected workflow result type: {type(workflow_result)}"
                            )
                            result = {
                                "success": False,
                                "error": f"Unexpected result type: {type(workflow_result)}",
                                "latency_ms": 0.0,
                            }

                        logger.info(
                            f"Test case {i + 1} extracted result",
                            extra={
                                "context": {
                                    "success": result["success"],
                                    "latency_ms": result["latency_ms"],
                                }
                            },
                        )

                    except TimeoutError as e:
                        logger.warning(f"Test case {i + 1} timed out: {e}")
                        result = {
                            "success": False,
                            "error": "Workflow execution timed out",
                            "latency_ms": 60000.0,  # Updated to match timeout
                        }
                    except Exception as e:
                        logger.error(f"Test case {i + 1} failed: {e}", exc_info=True)
                        result = {
                            "success": False,
                            "error": str(e),
                            "latency_ms": 0.0,
                        }

                    # Count tokens if available
                    tokens_used = 0
                    if token_counter and result.get("success"):
                        result_content = str(result.get("results", ""))
                        if result_content:
                            tokens_used = token_counter.count_tokens(result_content)
                            total_tokens += tokens_used

                    # Prepare result for logging
                    result_for_logging = {
                        "success": result.get("success", False),
                        "latency_ms": result.get("latency_ms", 0.0),
                    }
                    if tokens_used > 0:
                        result_for_logging["tokens"] = tokens_used
                    if not result.get("success"):
                        result_for_logging["error"] = result.get("error", "Unknown error")

                    # Log per-test-case metrics
                    if result.get("success"):
                        ctx.log_test_case_metric(i, "success", 1)
                        if "latency_ms" in result:
                            ctx.log_test_case_metric(i, "latency_ms", result["latency_ms"])
                        if tokens_used > 0:
                            ctx.log_test_case_metric(i, "tokens", tokens_used)
                    else:
                        ctx.log_test_case_metric(i, "success", 0)

                    results.append(result_for_logging)
                    logger.info(
                        f"Test case {i + 1} completed",
                        extra={
                            "context": {
                                "success": result.get("success", False),
                                "latency_ms": result.get("latency_ms", 0.0),
                                "tokens_used": tokens_used,
                            }
                        },
                    )

            # Calculate and log aggregated results
            async with observe_execution("log_results_to_mlflow", num_results=len(results)):
                metrics = None
                if total_tokens > 0:
                    successful_results = [r for r in results if r.get("success", False)]
                    avg_tokens = total_tokens / len(successful_results) if successful_results else 0
                    metrics = {
                        "total_tokens": total_tokens,
                        "avg_tokens_per_request": avg_tokens,
                    }

                # Log to MLflow
                try:
                    summary = ctx.log_evaluation_results(results, metrics=metrics)
                except Exception as e:
                    logger.error(f"Error logging to MLflow: {e}", exc_info=True)
                    # Create fallback summary
                    summary = {
                        "mlflow_run_id": "error",
                        "mlflow_experiment_id": "error",
                        "metrics": {
                            "success_rate": sum(1 for r in results if r.get("success", False))
                            / len(results)
                            if results
                            else 0.0,
                            "avg_latency_ms": sum(r.get("latency_ms", 0.0) for r in results)
                            / len(results)
                            if results
                            else 0.0,
                        },
                    }

                summary_metrics = summary.get("metrics", {})
                logger.info(
                    "Evaluation complete",
                    extra={
                        "context": {
                            "success_rate": summary_metrics.get("success_rate", 0.0),
                            "avg_latency_ms": summary_metrics.get("avg_latency_ms", 0.0),
                            "total_tokens": total_tokens,
                        }
                    },
                )

                return {
                    "run_id": summary["mlflow_run_id"],
                    "experiment_id": summary["mlflow_experiment_id"],
                    "success_rate": summary_metrics.get("success_rate", 0.0),
                    "avg_latency_ms": summary_metrics.get("avg_latency_ms", 0.0),
                    "avg_tokens_per_request": summary_metrics.get("avg_tokens_per_request", 0),
                    "results": results,
                }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Evaluate Workflow Orchestrator Hybrid v1")
    parser.add_argument("--cycle", type=int, help="Cycle number (for TCEL cycles)")
    parser.add_argument("--feature", type=str, help="Feature name (for TCEL cycles)")
    parser.add_argument(
        "--baseline-run-id", type=str, help="Baseline run ID for comparison (for cycle evaluation)"
    )
    parser.add_argument("--baseline", action="store_true", help="Run baseline evaluation (cycle=0)")

    args = parser.parse_args()

    logger.info("Starting Workflow Orchestrator Hybrid V1 evaluation")
    logger.info("=" * 60)

    # Handle --baseline flag
    cycle = args.cycle
    if args.baseline:
        cycle = 0
        logger.info("Running baseline evaluation (cycle=0)")

    try:
        # Use standard asyncio.run - much simpler than custom event loop management
        result = asyncio.run(
            evaluate_workflow_orchestrator(
                cycle=cycle, feature_name=args.feature, baseline_run_id=args.baseline_run_id
            )
        )

        logger.info("\n" + "=" * 60)
        logger.info("Evaluation completed successfully!")
        logger.info(f"MLflow run ID: {result.get('run_id', 'N/A')}")

        print("\nEvaluation Results:")
        print(f"  Run ID: {result.get('run_id', 'N/A')}")
        print(f"  Success Rate: {result['success_rate']:.1%}")
        print(f"  Avg Latency: {result['avg_latency_ms']:.1f}ms")

        return 0

    except KeyboardInterrupt:
        logger.warning("Evaluation interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Evaluation failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
