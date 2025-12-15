#!/usr/bin/env python3
"""Test script to embed Ableton PDF into Redis."""

import asyncio
import logging
import sys
from pathlib import Path

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


async def main():
    """Test embedding the Ableton PDF."""
    logger.info("Starting PDF embedding test...")

    # Get settings
    settings = get_settings()
    logger.info(f"PDF path: {settings.pdf_path}")
    logger.info(f"PDF exists: {settings.pdf_path.exists()}")
    logger.info(f"Redis URL: {settings.redis_url}")
    logger.info(f"Embedding model: {settings.embedding_model}")

    # Create embeddings instance
    embeddings = AbletonDocEmbeddings(
        pdf_path=settings.pdf_path,
        redis_url=settings.redis_url,
        index_name=settings.redis_index_name,
        embedding_model=settings.embedding_model,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    # Test Redis connection
    logger.info("Testing Redis connection...")
    redis_client = embeddings._get_redis_client()
    if redis_client:
        logger.info("✓ Redis connection successful")
    else:
        logger.error("✗ Redis connection failed")
        return

    # Test embedding model
    logger.info("Testing embedding model...")
    model = embeddings._get_embedding_model()
    if model:
        logger.info("✓ Embedding model loaded")
    else:
        logger.error("✗ Embedding model failed to load")
        return

    # Run embedding
    logger.info("Starting PDF embedding...")
    try:
        result = await embeddings.embed_document()
        logger.info("✓ Embedding completed successfully!")
        logger.info(f"  - Chunks stored: {result.get('chunks_stored', 0)}")
        logger.info(f"  - Total pages: {result.get('total_pages', 0)}")
        logger.info(f"  - Total time: {result.get('total_elapsed_seconds', 0):.1f}s")
    except Exception as e:
        logger.error(f"✗ Embedding failed: {e}", exc_info=True)
        return


if __name__ == "__main__":
    asyncio.run(main())
