# Domain: Autonomous Research

## Overview

Autonomous research workflows. This command provides direct access to the pure domain logic in `app/research/autonomous_research.py` for conducting autonomous research with minimal human intervention.

## Usage

Type `/domain-autonomous-research` followed by the research topic.

## Parameters

- `topic`: Research topic (required)
- `depth`: Research depth (shallow, medium, deep, exhaustive) (default: "medium")
- `max_iterations`: Maximum research iterations (default: 5)
- `use_web_search`: Enable web search (default: true)
- `use_codebase_search`: Enable codebase search (default: true)
- `save_to_gam`: Save findings to GAM (default: true)
- `create_report`: Generate research report (default: true)

## Example Usage

### Deep Research

```
/domain-autonomous-research
Topic: Microservices architecture patterns for high-scale systems
Depth: deep
Max Iterations: 10
Use Web Search: true
```

### Codebase Research

```
/domain-autonomous-research
Topic: Current authentication implementation
Depth: medium
Use Web Search: false
Use Codebase Search: true
```

### Quick Research

```
/domain-autonomous-research
Topic: Python async best practices
Depth: shallow
Max Iterations: 3
```

## Domain Logic

### AutonomousResearcher

Pure domain class for autonomous research.

```python
from app.research.autonomous_research import AutonomousResearcher

# Initialize
researcher = AutonomousResearcher(
    topic="Microservices architecture patterns",
    depth="deep",
    max_iterations=10
)

# Execute research
result = await researcher.research()

# Get findings
findings = researcher.get_findings()

# Generate report
report = researcher.generate_report()
```

## Research Workflow

### Phase 1: Topic Analysis

1. Parse research topic
2. Identify key concepts
3. Generate search queries
4. Determine research scope

### Phase 2: Information Gathering

1. Web search for latest information
2. Codebase search for existing patterns
3. GAM search for stored knowledge
4. Documentation review

### Phase 3: Synthesis

1. Analyze gathered information
2. Identify patterns and themes
3. Extract key insights
4. Validate findings

### Phase 4: Iteration

1. Identify knowledge gaps
2. Generate follow-up queries
3. Repeat gathering and synthesis
4. Stop when depth reached or max iterations

### Phase 5: Reporting

1. Organize findings
2. Create structured report
3. Save to GAM
4. Generate actionable recommendations

## Output Format

```python
{
    "topic": "Microservices architecture patterns for high-scale systems",
    "depth": "deep",
    "iterations_completed": 8,
    "research_summary": {
        "key_findings": [
            "API Gateway pattern essential for routing and authentication",
            "Service mesh (Istio/Linkerd) provides observability and resilience",
            "Event-driven architecture reduces coupling",
            "CQRS pattern improves read/write scalability",
            "Saga pattern handles distributed transactions"
        ],
        "best_practices": [
            "Use circuit breakers for fault tolerance",
            "Implement distributed tracing (OpenTelemetry)",
            "Design for failure with retry and timeout policies",
            "Use asynchronous communication where possible",
            "Implement proper service discovery"
        ],
        "anti_patterns": [
            "Shared database across services",
            "Synchronous inter-service communication for everything",
            "Lack of monitoring and observability",
            "No API versioning strategy"
        ],
        "challenges": [
            "Data consistency across services",
            "Increased operational complexity",
            "Network latency and reliability",
            "Debugging distributed systems"
        ]
    },
    "sources": [
        {
            "type": "web",
            "url": "https://microservices.io/patterns/",
            "title": "Microservices Patterns",
            "relevance": 0.95
        },
        {
            "type": "codebase",
            "file": "docs/architecture.md",
            "relevance": 0.87
        },
        {
            "type": "gam",
            "entity": "microservices-best-practices",
            "relevance": 0.92
        }
    ],
    "recommendations": [
        {
            "priority": "high",
            "recommendation": "Implement API Gateway pattern",
            "rationale": "Centralizes routing, authentication, and rate limiting",
            "implementation": "Use Kong or AWS API Gateway"
        },
        {
            "priority": "high",
            "recommendation": "Deploy service mesh",
            "rationale": "Provides observability, security, and traffic management",
            "implementation": "Use Istio with Kubernetes"
        },
        {
            "priority": "medium",
            "recommendation": "Adopt event-driven architecture",
            "rationale": "Reduces coupling and improves scalability",
            "implementation": "Use Kafka or RabbitMQ for event bus"
        }
    ],
    "report_path": "research/microservices-architecture-2025-12-04.md",
    "gam_entity": "research-microservices-architecture",
    "research_time_ms": 45678
}
```

## Research Depths

### Shallow (1-3 iterations)
- Quick overview
- Basic concepts
- Common patterns
- 5-10 sources

### Medium (3-5 iterations)
- Detailed analysis
- Best practices
- Tradeoffs
- 10-20 sources

### Deep (5-10 iterations)
- Comprehensive research
- Advanced patterns
- Case studies
- 20-50 sources

### Exhaustive (10+ iterations)
- Expert-level knowledge
- Cutting-edge research
- Academic papers
- 50+ sources

## Best Practices

- Start with medium depth
- Use deep for unfamiliar topics
- Enable web search for latest information
- Enable codebase search for existing patterns
- Always save findings to GAM
- Review and validate recommendations

## Integration

- Used by `/autonomous-research` command
- Wrapped by `/deep-research` workflow
- Saves to GAM via `GAMMemoryManager`
- Pure domain logic, no infrastructure

## Related Commands

- `/autonomous-research` - Command wrapper
- `/deep-research` - Deep research workflow
- `/skill-research-and-plan` - Research + planning
- `/research-memory` - Research memory operations

## Source

- **File**: `app/research/autonomous_research.py`
- **Class**: `AutonomousResearcher`
- **Layer**: Domain (Research)
