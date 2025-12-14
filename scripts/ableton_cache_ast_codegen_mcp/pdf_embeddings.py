#!/usr/bin/env python3
"""PDF embeddings for Ableton Live documentation.

Extracts, chunks, and embeds the Ableton Live 12 manual into Redis
for semantic search during code generation.
"""

import hashlib
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger("ableton-codegen-pdf")

# Optional imports with graceful fallbacks
try:
    import fitz  # PyMuPDF

    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    fitz = None

try:
    from sentence_transformers import SentenceTransformer

    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None

try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None

try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None


class Chunk:
    """A chunk of text from the PDF."""

    def __init__(
        self,
        text: str,
        page_num: int,
        section: str = "",
        chunk_id: str = "",
    ):
        self.text = text
        self.page_num = page_num
        self.section = section
        self.chunk_id = chunk_id or self._generate_id()

    def _generate_id(self) -> str:
        """Generate unique chunk ID."""
        content = f"{self.page_num}:{self.section}:{self.text[:100]}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "page_num": self.page_num,
            "section": self.section,
        }


class AbletonDocEmbeddings:
    """Embed and search Ableton Live documentation."""

    def __init__(
        self,
        pdf_path: str | Path = "docs/live12-manual-en.pdf",
        redis_url: str = "redis://localhost:6379",
        index_name: str = "ableton_docs",
        embedding_model: str = "all-MiniLM-L6-v2",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.pdf_path = Path(pdf_path)
        self.redis_url = redis_url
        self.index_name = index_name
        self.embedding_model_name = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self._redis_client = None
        self._embedding_model = None

    def _get_redis_client(self):
        """Get or create Redis client."""
        if not REDIS_AVAILABLE:
            logger.warning("Redis not available. Install with: uv add redis")
            return None

        if self._redis_client is None:
            try:
                self._redis_client = redis.from_url(
                    self.redis_url,
                    decode_responses=False,  # Binary for vectors
                )
                self._redis_client.ping()
                logger.info(f"Redis connected: {self.redis_url}")
            except Exception as e:
                logger.error(f"Redis connection failed: {e}")
                return None

        return self._redis_client

    def _get_embedding_model(self):
        """Get or create embedding model."""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            logger.warning(
                "sentence-transformers not available. "
                "Install with: uv add sentence-transformers"
            )
            return None

        if self._embedding_model is None:
            try:
                logger.info(f"Loading embedding model: {self.embedding_model_name}")
                self._embedding_model = SentenceTransformer(self.embedding_model_name)
                logger.info("Embedding model loaded")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                return None

        return self._embedding_model

    def extract_pdf_text(self) -> list[dict[str, Any]]:
        """Extract text from PDF with page metadata.

        Returns:
            List of dicts with 'page_num', 'text', 'section'
        """
        if not PYMUPDF_AVAILABLE:
            raise ImportError("PyMuPDF required. Install with: uv add pymupdf")

        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")

        logger.info(f"Extracting text from: {self.pdf_path}")
        start_time = time.perf_counter()

        pages = []
        doc = fitz.open(str(self.pdf_path))

        current_section = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()

            # Try to extract section headers (typically larger fonts)
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            # Detect headers by font size
                            if span["size"] > 14 and len(span["text"].strip()) > 3:
                                current_section = span["text"].strip()
                                break

            pages.append(
                {
                    "page_num": page_num + 1,
                    "text": text.strip(),
                    "section": current_section,
                }
            )

        doc.close()

        elapsed = time.perf_counter() - start_time
        logger.info(f"Extracted {len(pages)} pages in {elapsed:.1f}s")

        return pages

    def chunk_document(self, pages: list[dict[str, Any]]) -> list[Chunk]:
        """Chunk pages into smaller pieces for embedding.

        Uses semantic chunking with overlap.
        """
        chunks = []

        for page in pages:
            text = page["text"]
            page_num = page["page_num"]
            section = page["section"]

            if not text or len(text) < 50:
                continue

            # Simple chunking by character count with overlap
            start = 0
            while start < len(text):
                end = start + self.chunk_size
                chunk_text = text[start:end]

                # Try to break at sentence boundary
                if end < len(text):
                    last_period = chunk_text.rfind(".")
                    if last_period > self.chunk_size // 2:
                        chunk_text = chunk_text[: last_period + 1]
                        end = start + last_period + 1

                if chunk_text.strip():
                    chunks.append(
                        Chunk(
                            text=chunk_text.strip(),
                            page_num=page_num,
                            section=section,
                        )
                    )

                start = end - self.chunk_overlap

        logger.info(f"Created {len(chunks)} chunks from {len(pages)} pages")
        return chunks

    def generate_embeddings(self, chunks: list[Chunk]) -> list[tuple[Chunk, Any]]:
        """Generate embeddings for chunks.

        Returns:
            List of (chunk, embedding) tuples
        """
        model = self._get_embedding_model()
        if not model:
            raise RuntimeError("Embedding model not available")

        logger.info(f"Generating embeddings for {len(chunks)} chunks...")
        start_time = time.perf_counter()

        texts = [chunk.text for chunk in chunks]
        embeddings = model.encode(texts, show_progress_bar=True)

        elapsed = time.perf_counter() - start_time
        logger.info(f"Generated embeddings in {elapsed:.1f}s")

        return list(zip(chunks, embeddings, strict=False))

    def store_in_redis(
        self, chunk_embeddings: list[tuple[Chunk, Any]]
    ) -> dict[str, Any]:
        """Store chunks and embeddings in Redis.

        Returns:
            dict with storage stats
        """
        client = self._get_redis_client()
        if not client:
            raise RuntimeError("Redis not available")

        logger.info(f"Storing {len(chunk_embeddings)} chunks in Redis...")
        start_time = time.perf_counter()

        stored = 0
        for chunk, embedding in chunk_embeddings:
            key = f"{self.index_name}:chunk:{chunk.chunk_id}"

            # Store as hash with metadata and embedding
            data = {
                "text": chunk.text,
                "page_num": str(chunk.page_num),
                "section": chunk.section,
                "embedding": embedding.tobytes() if NUMPY_AVAILABLE else b"",
            }
            client.hset(key, mapping=data)
            stored += 1

        # Store index metadata
        meta_key = f"{self.index_name}:meta"
        client.hset(
            meta_key,
            mapping={
                "total_chunks": str(stored),
                "embedding_model": self.embedding_model_name,
                "chunk_size": str(self.chunk_size),
                "pdf_path": str(self.pdf_path),
                "indexed_at": str(int(time.time())),
            },
        )

        elapsed = time.perf_counter() - start_time
        logger.info(f"Stored {stored} chunks in {elapsed:.1f}s")

        return {
            "success": True,
            "chunks_stored": stored,
            "index_name": self.index_name,
            "elapsed_seconds": elapsed,
        }

    async def embed_document(self) -> dict[str, Any]:
        """Full pipeline: extract, chunk, embed, store.

        Returns:
            dict with embedding stats
        """
        start_time = time.perf_counter()

        # Extract text
        pages = self.extract_pdf_text()

        # Chunk
        chunks = self.chunk_document(pages)

        # Embed
        chunk_embeddings = self.generate_embeddings(chunks)

        # Store
        result = self.store_in_redis(chunk_embeddings)

        total_elapsed = time.perf_counter() - start_time
        result["total_pages"] = len(pages)
        result["total_elapsed_seconds"] = total_elapsed

        return result

    async def search_docs(
        self,
        query: str,
        top_k: int = 5,
    ) -> dict[str, Any]:
        """Search embedded documentation.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            dict with search results
        """
        model = self._get_embedding_model()
        client = self._get_redis_client()

        if not model or not client:
            return {
                "success": False,
                "error": "Embedding model or Redis not available",
                "results": [],
            }

        start_time = time.perf_counter()

        # Generate query embedding
        query_embedding = model.encode([query])[0]

        # Get all chunks (for simple cosine similarity search)
        # Note: For production, use Redis Vector Search (RediSearch)
        keys = client.keys(f"{self.index_name}:chunk:*")

        results = []
        for key in keys:
            data = client.hgetall(key)
            if not data:
                continue

            # Decode bytes
            text = data.get(b"text", b"").decode("utf-8")
            page_num = int(data.get(b"page_num", b"0").decode("utf-8"))
            section = data.get(b"section", b"").decode("utf-8")
            embedding_bytes = data.get(b"embedding", b"")

            if not embedding_bytes or not NUMPY_AVAILABLE:
                continue

            # Reconstruct embedding and compute similarity
            stored_embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
            similarity = float(
                np.dot(query_embedding, stored_embedding)
                / (np.linalg.norm(query_embedding) * np.linalg.norm(stored_embedding))
            )

            results.append(
                {
                    "text": text[:500],  # Truncate for response
                    "page_num": page_num,
                    "section": section,
                    "similarity": similarity,
                }
            )

        # Sort by similarity and take top_k
        results.sort(key=lambda x: x["similarity"], reverse=True)
        results = results[:top_k]

        elapsed = time.perf_counter() - start_time

        return {
            "success": True,
            "query": query,
            "results": results,
            "result_count": len(results),
            "latency_ms": elapsed * 1000,
        }

    def get_index_stats(self) -> dict[str, Any]:
        """Get statistics about the embedded index."""
        client = self._get_redis_client()
        if not client:
            return {"success": False, "error": "Redis not available"}

        meta_key = f"{self.index_name}:meta"
        meta = client.hgetall(meta_key)

        if not meta:
            return {
                "success": False,
                "error": "Index not found. Run embed_document first.",
            }

        return {
            "success": True,
            "total_chunks": int(meta.get(b"total_chunks", b"0").decode()),
            "embedding_model": meta.get(b"embedding_model", b"").decode(),
            "chunk_size": int(meta.get(b"chunk_size", b"0").decode()),
            "pdf_path": meta.get(b"pdf_path", b"").decode(),
            "indexed_at": int(meta.get(b"indexed_at", b"0").decode()),
        }
