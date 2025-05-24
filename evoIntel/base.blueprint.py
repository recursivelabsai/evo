"""
BaseBlueprint - Abstract base class for all evolution blueprints in the EvoIntel system.

Blueprints are pre-packaged evolutionary recipes that encode domain-specific knowledge about
effective evolution patterns for specific types of tasks. They include AI agent sequences,
prompt templates, evaluation metrics, test suites, and meta-instructions for guiding the
evolutionary process.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple, Optional
import json
import uuid
from datetime import datetime


class BaseBlueprint(ABC):
    """
    Abstract base class for all evolution blueprints.
    
    A blueprint defines a strategy for evolving a specific type of artifact (e.g., an algorithm,
    a prompt, a model configuration). It encodes domain-specific knowledge about effective
    evolution patterns, AI agent sequences, evaluation metrics, and more.
    
    Concrete implementations must override the abstract methods to provide blueprint-specific
    functionality.
    """
    
    def __init__(self):
        """
        Initialize a blueprint with default values.
        """
        self.id = str(uuid.uuid4())
        self.name = "Base Blueprint"
        self.version = "0.1.0"
        self.description = "Abstract base blueprint"
        self.tags = []
        self.author = "evo-team"
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.domain = "general"
        
        # These should be set by concrete implementations
        self.agent_sequence = []
        self.evaluation_metrics = {}
        self.evolution_parameters = {}
        self.prompt_templates = {}
        self.test_suite = {}
        self.residue_patterns = {}
        self.meta_instructions = {}
    
    @abstractmethod
    def get_agent_for_stage(self, stage: str):
        """
        Get the appropriate AI agent for a specific evolution stage.
        
        Args:
            stage: The evolution stage (e.g., "initial_optimization", "code_review")
            
        Returns:
            An initialized AI agent object
        """
        pass
    
    @abstractmethod
    def get_prompt_for_stage(self, stage: str, **variables) -> str:
        """
        Get the appropriate prompt template for a specific evolution stage,
        filled with the provided variables.
        
        Args:
            stage: The evolution stage (e.g., "initial_optimization", "code_review")
            **variables: Variables to fill in the prompt template
            
        Returns:
            A prompt string
        """
        pass
    
    @abstractmethod
    def get_evaluator(self):
        """
        Create an evaluator based on the blueprint's evaluation metrics.
        
        Returns:
            An evaluator object configured according to the blueprint
        """
        pass
    
    @abstractmethod
    def get_evolution_parameters(self) -> Dict[str, Any]:
        """
        Get the evolution parameters for this blueprint.
        
        Returns:
            A dictionary of evolution parameters
        """
        pass
    
    @abstractmethod
    def get_test_cases(self) -> List[Dict[str, Any]]:
        """
        Get the test cases for this blueprint.
        
        Returns:
            A list of test case configurations
        """
        pass
    
    @abstractmethod
    def get_relevant_residue_patterns(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get relevant residue patterns based on the current evolution context.
        
        Args:
            context: The current evolution context (e.g., algorithm type, current issues)
            
        Returns:
            A list of relevant residue patterns
        """
        pass
    
    @abstractmethod
    def get_meta_instructions(self) -> Dict[str, List[str]]:
        """
        Get meta-instructions for guiding the evolution process.
        
        Returns:
            A dictionary of meta-instruction categories and their values
        """
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the blueprint to a dictionary representation.
        
        Returns:
            A dictionary representing the blueprint
        """
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "tags": self.tags,
            "author": self.author,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "domain": self.domain,
            "agent_sequence": self.agent_sequence,
            "evaluation_metrics": self.evaluation_metrics,
            "evolution_parameters": self.evolution_parameters,
            "prompt_templates": self.prompt_templates,
            "test_suite": self.test_suite,
            "residue_patterns": self.residue_patterns,
            "meta_instructions": self.meta_instructions
        }
    
    def to_json(self, indent: int = 2) -> str:
        """
        Convert the blueprint to a JSON string.
        
        Args:
            indent: Indentation level for JSON formatting
            
        Returns:
            A JSON string representing the blueprint
        """
        return json.dumps(self.to_dict(), indent=indent)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Create a blueprint instance from a dictionary.
        
        Args:
            data: Dictionary representation of a blueprint
            
        Returns:
            A blueprint instance
        
        Note:
            This method must be implemented by concrete subclasses to properly
            initialize all blueprint-specific attributes.
        """
        blueprint = cls()
        blueprint.id = data.get("id", blueprint.id)
        blueprint.name = data.get("name", blueprint.name)
        blueprint.version = data.get("version", blueprint.version)
        blueprint.description = data.get("description", blueprint.description)
        blueprint.tags = data.get("tags", blueprint.tags)
        blueprint.author = data.get("author", blueprint.author)
        blueprint.created_at = data.get("created_at", blueprint.created_at)
        blueprint.updated_at = data.get("updated_at", blueprint.updated_at)
        blueprint.domain = data.get("domain", blueprint.domain)
        
        # Blueprint-specific attributes should be set by concrete implementations
        blueprint.agent_sequence = data.get("agent_sequence", blueprint.agent_sequence)
        blueprint.evaluation_metrics = data.get("evaluation_metrics", blueprint.evaluation_metrics)
        blueprint.evolution_parameters = data.get("evolution_parameters", blueprint.evolution_parameters)
        blueprint.prompt_templates = data.get("prompt_templates", blueprint.prompt_templates)
        blueprint.test_suite = data.get("test_suite", blueprint.test_suite)
        blueprint.residue_patterns = data.get("residue_patterns", blueprint.residue_patterns)
        blueprint.meta_instructions = data.get("meta_instructions", blueprint.meta_instructions)
        
        return blueprint
    
    @classmethod
    def from_json(cls, json_str: str):
        """
        Create a blueprint instance from a JSON string.
        
        Args:
            json_str: JSON string representation of a blueprint
            
        Returns:
            A blueprint instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @classmethod
    def from_file(cls, file_path: str):
        """
        Create a blueprint instance from a JSON file.
        
        Args:
            file_path: Path to a JSON file containing blueprint data
            
        Returns:
            A blueprint instance
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)


class BlueprintRegistry:
    """
    Registry for managing and retrieving evolution blueprints.
    
    This class provides methods for registering, retrieving, and searching
    for blueprints based on various criteria.
    """
    
    _blueprints = {}
    
    @classmethod
    def register(cls, blueprint: BaseBlueprint):
        """
        Register a blueprint with the registry.
        
        Args:
            blueprint: The blueprint to register
        """
        cls._blueprints[blueprint.id] = blueprint
    
    @classmethod
    def get(cls, blueprint_id: str) -> Optional[BaseBlueprint]:
        """
        Get a blueprint by ID.
        
        Args:
            blueprint_id: The ID of the blueprint to retrieve
            
        Returns:
            The blueprint instance if found, None otherwise
        """
        return cls._blueprints.get(blueprint_id)
    
    @classmethod
    def search(cls, query: str) -> List[BaseBlueprint]:
        """
        Search for blueprints matching a query string.
        
        Args:
            query: The search query
            
        Returns:
            A list of matching blueprint instances
        """
        results = []
        query = query.lower()
        
        for blueprint in cls._blueprints.values():
            # Search in name, description, and tags
            if (query in blueprint.name.lower() or
                query in blueprint.description.lower() or
                any(query in tag.lower() for tag in blueprint.tags)):
                results.append(blueprint)
        
        return results
    
    @classmethod
    def search_by_domain(cls, domain: str) -> List[BaseBlueprint]:
        """
        Search for blueprints in a specific domain.
        
        Args:
            domain: The domain to search in
            
        Returns:
            A list of blueprint instances in the specified domain
        """
        return [bp for bp in cls._blueprints.values() if bp.domain == domain]
    
    @classmethod
    def list_all(cls) -> List[BaseBlueprint]:
        """
        List all registered blueprints.
        
        Returns:
            A list of all blueprint instances
        """
        return list(cls._blueprints.values())
