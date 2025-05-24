# 🔗 EvoAPI

> *"The REST API interface—where evolutionary power meets programmatic accessibility."*

## Overview

EvoAPI is the RESTful gateway to the `evo` framework, providing a standardized, programmatic interface for accessing evolutionary capabilities. It enables integration with existing workflows, toolchains, and third-party applications, making AI-driven evolution accessible through standard HTTP requests. Think of it as the bridge that connects the powerful evolutionary engine with the broader software ecosystem.

## Core Responsibilities

- **Expose evolutionary capabilities** through standardized REST endpoints
- **Manage authentication and authorization** for secure access
- **Handle task lifecycle management** (creation, status, guidance, results)
- **Provide access to EvoBlueprints** and intelligence resources
- **Enable GitHub and CI/CD integration** through webhook endpoints
- **Support various client libraries** for different programming languages

## Directory Structure

```
evoapi/
├── __init__.py
├── app.py                    # Main API application
├── routes/                   # API routes
├── middleware/               # API middleware
├── schemas/                  # API schemas
└── services/                 # API services
```

## Key Concepts

### Core Endpoints

EvoAPI provides a set of intuitive endpoints that map to the evolutionary process:

- **/evolve/start**: Start a new evolution task
- **/evolve/{task_id}/status**: Get the status of an evolution task
- **/evolve/{task_id}/guide**: Provide guidance during evolution
- **/evolve/{task_id}/peek**: View intermediate results
- **/evolve/{task_id}/results**: Get final results
- **/evolve/{task_id}/accept_solution**: Accept a specific solution
- **/blueprints/list**: List available EvoBlueprints
- **/blueprints/{id}/info**: Get details about a specific blueprint
- **/intel/insights?query={query}**: Search EvoIntel for insights

```http
POST /evolve/start
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "code": "def bubble_sort(arr): ...",
  "goal": "Optimize for time complexity",
  "blueprint": "algorithm_optimization",
  "options": {
    "max_iterations": 5,
    "preferred_agents": ["claude", "gemini"]
  }
}
```

### Request/Response Schemas

EvoAPI uses consistent, well-documented schemas for all requests and responses:

```json
// Example response for /evolve/start
{
  "task_id": "task-1234-5678-90ab-cdef",
  "status": "initialized",
  "estimated_time": 120,
  "meta": {
    "blueprint": "algorithm_optimization",
    "target_artifact_type": "code",
    "language": "python"
  },
  "_links": {
    "status": "/evolve/task-1234-5678-90ab-cdef/status",
    "guide": "/evolve/task-1234-5678-90ab-cdef/guide",
    "peek": "/evolve/task-1234-5678-90ab-cdef/peek",
    "results": "/evolve/task-1234-5678-90ab-cdef/results"
  }
}
```

### Authentication and Authorization

EvoAPI uses industry-standard authentication mechanisms:

- **API Key Authentication**: For server-to-server integration
- **OAuth 2.0**: For third-party applications
- **JWT**: For authenticated user sessions

Authorization is managed through a role-based system:

- **User Roles**: Regular, Pro, Enterprise
- **Rate Limiting**: Based on role and subscription level
- **Resource Access**: Control over which blueprints and agents can be used

### Middleware Stack

EvoAPI includes several middleware layers:

- **Authentication**: Verifies API keys and tokens
- **Rate Limiting**: Prevents abuse and ensures fair resource allocation
- **Logging**: Records all API activity for auditing and debugging
- **Error Handling**: Provides consistent, informative error responses

### Event Webhooks

EvoAPI supports webhooks for asynchronous notifications:

- **Task Status Changes**: Get notified when a task progresses
- **Completion Events**: Receive a webhook when evolution completes
- **Error Notifications**: Get notified of any issues

```http
POST /webhooks/register
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "url": "https://your-server.com/webhooks/evo",
  "events": ["task.completed", "task.error"],
  "secret": "your_webhook_secret"
}
```

## Integration Points

### With EvoOps

EvoAPI translates HTTP requests into internal EvoOps task objects:

```python
# Example of how EvoAPI routes connect to EvoOps
@app.post("/evolve/start")
async def start_evolution_task(request: StartTaskRequest):
    # Validate request
    validate_request(request)
    
    # Translate to EvoOps task
    task = await TaskService.create_task(
        code=request.code,
        goal=request.goal,
        blueprint=request.blueprint,
        options=request.options
    )
    
    # Return response
    return {
        "task_id": task.id,
        "status": task.status,
        # Other response fields...
    }
```

### With GitHub

EvoAPI includes specialized endpoints for GitHub integration:

- **/github/webhook**: Receives GitHub webhook events
- **/github/authorize**: OAuth flow for GitHub App installation
- **/github/issue/{id}/evolve**: Start evolution from a GitHub issue

```python
# Example GitHub integration
@app.post("/github/webhook")
async def github_webhook(request: GitHubWebhookPayload):
    # Verify GitHub webhook signature
    verify_github_signature(request)
    
    # Process based on event type
    if request.event == "issue_comment" and "/evolve" in request.comment.body:
        # Extract evolution parameters from comment
        params = extract_evolution_params(request.comment.body)
        
        # Create evolution task
        task = await TaskService.create_task(
            repository=request.repository.full_name,
            issue_number=request.issue.number,
            params=params
        )
        
        # Post comment acknowledging the task
        await GitHubService.post_comment(
            repository=request.repository.full_name,
            issue_number=request.issue.number,
            comment=f"Evolution task started (ID: {task.id}). I'll update this thread with progress."
        )
    
    # Handle other GitHub events...
```

## Client Libraries

EvoAPI provides official client libraries for popular programming languages:

### Python Client

```python
from evo_client import Evolution

# Initialize client
evo = Evolution(api_key="YOUR_API_KEY")

# Start an evolution task
task = evo.evolve(
    code="def bubble_sort(arr): ...",
    goal="Optimize for time complexity",
    blueprint="algorithm_optimization"
)

# Check status
status = task.status()
print(f"Task status: {status.stage}, progress: {status.progress}%")

# Provide guidance
task.guide("Consider using a heap-based approach")

# Get results when complete
results = task.results()
print(f"Evolved code: {results.code}")
print(f"Performance improvement: {results.metrics.improvement}%")
```

### JavaScript Client

```javascript
const { Evolution } = require('evo-client');

// Initialize client
const evo = new Evolution({ apiKey: 'YOUR_API_KEY' });

// Start an evolution task
evo.evolve({
  code: 'function bubbleSort(arr) { ... }',
  goal: 'Optimize for time complexity',
  blueprint: 'algorithm_optimization'
})
.then(task => {
  // Check status
  return task.status();
})
.then(status => {
  console.log(`Task status: ${status.stage}, progress: ${status.progress}%`);
  
  // Provide guidance
  return task.guide('Consider using a quicksort approach');
})
.then(() => {
  // Get results when complete
  return task.results();
})
.then(results => {
  console.log(`Evolved code: ${results.code}`);
  console.log(`Performance improvement: ${results.metrics.improvement}%`);
})
.catch(error => {
  console.error('Evolution error:', error);
});
```

## OpenAPI Specification

EvoAPI includes a complete OpenAPI (Swagger) specification at `/docs`, enabling:

- **Interactive Documentation**: Try API endpoints directly from the browser
- **Client Generation**: Generate client libraries for any language
- **Schema Validation**: Ensure requests and responses match the specification

## Usage Examples

### Starting an Evolution Task

```bash
# Using curl
curl -X POST "https://api.evochat.ai/evolve/start" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "code": "def bubble_sort(arr): ...",
    "goal": "Optimize for time complexity",
    "blueprint": "algorithm_optimization"
  }'
```

### Checking Task Status

```bash
# Using curl
curl -X GET "https://api.evochat.ai/evolve/task-1234-5678-90ab-cdef/status" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Providing Guidance

```bash
# Using curl
curl -X POST "https://api.evochat.ai/evolve/task-1234-5678-90ab-cdef/guide" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "guidance": "Consider using a heap-based approach instead"
  }'
```

### Getting Results

```bash
# Using curl
curl -X GET "https://api.evochat.ai/evolve/task-1234-5678-90ab-cdef/results" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Contributing

To contribute to EvoAPI, you can:

1. Extend the API with new endpoints or features
2. Improve existing client libraries or create new ones
3. Enhance documentation and examples
4. Optimize performance or security aspects
5. Add support for new authentication methods or integrations

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

## Related Components

- [EvoCore](../evocore/README.md): The evolvable artifact repository
- [EvoIntel](../evointel/README.md): The evolutionary memory and intelligence center
- [EvoOps](../evoops/README.md): The orchestration engine
- [EvoChat](../evochat/README.md): Natural language interface for evolution
