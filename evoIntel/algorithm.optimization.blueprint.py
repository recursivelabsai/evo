"""
AlgorithmOptimizationBlueprint - A concrete implementation of the EvoBlueprint base class
for evolving algorithms to improve performance while maintaining correctness.
"""

from typing import Dict, List, Any, Tuple, Optional
import json
import os
from datetime import datetime

from evointel.blueprints.base_blueprint import BaseBlueprint
from evocore.evaluators import CorrectnessEvaluator, TimeComplexityEvaluator, SpaceComplexityEvaluator, ReadabilityEvaluator
from evocore.evaluators import CompositeEvaluator
from evoops.agents import AgentFactory


class AlgorithmOptimizationBlueprint(BaseBlueprint):
    """
    A blueprint for evolving algorithms to improve performance while maintaining correctness.
    This blueprint is designed for optimizing algorithms in terms of time complexity, space complexity,
    and readability, with correctness as a non-negotiable requirement.
    """
    
    ID = "algorithm_optimization"
    NAME = "Algorithm Optimization Blueprint"
    VERSION = "1.0.0"
    DESCRIPTION = "Optimizes algorithms for performance while maintaining correctness"
    TAGS = ["algorithm", "optimization", "performance", "time-complexity"]
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the AlgorithmOptimizationBlueprint.
        
        Args:
            config_path: Optional path to a custom configuration JSON file.
                         If not provided, the default configuration will be used.
        """
        super().__init__()
        
        # Load configuration
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            # Use default configuration
            self.config = self._get_default_config()
            
        # Set up blueprint metadata
        self.id = self.ID
        self.name = self.NAME
        self.version = self.VERSION
        self.description = self.DESCRIPTION
        self.tags = self.TAGS
        self.author = self.config.get("author", "evo-team")
        self.created_at = self.config.get("created_at", datetime.now().isoformat())
        self.updated_at = self.config.get("updated_at", datetime.now().isoformat())
        self.domain = self.config.get("domain", "algorithm_optimization")
        
        # Set up blueprint components
        self.agent_sequence = self.config.get("agent_sequence", self._get_default_agent_sequence())
        self.evaluation_metrics = self.config.get("evaluation_metrics", self._get_default_evaluation_metrics())
        self.evolution_parameters = self.config.get("evolution_parameters", self._get_default_evolution_parameters())
        self.prompt_templates = self.config.get("prompt_templates", self._get_default_prompt_templates())
        self.test_suite = self.config.get("test_suite", self._get_default_test_suite())
        self.residue_patterns = self.config.get("residue_patterns", self._get_default_residue_patterns())
        self.meta_instructions = self.config.get("meta_instructions", self._get_default_meta_instructions())
    
    def get_agent_for_stage(self, stage: str):
        """
        Get the appropriate AI agent for a specific evolution stage.
        
        Args:
            stage: The evolution stage (e.g., "initial_optimization", "code_review")
            
        Returns:
            An initialized AI agent object
        """
        for agent_config in self.agent_sequence:
            if agent_config["role"] == stage:
                agent_name = agent_config["agent"]
                return AgentFactory.create(agent_name)
        
        # Default to first agent if stage not found
        default_agent_name = self.agent_sequence[0]["agent"]
        return AgentFactory.create(default_agent_name)
    
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
        # Find the agent config for this stage
        agent_config = None
        for config in self.agent_sequence:
            if config["role"] == stage:
                agent_config = config
                break
        
        if not agent_config:
            raise ValueError(f"No agent configuration found for stage: {stage}")
        
        # Get the prompt template
        template_id = agent_config["prompt_template"]
        if template_id not in self.prompt_templates:
            raise ValueError(f"Prompt template not found: {template_id}")
        
        template = self.prompt_templates[template_id]["template"]
        
        # Validate variables
        required_vars = self.prompt_templates[template_id]["variables"]
        for var in required_vars:
            if var not in variables:
                raise ValueError(f"Missing required variable for prompt template: {var}")
        
        # Fill in the template
        return template.format(**variables)
    
    def get_evaluator(self) -> CompositeEvaluator:
        """
        Create a composite evaluator based on the blueprint's evaluation metrics.
        
        Returns:
            A CompositeEvaluator configured according to the blueprint
        """
        evaluators = []
        weights = []
        
        # Create individual evaluators
        metrics = self.evaluation_metrics
        if "correctness" in metrics:
            evaluators.append(CorrectnessEvaluator(
                minimum_threshold=metrics["correctness"].get("minimum_threshold", 1.0)
            ))
            weights.append(metrics["correctness"].get("weight", 0.5))
        
        if "time_complexity" in metrics:
            evaluators.append(TimeComplexityEvaluator())
            weights.append(metrics["time_complexity"].get("weight", 0.3))
        
        if "space_complexity" in metrics:
            evaluators.append(SpaceComplexityEvaluator())
            weights.append(metrics["space_complexity"].get("weight", 0.1))
        
        if "readability" in metrics:
            evaluators.append(ReadabilityEvaluator())
            weights.append(metrics["readability"].get("weight", 0.1))
        
        # Create and return composite evaluator
        return CompositeEvaluator(evaluators=evaluators, weights=weights)
    
    def get_evolution_parameters(self) -> Dict[str, Any]:
        """
        Get the evolution parameters for this blueprint.
        
        Returns:
            A dictionary of evolution parameters
        """
        return self.evolution_parameters
    
    def get_test_cases(self) -> List[Dict[str, Any]]:
        """
        Get the test cases for this blueprint.
        
        Returns:
            A list of test case configurations
        """
        return self.test_suite.get("default_test_cases", [])
    
    def get_relevant_residue_patterns(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get relevant residue patterns based on the current evolution context.
        
        Args:
            context: The current evolution context (e.g., algorithm type, current issues)
            
        Returns:
            A list of relevant residue patterns
        """
        relevant_patterns = []
        
        # Simple relevance matching for now - can be made more sophisticated
        algorithm_type = context.get("algorithm_type", "")
        
        for pattern_type in ["near_misses", "innovative_fragments"]:
            if pattern_type in self.residue_patterns:
                for pattern in self.residue_patterns[pattern_type]:
                    # Check if pattern is relevant to this algorithm type
                    if algorithm_type.lower() in pattern.get("pattern", "").lower():
                        relevant_patterns.append(pattern)
        
        return relevant_patterns
    
    def get_meta_instructions(self) -> Dict[str, List[str]]:
        """
        Get meta-instructions for guiding the evolution process.
        
        Returns:
            A dictionary of meta-instruction categories and their values
        """
        return self.meta_instructions
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get the default configuration for this blueprint.
        
        Returns:
            A default configuration dictionary
        """
        # In a real implementation, this would be loaded from a file
        return {
            "author": "evo-team",
            "created_at": "2025-05-24T10:00:00Z",
            "updated_at": "2025-05-24T10:00:00Z",
            "domain": "algorithm_optimization"
        }
    
    def _get_default_agent_sequence(self) -> List[Dict[str, str]]:
        """
        Get the default AI agent sequence for this blueprint.
        
        Returns:
            A list of agent configurations
        """
        return [
            {
                "agent": "gemini",
                "role": "initial_optimization",
                "prompt_template": "initial_optimization"
            },
            {
                "agent": "claude",
                "role": "code_review",
                "prompt_template": "code_review"
            },
            {
                "agent": "gpt",
                "role": "edge_case_testing",
                "prompt_template": "edge_case_testing"
            },
            {
                "agent": "claude",
                "role": "final_synthesis",
                "prompt_template": "final_synthesis"
            }
        ]
    
    def _get_default_evaluation_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the default evaluation metrics for this blueprint.
        
        Returns:
            A dictionary of evaluation metric configurations
        """
        return {
            "correctness": {
                "weight": 0.5,
                "evaluator": "correctness_evaluator",
                "minimum_threshold": 1.0
            },
            "time_complexity": {
                "weight": 0.3,
                "evaluator": "time_complexity_evaluator"
            },
            "space_complexity": {
                "weight": 0.1,
                "evaluator": "space_complexity_evaluator"
            },
            "readability": {
                "weight": 0.1,
                "evaluator": "readability_evaluator"
            }
        }
    
    def _get_default_evolution_parameters(self) -> Dict[str, Any]:
        """
        Get the default evolution parameters for this blueprint.
        
        Returns:
            A dictionary of evolution parameters
        """
        return {
            "max_iterations": 5,
            "convergence_threshold": 0.01,
            "exploration_rate": 0.2,
            "divergence_probability": 0.1,
            "residue_injection_rate": 0.3
        }
    
    def _get_default_prompt_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the default prompt templates for this blueprint.
        
        Returns:
            A dictionary of prompt templates
        """
        return {
            "initial_optimization": {
                "template": "You are an expert algorithm optimizer. Your task is to improve the performance of the following algorithm while maintaining its correctness.\n\nOriginal Algorithm:\n```{language}\n{code}\n```\n\nGoal: {goal}\n\nFirst, analyze the current implementation and identify its time and space complexity. Then, propose an optimized version that improves these aspects while ensuring all functionality is preserved.\n\nIf you recognize this as a standard algorithm type (sorting, searching, etc.), consider well-known optimizations or alternative algorithms that might be more efficient.\n\nProvide your optimized solution as a complete implementation, not just snippets or pseudocode.",
                "variables": ["language", "code", "goal"]
            },
            "code_review": {
                "template": "You are an expert code reviewer focused on algorithm optimization. Review the following original algorithm and proposed optimization:\n\nOriginal Algorithm:\n```{language}\n{original_code}\n```\n\nProposed Optimization:\n```{language}\n{proposed_code}\n```\n\nGoal: {goal}\n\nPlease analyze the proposed optimization critically:\n1. Verify correctness: Does it maintain all functionality of the original algorithm?\n2. Analyze complexity: What are the time and space complexity improvements?\n3. Identify edge cases: Are there any scenarios where this optimization might fail?\n4. Suggest improvements: How could this optimization be further enhanced?\n\nProvide specific code suggestions for any improvements you identify.",
                "variables": ["language", "original_code", "proposed_code", "goal"]
            },
            "edge_case_testing": {
                "template": "You are an expert in identifying edge cases and testing algorithms. Review the following algorithm optimization:\n\nOriginal Algorithm:\n```{language}\n{original_code}\n```\n\nOptimized Algorithm:\n```{language}\n{optimized_code}\n```\n\nGoal: {goal}\n\nYour task is to:\n1. Identify potential edge cases where the optimized algorithm might fail or perform poorly\n2. Suggest test cases that would verify the algorithm's correctness and performance in these scenarios\n3. Propose specific improvements to handle these edge cases\n\nBe creative in identifying edge cases that might not be immediately obvious. Consider extreme inputs, special cases, and boundary conditions.",
                "variables": ["language", "original_code", "optimized_code", "goal"]
            },
            "final_synthesis": {
                "template": "You are an expert algorithm designer tasked with creating the final optimized version of an algorithm. You have access to the original algorithm, initial optimization, code review, and edge case analysis:\n\nOriginal Algorithm:\n```{language}\n{original_code}\n```\n\nInitial Optimization:\n```{language}\n{initial_optimization}\n```\n\nCode Review Feedback:\n{code_review_feedback}\n\nEdge Case Analysis:\n{edge_case_analysis}\n\nGoal: {goal}\n\nCreate a final, optimized version of the algorithm that:\n1. Incorporates the best ideas from all previous steps\n2. Addresses all identified edge cases\n3. Maintains complete correctness\n4. Achieves optimal performance for the stated goal\n5. Remains readable and maintainable\n\nProvide your final solution as a complete implementation, along with a brief explanation of your design decisions and the expected performance characteristics.",
                "variables": ["language", "original_code", "initial_optimization", "code_review_feedback", "edge_case_analysis", "goal"]
            }
        }
    
    def _get_default_test_suite(self) -> Dict[str, Any]:
        """
        Get the default test suite configuration for this blueprint.
        
        Returns:
            A dictionary of test suite configuration
        """
        return {
            "default_test_cases": [
                {
                    "name": "empty_input",
                    "description": "Tests behavior with empty input"
                },
                {
                    "name": "single_element",
                    "description": "Tests behavior with just one element"
                },
                {
                    "name": "already_optimized",
                    "description": "Tests with input that's already in optimal state"
                },
                {
                    "name": "worst_case",
                    "description": "Tests with input that triggers worst-case behavior"
                },
                {
                    "name": "large_input",
                    "description": "Tests performance with large input sizes"
                }
            ],
            "custom_test_generators": [
                "random_input_generator",
                "adversarial_input_generator"
            ]
        }
    
    def _get_default_residue_patterns(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Get the default residue patterns for this blueprint.
        
        Returns:
            A dictionary of residue pattern categories and their values
        """
        return {
            "near_misses": [
                {
                    "pattern": "Algorithm works faster but fails on empty arrays",
                    "potential_value": "May contain novel partitioning approach"
                },
                {
                    "pattern": "Reduces time complexity but increases space complexity",
                    "potential_value": "Trade-off approach that might be valuable in memory-abundant scenarios"
                }
            ],
            "innovative_fragments": [
                {
                    "pattern": "Novel caching mechanism",
                    "potential_value": "Could be applied to other algorithms with repetitive computations"
                },
                {
                    "pattern": "Interesting parallelization approach",
                    "potential_value": "May be applicable to other divide-and-conquer algorithms"
                }
            ]
        }
    
    def _get_default_meta_instructions(self) -> Dict[str, List[str]]:
        """
        Get the default meta-instructions for this blueprint.
        
        Returns:
            A dictionary of meta-instruction categories and their values
        """
        return {
            "prioritize_goals": [
                "Correctness is non-negotiable",
                "Time complexity is the primary optimization target",
                "Space complexity is secondary unless specified otherwise",
                "Maintain readability and clarity of implementation"
            ],
            "symbolic_residue_focus": [
                "Pay special attention to trade-offs between time and space complexity",
                "Catalog innovative partitioning or divide-and-conquer approaches even if they don't fully succeed",
                "Track optimization patterns that could be applied across algorithm classes"
            ]
        }
