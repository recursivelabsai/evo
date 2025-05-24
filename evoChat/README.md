# 💬 EvoChat

> *"The natural language interface—where evolutionary AI power meets intuitive human interaction."*

## Overview

EvoChat is the conversational front-end of the `evo` framework, making evolutionary AI accessible to everyone through natural language. It allows users to evolve code, prompts, and other artifacts by simply describing what they want to achieve, without needing to understand the underlying evolutionary mechanisms or API structures. Think of it as the bridge between human intention and the powerful evolutionary engine that drives `evo`.

## Core Responsibilities

- **Translate natural language** into structured evolution tasks
- **Guide users** through defining goals and providing context
- **Present results and insights** in an accessible way
- **Enable real-time feedback** during evolution
- **Adjust complexity level** based on user expertise
- **Integrate with multiple interfaces** (CLI, web, IDE plugins)

## Directory Structure

```
evochat/
├── __init__.py
├── interface/                # Chat interface implementation
├── dialogue/                 # Dialogue management
├── nlu/                      # Natural language understanding
└── wizards/                  # Guided workflows
```

## Key Concepts

### Natural Language Understanding

EvoChat includes sophisticated NLU components that extract structured intent from user messages:

- **Intent Detection**: Identifying what the user wants to achieve (optimize code, improve a prompt, etc.)
- **Entity Extraction**: Identifying key elements in user input (code snippets, file paths, goals)
- **Context Analysis**: Understanding the ongoing conversation and user preferences

```python
# Example NLU flow
user_message = "Can you optimize this sorting algorithm for better performance?"

intent = IntentDetector.detect(user_message)
# intent = "code_optimization"

entities = EntityExtractor.extract(user_message, intent)
# entities = {
#   "target_type": "algorithm",
#   "algorithm_type": "sorting",
#   "goal": "better_performance"
# }

# Request code if not provided
if "code" not in entities:
    response = "I'd be happy to help optimize your sorting algorithm. Could you share the code?"
```

### Dialogue Management

EvoChat manages conversations through a state-tracking dialogue system:

- **Conversation State**: Tracking what stage of the evolution process the user is in
- **Information Gathering**: Collecting necessary inputs for the evolution task
- **Guided Exploration**: Helping users explore options and provide feedback
- **Task Supervision**: Keeping users informed of evolution progress

```python
# Example dialogue flow
class EvolutionDialogue:
    def __init__(self):
        self.state = "initial"
        self.collected_info = {}
    
    def next_response(self, user_message):
        if self.state == "initial":
            # Set state based on intent
            intent = IntentDetector.detect(user_message)
            self.state = intent
            return self._request_missing_info()
        
        elif self.state == "code_optimization" and "code" not in self.collected_info:
            # Store code and ask for goal if not clear
            self.collected_info["code"] = CodeExtractor.extract(user_message)
            return self._request_missing_info()
        
        # More state handling...
    
    def _request_missing_info(self):
        if self.state == "code_optimization":
            if "code" not in self.collected_info:
                return "Please share the code you'd like to optimize."
            if "goal" not in self.collected_info:
                return "What specific aspects would you like to optimize? (e.g., speed, memory usage, readability)"
        
        # More info requests based on state...
```

### Guided Workflows (Wizards)

EvoChat includes specialized wizards that guide users through complex tasks:

- **Evolution Wizard**: Helps users set up and configure evolution tasks
- **Blueprint Wizard**: Assists in selecting appropriate blueprints for specific needs
- **Feedback Wizard**: Guides users through providing effective feedback during evolution

```python
# Example wizard interaction
class EvolutionWizard:
    def __init__(self):
        self.steps = ["intro", "code_collection", "goal_definition", "blueprint_selection", "confirmation"]
        self.current_step = "intro"
        self.collected_data = {}
    
    def next_step(self, user_input):
        if self.current_step == "intro":
            self.current_step = "code_collection"
            return "I'll help you evolve your code. Please share the code you'd like to work with."
        
        elif self.current_step == "code_collection":
            self.collected_data["code"] = user_input
            self.current_step = "goal_definition"
            return "Great! Now, what's your main goal for this evolution? (e.g., optimize for speed, improve readability)"
        
        # More step handling...
        
        elif self.current_step == "confirmation":
            # Start the evolution task
            task_id = self._start_evolution_task()
            return f"Perfect! I've started the evolution process (Task ID: {task_id}). I'll keep you updated on progress."
```

### Interface Implementations

EvoChat supports multiple interface implementations:

- **CLI**: Command-line interface for terminal users and scripts
- **Web**: Browser-based chat interface
- **IDE Plugins**: Direct integration with popular development environments

Each interface communicates with the same core dialogue management system, ensuring consistent user experience across platforms.

## Integration Points

### With EvoAPI

EvoChat uses EvoAPI to:
- Start evolution tasks
- Check task status
- Provide mid-cycle guidance
- Retrieve results
- Access blueprint information

### With EvoIntel

EvoChat leverages EvoIntel to:
- Retrieve appropriate blueprints based on user needs
- Access meta-prompts for effective communication
- Learn from past user interactions
- Identify common user intents and scenarios

## Usage Examples

### CLI Interface

```bash
# Start EvoChat CLI
$ evo chat

# EvoChat CLI interaction
> Hi! I'd like to optimize my Python sorting algorithm.
EvoChat: I'd be happy to help with that! Could you share your sorting algorithm code?

> def bubble_sort(arr):
>     n = len(arr)
>     for i in range(n):
>         for j in range(0, n-i-1):
>             if arr[j] > arr[j+1]:
>                 arr[j], arr[j+1] = arr[j+1], arr[j]
>     return arr
EvoChat: Thanks for sharing your bubble sort implementation. What's your main goal for optimizing this algorithm? Are you looking to improve:
1. Time complexity (speed)
2. Space complexity (memory usage)
3. Readability
4. All of the above

> 1
EvoChat: Great! I'll focus on improving the time complexity. Would you like to use the "Sorting Algorithm Optimization" blueprint, or would you prefer a customized approach?

> Use the blueprint please.
EvoChat: Perfect! I'm starting the evolution process with the "Sorting Algorithm Optimization" blueprint focused on time complexity. This will take a few moments...

[Evolution progress updates...]

EvoChat: I've completed the evolution! Here's the optimized sorting algorithm:

```python
def optimized_sort(arr):
    # Using Timsort, Python's built-in sorting algorithm
    return sorted(arr)
    
    # Alternative implementation if you want to keep a custom algorithm:
    # if len(arr) <= 1:
    #     return arr
    # pivot = arr[len(arr) // 2]
    # left = [x for x in arr if x < pivot]
    # middle = [x for x in arr if x == pivot]
    # right = [x for x in arr if x > pivot]
    # return optimized_sort(left) + middle + optimized_sort(right)
```

This optimization achieves O(n log n) time complexity compared to the original O(n²) of bubble sort, resulting in approximately 100x faster performance for arrays of 1000 elements.

Would you like me to explain the changes in more detail?
```

### Web Interface Example

The web interface would provide similar functionality but with a more visual experience, including:

- Code highlighting
- Real-time evolution progress visualization
- Interactive feedback mechanisms
- Visual comparison of original and evolved code

## Contributing

To contribute to EvoChat, you can:

1. Improve natural language understanding for specific domains
2. Add support for new interfaces or integration points
3. Create new guided workflows for specialized tasks
4. Enhance dialogue management for better user experience
5. Develop user personalization features

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

## Related Components

- [EvoCore](../evocore/README.md): The evolvable artifact repository
- [EvoIntel](../evointel/README.md): The evolutionary memory and intelligence center
- [EvoOps](../evoops/README.md): The orchestration engine
- [EvoAPI](../evoapi/README.md): REST API for integration with existing workflows
