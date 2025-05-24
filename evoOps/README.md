# ⚙️ EvoOps

> *"The orchestration engine—where AI agents, evaluation pipelines, and evolutionary workflows come together to drive emergence."*

## Overview

EvoOps is the central orchestration system of the `evo` framework that coordinates the evolutionary process. It manages the flow of information between AI agents, evaluation pipelines, and the repository of evolvable artifacts. Think of it as the "nervous system" that connects the "brain" (EvoIntel) with the "body" (EvoCore) to produce coherent, purposeful evolution.

## Core Responsibilities

- **Orchestrate AI agent interactions** in the evolutionary loop
- **Manage evolution tasks** from inception to completion
- **Coordinate evaluation pipelines** for evolved artifacts
- **Process and route symbolic residue** to EvoIntel
- **Integrate with GitHub** workflows and repositories
- **Monitor and log** the evolutionary process
- **Handle user feedback** during evolution

## Directory Structure

```
evoops/
├── __init__.py
├── orchestrator/             # Core orchestration engine
├── agents/                   # AI agent wrappers
├── prompting/                # Prompt generation and management
├── github/                   # GitHub integration
├── monitoring/               # Monitoring and logging
└── evaluation/               # Evaluation orchestration
```

## Key Concepts

### The Orchestration Engine

The orchestration engine is the heart of EvoOps, managing the overall flow of the evolutionary process:

- **Task Management**: Tracks evolution tasks from inception to completion
- **Agent Selection**: Chooses appropriate AI agents for specific evolution stages
- **Evolution Tracking**: Monitors the progress and state of each evolution task
- **Workflow Execution**: Coordinates the sequence of operations in the evolutionary loop

```python
# Example orchestration flow
async def orchestrate_evolution(task_id, goal, code, blueprint=None):
    # Initialize task
    task = TaskManager.create(task_id, goal, code, blueprint)
    
    # Select initial AI agent based on blueprint or heuristics
    agent = AgentSelector.select_for_stage(task, "initial_optimization")
    
    # Generate prompt using EvoIntel resources
    prompt = PromptBuilder.build(
        template=MetaPromptRegistry.get("code_optimization"),
        code=code,
        goal=goal,
        blueprint=blueprint,
        residue=ResidueRegistry.get_relevant(code, goal)
    )
    
    # Get response from AI agent
    response = await agent.generate(prompt)
    
    # Extract diff and reflection
    diff = DiffExtractor.extract(response)
    reflection = ReflectionExtractor.extract(response)
    
    # Apply diff to create evolved artifact
    evolved_artifact = DiffApplier.apply(code, diff)
    
    # Evaluate evolved artifact
    evaluation_results = await EvaluatorRunner.run(
        evolved_artifact, 
        evaluators=blueprint.evaluators if blueprint else DefaultEvaluators.get()
    )
    
    # Register reflection and residue
    await ReflectionRegistry.register(task_id, reflection)
    await ResidueCollector.process(task_id, response, evaluation_results)
    
    # Determine next steps based on evaluation
    if evaluation_results.should_continue():
        # Continue evolution with another agent or stage
        return await next_evolution_stage(task_id, evolved_artifact)
    else:
        # Finalize evolution
        return finalize_evolution(task_id, evolved_artifact, evaluation_results)
```

### AI Agent Wrappers

EvoOps provides wrappers for different AI agents, allowing the orchestration engine to interact with them in a unified way:

- **Model-Specific Adapters**: Tailored for Claude, Gemini, GPT, etc.
- **Prompt Handling**: Converting internal representations to model-specific formats
- **Response Processing**: Extracting structured data from natural language responses
- **Error Handling**: Managing failed calls, timeouts, or unexpected responses

```python
# Example AI agent wrapper
class ClaudeAgent:
    def __init__(self, api_key, model="claude-3-opus-20240229"):
        self.api_key = api_key
        self.model = model
        self.client = AnthropicClient(api_key)
    
    async def generate(self, prompt):
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return self._fallback_handler(e)
    
    def _fallback_handler(self, error):
        # Implement error handling and fallback strategies
        pass
```

### Prompt Generation and Management

EvoOps includes sophisticated prompting utilities that leverage EvoIntel resources to generate effective prompts for AI agents:

- **Prompt Building**: Assembling context, instructions, and relevant information
- **Context Management**: Ensuring prompt content stays within token limits
- **Feedback Integration**: Incorporating user feedback into subsequent prompts
- **Residue Injection**: Strategically including symbolic residue from past attempts

```python
# Example prompt building
class PromptBuilder:
    @staticmethod
    def build(template, **variables):
        """
        Build a prompt using a template and variables.
        
        Args:
            template: A template string or template ID from EvoIntel
            **variables: Variables to fill in the template
            
        Returns:
            A complete prompt string
        """
        # Get template if string ID was provided
        if isinstance(template, str):
            template = MetaPromptRegistry.get(template)
        
        # Process special variables
        if "residue" in variables and variables["residue"]:
            variables["residue_patterns"] = ResidueProcessor.extract_patterns(variables["residue"])
        
        # Fill template with variables
        return template.format(**variables)
```

### GitHub Integration

EvoOps provides integration with GitHub to enable evolution directly from repositories:

- **GitHub App**: Responds to repository events (issues, PRs, comments)
- **GitHub Action**: Runs evolution as part of CI/CD workflows
- **Issue Handling**: Processes evolution requests from issue comments
- **PR Handling**: Creates PRs with evolved code and explanations

```yaml
# Example GitHub Action configuration
name: Evo Code Evolution
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  evolve:
    if: contains(github.event.comment.body, '/evolve')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: evolve-ai/evo-action@v1
        with:
          api_key: ${{ secrets.EVO_API_KEY }}
          goal: ${{ github.event.comment.body }}
```

### Evaluation Orchestration

EvoOps coordinates the evaluation of evolved artifacts using evaluators from EvoCore:

- **Evaluator Selection**: Choosing appropriate evaluators based on the task
- **Parallel Evaluation**: Running multiple evaluations concurrently
- **Result Analysis**: Interpreting evaluation results to guide further evolution
- **Feedback Generation**: Creating feedback for AI agents based on evaluation

```python
# Example evaluation orchestration
class EvaluatorRunner:
    @staticmethod
    async def run(artifact, evaluators):
        """
        Run a set of evaluators on an artifact.
        
        Args:
            artifact: The artifact to evaluate
            evaluators: List of evaluator configurations
            
        Returns:
            EvaluationResults object
        """
        # Prepare evaluation tasks
        tasks = []
        for eval_config in evaluators:
            evaluator = EvaluatorFactory.create(
                eval_config["type"],
                **eval_config.get("params", {})
            )
            tasks.append(evaluator.evaluate(artifact))
        
        # Run evaluations in parallel
        results = await asyncio.gather(*tasks)
        
        # Combine and analyze results
        return EvaluationResults(
            individual_results=results,
            weights=[e.get("weight", 1.0) for e in evaluators],
            metadata={"artifact_type": type(artifact).__name__}
        )
```

## Integration Points

### With EvoCore

EvoOps interacts with EvoCore to:
- Retrieve target artifacts for evolution
- Apply diffs to create evolved artifacts
- Trigger evaluations of evolved artifacts
- Commit changes to the repository

### With EvoIntel

EvoOps interacts with EvoIntel to:
- Retrieve blueprints for evolutionary guidance
- Get prompt templates and meta-prompts
- Store reflections from AI agents
- Process and store symbolic residue
- Update coherence metrics and other intelligence

## Usage Examples

### Orchestrating an Evolution Task

```python
from evoops.orchestrator import Engine

# Create an orchestration engine
engine = Engine()

# Start an evolution task
task_id = await engine.start_task(
    code="def bubble_sort(arr): ...",
    goal="Optimize for time complexity",
    blueprint="algorithm_optimization"
)

# Check task status
status = await engine.get_task_status(task_id)
print(f"Task status: {status.stage}, progress: {status.progress}%")

# Provide mid-cycle guidance
await engine.provide_guidance(
    task_id=task_id,
    guidance="Consider using a heap-based approach instead"
)

# Get task results when complete
results = await engine.get_task_results(task_id)
print(f"Evolved code: {results.code}")
print(f"Performance improvement: {results.metrics.improvement}%")
```

### Using the GitHub Integration

```python
from evoops.github import IssueHandler

# Create an issue handler
handler = IssueHandler()

# Process an issue comment
await handler.process_comment(
    repo="username/repo",
    issue_number=42,
    comment_body="/evolve optimize path/to/file.py for speed"
)
```

## Contributing

To contribute to EvoOps, you can:

1. Implement support for additional AI agents
2. Improve orchestration strategies and algorithms
3. Enhance GitHub integration features
4. Develop better prompting techniques
5. Create new monitoring and logging features

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

## Related Components

- [EvoCore](../evocore/README.md): The evolvable artifact repository
- [EvoIntel](../evointel/README.md): The evolutionary memory and intelligence center
- [EvoAPI](../evoapi/README.md): REST API for integration with existing workflows
- [EvoChat](../evochat/README.md): Natural language interface for evolution
