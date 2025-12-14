#!/usr/bin/env python3
"""Batch processing for parallel code generation (Claude feature integration).

Enables 5-20x faster processing for multiple features by executing in parallel.
Uses asyncio.gather() for concurrent execution.
"""

import asyncio
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logger = None
try:
    import logging

    logger = logging.getLogger("batch-processor-ollama")
except Exception:
    pass


class BatchProcessorOllama:
    """Batch processor for parallel code generation using Ollama.

    Processes multiple code generation tasks in parallel for 5-20x speedup.
    """

    def __init__(self, max_concurrent: int = 5):
        """Initialize batch processor.

        Args:
            max_concurrent: Maximum concurrent operations (default: 5)
        """
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def process_batch(
        self,
        tasks: list[str],
        process_func: callable,
        batch_size: int | None = None,
    ) -> list[dict[str, Any]]:
        """Process multiple tasks in parallel batches.

        Args:
            tasks: List of task descriptions
            process_func: Async function to process each task
            batch_size: Optional batch size (default: max_concurrent)

        Returns:
            List of results for each task
        """
        if batch_size is None:
            batch_size = self.max_concurrent

        results = []

        # Process in batches
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i : i + batch_size]
            batch_results = await self._process_batch_parallel(batch, process_func)
            results.extend(batch_results)

        return results

    async def _process_batch_parallel(
        self, tasks: list[str], process_func: callable
    ) -> list[dict[str, Any]]:
        """Process a batch of tasks in parallel.

        Args:
            tasks: Batch of tasks
            process_func: Async function to process each task

        Returns:
            List of results
        """

        async def process_with_semaphore(task: str) -> dict[str, Any]:
            """Process single task with semaphore control."""
            async with self.semaphore:
                return await process_func(task)

        task_coroutines = [process_with_semaphore(task) for task in tasks]
        return await asyncio.gather(*task_coroutines, return_exceptions=True)

    async def process_batch_with_retry(
        self,
        tasks: list[str],
        process_func: callable,
        max_retries: int = 3,
    ) -> list[dict[str, Any]]:
        """Process batch with automatic retry on failure.

        Args:
            tasks: List of tasks
            process_func: Async function to process each task
            max_retries: Maximum retry attempts

        Returns:
            List of results
        """
        results = await self.process_batch(tasks, process_func)

        # Retry failed requests
        failed_indices = [i for i, result in enumerate(results) if not self._is_success(result)]

        for retry in range(max_retries):
            if not failed_indices:
                break

            # Retry failed tasks
            failed_tasks = [tasks[i] for i in failed_indices]
            retry_results = await self.process_batch(failed_tasks, process_func)

            # Update results
            for idx, retry_result in zip(failed_indices, retry_results, strict=False):
                if self._is_success(retry_result):
                    results[idx] = retry_result

            # Update failed indices
            failed_indices = [i for i in failed_indices if not self._is_success(results[i])]

        return results

    def _is_success(self, result: Any) -> bool:
        """Check if result indicates success."""
        if isinstance(result, Exception):
            return False
        if isinstance(result, dict):
            return result.get("success", False)
        return True
