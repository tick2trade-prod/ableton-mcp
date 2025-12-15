#!/usr/bin/env python3
"""Example Core Logic.

This is an example of a core logic module that can be plugged into the MCP server.
It's based on the original GAM DeepAgents Core Logic v3.
"""

import asyncio
import logging
import os
import re
import shutil
import time
from collections.abc import AsyncIterator, Callable
from contextlib import nullcontext
from pathlib import Path
from typing import Any

from .base_core import BaseCore
from .settings import Settings, get_settings
from .shared.token_counter import TokenCounter

# AST/tree-sitter support for code chunking (optional, graceful fallback)
try:
    from code_splitter import ASTSnowballSplitter

    AST_SPLITTER_AVAILABLE = True
except ImportError:
    AST_SPLITTER_AVAILABLE = False
    ASTSnowballSplitter = None

# Initialize logger
logger = logging.getLogger("mcp-example-core")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Suppress OpenTelemetry tracing export errors (non-critical)
logging.getLogger("opentelemetry.exporter.otlp.proto.http.trace_exporter").setLevel(
    logging.CRITICAL
)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

# OpenTelemetry: Required for observability (LLM debugging)
try:
    from app.mcp.opentelemetry_config import get_opentelemetry_tracer
except ImportError as e:
    get_opentelemetry_tracer = None
    logger.warning(f"OpenTelemetry config not available: {e}")


# Set Java environment variables BEFORE importing GAM (GAM imports pyserini which needs Java)
# This ensures Java is available even if env vars aren't set in MCP config
def _setup_java_environment():
    """Setup Java environment variables for GAM BM25 retriever."""
    java_home = os.environ.get("JAVA_HOME")
    jvm_path = os.environ.get("JVM_PATH")

    # Auto-detect Java 21 if not set
    if not java_home:
        java_21_path = Path("/usr/lib/jvm/java-21-openjdk-amd64")
        if java_21_path.exists():
            java_home = str(java_21_path)
            os.environ["JAVA_HOME"] = java_home
            logger.info(f"Auto-detected JAVA_HOME: {java_home}")

    # Set JVM_PATH if not set but JAVA_HOME is available
    if java_home and not jvm_path:
        jvm_paths = [
            Path(java_home) / "lib" / "server" / "libjvm.so",
            Path(java_home) / "lib" / "amd64" / "server" / "libjvm.so",
            Path(java_home) / "jre" / "lib" / "amd64" / "server" / "libjvm.so",
        ]
        for path in jvm_paths:
            if path.exists():
                jvm_path = str(path)
                os.environ["JVM_PATH"] = jvm_path
                logger.info(f"Auto-detected JVM_PATH: {jvm_path}")
                break

    # Update PATH to include Java bin directory if JAVA_HOME is set
    if java_home:
        java_bin = str(Path(java_home) / "bin")
        current_path = os.environ.get("PATH", "")
        if java_bin not in current_path:
            os.environ["PATH"] = f"{java_bin}:{current_path}"

    # Verify Java setup before importing GAM (GAM imports pyserini which needs Java)
    if not java_home or not jvm_path:
        logger.warning(
            "Java environment variables not fully set. GAM BM25 retriever requires Java. "
            "Dense vector search will work without Java, but BM25 keyword search will fail. "
            f"JAVA_HOME: {java_home}, JVM_PATH: {jvm_path}"
        )
    else:
        # Verify libjvm.so exists
        if not Path(jvm_path).exists():
            logger.error(f"JVM_PATH points to non-existent file: {jvm_path}")
            logger.warning("GAM BM25 retriever will fail. Dense vector search will still work.")
        else:
            logger.info(f"Java environment configured: JAVA_HOME={java_home}, JVM_PATH={jvm_path}")


# Setup Java environment at module level (runs before GAM imports)
_setup_java_environment()


def _estimate_tokens(text: str) -> int:
    """Estimate tokens using accurate tiktoken counting (Claude feature integration).

    Uses tiktoken for 85-90% accuracy (vs 60-70% for character-based).
    Falls back to character-based if tiktoken not available.

    Args:
        text: Text to estimate tokens for

    Returns:
        Estimated token count
    """
    try:
        counter = TokenCounter()
        return counter.count_tokens(text)
    except Exception:
        # Fallback to character-based estimation
        return max(1, len(text) // 4)


def _check_docker_service(service_name: str, port: int) -> bool:
    """Check if Docker service is available (KISS v3).

    Args:
        service_name: Docker service name
        port: Service port

    Returns:
        True if service is accessible
    """
    try:
        import socket

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(("localhost", port))
        sock.close()
        return result == 0
    except Exception:
        return False


class ExampleCore(BaseCore):
    """Example Core GAM DeepAgents business logic.
    """

    def __init__(self, settings: Settings | None = None):
        """Initialize core with settings.

        Args:
            settings: Optional settings (defaults to get_settings())
        """
        self.settings = settings or get_settings()
        self.tracer = (
            get_opentelemetry_tracer("mcp-example-core") if get_opentelemetry_tracer else None
        )

        # Retry configuration
        self.max_retries = 3
        self.retry_delay = 1.0  # seconds

        # Lazy initialization state
        self._initialized = False
        self._generator = None
        self._memory_store = None
        self._page_store = None
        self._memory_agent = None
        self._retrievers = None
        self._research_agent = None
        self._checkpointer = None
        self._store = None
        self._agent = None
        self._gam_memorize_tool = None
        self._gam_research_tool = None
        self._ast_splitter = None  # Lazy initialization for code chunking

        # Docker service availability (v3)
        self._docker_services = {
            "mlflow": _check_docker_service("mlflow", 5000),
            "mindsdb": _check_docker_service("mindsdb", 47334),
            "redis": _check_docker_service("redis", 6379),
            "postgres": _check_docker_service("postgres", 5432),
        }
        if any(self._docker_services.values()):
            logger.info(
                f"Docker services available: {[k for k, v in self._docker_services.items() if v]}"
            )

    async def initialize(self) -> None:
        """Lazy initialization of GAM components with enhanced error handling.

        This allows the core to be instantiated quickly,
        then initialize heavy components on first use.
        """
        if self._initialized:
            return

        logger.info("Initializing GAM components (v3)...")

        # Lazy import GAM (prevents pytest hanging)
        try:
            from gam import (
                BM25Retriever,
                BM25RetrieverConfig,
                DenseRetriever,
                DenseRetrieverConfig,
                IndexRetriever,
                IndexRetrieverConfig,
                InMemoryMemoryStore,
                InMemoryPageStore,
                MemoryAgent,
                OpenAIGenerator,
                OpenAIGeneratorConfig,
                ResearchAgent,
            )
        except ImportError as e:
            if self.settings.require_validation:
                raise ImportError(
                    f"GAM (general-agentic-memory) is required: {e}. "
                    f"Install with: uv add general-agentic-memory"
                ) from e
            raise

        # Import DeepAgents and LangGraph components
        try:
            from deepagents import create_deep_agent
            from langchain_core.tools import tool
            from langgraph.checkpoint.memory import MemorySaver
            from langgraph.store.memory import InMemoryStore
        except ImportError as e:
            if self.settings.require_validation:
                raise ImportError(f"DeepAgents is required: {e}. Install with: uv sync") from e
            raise

        # Initialize GAM components with retry logic
        await self._initialize_generator_with_retry()
        await self._initialize_stores()
        await self._initialize_agents()
        await self._initialize_retrievers_with_retry()
        await self._initialize_deepagent()

        self._initialized = True
        logger.info("✓ GAM components initialized successfully (v3)")

    async def _initialize_generator_with_retry(self) -> None:
        """Initialize generator with retry logic."""
        # Import here to avoid circular imports
        try:
            from gam import OpenAIGenerator, OpenAIGeneratorConfig
        except ImportError as e:
            if self.settings.require_validation:
                raise ImportError(
                    f"GAM (general-agentic-memory) is required: {e}. "
                    f"Install with: uv add general-agentic-memory"
                ) from e
            raise

        last_exception = None

        for attempt in range(self.max_retries):
            with (
                self.tracer.start_as_current_span("gam.generator.init")
                if self.tracer
                else nullcontext()
            ) as span:
                try:
                    if self.settings.use_ollama:
                        gen_config = OpenAIGeneratorConfig(
                            model_name=self.settings.ollama_model,
                            api_key=self.settings.ollama_api_key,
                            base_url=self.settings.ollama_base_url,
                            temperature=self.settings.generator_temperature,
                            max_tokens=self.settings.generator_max_tokens,
                        )
                        if span:
                            span.set_attribute("generator.type", "ollama")
                            span.set_attribute("generator.model", self.settings.ollama_model)
                    else:
                        if not self.settings.openai_api_key:
                            raise ValueError(
                                "OpenAI API key required when Ollama is disabled. "
                                "Set GAM_DEEPAGENTS_OPENAI_API_KEY or enable Ollama"
                            )
                        gen_config = OpenAIGeneratorConfig(
                            model_name=self.settings.openai_model,
                            api_key=self.settings.openai_api_key,
                            base_url=self.settings.openai_base_url,
                            temperature=self.settings.generator_temperature,
                            max_tokens=self.settings.generator_max_tokens,
                        )
                        if span:
                            span.set_attribute("generator.type", "openai")
                            span.set_attribute("generator.model", self.settings.openai_model)

                    self._generator = OpenAIGenerator.from_config(gen_config)
                    if span:
                        span.set_attribute("generator.status", "success")
                        span.set_attribute("generator.attempt", attempt + 1)
                    logger.info("✓ GAM generator initialized successfully")
                    return

                except Exception as e:
                    last_exception = e
                    if span:
                        span.set_attribute("generator.status", "error")
                        span.set_attribute("generator.error", str(e))
                        span.set_attribute("generator.attempt", attempt + 1)

                    if attempt < self.max_retries - 1:
                        wait_time = self.retry_delay * (2**attempt)
                        logger.warning(
                            f"Generator initialization failed (attempt {attempt + 1}/{self.max_retries}): {e}. "
                            f"Retrying in {wait_time}s..."
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(
                            f"Generator initialization failed after {self.max_retries} attempts: {e}"
                        )
                        raise

        raise RuntimeError(
            f"Generator initialization failed after {self.max_retries} attempts: {last_exception}"
        ) from last_exception

    async def _initialize_stores(self) -> None:
        """Initialize memory and page stores."""
        # Import here to avoid circular imports
        try:
            from gam import InMemoryMemoryStore, InMemoryPageStore
        except ImportError as e:
            if self.settings.require_validation:
                raise ImportError(
                    f"GAM (general-agentic-memory) is required: {e}. "
                    f"Install with: uv add general-agentic-memory"
                ) from e
            raise

        self._memory_store = InMemoryMemoryStore()
        self._page_store = InMemoryPageStore()
        logger.info("✓ Memory stores initialized")

    async def _initialize_agents(self) -> None:
        """Initialize GAM agents."""
        # Import here to avoid circular imports
        try:
            from gam import MemoryAgent
        except ImportError as e:
            if self.settings.require_validation:
                raise ImportError(
                    f"GAM (general-agentic-memory) is required: {e}. "
                    f"Install with: uv add general-agentic-memory"
                ) from e
            raise

        self._memory_agent = MemoryAgent(
            generator=self._generator,
            memory_store=self._memory_store,
            page_store=self._page_store,
        )
        logger.info("✓ Memory agent initialized")

        # Add a simple initialization page to prevent empty page store issues
        # This ensures retrievers can build successfully even when no content has been memorized yet
        try:
            init_page_content = "GAM initialization page. This page ensures the page store is never empty during retriever initialization."
            await self._memory_agent.memorize(init_page_content)
            logger.info("✓ Initialization page added to page store")
        except Exception as e:
            logger.warning(f"Failed to add initialization page (non-critical): {e}")

    async def _initialize_retrievers_with_retry(self) -> None:
        """Initialize retrievers with retry logic and parallel building (KISS v3)."""
        # Import here to avoid circular imports
        try:
            from gam import (
                BM25Retriever,
                BM25RetrieverConfig,
                DenseRetriever,
                DenseRetrieverConfig,
                IndexRetriever,
                IndexRetrieverConfig,
                ResearchAgent,
            )
        except ImportError as e:
            if self.settings.require_validation:
                raise ImportError(
                    f"GAM (general-agentic-memory) is required: {e}. "
                    f"Install with: uv add general-agentic-memory"
                ) from e
            raise

        self._retrievers = {}
        index_dir = self.settings.gam_index_dir

        # Build all retrievers in parallel for 2-3x speedup (KISS v3 improvement)
        await asyncio.gather(
            self._build_retriever_with_retry(
                "index",
                lambda: IndexRetriever(
                    IndexRetrieverConfig(index_dir=str(index_dir / "page_index")).__dict__
                ),
                index_dir / "page_index",
            ),
            self._build_retriever_with_retry(
                "bm25",
                lambda: BM25Retriever(
                    BM25RetrieverConfig(
                        index_dir=str(index_dir / "bm25_index"),
                        threads=self.settings.gam_bm25_threads,
                    ).__dict__
                ),
                index_dir / "bm25_index",
            ),
            self._build_retriever_with_retry(
                "dense",
                lambda: DenseRetriever(
                    DenseRetrieverConfig(
                        index_dir=str(index_dir / "dense_index"),
                        model_name=self.settings.gam_dense_model,
                    ).__dict__
                ),
                index_dir / "dense_index",
            ),
        )

        # Initialize research agent
        self._research_agent = ResearchAgent(
            page_store=self._page_store,
            memory_store=self._memory_store,
            retrievers=self._retrievers,
            generator=self._generator,
            max_iters=self.settings.gam_research_max_iters,
        )
        logger.info("✓ Research agent initialized")

    async def _build_retriever_with_retry(
        self, retriever_type: str, retriever_factory, index_dir: Path
    ) -> None:
        """Build retriever with retry logic."""
        last_exception = None

        for attempt in range(self.max_retries):
            with (
                self.tracer.start_as_current_span(f"gam.retriever.{retriever_type}.build")
                if self.tracer
                else nullcontext()
            ) as span:
                try:
                    # Clean index directory
                    if index_dir.exists():
                        shutil.rmtree(index_dir)

                    retriever = retriever_factory()
                    retriever.build(self._page_store)

                    self._retrievers[retriever_type] = retriever
                    if span:
                        span.set_attribute("retriever.status", "success")
                        span.set_attribute("retriever.attempt", attempt + 1)
                    logger.info(f"✓ {retriever_type} retriever built")
                    return

                except Exception as e:
                    last_exception = e
                    if span:
                        span.set_attribute("retriever.status", "error")
                        span.set_attribute("retriever.error", str(e))
                        span.set_attribute("retriever.attempt", attempt + 1)

                    if attempt < self.max_retries - 1:
                        wait_time = self.retry_delay * (2**attempt)
                        logger.warning(
                            f"{retriever_type} retriever build failed (attempt {attempt + 1}/{self.max_retries}): {e}. "
                            f"Retrying in {wait_time}s..."
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(
                            f"{retriever_type} retriever build failed after {self.max_retries} attempts: {e}"
                        )
                        if self.settings.require_validation:
                            raise

        if self.settings.require_validation:
            raise RuntimeError(
                f"{retriever_type} retriever build failed after {self.max_retries} attempts: {last_exception}"
            ) from last_exception

    async def _initialize_deepagent(self) -> None:
        """Initialize DeepAgent with GAM tools."""
        from langchain_core.tools import tool
        from langgraph.checkpoint.memory import MemorySaver
        from langgraph.store.memory import InMemoryStore

        self._checkpointer = MemorySaver()
        self._store = InMemoryStore()

        # Create GAM tools (token-efficient: concise descriptions)
        @tool
        async def gam_memorize_tool(content: str) -> str:
            """Save information to GAM memory."""
            result = await self.memorize(content)
            return result["message"]

        @tool
        async def gam_research_tool(query: str) -> str:
            """Research from GAM memory."""
            result = await self.research(query)
            return result["memory"]

        self._gam_memorize_tool = gam_memorize_tool
        self._gam_research_tool = gam_research_tool
        logger.info("✓ GAM tools created")

    def _null_context(self):
        """Return a null context manager for when tracer is not available."""
        return nullcontext()

    def _is_code_content(self, content: str) -> bool:
        """Detect if content is code using simple heuristics (KISS).

        Args:
            content: Content to check

        Returns:
            True if content appears to be code
        """
        if not content or len(content.strip()) < 10:
            return False

        # Check first 500 chars for code indicators
        preview = content[:500].strip()
        code_indicators = [
            "def ",
            "class ",
            "import ",
            "from ",
            "async def ",
            "function ",
            "const ",
            "let ",
            "var ",
            "public ",
            "private ",
            "interface ",
        ]
        return any(indicator in preview for indicator in code_indicators)

    def _detect_language(self, content: str) -> str:
        """Detect programming language from content (simple heuristics).

        Args:
            content: Content to analyze

        Returns:
            Detected language or "text"
        """
        preview = content[:500].lower()
        if (
            "def " in preview
            or "import " in preview
            or "class " in preview
            or "async def " in preview
        ):
            return "python"
        elif (
            "function " in preview or "const " in preview or "let " in preview or "var " in preview
        ):
            return "javascript"
        elif "public " in preview or "private " in preview or "interface " in preview:
            return "java"
        return "text"

    def _chunk_code_semantically(self, code: str, language: str = "python") -> list[str]:
        """Chunk code at semantic boundaries (functions, classes) for better retrieval.

        Args:
            code: Code content to chunk
            language: Programming language

        Returns:
            List of code chunks at semantic boundaries
        """
        chunks = []

        # Python: Use AST splitter if available
        if language == "python" and AST_SPLITTER_AVAILABLE and ASTSnowballSplitter:
            try:
                if self._ast_splitter is None:
                    self._ast_splitter = ASTSnowballSplitter(language="python")
                code_normalized = code.rstrip("\n") + "\n"
                ast_chunks = self._ast_splitter.split(code_normalized)

                for chunk in ast_chunks:
                    chunk_text = getattr(chunk, "content", str(chunk)).strip()
                    if chunk_text:
                        chunks.append(chunk_text)
                return chunks if chunks else [code]
            except Exception as e:
                logger.debug(f"AST chunking failed: {e}, using simple chunking")

        # Fallback: Simple pattern-based chunking (KISS)
        # Split at function/class boundaries
        if language == "python":
            # Split by def/class with lookbehind to keep the keyword
            pattern = r"(?=^(?:def |class |async def |@))"
            parts = re.split(pattern, code, flags=re.MULTILINE)
            chunks = [p.strip() for p in parts if p.strip()]
        elif language == "javascript":
            # Split by function/class/const/let
            pattern = r"(?=^(?:function |class |const |let |export |import ))"
            parts = re.split(pattern, code, flags=re.MULTILINE)
            chunks = [p.strip() for p in parts if p.strip()]
        else:
            # Generic: Split by blank lines (simple but effective)
            chunks = [c.strip() for c in code.split("\n\n") if c.strip()]

        return chunks if chunks else [code]

    async def memorize(self, content: str) -> dict[str, Any]:
        """Memorize content using GAM MemoryAgent with retry logic.

        Args:
            content: Content to memorize

        Returns:
            dict with success status and details
        """
        await self.initialize()

        start_time = time.perf_counter()
        last_exception = None

        for attempt in range(self.max_retries):
            with (
                self.tracer.start_as_current_span("gam.memorize") if self.tracer else nullcontext()
            ) as span:
                if span:
                    span.set_attribute("content.length", len(content))
                    span.set_attribute("attempt", attempt + 1)

                try:
                    # If content is code, chunk semantically for better retrieval
                    if self._is_code_content(content):
                        language = self._detect_language(content)
                        code_chunks = self._chunk_code_semantically(content, language)

                        if span:
                            span.set_attribute("content.type", "code")
                            span.set_attribute("content.language", language)
                            span.set_attribute("content.chunks", len(code_chunks))

                        # Memorize each chunk separately for better retrieval
                        for idx, chunk in enumerate(code_chunks):
                            await self._memory_agent.memorize(chunk)
                            logger.debug(
                                f"Memorized code chunk {idx + 1}/{len(code_chunks)} ({language})"
                            )

                        chunks_memorized = len(code_chunks)
                    else:
                        # Regular text content
                        await self._memory_agent.memorize(content)
                        chunks_memorized = 1

                        if span:
                            span.set_attribute("content.type", "text")

                    latency_ms = (time.perf_counter() - start_time) * 1000
                    if span:
                        span.set_attribute("status", "success")
                        span.set_attribute("latency_ms", latency_ms)
                        span.set_attribute("chunks_memorized", chunks_memorized)
                    logger.info(f"Memorized {len(content)} characters ({chunks_memorized} chunks)")

                    return {
                        "success": True,
                        "content_length": len(content),
                        "message": f"Memorized {len(content)} characters",
                        "latency_ms": latency_ms,
                    }
                except Exception as e:
                    last_exception = e
                    latency_ms = (time.perf_counter() - start_time) * 1000
                    if span:
                        span.set_attribute("status", "error")
                        span.set_attribute("error", str(e))
                        span.set_attribute("latency_ms", latency_ms)

                    if attempt < self.max_retries - 1:
                        wait_time = self.retry_delay * (2**attempt)
                        logger.warning(
                            f"Memorize failed (attempt {attempt + 1}/{self.max_retries}): {e}. "
                            f"Retrying in {wait_time}s..."
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"Memorize failed after {self.max_retries} attempts: {e}")
                        raise

        raise RuntimeError(
            f"Memorize failed after {self.max_retries} attempts: {last_exception}"
        ) from last_exception

    async def research(self, query: str) -> dict[str, Any]:
        """Research from memory using GAM ResearchAgent with retry logic.

        Args:
            query: Research query

        Returns:
            dict with research results
        """
        await self.initialize()

        start_time = time.perf_counter()
        last_exception = None

        for attempt in range(self.max_retries):
            with (
                self.tracer.start_as_current_span("gam.research") if self.tracer else nullcontext()
            ) as span:
                if span:
                    span.set_attribute("query", query)
                    span.set_attribute("attempt", attempt + 1)

                try:
                    result = await self._research_agent.research(request=query)
                    iterations = len(result.raw_memory.get("iterations", []))

                    latency_ms = (time.perf_counter() - start_time) * 1000
                    if span:
                        span.set_attribute("status", "success")
                        span.set_attribute("research.iterations", iterations)
                        span.set_attribute("research.memory_length", len(result.integrated_memory))
                        span.set_attribute("latency_ms", latency_ms)
                    logger.info(
                        f"Research completed: {iterations} iterations, "
                        f"{len(result.integrated_memory)} chars"
                    )

                    return {
                        "success": True,
                        "memory": result.integrated_memory,
                        "iterations": iterations,
                        "latency_ms": latency_ms,
                    }
                except Exception as e:
                    last_exception = e
                    latency_ms = (time.perf_counter() - start_time) * 1000
                    if span:
                        span.set_attribute("status", "error")
                        span.set_attribute("error", str(e))
                        span.set_attribute("latency_ms", latency_ms)

                    if attempt < self.max_retries - 1:
                        wait_time = self.retry_delay * (2**attempt)
                        logger.warning(
                            f"Research failed (attempt {attempt + 1}/{self.max_retries}): {e}. "
                            f"Retrying in {wait_time}s..."
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"Research failed after {self.max_retries} attempts: {e}")
                        raise

        raise RuntimeError(
            f"Research failed after {self.max_retries} attempts: {last_exception}"
        ) from last_exception

    async def create_agent(
        self,
        agent_name: str,
        description: str,
        system_prompt: str | None = None,
    ) -> dict[str, Any]:
        """Create DeepAgent with GAM memory capabilities.

        Args:
            agent_name: Name for the agent
            description: What the agent should do
            system_prompt: Optional custom system prompt

        Returns:
            dict with agent creation status
        """
        await self.initialize()

        start_time = time.perf_counter()

        with (
            self.tracer.start_as_current_span("create_agent") if self.tracer else nullcontext()
        ) as span:
            if span:
                span.set_attribute("agent.name", agent_name)
                span.set_attribute("agent.description", description)

            try:
                from deepagents import create_deep_agent

                # Use default prompt or custom (token-efficient: concise)
                if system_prompt is None:
                    system_prompt = f"""You are {agent_name}: {description}

You have GAM memory tools:
- gam_memorize: Save information to memory
- gam_research: Retrieve memories before tasks

Workflow: Research → Memorize → Respond
"""

                # Configure Ollama model if enabled
                llm_model = None
                if self.settings.use_ollama:
                    try:
                        from langchain_ollama import ChatOllama

                        # Use llama3.2:latest for tool calling support (codellama-34b doesn't support it)
                        # DeepAgents requires tool calling support
                        ollama_model = (
                            "llama3.2:latest"  # Tool calling support required for DeepAgents
                        )
                        base_url = self.settings.ollama_base_url.replace("/v1", "")
                        llm_model = ChatOllama(
                            model=ollama_model,
                            base_url=base_url,
                            temperature=0.7,
                        )
                        logger.info(
                            f"Using Ollama model: {ollama_model} at {base_url} (FREE - no API costs)"
                        )
                    except ImportError as e:
                        logger.warning(
                            f"langchain-ollama not available: {e}. "
                            "Install with: uv add langchain-ollama. Using DeepAgents default (may require API key)."
                        )
                        llm_model = None
                    except Exception as e:
                        logger.warning(
                            f"Failed to initialize Ollama: {e}. Using DeepAgents default (may require API key)."
                        )
                        llm_model = None

                # Create agent with Ollama model if available
                agent_kwargs = {
                    "tools": [self._gam_memorize_tool, self._gam_research_tool],
                    "system_prompt": system_prompt,
                    "checkpointer": self._checkpointer,
                    "store": self._store,
                }
                if llm_model:
                    agent_kwargs["model"] = llm_model

                self._agent = create_deep_agent(**agent_kwargs)

                latency_ms = (time.perf_counter() - start_time) * 1000
                if span:
                    span.set_attribute("status", "success")
                    span.set_attribute("latency_ms", latency_ms)
                logger.info(f"Created agent: {agent_name}")

                return {
                    "success": True,
                    "agent_name": agent_name,
                    "description": description,
                    "status": "created",
                    "latency_ms": latency_ms,
                }
            except Exception as e:
                latency_ms = (time.perf_counter() - start_time) * 1000
                if span:
                    span.set_attribute("status", "error")
                    span.set_attribute("error", str(e))
                    span.set_attribute("latency_ms", latency_ms)
                logger.error(f"Create agent failed: {e}")
                raise

    async def run_agent(
        self,
        task: str,
        agent_name: str | None = None,
    ) -> dict[str, Any]:
        """Run DeepAgent task with GAM memory integration.

        Args:
            task: Task description
            agent_name: Optional agent name

        Returns:
            dict with agent response
        """
        await self.initialize()

        start_time = time.perf_counter()

        with (
            self.tracer.start_as_current_span("run_agent") if self.tracer else nullcontext()
        ) as span:
            if span:
                span.set_attribute("task", task)
                if agent_name:
                    span.set_attribute("agent.name", agent_name)

            try:
                agent = self.get_agent()
                config = {"configurable": {"thread_id": self.settings.agent_thread_id}}

                result = await agent.ainvoke(
                    {"messages": [{"role": "user", "content": task}]},
                    config=config,
                )

                # Extract final message (token-efficient: only extract what's needed)
                messages = result.get("messages", [])
                final_message = messages[-1] if messages else None

                if hasattr(final_message, "content"):
                    content = final_message.content
                elif isinstance(final_message, dict):
                    content = final_message.get("content", "")
                else:
                    content = str(final_message) if final_message else ""

                latency_ms = (time.perf_counter() - start_time) * 1000
                if span:
                    span.set_attribute("status", "success")
                    span.set_attribute("run_agent.message_count", len(messages))
                    span.set_attribute("run_agent.response_length", len(content))
                    span.set_attribute("latency_ms", latency_ms)
                logger.info(f"Agent task completed: {len(messages)} messages, {len(content)} chars")

                return {
                    "success": True,
                    "response": content,
                    "message_count": len(messages),
                    "latency_ms": latency_ms,
                }
            except Exception as e:
                latency_ms = (time.perf_counter() - start_time) * 1000
                if span:
                    span.set_attribute("status", "error")
                    span.set_attribute("error", str(e))
                    span.set_attribute("latency_ms", latency_ms)
                logger.error(f"Run agent failed: {e}")
                raise

    async def run_agent_stream(
        self,
        task: str,
        agent_name: str | None = None,
        callback: Callable[[str], Any] | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        """Run DeepAgent task with streaming support for real-time code generation.

        Args:
            task: Task description
            agent_name: Optional agent name
            callback: Optional callback function for progress tracking

        Yields:
            dict with streaming chunks:
                - chunk: str - Current chunk of response
                - accumulated: str - Accumulated response so far
                - done: bool - Whether generation is complete
                - tokens_so_far: int - Total tokens generated (approximate)
                - elapsed_ms: float - Elapsed time in milliseconds
        """
        await self.initialize()

        start_time = time.perf_counter()
        tokens_so_far = 0
        accumulated_content = ""
        first_token_time = None

        with (
            self.tracer.start_as_current_span("run_agent_stream") if self.tracer else nullcontext()
        ) as span:
            if span:
                span.set_attribute("task", task)
                if agent_name:
                    span.set_attribute("agent.name", agent_name)

            try:
                agent = self.get_agent()
                config = {"configurable": {"thread_id": self.settings.agent_thread_id}}

                # Stream agent response
                async for chunk in agent.astream(
                    {"messages": [{"role": "user", "content": task}]},
                    config=config,
                    stream_mode=["messages"],  # Stream messages
                ):
                    # Extract content from chunk
                    # Chunk format depends on DeepAgents implementation
                    content = ""
                    if isinstance(chunk, dict):
                        # Handle dict chunks
                        messages = chunk.get("messages", [])
                        if messages:
                            last_msg = messages[-1]
                            if hasattr(last_msg, "content"):
                                content = last_msg.content
                            elif isinstance(last_msg, dict):
                                content = last_msg.get("content", "")
                    elif hasattr(chunk, "content"):
                        content = chunk.content
                    elif isinstance(chunk, str):
                        content = chunk

                    # Early return on empty content (KISS v3 improvement)
                    if content and content.strip():
                        accumulated_content += content
                        # Better token approximation: ~4 chars per token (KISS v3 improvement)
                        tokens_so_far += _estimate_tokens(content)

                        elapsed_ms = (time.perf_counter() - start_time) * 1000

                        # Track first token latency
                        if first_token_time is None:
                            first_token_time = elapsed_ms
                            if span:
                                span.set_attribute("first_token_latency_ms", first_token_time)

                        # Call callback if provided
                        if callback:
                            try:
                                if asyncio.iscoroutinefunction(callback):
                                    await callback(content)
                                else:
                                    callback(content)
                            except Exception as e:
                                logger.debug(f"Callback error: {e}")

                        yield {
                            "chunk": content,
                            "accumulated": accumulated_content,
                            "tokens_so_far": tokens_so_far,
                            "elapsed_ms": elapsed_ms,
                            "first_token_latency_ms": first_token_time,
                            "tokens_per_second": tokens_so_far / (elapsed_ms / 1000)
                            if elapsed_ms > 0
                            else 0,
                            "done": False,
                        }

                # Final yield
                elapsed_ms = (time.perf_counter() - start_time) * 1000
                if span:
                    span.set_attribute("status", "success")
                    span.set_attribute("run_agent_stream.response_length", len(accumulated_content))
                    span.set_attribute("run_agent_stream.tokens_so_far", tokens_so_far)
                    span.set_attribute("run_agent_stream.latency_ms", elapsed_ms)
                    if first_token_time:
                        span.set_attribute("first_token_latency_ms", first_token_time)

                # Log completion (info level for milestones, reduced logging overhead - KISS v3)
                logger.info(
                    f"Agent streaming completed: {tokens_so_far} tokens, "
                    f"{len(accumulated_content)} chars, {elapsed_ms:.1f}ms"
                )

                yield {
                    "chunk": "",
                    "accumulated": accumulated_content,
                    "tokens_so_far": tokens_so_far,
                    "elapsed_ms": elapsed_ms,
                    "first_token_latency_ms": first_token_time,
                    "tokens_per_second": tokens_so_far / (elapsed_ms / 1000)
                    if elapsed_ms > 0
                    else 0,
                    "done": True,
                }

            except Exception as e:
                elapsed_ms = (time.perf_counter() - start_time) * 1000
                if span:
                    span.set_attribute("status", "error")
                    span.set_attribute("error", str(e))
                    span.set_attribute("latency_ms", elapsed_ms)
                logger.error(f"Run agent stream failed: {e}")

                yield {
                    "chunk": "",
                    "accumulated": accumulated_content,
                    "tokens_so_far": tokens_so_far,
                    "elapsed_ms": elapsed_ms,
                    "done": True,
                    "error": str(e),
                }

    async def generate_code_stream(
        self,
        task: str,
        language: str = "python",
        agent_name: str | None = None,
        callback: Callable[[str], Any] | None = None,
        use_structured_output: bool = False,
    ) -> AsyncIterator[dict[str, Any]]:
        """Generate code with streaming support optimized for code generation (v3 enhanced).

        Enhanced with Claude features:
        - Structured outputs (JSON/Pydantic) for better code quality
        - Token-efficient result handling
        - Better package utilization

        Args:
            task: Code generation task description
            language: Programming language (default: python)
            agent_name: Optional agent name
            callback: Optional callback function for progress tracking
            use_structured_output: Use structured output format (default: False)

        Yields:
            dict with code chunks:
                - code_chunk: str - Current code chunk
                - accumulated_code: str - Accumulated code so far
                - language: str - Programming language
                - done: bool - Whether generation is complete
                - tokens_so_far: int - Total tokens generated
                - elapsed_ms: float - Elapsed time in milliseconds
        """
        # Enhanced prompt for code generation (v3 + Claude features)
        docker_services_info = ""
        if any(self._docker_services.values()):
            available_services = [k for k, v in self._docker_services.items() if v]
            docker_services_info = f"\n\nAvailable Docker Services: {', '.join(available_services)}"

        structured_instruction = ""
        if use_structured_output:
            structured_instruction = """
IMPORTANT: Generate code as valid JSON with this structure:
{
  "code": "<generated code>",
  "dependencies": ["<package1>", "<package2>"],
  "description": "<brief description>",
  "usage": "<usage example>"
}
"""

        code_prompt = f"""Generate {language} code for the following task:

{task}

Requirements:
- Use proper {language} syntax
- Include type hints if applicable (for Python)
- Add docstrings
- Follow best practices
- Generate complete, runnable code
- Use packages from pyproject.toml when available (tiktoken, diskcache, instructor, pydantic-ai, etc.)
{docker_services_info}{structured_instruction}

Generate the code:"""

        # Stream with code-aware processing
        async for chunk in self.run_agent_stream(code_prompt, agent_name, callback):
            code_chunk = chunk.get("chunk", "")
            accumulated_code = chunk.get("accumulated", "")

            yield {
                **chunk,
                "code_chunk": code_chunk,
                "accumulated_code": accumulated_code,
                "language": language,
            }

    def get_agent(self):
        """Get or create the DeepAgent instance with GAM tools.

        Returns:
            DeepAgent instance
        """
        if self._agent is None:
            from deepagents import create_deep_agent

            # Enhanced system prompt with Claude features integration
            docker_services_list = ""
            if any(self._docker_services.values()):
                available_services = [k for k, v in self._docker_services.items() if v]
                docker_services_list = (
                    f"\n\nDocker services available: {', '.join(available_services)}"
                )

            system_prompt = f"""You are an expert assistant with GAM memory and advanced code generation capabilities.

Tools:
- gam_memorize: Save information to GAM memory
- gam_research: Retrieve memories from GAM

Workflow: Research → Memorize → Generate → Improve

Advanced Features (Claude integration):
- Batch Processing: Generate multiple features in parallel (5-20x faster)
- Token Efficiency: Summarize and cache tool results (30-50% token reduction)
- Structured Outputs: Generate type-safe code with Pydantic validation
- Programmatic Tools: Write code that calls tools directly (reduced latency)

Package Utilization:
- Use tiktoken for accurate token counting
- Use diskcache for persistent caching
- Use instructor for structured outputs
- Use pydantic-ai for AI-powered code generation
- Use msgpack for faster serialization
- Use aiofiles for async file I/O
- Use aiosqlite for async database operations{docker_services_list}

For code generation:
- Always research from memory first
- Use parallel execution for multiple features
- Generate structured outputs when possible
- Utilize packages from pyproject.toml
- Use Docker services when available"""

            # Configure Ollama model if enabled
            llm_model = None
            if self.settings.use_ollama:
                try:
                    from langchain_ollama import ChatOllama

                    # Use a model that supports tool calling (required for DeepAgents)
                    # llama3.2, llama3.1, or qwen2.5 are recommended
                    # codellama-34b-optimized does NOT support tool calling
                    ollama_model = os.environ.get("OLLAMA_MODEL", "llama3.2:latest")
                    # ChatOllama expects base_url without /v1
                    ollama_base_url = self.settings.ollama_base_url.replace("/v1", "")
                    llm_model = ChatOllama(
                        model=ollama_model,
                        base_url=ollama_base_url,
                        temperature=0.7,
                    )
                    logger.info(
                        f"Using Ollama model for DeepAgent: {ollama_model} (FREE - no API costs)"
                    )
                except ImportError:
                    logger.warning(
                        "langchain-ollama not available. Install with: uv sync langchain-ollama. "
                        "Falling back to DeepAgents default (may require Anthropic API)."
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to initialize Ollama model: {e}. Using DeepAgents default."
                    )
                    logger.exception("Ollama initialization error details:")
                    llm_model = None

            # Create agent with Ollama model if available
            agent_kwargs = {
                "tools": [self._gam_memorize_tool, self._gam_research_tool],
                "system_prompt": system_prompt,
                "checkpointer": self._checkpointer,
                "store": self._store,
            }
            if llm_model:
                agent_kwargs["model"] = llm_model

            self._agent = create_deep_agent(**agent_kwargs)
        return self._agent

    async def generate_code_batch(
        self,
        tasks: list[str],
        language: str = "python",
        agent_name: str | None = None,
        max_concurrent: int = 5,
    ) -> list[dict[str, Any]]:
        """Generate multiple code features in parallel (Claude batch processing feature).

        Processes multiple code generation tasks in parallel for 5-20x speedup.

        Args:
            tasks: List of code generation task descriptions
            language: Programming language (default: python)
            agent_name: Optional agent name
            max_concurrent: Maximum concurrent operations (default: 5)

        Returns:
            List of code generation results
        """
        await self.initialize()

        try:
            from scripts.gam_deepagents.shared.batch_processor_ollama import (
                BatchProcessorOllama,
            )
        except ImportError:
            # Fallback to sequential if batch processor not available
            logger.warning("BatchProcessorOllama not available, using sequential processing")
            results = []
            for task in tasks:
                accumulated_code = ""
                async for chunk in self.generate_code_stream(task, language, agent_name):
                    accumulated_code = chunk.get("accumulated_code", "")
                    if chunk.get("done"):
                        break
                results.append(
                    {
                        "success": True,
                        "code": accumulated_code,
                        "language": language,
                        "task": task,
                    }
                )
            return results

        processor = BatchProcessorOllama(max_concurrent=max_concurrent)

        async def process_single_task(task: str) -> dict[str, Any]:
            """Process a single code generation task."""
            try:
                accumulated_code = ""
                tokens_so_far = 0
                elapsed_ms = 0.0

                async for chunk in self.generate_code_stream(task, language, agent_name):
                    accumulated_code = chunk.get("accumulated_code", "")
                    tokens_so_far = chunk.get("tokens_so_far", 0)
                    elapsed_ms = chunk.get("elapsed_ms", 0.0)
                    if chunk.get("done"):
                        break

                return {
                    "success": True,
                    "code": accumulated_code,
                    "language": language,
                    "task": task,
                    "tokens_so_far": tokens_so_far,
                    "elapsed_ms": elapsed_ms,
                }
            except Exception as e:
                logger.error(f"Code generation failed for task: {task}, error: {e}")
                return {
                    "success": False,
                    "code": "",
                    "language": language,
                    "task": task,
                    "error": str(e),
                }

        results = await processor.process_batch(tasks, process_single_task)
        return results
