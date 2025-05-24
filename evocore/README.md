# 🜏 EvoCore

> *"The evolvable artifact repository—a place where code, prompts, and algorithms learn to adapt through evolutionary pressure."*

## Overview

EvoCore is the central component of the `evo` framework that houses the actual evolvable artifacts—code, prompts, algorithms, or any other digital artifact that can benefit from AI-driven evolution. It provides the structure, evaluation mechanisms, and integration points that enable these artifacts to evolve through recursive interactions with AI agents.

## Core Responsibilities

- **House target artifacts** for evolution (code, prompts, algorithms)
- **Define evolutionary boundaries** via EVOLVE-BLOCK markers
- **Evaluate evolved solutions** through flexible, composable evaluation harnesses
- **Manage Git integration** for tracking evolutionary history
- **Ensure compatibility** with different programming languages and domains
- **Validate evolved artifacts** for correctness and safety

## Directory Structure

```
evocore/
├── __init__.py
├── templates/                # Code templates for various languages and domains
├── evaluators/               # Evaluation harnesses and metrics
├── git/                      # Git integration utilities
├── evolve_markers/           # Utilities for EVOLVE-BLOCK API
└── validators/               # Input and output validation
```

## Key Concepts

### EVOLVE-BLOCK API

The EVOLVE-BLOCK API allows users to mark specific sections of code for evolution, similar to AlphaEvolve:

```python
# EVOLVE-BLOCK-START
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
# EVOLVE-BLOCK-END
```

The rest of the code remains untouched during evolution, providing a stable framework around the evolving components.

### Evaluation Harnesses

EvoCore includes a flexible evaluation system that can assess evolved artifacts along multiple dimensions:

- **Performance**: Time complexity, memory usage, latency, throughput
- **Quality**: Readability, maintainability, test coverage
- **Prompt Effectiveness**: Response quality, instruction following, creativity
- **Custom Metrics**: Domain-specific evaluation criteria

Evaluators can be composed and weighted to create complex fitness functions:

```python
from evocore.evaluators import TimeComplexity, MemoryUsage, Readability

evaluator = TimeComplexity(weight=0.6) + MemoryUsage(weight=0.3) + Readability(weight=0.1)
result = evaluator.evaluate(evolved_code)
```

### Git Integration

EvoCore integrates with Git to track evolutionary history and manage collaborative evolution:

- **Branch Management**: Creates branches for evolutionary cycles and AI agent contributions
- **Diff Analysis**: Analyzes diffs for quality and impact
- **PR Generation**: Generates pull requests for evolved code

## Integration Points

### With EvoOps

EvoCore provides hooks for EvoOps to:
- Trigger evaluations
- Apply diffs
- Create and manage branches
- Generate pull requests

### With EvoIntel

EvoCore consumes from EvoIntel:
- EvoBlueprints for domain-specific evolution strategies
- Historical performance data for similar artifacts
- Symbolic residue from past evolutions

## Usage Examples

### Defining an Evolvable Block

```python
# In your code file
from evocore import evolve_markers

# EVOLVE-BLOCK-START
def calculate_fibonacci(n):
    if n <= 1:
        return n
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
# EVOLVE-BLOCK-END
```

### Creating a Custom Evaluator

```python
from evocore.evaluators import BaseEvaluator

class FibonacciEvaluator(BaseEvaluator):
    def evaluate(self, code):
        # Import the evolved code
        module = self.import_code(code)
        
        # Benchmark it on various inputs
        results = []
        for n in [10, 20, 30]:
            start_time = time.time()
            result = module.calculate_fibonacci(n)
            end_time = time.time()
            
            # Check correctness
            expected = self.reference_fibonacci(n)
            is_correct = result == expected
            
            # Measure performance
            execution_time = end_time - start_time
            
            results.append({
                "input": n,
                "is_correct": is_correct,
                "execution_time": execution_time
            })
        
        # Calculate overall score
        correctness = sum(r["is_correct"] for r in results) / len(results)
        performance = sum(r["execution_time"] for r in results)
        
        return {
            "correctness": correctness,
            "performance": performance,
            "score": correctness * (1.0 / (1.0 + performance))  # Higher is better
        }
    
    def reference_fibonacci(self, n):
        # Reference implementation for correctness checking
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
```

## Contributing

To contribute to EvoCore, you can:

1. Add new evaluators for different domains or metrics
2. Improve Git integration features
3. Enhance EVOLVE-BLOCK marker support for more languages
4. Create new templates for common evolution tasks
5. Extend validation capabilities for different artifact types

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

## Related Components

- [EvoOps](../evoops/README.md): Orchestrates the evolution process
- [EvoIntel](../evointel/README.md): Provides intelligence and memory for evolution
- [EvoAPI](../evoapi/README.md): Exposes evolution capabilities via REST API
- [EvoChat](../evochat/README.md): Provides a natural language interface for evolution
