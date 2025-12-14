"""OpenTelemetry configuration for MCP servers."""

import json
import logging
import os
from pathlib import Path
from typing import Any

# Suppress OpenTelemetry export errors (non-critical)
logging.getLogger("opentelemetry.exporter.otlp.proto.http.trace_exporter").setLevel(
    logging.CRITICAL
)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

# Try to import OpenTelemetry, fall back to no-op if not available
try:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import (
        BatchSpanProcessor,
        ConsoleSpanExporter,
        SimpleSpanProcessor,
    )

    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    trace = None
    Resource = None
    TracerProvider = None
    BatchSpanProcessor = None
    ConsoleSpanExporter = None
    SimpleSpanProcessor = None

# Try to import OTLP exporter (optional)
try:
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

    OTLP_AVAILABLE = True
except ImportError:
    OTLP_AVAILABLE = False
    OTLPSpanExporter = None


class NoOpSpan:
    """No-op span for when OpenTelemetry is not available."""

    def set_attribute(self, key: str, value: Any) -> None:
        """No-op set attribute."""
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class NoOpTracer:
    """No-op tracer for when OpenTelemetry is not available."""

    def start_as_current_span(self, name: str, **kwargs):
        """Return a no-op span context manager."""
        return NoOpSpan()


def get_opentelemetry_tracer(name: str):
    """Get an OpenTelemetry tracer for the given name.

    Configures OpenTelemetry with:
    - OTLP exporter if OTEL_EXPORTER_OTLP_ENDPOINT is set
    - Console exporter for local development
    - Resource attributes for service identification

    If OpenTelemetry is not installed, returns a no-op tracer.

    Args:
        name: Tracer name (typically the service/module name)

    Returns:
        Configured OpenTelemetry tracer or no-op tracer

    Example:
        >>> tracer = get_opentelemetry_tracer("my-service")
        >>> with tracer.start_as_current_span("operation") as span:
        ...     span.set_attribute("key", "value")
        ...     # do work
    """
    if not OTEL_AVAILABLE:
        return NoOpTracer()

    # Check if tracer provider is already configured
    if isinstance(trace.get_tracer_provider(), TracerProvider):
        # Already configured, just return a tracer
        return trace.get_tracer(name)

    # Create resource with service name
    resource = Resource.create(
        {
            "service.name": name,
            "service.namespace": "deepagents-mcp",
        }
    )

    # Create tracer provider
    provider = TracerProvider(resource=resource)

    # Add OTLP exporter if endpoint is configured
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if otlp_endpoint and OTLP_AVAILABLE:
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    # Add console exporter for local development (if not in production)
    if os.getenv("OTEL_CONSOLE_EXPORTER", "false").lower() == "true":
        console_exporter = ConsoleSpanExporter()
        provider.add_span_processor(BatchSpanProcessor(console_exporter))

    # Add file exporter for local trace files (JSON format)
    trace_file_path = os.getenv("OTEL_TRACE_FILE")
    if trace_file_path:
        trace_path = Path(trace_file_path)
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        file_exporter = JSONFileSpanExporter(trace_path)
        # Use SimpleSpanProcessor for file export to ensure all spans are written
        provider.add_span_processor(SimpleSpanProcessor(file_exporter))

    # Set the global tracer provider
    trace.set_tracer_provider(provider)

    return trace.get_tracer(name)


class JSONFileSpanExporter:
    """Simple file-based span exporter that writes spans to JSON file.

    Writes spans in a human-readable JSON format for local debugging.
    Each span is written as a JSON object on a new line (JSONL format).
    """

    def __init__(self, file_path: Path):
        """Initialize JSON file span exporter.

        Args:
            file_path: Path to JSON file for writing traces
        """
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._file_handle = None

    def _get_file_handle(self):
        """Get or create file handle lazily."""
        if self._file_handle is None:
            self._file_handle = open(self.file_path, "a", encoding="utf-8")
        return self._file_handle

    def export(self, spans):
        """Export spans to JSON file.

        Args:
            spans: List of spans to export
        """
        file_handle = self._get_file_handle()
        for span in spans:
            span_data = {
                "name": span.name,
                "context": {
                    "trace_id": format(span.context.trace_id, "032x"),
                    "span_id": format(span.context.span_id, "016x"),
                },
                "parent_span_id": (
                    format(span.parent.span_id, "016x") if span.parent else None
                ),
                "start_time": span.start_time,
                "end_time": span.end_time,
                "duration_ns": (
                    span.end_time - span.start_time if span.end_time else None
                ),
                "attributes": dict(span.attributes) if span.attributes else {},
                "events": [
                    {
                        "name": event.name,
                        "timestamp": event.timestamp,
                        "attributes": (
                            dict(event.attributes) if event.attributes else {}
                        ),
                    }
                    for event in span.events
                ],
                "status": {
                    "status_code": (
                        span.status.status_code.name if span.status else None
                    ),
                    "description": span.status.description if span.status else None,
                },
            }
            file_handle.write(json.dumps(span_data, default=str) + "\n")
            file_handle.flush()

    def shutdown(self):
        """Shutdown the exporter and close file."""
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None
