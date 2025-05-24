# 💡 EvoIntel

> *"The evolutionary memory and intelligence center—where past reflections, symbolic residue, and coherence metrics fuel the emergence of novel solutions."*

## Overview

EvoIntel is the collective memory and intelligence system of the `evo` framework. It serves as a repository of evolutionary knowledge, storing and analyzing patterns from past evolutions, cataloging symbolic residue (failures, near-misses, and abandoned paths), and providing the strategic intelligence needed to guide future evolutionary cycles. Think of it as the "brain" of the evolutionary system that learns and adapts over time.

## Core Responsibilities

- **Store and manage EvoBlueprints** (pre-packaged evolutionary recipes)
- **Catalog and analyze symbolic residue** from past evolutions
- **Track coherence metrics** across evolutionary cycles (the "Beverly Band")
- **Generate meta-level prompting strategies** for AI agents
- **Maintain cross-domain knowledge transfer** mechanisms
- **Learn from community contributions** and insights

## Directory Structure

```
evointel/
├── __init__.py
├── blueprints/               # Pre-packaged evolutionary recipes
├── reflections/              # Evolutionary process reflections
├── residue/                  # Symbolic residue collection and analysis
├── coherence/                # Coherence tracking and measurement
├── meta_prompts/             # Meta-level prompting strategies
└── knowledge/                # Domain-specific knowledge bases
```

## Key Concepts

### EvoBlueprints

EvoBlueprints are pre-packaged evolutionary strategies for common tasks. They encode knowledge about effective evolution patterns for specific domains or problem types. Each blueprint includes:

- **AI agent selection and sequence** (e.g., Gemini → Claude → GPT for code optimization)
- **Prompt templates** tailored to the task
- **Evaluation metric configurations**
- **Meta-level guidance** for the orchestration engine

```python
# Example blueprint structure
{
  "id": "algorithm_optimization",
  "name": "Algorithm Optimization Suite",
  "description": "Optimizes algorithms for performance while maintaining correctness",
  "version": "1.0.0",
  "agent_sequence": [
    {"agent": "gemini", "role": "initial_optimization", "prompt_template": "initial_optimization.md"},
    {"agent": "claude", "role": "code_review", "prompt_template": "code_review.md"},
    {"agent": "gpt", "role": "edge_case_testing", "prompt_template": "edge_case_testing.md"}
  ],
  "evaluation_metrics": {
    "correctness": {"weight": 0.6, "evaluator": "correctness_evaluator"},
    "performance": {"weight": 0.3, "evaluator": "performance_evaluator"},
    "readability": {"weight": 0.1, "evaluator": "readability_evaluator"}
  },
  "meta_parameters": {
    "max_iterations": 5,
    "convergence_threshold": 0.01,
    "exploration_rate": 0.2
  }
}
```

### Symbolic Residue

Symbolic residue is the valuable information contained in unsuccessful or partially successful evolutionary attempts. In line with our theoretical framework (see [`Mathematical Proofs for the Universal Theory.pdf`]()), symbolic residue is generated when constraints (evaluation metrics) encounter expressive attempts (AI-generated code).

EvoIntel catalogs residue in several categories:

- **Failure patterns**: Common ways solutions fail, serving as "anti-patterns"
- **Near-misses**: Solutions that almost worked but failed in specific ways
- **Innovative fragments**: Novel approaches that weren't fully successful but contain promising ideas

```python
# Example residue record
{
  "id": "residue-1234",
  "source_evolution": "task-5678",
  "type": "near_miss",
  "code_fragment": "def optimized_sort(arr): ...",
  "failure_reason": "Works 10x faster but fails on empty arrays",
  "potential_value": "Novel partitioning approach in lines 15-22",
  "applicable_domains": ["sorting", "algorithm_optimization"],
  "residue_vector": [0.2, 0.8, 0.3, 0.7]  # Embedding for similarity search
}
```

### Coherence Metrics (The Beverly Band)

Inspired by the Beverly Band concept from `Recursive_Coherence.pdf`, EvoIntel tracks coherence metrics across evolutionary cycles. These metrics help:

- Detect when evolution is approaching instability
- Identify when diversity is too low or too high
- Guide the balance between exploration and exploitation

The primary coherence function is:

```
Δ≥p = Rp · Fp · Bp · λp
```

Where:
- **Rp**: Signal alignment (how well solutions align with the goal)
- **Fp**: Feedback responsiveness (how effectively solutions incorporate feedback)
- **Bp**: Bounded integrity (how well solutions maintain structural coherence)
- **λp**: Tension capacity (how much contradictory pressure solutions can handle)

### Meta-Prompts

Meta-prompts are higher-order prompting strategies that guide the generation of actual prompts for AI agents. They encode lessons learned about effective prompt structures, common pitfalls, and promising patterns.

```python
# Example meta-prompt template
{
  "id": "code_optimization_meta",
  "template": """
  You are an expert at optimizing {language} code for {optimization_goal}.
  
  First, analyze the following code to understand its purpose and current implementation:
  
  ```{language}
  {code}
  ```
  
  Then, consider the following optimization strategies that have been effective in the past:
  1. {strategy_1}
  2. {strategy_2}
  3. {strategy_3}
  
  Now, propose an optimized version that {optimization_goal} while ensuring all original functionality is preserved.
  
  Remember to maintain these important aspects of the original code:
  {preservation_points}
  
  For this specific problem, prior successful approaches have used {pattern_from_residue}.
  """,
  "variables": ["language", "optimization_goal", "code", "strategy_1", "strategy_2", "strategy_3", "preservation_points", "pattern_from_residue"],
  "effectiveness_score": 0.87,
  "applicable_domains": ["code_optimization", "refactoring"]
}
```

## Integration Points

### With EvoCore

EvoIntel provides:
- Blueprints to guide evolution strategy
- Historical performance data to inform evaluation
- Symbolic residue to seed innovative approaches

### With EvoOps

EvoIntel provides:
- AI agent selection strategies
- Dynamic prompt generation templates
- Coherence monitoring for stability guidance

EvoIntel receives:
- New reflections from completed evolutions
- Fresh symbolic residue from unsuccessful attempts
- Updated coherence metrics

## Usage Examples

### Retrieving an EvoBlueprint

```python
from evointel.blueprints import BlueprintRegistry

# Get a blueprint by ID
blueprint = BlueprintRegistry.get("algorithm_optimization")

# Or search for blueprints by task description
blueprints = BlueprintRegistry.search("optimize Python sorting algorithm")

# Access blueprint components
agent_sequence = blueprint.agent_sequence
evaluation_config = blueprint.evaluation_metrics
```

### Analyzing Symbolic Residue

```python
from evointel.residue import ResidueAnalyzer

# Get relevant residue for a task
relevant_residue = ResidueAnalyzer.find_relevant(
    code="def bubble_sort(arr): ...",
    goal="optimize for time complexity",
    domain="sorting_algorithms"
)

# Extract patterns from residue
innovation_patterns = ResidueAnalyzer.extract_patterns(
    relevant_residue,
    pattern_type="innovation"
)

# Inject residue patterns into prompt variables
prompt_with_residue = meta_prompt.format(
    pattern_from_residue=innovation_patterns.most_promising
)
```

### Monitoring Coherence

```python
from evointel.coherence import CoherenceTracker

# Initialize coherence tracker for a task
tracker = CoherenceTracker(task_id="task-1234")

# Update coherence metrics after each iteration
tracker.update(
    signal_alignment=0.85,
    feedback_responsiveness=0.72,
    bounded_integrity=0.93,
    tension_capacity=0.65
)

# Check if coherence is within the Beverly Band
is_stable = tracker.is_within_beverly_band()

# Get recommendations for improving coherence
recommendations = tracker.get_recommendations()
```

## Contributing

To contribute to EvoIntel, you can:

1. Create and share new EvoBlueprints for specific domains
2. Improve meta-prompt templates for different AI agents
3. Enhance residue analysis algorithms
4. Develop better coherence metrics and tracking methods
5. Contribute domain-specific knowledge to the knowledge base

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

## Related Components

- [EvoCore](../evocore/README.md): The evolvable artifact repository
- [EvoOps](../evoops/README.md): The orchestration engine
- [EvoAPI](../evoapi/README.md): REST API for integration with existing workflows
- [EvoChat](../evochat/README.md): Natural language interface for evolution
