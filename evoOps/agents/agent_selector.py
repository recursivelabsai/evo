"""
AgentSelector - Utility for selecting appropriate AI agents for different evolution stages.

This module provides functionality for dynamically selecting AI agents based on the
current evolution stage, task characteristics, and agent capabilities. It implements
various selection strategies, including blueprint-defined, capability-based, and
adaptive selection.
"""

import logging
from typing import Dict, List, Any, Optional, Union, Callable
import random

from evoops.agents.agent_factory import AgentFactory
from evoops.orchestrator.task_manager import Task
from evointel.blueprints import BlueprintRegistry
from evointel.reflections import ReflectionRegistry


# Configure logging
logger = logging.getLogger(__name__)


class AgentSelector:
    """
    Utility for selecting appropriate AI agents for different evolution stages.
    
    This class provides methods for selecting AI agents based on the current evolution
    stage, task characteristics, and agent capabilities. It supports different selection
    strategies and fallback mechanisms.
    """
    
    def __init__(self):
        """
        Initialize the AgentSelector.
        """
        self.agent_factory = AgentFactory()
        self.agent_capabilities = self._initialize_agent_capabilities()
        self.stage_preferences = self._initialize_stage_preferences()
    
    def select_agent(self, task: Task, stage: str):
        """
        Select an appropriate AI agent for a specific evolution stage.
        
        This method uses a multi-step selection process:
        1. If the task has a blueprint with a defined agent sequence, use that
        2. If the task has preferred agents specified in options, consider those
        3. If the stage has defined agent preferences, use those
        4. Fall back to capability-based selection
        
        Args:
            task: The evolution task
            stage: The current evolution stage
            
        Returns:
            An initialized AI agent object
        """
        # Check if blueprint specifies an agent for this stage
        if task.blueprint:
            try:
                return task.blueprint.get_agent_for_stage(stage)
            except Exception as e:
                logger.warning(f"Failed to get agent from blueprint: {e}")
        
        # Check if task options specify preferred agents
        preferred_agents = task.options.get("preferred_agents", [])
        if preferred_agents:
            for agent_name in preferred_agents:
                if self._agent_suitable_for_stage(agent_name, stage):
                    return self.agent_factory.create(agent_name)
        
        # Check stage preferences
        if stage in self.stage_preferences:
            for agent_name in self.stage_preferences[stage]:
                try:
                    return self.agent_factory.create(agent_name)
                except Exception as e:
                    logger.warning(f"Failed to create preferred agent {agent_name}: {e}")
        
        # Fall back to capability-based selection
        return self._select_by_capabilities(stage, task)
    
    def select_fallback_agent(self, task: Task, stage: str):
        """
        Select a fallback agent to use if the primary agent fails.
        
        Args:
            task: The evolution task
            stage: The current evolution stage
            
        Returns:
            An initialized AI agent object
        """
        # Get currently attempted agent
        current_agent = None
        if task.blueprint:
            try:
                current_agent = task.blueprint.get_agent_for_stage(stage)
            except Exception:
                pass
        
        # Get all available agents
        available_agents = list(self.agent_capabilities.keys())
        
        # Filter out the current agent
        if current_agent:
            agent_name = current_agent.__class__.__name__.lower()
            if agent_name in available_agents:
                available_agents.remove(agent_name)
        
        # Select a different agent with appropriate capabilities
        for agent_name in available_agents:
            if self._agent_suitable_for_stage(agent_name, stage):
                return self.agent_factory.create(agent_name)
        
        # If no suitable agent found, just pick any different one
        if available_agents:
            return self.agent_factory.create(random.choice(available_agents))
        
        # If all else fails, return Claude (our most reliable agent)
        return self.agent_factory.create("claude")
    
    def _select_by_capabilities(self, stage: str, task: Task):
        """
        Select an agent based on capabilities required for the current stage.
        
        Args:
            stage: The current evolution stage
            task: The evolution task
            
        Returns:
            An initialized AI agent object
        """
        # Define required capabilities for different stages
        stage_capabilities = {
            "initial_optimization": ["code_generation", "algorithm_knowledge"],
            "code_review": ["code_analysis", "critique"],
            "edge_case_testing": ["creativity", "test_generation"],
            "final_synthesis": ["code_generation", "synthesis"],
            "iteration_1": ["code_generation", "algorithm_knowledge"],
            "iteration_2": ["code_analysis", "critique"],
            "iteration_3": ["creativity", "innovation"],
            "iteration_4": ["code_generation", "synthesis"],
            "iteration_5": ["code_analysis", "verification"]
        }
        
        # Get required capabilities for this stage
        required_capabilities = stage_capabilities.get(stage, ["code_generation"])
        
        # Score each agent based on their capabilities
        agent_scores = {}
        for agent_name, capabilities in self.agent_capabilities.items():
            score = sum(1 for cap in required_capabilities if cap in capabilities)
            agent_scores[agent_name] = score
        
        # Sort agents by score
        sorted_agents = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Try to create the highest-scoring agent
        for agent_name, _ in sorted_agents:
            try:
                return self.agent_factory.create(agent_name)
            except Exception as e:
                logger.warning(f"Failed to create agent {agent_name}: {e}")
        
        # Fall back to claude if all else fails
        return self.agent_factory.create("claude")
    
    def _agent_suitable_for_stage(self, agent_name: str, stage: str) -> bool:
        """
        Check if an agent is suitable for a particular stage.
        
        Args:
            agent_name: The name of the agent
            stage: The current evolution stage
            
        Returns:
            True if the agent is suitable, False otherwise
        """
        # Define required capabilities for different stages
        stage_capabilities = {
            "initial_optimization": ["code_generation", "algorithm_knowledge"],
            "code_review": ["code_analysis", "critique"],
            "edge_case_testing": ["creativity", "test_generation"],
            "final_synthesis": ["code_generation", "synthesis"],
            "iteration_1": ["code_generation", "algorithm_knowledge"],
            "iteration_2": ["code_analysis", "critique"],
            "iteration_3": ["creativity", "innovation"],
            "iteration_4": ["code_generation", "synthesis"],
            "iteration_5": ["code_analysis", "verification"]
        }
        
        # Get required capabilities for this stage
        required_capabilities = stage_capabilities.get(stage, ["code_generation"])
        
        # Get agent capabilities
        agent_capabilities = self.agent_capabilities.get(agent_name.lower(), [])
        
        # Check if agent has at least one required capability
        return any(cap in agent_capabilities for cap in required_capabilities)
    
    def _initialize_agent_capabilities(self) -> Dict[str, List[str]]:
        """
        Initialize the capabilities of different AI agents.
        
        Returns:
            A dictionary mapping agent names to lists of capabilities
        """
        return {
            "claude": [
                "code_generation", 
                "code_analysis", 
                "algorithm_knowledge", 
                "critique", 
                "synthesis", 
                "verification",
                "creativity",
                "innovation",
                "coherence_analysis",
                "edge_case_analysis"
            ],
            "gemini": [
                "code_generation", 
                "algorithm_knowledge", 
                "test_generation", 
                "verification",
                "context_handling",
                "edge_case_analysis"
            ],
            "gpt": [
                "code_generation", 
                "code_analysis", 
                "creativity", 
                "innovation",
                "test_generation",
                "synthesis"
            ],
            "mistral": [
                "code_generation",
                "algorithm_knowledge",
                "code_analysis"
            ],
            "llama": [
                "code_generation",
                "code_analysis"
            ]
        }
    
    def _initialize_stage_preferences(self) -> Dict[str, List[str]]:
        """
        Initialize agent preferences for different evolution stages.
        
        Returns:
            A dictionary mapping stage names to lists of preferred agent names
        """
        return {
            "initial_optimization": ["gemini", "claude", "gpt"],
            "code_review": ["claude", "gpt", "gemini"],
            "edge_case_testing": ["gpt", "claude", "gemini"],
            "final_synthesis": ["claude", "gpt", "gemini"],
            "iteration_1": ["gemini", "claude", "gpt"],
            "iteration_2": ["claude", "gpt", "gemini"],
            "iteration_3": ["gpt", "claude", "gemini"],
            "iteration_4": ["claude", "gemini", "gpt"],
            "iteration_5": ["claude", "gpt", "gemini"]
        }
    
    def get_agent_capabilities(self, agent_name: str) -> List[str]:
        """
        Get the capabilities of a specific agent.
        
        Args:
            agent_name: The name of the agent
            
        Returns:
            A list of capability strings
        """
        return self.agent_capabilities.get(agent_name.lower(), [])
    
    def get_best_agent_for_capability(self, capability: str) -> str:
        """
        Get the best agent for a specific capability.
        
        Args:
            capability: The required capability
            
        Returns:
            The name of the best agent for the capability
        """
        best_agent = None
        best_score = -1
        
        for agent_name, capabilities in self.agent_capabilities.items():
            if capability in capabilities:
                # Score is based on position in the capabilities list (earlier is better)
                score = len(capabilities) - capabilities.index(capability)
                if score > best_score:
                    best_score = score
                    best_agent = agent_name
        
        return best_agent or "claude"  # Fall back to claude if no match
    
    def update_agent_performance(self, agent_name: str, stage: str, success: bool):
        """
        Update the recorded performance of an agent for a specific stage.
        This is used for adaptive agent selection over time.
        
        Args:
            agent_name: The name of the agent
            stage: The evolution stage
            success: Whether the agent was successful
        """
        # This would connect to a persistent store to track agent performance
        # For now, just log the information
        logger.info(f"Agent {agent_name} {'succeeded' if success else 'failed'} at stage {stage}")
        
        # In a real implementation, this would update a performance database
        # that would influence future agent selection
