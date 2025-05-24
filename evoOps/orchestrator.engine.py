"""
Orchestration Engine - The central coordinator for the evolutionary process.

The Orchestrator manages the flow of information between AI agents, evaluation pipelines,
and the repository of evolvable artifacts. It is responsible for task management, agent selection,
prompt generation, and coordinating the overall evolutionary process.
"""

import asyncio
from typing import Dict, List, Any, Optional, Tuple
import uuid
from datetime import datetime
import logging

from evoops.orchestrator.task_manager import TaskManager, Task
from evoops.agents.agent_selector import AgentSelector
from evoops.prompting.prompt_builder import PromptBuilder
from evoops.evaluation.evaluator_runner import EvaluatorRunner
from evoops.github.pr_handler import PRHandler
from evointel.blueprints import BlueprintRegistry
from evointel.reflections import ReflectionRegistry
from evointel.residue import ResidueCollector, ResidueRegistry
from evointel.meta_prompts import MetaPromptRegistry
from evocore.evolve_markers import DiffApplier, DiffExtractor


# Configure logging
logger = logging.getLogger(__name__)


class Engine:
    """
    The central orchestration engine for the evo framework.
    
    This class coordinates the evolutionary process, managing the flow of information
    between AI agents, evaluation pipelines, and the repository of evolvable artifacts.
    It is responsible for task management, agent selection, prompt generation, and
    coordinating the overall evolutionary process.
    """
    
    def __init__(self):
        """
        Initialize the orchestration engine.
        """
        self.task_manager = TaskManager()
        self.agent_selector = AgentSelector()
        self.prompt_builder = PromptBuilder()
        self.evaluator_runner = EvaluatorRunner()
        self.pr_handler = PRHandler()
    
    async def start_task(
        self, 
        code: str,
        goal: str,
        blueprint_id: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Start a new evolution task.
        
        Args:
            code: The code to evolve
            goal: The evolution goal
            blueprint_id: Optional ID of the EvoBlueprint to use
            options: Optional dictionary of additional options
            
        Returns:
            The ID of the created task
        """
        # Create a new task
        task_id = str(uuid.uuid4())
        
        # Get blueprint if specified
        blueprint = None
        if blueprint_id:
            blueprint = BlueprintRegistry.get(blueprint_id)
            if not blueprint:
                raise ValueError(f"Blueprint not found: {blueprint_id}")
        
        # Create task
        task = Task(
            id=task_id,
            code=code,
            goal=goal,
            blueprint=blueprint,
            options=options or {},
            status="initialized",
            stage="preparation",
            progress=0,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )
        
        # Register task with task manager
        self.task_manager.register_task(task)
        
        # Start task execution asynchronously
        asyncio.create_task(self._execute_task(task_id))
        
        # Return task ID
        return task_id
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of an evolution task.
        
        Args:
            task_id: The ID of the task
            
        Returns:
            A dictionary with task status information
        """
        task = self.task_manager.get_task(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")
        
        return {
            "id": task.id,
            "status": task.status,
            "stage": task.stage,
            "progress": task.progress,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
        }
    
    async def provide_guidance(self, task_id: str, guidance: str) -> Dict[str, Any]:
        """
        Provide guidance for an ongoing evolution task.
        
        Args:
            task_id: The ID of the task
            guidance: The guidance to provide
            
        Returns:
            A dictionary with updated task status
        """
        task = self.task_manager.get_task(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")
        
        # Add guidance to task
        task.guidance_history.append({
            "timestamp": datetime.now().isoformat(),
            "guidance": guidance
        })
        
        # Update task status
        task.updated_at = datetime.now().isoformat()
        self.task_manager.update_task(task)
        
        # Return updated status
        return {
            "id": task.id,
            "status": task.status,
            "stage": task.stage,
            "progress": task.progress,
            "updated_at": task.updated_at,
            "guidance_acknowledged": True
        }
    
    async def get_task_results(self, task_id: str) -> Dict[str, Any]:
        """
        Get the results of a completed evolution task.
        
        Args:
            task_id: The ID of the task
            
        Returns:
            A dictionary with task results
        """
        task = self.task_manager.get_task(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")
        
        if task.status != "completed":
            return {
                "id": task.id,
                "status": task.status,
                "stage": task.stage,
                "progress": task.progress,
                "message": "Task not yet completed"
            }
        
        # Return completed task results
        return {
            "id": task.id,
            "status": task.status,
            "stage": task.stage,
            "progress": task.progress,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "code": task.results.get("code"),
            "metrics": task.results.get("metrics"),
            "reflections": task.results.get("reflections"),
        }
    
    async def _execute_task(self, task_id: str):
        """
        Execute an evolution task asynchronously.
        
        Args:
            task_id: The ID of the task to execute
        """
        task = self.task_manager.get_task(task_id)
        if not task:
            logger.error(f"Task not found: {task_id}")
            return
        
        try:
            # Update task status
            task.status = "in_progress"
            task.stage = "preparation"
            task.progress = 5
            self.task_manager.update_task(task)
            
            # Prepare evolution process
            blueprint = task.blueprint
            evolution_params = blueprint.get_evolution_parameters() if blueprint else {}
            max_iterations = evolution_params.get("max_iterations", 3)
            convergence_threshold = evolution_params.get("convergence_threshold", 0.01)
            
            # Initialize evolution variables
            current_code = task.code
            best_code = current_code
            best_score = 0
            previous_score = 0
            iterations = 0
            reflections = []
            
            # Main evolution loop
            while iterations < max_iterations:
                iterations += 1
                
                # Update task status
                task.stage = f"iteration_{iterations}"
                task.progress = int(10 + (iterations / max_iterations) * 80)
                self.task_manager.update_task(task)
                
                # Determine current stage in the blueprint's agent sequence
                if blueprint:
                    if iterations == 1:
                        stage = blueprint.agent_sequence[0]["role"]
                    elif iterations == max_iterations:
                        # Use final synthesis agent for last iteration
                        stage = blueprint.agent_sequence[-1]["role"]
                    else:
                        # Cycle through intermediate agents
                        stage_index = (iterations - 1) % (len(blueprint.agent_sequence) - 2) + 1
                        stage = blueprint.agent_sequence[stage_index]["role"]
                else:
                    stage = f"iteration_{iterations}"
                
                # Select appropriate AI agent
                agent = self.agent_selector.select_agent(task, stage)
                
                # Build prompt
                context = {
                    "original_code": task.code,
                    "current_code": current_code,
                    "goal": task.goal,
                    "language": task.options.get("language", "python"),
                    "iteration": iterations,
                    "max_iterations": max_iterations,
                    "previous_reflections": reflections,
                    "user_guidance": task.guidance_history
                }
                
                # Get relevant residue from EvoIntel
                residue = ResidueRegistry.get_relevant(
                    code=current_code,
                    goal=task.goal,
                    domain=blueprint.domain if blueprint else "general"
                )
                if residue:
                    context["residue"] = residue
                
                # Build prompt using blueprint or default template
                if blueprint:
                    prompt = blueprint.get_prompt_for_stage(stage, **context)
                else:
                    prompt = self.prompt_builder.build_default_prompt(stage, **context)
                
                # Generate response from AI agent
                try:
                    response = await agent.generate(prompt)
                except Exception as e:
                    logger.error(f"Agent generation error: {e}")
                    # Try fallback agent if available
                    fallback_agent = self.agent_selector.select_fallback_agent(task, stage)
                    if fallback_agent and fallback_agent != agent:
                        response = await fallback_agent.generate(prompt)
                    else:
                        raise
                
                # Extract diff and reflection
                diff = DiffExtractor.extract(response)
                reflection = {
                    "stage": stage,
                    "agent": agent.name,
                    "content": DiffExtractor.extract_reflection(response)
                }
                reflections.append(reflection)
                
                # Register reflection with EvoIntel
                await ReflectionRegistry.register(task_id, reflection)
                
                # Apply diff to create evolved artifact
                evolved_code = DiffApplier.apply(current_code, diff)
                
                # Evaluate evolved artifact
                evaluator = blueprint.get_evaluator() if blueprint else self.evaluator_runner.get_default_evaluator()
                evaluation_results = await self.evaluator_runner.run(evolved_code, evaluator, task.code)
                
                # Process symbolic residue
                await ResidueCollector.process(
                    task_id=task_id,
                    code=evolved_code,
                    response=response,
                    evaluation_results=evaluation_results
                )
                
                # Update best solution if improved
                current_score = evaluation_results.get("score", 0)
                if current_score > best_score:
                    best_code = evolved_code
                    best_score = current_score
                
                # Check for convergence
                if abs(current_score - previous_score) < convergence_threshold:
                    # Convergence reached
                    break
                
                # Update for next iteration
                current_code = evolved_code
                previous_score = current_score
                
                # Check for user guidance
                if task.guidance_history and len(task.guidance_history) > 0:
                    # Process recent guidance in next iteration
                    context["recent_guidance"] = task.guidance_history[-1]["guidance"]
            
            # Final evaluation and cleanup
            task.stage = "finalization"
            task.progress = 90
            self.task_manager.update_task(task)
            
            # Final detailed evaluation
            final_evaluator = blueprint.get_evaluator() if blueprint else self.evaluator_runner.get_detailed_evaluator()
            final_results = await self.evaluator_runner.run(best_code, final_evaluator, task.code)
            
            # Create PR if requested
            if task.options.get("create_pr", False):
                pr_url = await self.pr_handler.create_pr(
                    repository=task.options.get("repository"),
                    branch=task.options.get("branch", f"evo-{task_id}"),
                    title=f"Evolution: {task.goal}",
                    body=self._generate_pr_description(task, reflections, final_results),
                    code=best_code,
                    original_code=task.code,
                    path=task.options.get("path"),
                )
                task.results["pr_url"] = pr_url
            
            # Store results
            task.results = {
                "code": best_code,
                "metrics": final_results,
                "reflections": reflections,
                "iterations": iterations
            }
            
            # Complete task
            task.status = "completed"
            task.stage = "completed"
            task.progress = 100
            task.updated_at = datetime.now().isoformat()
            self.task_manager.update_task(task)
            
            logger.info(f"Task completed: {task_id}")
            
        except Exception as e:
            logger.error(f"Task execution error: {e}", exc_info=True)
            
            # Update task status
            task.status = "failed"
            task.stage = "error"
            task.updated_at = datetime.now().isoformat()
            task.error = str(e)
            self.task_manager.update_task(task)
    
    def _generate_pr_description(
        self, 
        task: Task, 
        reflections: List[Dict[str, Any]], 
        evaluation_results: Dict[str, Any]
    ) -> str:
        """
        Generate a PR description for the evolved code.
        
        Args:
            task: The evolution task
            reflections: List of reflections from AI agents
            evaluation_results: Results of the final evaluation
            
        Returns:
            A formatted PR description
        """
        description = f"# Evolution: {task.goal}\n\n"
        
        # Add summary
        description += "## Summary\n\n"
        description += f"This PR was generated by the evo framework to {task.goal.lower()}.\n\n"
        
        # Add metrics
        description += "## Metrics\n\n"
        description += "| Metric | Value | Improvement |\n"
        description += "| ------ | ----- | ---------- |\n"
        
        for metric, value in evaluation_results.get("metrics", {}).items():
            improvement = evaluation_results.get("improvements", {}).get(metric, "N/A")
            description += f"| {metric} | {value} | {improvement} |\n"
        
        # Add key reflections
        description += "\n## Key Insights\n\n"
        for reflection in reflections:
            content = reflection.get("content", "")
            if content:
                # Extract the first paragraph or sentence for brevity
                summary = content.split("\n\n")[0].strip()
                summary = summary[:200] + "..." if len(summary) > 200 else summary
                description += f"- **{reflection['stage']}**: {summary}\n"
        
        # Add task details
        description += f"\n## Task Details\n\n"
        description += f"- **Task ID**: {task.id}\n"
        description += f"- **Created**: {task.created_at}\n"
        description += f"- **Completed**: {task.updated_at}\n"
        
        if task.blueprint:
            description += f"- **Blueprint**: {task.blueprint.name} (v{task.blueprint.version})\n"
        
        return description
