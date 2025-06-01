"""
BaseEvaluator - Abstract base class for all evaluators in the EvoCore system.

Evaluators assess the quality of evolved artifacts along various dimensions such as
performance, correctness, readability, and more. They provide a standardized interface
for evaluation and can be composed to create complex fitness functions.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union


class BaseEvaluator(ABC):
    """
    Abstract base class for all evaluators in the EvoCore system.
    
    An evaluator assesses the quality of an evolved artifact (e.g., code, prompt, model configuration)
    along a specific dimension (e.g., performance, correctness, readability). It provides a score
    between 0.0 and 1.0 to indicate the quality of the artifact.
    
    Evaluators can be composed to create complex fitness functions by weighting and combining
    multiple evaluators.
    """
    
    def __init__(self, weight: float = 1.0):
        """
        Initialize an evaluator with a weight.
        
        Args:
            weight: The weight of this evaluator in a composite evaluation (default: 1.0)
        """
        self.weight = weight
    
    @abstractmethod
    def evaluate(self, artifact: str, original_artifact: Optional[str] = None) -> Dict[str, Any]:
        """
        Evaluate the quality of an artifact.
        
        Args:
            artifact: The artifact to evaluate (e.g., code, prompt, model configuration)
            original_artifact: Optional original artifact for comparison (e.g., before evolution)
            
        Returns:
            A dictionary containing evaluation results, including a 'score' key with a value
            between 0.0 and 1.0
        """
        pass
    
    def __add__(self, other: 'BaseEvaluator') -> 'CompositeEvaluator':
        """
        Combine this evaluator with another evaluator to create a composite evaluator.
        
        Args:
            other: Another evaluator to combine with this one
            
        Returns:
            A CompositeEvaluator that combines the results of both evaluators
        """
        if not isinstance(other, BaseEvaluator):
            raise TypeError("Can only add BaseEvaluator instances")
        
        return CompositeEvaluator([self, other], [self.weight, other.weight])


class CompositeEvaluator(BaseEvaluator):
    """
    A composite evaluator that combines the results of multiple evaluators.
    
    This evaluator runs multiple evaluators and combines their scores using a weighted average.
    It's useful for evaluating artifacts along multiple dimensions simultaneously.
    """
    
    def __init__(self, evaluators: List[BaseEvaluator], weights: Optional[List[float]] = None):
        """
        Initialize a composite evaluator with a list of evaluators and weights.
        
        Args:
            evaluators: List of evaluators to run
            weights: Optional list of weights for each evaluator (default: use evaluator weights)
        """
        super().__init__(weight=1.0)
        self.evaluators = evaluators
        
        # Use provided weights or the evaluators' own weights
        if weights:
            if len(weights) != len(evaluators):
                raise ValueError("Number of weights must match number of evaluators")
            self.weights = weights
        else:
            self.weights = [evaluator.weight for evaluator in evaluators]
        
        # Normalize weights
        weight_sum = sum(self.weights)
        if weight_sum > 0:
            self.weights = [w / weight_sum for w in self.weights]
    
    def evaluate(self, artifact: str, original_artifact: Optional[str] = None) -> Dict[str, Any]:
        """
        Evaluate the artifact using all component evaluators and combine their results.
        
        Args:
            artifact: The artifact to evaluate
            original_artifact: Optional original artifact for comparison
            
        Returns:
            A dictionary containing combined evaluation results, including:
            - individual_results: Results from each individual evaluator
            - score: Weighted average of individual scores
        """
        # Run all evaluators
        individual_results = []
        for evaluator in self.evaluators:
            try:
                result = evaluator.evaluate(artifact, original_artifact)
                individual_results.append(result)
            except Exception as e:
                # If an evaluator fails, record the error and continue
                individual_results.append({
                    "error": str(e),
                    "score": 0.0
                })
        
        # Calculate weighted average score
        total_score = 0.0
        for i, result in enumerate(individual_results):
            score = result.get("score", 0.0)
            total_score += score * self.weights[i]
        
        # Combine results
        combined_result = {
            "individual_results": individual_results,
            "weights": self.weights,
            "score": total_score
        }
        
        return combined_result
    
    def __add__(self, other: BaseEvaluator) -> 'CompositeEvaluator':
        """
        Add another evaluator to this composite evaluator.
        
        Args:
            other: Another evaluator to add
            
        Returns:
            A new CompositeEvaluator with the additional evaluator
        """
        if not isinstance(other, BaseEvaluator):
            raise TypeError("Can only add BaseEvaluator instances")
        
        # If other is a CompositeEvaluator, flatten the structure
        if isinstance(other, CompositeEvaluator):
            new_evaluators = self.evaluators + other.evaluators
            new_weights = self.weights + other.weights
        else:
            new_evaluators = self.evaluators + [other]
            new_weights = self.weights + [other.weight]
        
        return CompositeEvaluator(new_evaluators, new_weights)
