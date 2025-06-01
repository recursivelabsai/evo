"""
AgentFactory - Factory for creating and configuring AI agent instances.

This module provides a factory for creating and configuring AI agent instances
for different models (Claude, Gemini, GPT, etc.). It handles API key management,
model configuration, and agent initialization.
"""

import logging
import os
from typing import Dict, List, Any, Optional, Union

from evoops.agents.base_agent import BaseAgent
from evoops.agents.claude_agent import ClaudeAgent
from evoops.agents.gemini_agent import GeminiAgent
from evoops.agents.gpt_agent import GPTAgent
from evoops.agents.mistral_agent import MistralAgent
from evoops.agents.llama_agent import LlamaAgent


# Configure logging
logger = logging.getLogger(__name__)


class AgentFactory:
    """
    Factory for creating and configuring AI agent instances.
    
    This class provides methods for creating and configuring AI agent instances
    for different models (Claude, Gemini, GPT, etc.). It handles API key management,
    model configuration, and agent initialization.
    """
    
    def __init__(self):
        """
        Initialize the AgentFactory.
        """
        self.api_keys = self._load_api_keys()
        self.model_configs = self._initialize_model_configs()
        self.agent_registry = self._initialize_agent_registry()
    
    def create(self, agent_name: str, **kwargs) -> BaseAgent:
        """
        Create an AI agent instance.
        
        Args:
            agent_name: The name of the agent to create
            **kwargs: Additional configuration options for the agent
            
        Returns:
            An initialized BaseAgent instance
            
        Raises:
            ValueError: If the agent name is not recognized
            RuntimeError: If the agent cannot be created
        """
        # Normalize agent name
        agent_name = agent_name.lower()
        
        # Get agent class and model config
        agent_class = self.agent_registry.get(agent_name)
        if not agent_class:
            raise ValueError(f"Unknown agent: {agent_name}")
        
        # Get default model config
        model_config = self.model_configs.get(agent_name, {}).copy()
        
        # Override with provided kwargs
        model_config.update(kwargs)
        
        # Get API key
        api_key = kwargs.get('api_key') or self.api_keys.get(agent_name)
        if not api_key:
            raise ValueError(f"No API key found for {agent_name}")
        
        # Create agent
        try:
            return agent_class(api_key=api_key, **model_config)
        except Exception as e:
            logger.error(f"Error creating {agent_name} agent: {e}")
            raise RuntimeError(f"Failed to create {agent_name} agent: {e}")
    
    def list_available_agents(self) -> List[str]:
        """
        Get a list of available agent names.
        
        Returns:
            A list of available agent names
        """
        return list(self.agent_registry.keys())
    
    def get_model_config(self, agent_name: str) -> Dict[str, Any]:
        """
        Get the default model configuration for an agent.
        
        Args:
            agent_name: The name of the agent
            
        Returns:
            A dictionary containing the model configuration
        """
        return self.model_configs.get(agent_name.lower(), {}).copy()
    
    def update_model_config(self, agent_name: str, **kwargs):
        """
        Update the default model configuration for an agent.
        
        Args:
            agent_name: The name of the agent
            **kwargs: Configuration options to update
        """
        agent_name = agent_name.lower()
        if agent_name in self.model_configs:
            self.model_configs[agent_name].update(kwargs)
        else:
            self.model_configs[agent_name] = kwargs
    
    def register_agent(self, name: str, agent_class: type):
        """
        Register a new agent class.
        
        Args:
            name: The name to register the agent under
            agent_class: The agent class to register
        """
        name = name.lower()
        self.agent_registry[name] = agent_class
    
    def _load_api_keys(self) -> Dict[str, str]:
        """
        Load API keys from environment variables.
        
        Returns:
            A dictionary mapping agent names to API keys
        """
        return {
            "claude": os.environ.get("ANTHROPIC_API_KEY", ""),
            "gemini": os.environ.get("GOOGLE_API_KEY", ""),
            "gpt": os.environ.get("OPENAI_API_KEY", ""),
            "mistral": os.environ.get("MISTRAL_API_KEY", ""),
            "llama": os.environ.get("LLAMA_API_KEY", "")
        }
    
    def _initialize_model_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize default model configurations.
        
        Returns:
            A dictionary mapping agent names to model configurations
        """
        return {
            "claude": {
                "model": "claude-3-opus-20240229",
                "max_tokens": 4000,
                "temperature": 0.7,
                "top_p": 0.9,
                "timeout": 60.0
            },
            "gemini": {
                "model": "gemini-1.5-pro",
                "max_tokens": 4000,
                "temperature": 0.7,
                "top_p": 0.9,
                "timeout": 60.0
            },
            "gpt": {
                "model": "gpt-4-turbo",
                "max_tokens": 4000,
                "temperature": 0.7,
                "top_p": 0.9,
                "timeout": 60.0
            },
            "mistral": {
                "model": "mistral-large-latest",
                "max_tokens": 4000,
                "temperature": 0.7,
                "top_p": 0.9,
                "timeout": 60.0
            },
            "llama": {
                "model": "llama-3-70b-instruct",
                "max_tokens": 4000,
                "temperature": 0.7,
                "top_p": 0.9,
                "timeout": 60.0
            }
        }
    
    def _initialize_agent_registry(self) -> Dict[str, type]:
        """
        Initialize the agent class registry.
        
        Returns:
            A dictionary mapping agent names to agent classes
        """
        return {
            "claude": ClaudeAgent,
            "gemini": GeminiAgent,
            "gpt": GPTAgent,
            "mistral": MistralAgent,
            "llama": LlamaAgent
        }
