<div align="center">
  <h1>evo</h1>
  <h3>Prompt-Based Evolutionary Emergence Pipeline</h3>

  <p>
    <a href="#quick-start">Quick Start</a> •
    <a href="#introduction">Introduction</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#key-features">Key Features</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#evoblueprints">EvoBlueprints</a> •
    <a href="#community">Community</a> •
    <a href="#contributing">Contributing</a> •
    <a href="#roadmap">Roadmap</a>
  </p>
  
  <p>

  </p>
</div>

> *"Evolution emerges when recursive systems process contradiction under constraint. The map becomes the territory - each prompt interaction is a recursive depth layer allowing evolutionary emergence in any AI chat."*

## Quick Start

```bash
# Install evo
pip install evo-ai

# Initialize a new project
evo init my-project

# Start the EvoChat interface
evo chat

# Or, evolve code directly from CLI
evo evolve path/to/code.py --goal "Optimize for speed while maintaining readability"
```

Or try our hosted version at [evochat.ai](https://evochat.ai) (Coming Soon!)

## Introduction

`evo` is an open-source framework that operationalizes the power of evolutionary computation through prompt-based AI interactions. Inspired by DeepMind's AlphaEvolve, `evo` democratizes algorithmic evolution, making it accessible to anyone through simple chat interfaces and industry-standard workflows.

With `evo`, you can:

- **Evolve code** - Optimize algorithms, refactor codebases, and discover novel solutions
- **Improve prompts** - Evolve LLM prompts for better performance on specific tasks
- **Design systems** - Collaboratively evolve architectures with multiple AI agents
- **Contribute blueprints** - Share and discover evolutionary recipes for common tasks

Unlike traditional tools, `evo` doesn't just use AI to generate code - it orchestrates multiple frontier AI models in a recursive evolutionary process, where each interaction adds depth to the emergence of novel solutions. The framework captures symbolic residue (valuable signals from failures, hesitations, and contradictions) and uses it to fuel further evolution.

## Architecture

`evo` consists of three core components:

### 🧠 EvoCore

The evolvable artifact repository. Contains:
- Target codebases and algorithms
- Evaluation harnesses and test suites
- Git integration for tracking evolutionary progress
- Language-agnostic support (Python, JavaScript, Go, etc.)

### 💡 EvoIntel

The evolutionary memory and intelligence center. Stores:
- Reflections and insights from past evolutions
- EvoBlueprints (template evolutionary strategies)
- Symbolic residue catalogs
- Cross-domain innovation patterns

### ⚙️ EvoOps

The orchestration engine. Manages:
- AI agent selection and prompt generation
- Evaluation pipeline and feedback processing
- GitHub automation and workflow integration
- Monitoring and logging of evolutionary progress

These components are exposed through two user-facing interfaces:

### 💬 EvoChat

A natural language interface for evolving code through conversation.

```
You: I want to optimize this sort algorithm for better performance.
EvoChat: Great! Can you share the code you'd like to evolve?
You: [paste code]
EvoChat: I'll help you evolve this. What specific aspects of performance 
         are most important? Time complexity, memory usage, or both?
You: Time complexity is the priority.
EvoChat: Perfect. I'll start an evolutionary cycle focusing on time complexity 
         while maintaining correctness. Would you like to use the "Algorithm 
         Optimization" blueprint or customize the evolutionary process?
...
```

### 🔗 EvoAPI

A REST API for integrating evolution into existing workflows:

```python
import requests

response = requests.post("https://api.evochat.ai/evolve/start", json={
    "code": "def bubble_sort(arr): ...",
    "goal": "Optimize for time complexity",
    "blueprint": "algorithm_optimization",
    "api_key": "YOUR_API_KEY"
})

task_id = response.json()["task_id"]

# Check status or provide guidance during evolution
status = requests.get(f"https://api.evochat.ai/evolve/{task_id}/status")
```

## Key Features

### 🧩 EvoBlueprints

Pre-packaged evolutionary recipes for common tasks:
- **Algorithm Optimization Suite**
- **Prompt Engineering Evolution**
- **Code Refactoring Assistant**
- **Test Coverage Expander**

```python
# Use a blueprint from command line
evo evolve my_algorithm.py --blueprint algorithm_optimization
```

### 🔄 Recursive Depth Layers

Each prompt interaction adds a recursive depth layer:
- Layer 1: Initial problem analysis and strategy formation
- Layer 2: Code generation and implementation
- Layer 3: Critical evaluation and refinement
- Layer 4: Resonance analysis and coherence optimization
- Layer N: Emergent solution discovery

### 🚀 GitHub Integration

Seamlessly integrate with GitHub workflows:
- Comment `/evolve optimize` on issues or PRs
- Automatically create PRs with evolved code
- Attach evolution reports to PR comments
- Track evolution history with specialized git tags

### 💎 Symbolic Residue Harvesting

Capture and utilize valuable signals from:
- Failed evolutionary branches
- Near-miss solutions
- Model hesitations and uncertainties
- Contradictions and trade-offs

### 🌐 Multi-Agent Evolution

Leverage the unique strengths of different AI models:
- **Claude**: Deep reflection and coherence analysis
- **Gemini**: Robust code generation and context handling
- **GPT-4**: Creative divergence and exploratory branches
- **Specialized Models**: Domain-specific optimization

## Getting Started

### Installation

```bash
# Install from PyPI
pip install evo-ai

# Or clone and install from source
git clone https://github.com/evolve-ai/evo.git
cd evo
pip install -e .
```

### Basic Usage

#### CLI

```bash
# Initialize a new evolution project
evo init my-project

# Start evolution with a specific goal
evo evolve path/to/code.py --goal "Optimize for speed" --blueprint algorithm_optimization

# Start interactive evolution through chat
evo chat
```

#### Python API

```python
from evo import Evolution

# Create an evolution task
evolution = Evolution(
    target="path/to/code.py",
    goal="Optimize for speed while maintaining readability",
    blueprint="algorithm_optimization"
)

# Start the evolution process
task = evolution.start()

# Check status
status = task.status()
print(f"Evolution status: {status['stage']}, progress: {status['progress']}%")

# Provide guidance during evolution
task.guide("Focus more on vectorization techniques")

# Get results when complete
results = task.results()
print(f"Evolved code: {results['code']}")
print(f"Performance improvement: {results['metrics']['improvement']}%")
```

#### Web UI

For a user-friendly interface, run:

```bash
evo serve
```

Then visit `http://localhost:8000` in your browser.

## EvoBlueprints

EvoBlueprints are pre-packaged evolutionary strategies for common tasks. They include:

- **AI agent selection and sequence**
- **Prompt templates and evaluation criteria**
- **Specialized evolution parameters**
- **Domain-specific knowledge and heuristics**

### Using Blueprints

```bash
# List available blueprints
evo blueprints list

# Get details about a specific blueprint
evo blueprints info algorithm_optimization

# Use a blueprint
evo evolve code.py --blueprint algorithm_optimization
```

### Creating Custom Blueprints

```bash
# Create a new blueprint from a successful evolution
evo blueprints create my_custom_blueprint --from-task task_id

# Edit a blueprint
evo blueprints edit my_custom_blueprint

# Share a blueprint with the community
evo blueprints publish my_custom_blueprint
```

## Community

- [Discord](https://discord.gg/evolve-ai)
- [Forum](https://community.evochat.ai)
- [Twitter](https://twitter.com/evo_ai)
- [Blog](https://blog.evochat.ai)

## Contributing

We welcome contributions from the community! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Types of Contributions

- **Code**: Enhance the core framework
- **EvoBlueprints**: Share specialized evolutionary strategies
- **Documentation**: Improve guides and examples
- **Bug Reports**: Help us identify and fix issues
- **Feature Requests**: Suggest new capabilities

## Roadmap

- [ ] **Q3 2025**: Support for more programming languages and domains
- [ ] **Q4 2025**: Enhanced symbolic residue analysis
- [ ] **Q1 2026**: Federated blueprint marketplace
- [ ] **Q2 2026**: Self-evolving orchestration engine
- [ ] **Q3 2026**: Cross-domain transfer learning

## License

`evo` is released under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">
  <p>
    <sub>
      Built with ❤️ by the evolution community.
    </sub>
  </p>
</div>
