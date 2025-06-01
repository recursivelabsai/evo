"""
TimeComplexityEvaluator - Evaluates the time complexity of an algorithm both theoretically
and practically by measuring execution time across various input sizes.
"""

import time
import inspect
import logging
import math
import random
import numpy as np
import importlib.util
import sys
from typing import Dict, List, Any, Callable, Tuple, Optional, Union
from tempfile import NamedTemporaryFile
import os

from evocore.evaluators.base_evaluator import BaseEvaluator


# Configure logging
logger = logging.getLogger(__name__)


class TimeComplexityEvaluator(BaseEvaluator):
    """
    Evaluates the time complexity of an algorithm through a combination of
    theoretical analysis (via static code inspection) and practical timing
    measurements across various input sizes.
    
    This evaluator generates synthetic inputs of increasing size, measures
    execution time, and attempts to fit the results to known complexity classes.
    """
    
    def __init__(
        self,
        input_sizes: Optional[List[int]] = None,
        num_runs: int = 5,
        timeout: float = 30.0,
        weight: float = 1.0,
        input_generator: Optional[Callable] = None
    ):
        """
        Initialize the TimeComplexityEvaluator.
        
        Args:
            input_sizes: List of input sizes to test (e.g., [10, 100, 1000, 10000])
            num_runs: Number of times to run each test for averaging
            timeout: Maximum time (in seconds) to allow for each test run
            weight: The weight of this evaluator in a composite evaluation
            input_generator: Optional custom function to generate inputs of a given size
        """
        super().__init__(weight=weight)
        self.input_sizes = input_sizes or [10, 100, 1000, 10000]
        self.num_runs = num_runs
        self.timeout = timeout
        self.input_generator = input_generator or self._default_input_generator
    
    def evaluate(self, code: str, original_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Evaluate the time complexity of the provided code.
        
        Args:
            code: The code to evaluate
            original_code: Optional original code for comparison
            
        Returns:
            A dictionary containing evaluation results, including:
            - theoretical_complexity: Estimated big-O notation
            - measured_complexity: Complexity class based on measurements
            - execution_times: Dictionary mapping input sizes to average execution times
            - relative_improvement: Improvement over original code (if provided)
            - score: Overall score (0.0 to 1.0)
        """
        try:
            # Import the code as a module
            module, function_name = self._import_code(code)
            
            # Import original code if provided
            original_module = None
            original_function_name = None
            if original_code:
                original_module, original_function_name = self._import_code(original_code)
            
            # Get the function object
            function = getattr(module, function_name)
            original_function = getattr(original_module, original_function_name) if original_module else None
            
            # Run timing tests
            execution_times = self._measure_execution_times(function)
            original_execution_times = self._measure_execution_times(original_function) if original_function else None
            
            # Analyze complexity
            theoretical_complexity = self._estimate_theoretical_complexity(code, function_name)
            measured_complexity = self._estimate_measured_complexity(execution_times)
            
            # Calculate relative improvement if original code is provided
            relative_improvement = None
            if original_execution_times:
                relative_improvement = self._calculate_improvement(execution_times, original_execution_times)
            
            # Calculate overall score
            score = self._calculate_score(theoretical_complexity, measured_complexity, execution_times, original_execution_times)
            
            # Return results
            results = {
                "theoretical_complexity": theoretical_complexity,
                "measured_complexity": measured_complexity,
                "execution_times": execution_times,
                "score": score
            }
            
            if relative_improvement:
                results["relative_improvement"] = relative_improvement
            
            return results
            
        except Exception as e:
            logger.error(f"Error evaluating time complexity: {e}", exc_info=True)
            return {
                "error": str(e),
                "score": 0.0
            }
    
    def _import_code(self, code: str) -> Tuple[Any, str]:
        """
        Import the provided code as a module and identify the main function.
        
        Args:
            code: The code to import
            
        Returns:
            A tuple containing the imported module and the name of the main function
        """
        # Create a temporary file
        with NamedTemporaryFile(suffix='.py', delete=False) as temp_file:
            temp_file.write(code.encode('utf-8'))
            temp_file_path = temp_file.name
        
        try:
            # Import the module
            module_name = os.path.basename(temp_file_path)[:-3]  # Remove .py extension
            spec = importlib.util.spec_from_file_location(module_name, temp_file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find the main function
            # Heuristic: Look for functions with no args or only array args
            function_name = None
            for name, obj in inspect.getmembers(module, inspect.isfunction):
                # Skip helper functions (often start with underscore)
                if name.startswith('_'):
                    continue
                
                # Get function parameters
                sig = inspect.signature(obj)
                params = sig.parameters
                
                # If it has 1-2 parameters, it's likely the main function
                if len(params) in [1, 2]:
                    function_name = name
                    break
            
            if not function_name:
                # If no clear main function, use the first function
                for name, obj in inspect.getmembers(module, inspect.isfunction):
                    if not name.startswith('_'):
                        function_name = name
                        break
            
            if not function_name:
                raise ValueError("Could not identify a main function in the code")
            
            return module, function_name
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                logger.warning(f"Error cleaning up temporary file: {e}")
    
    def _measure_execution_times(self, function: Callable) -> Dict[int, float]:
        """
        Measure execution times of the function across various input sizes.
        
        Args:
            function: The function to evaluate
            
        Returns:
            A dictionary mapping input sizes to average execution times (in seconds)
        """
        execution_times = {}
        
        for size in self.input_sizes:
            times = []
            
            # Generate input once for consistency
            input_data = self.input_generator(size)
            
            for _ in range(self.num_runs):
                # Copy input to prevent modification between runs
                input_copy = self._copy_input(input_data)
                
                # Measure execution time
                start_time = time.time()
                function(input_copy)
                end_time = time.time()
                
                times.append(end_time - start_time)
            
            # Calculate average time (excluding outliers)
            times.sort()
            if len(times) >= 3:
                # Remove highest and lowest times
                avg_time = sum(times[1:-1]) / (len(times) - 2)
            else:
                avg_time = sum(times) / len(times)
            
            execution_times[size] = avg_time
        
        return execution_times
    
    def _copy_input(self, input_data: Any) -> Any:
        """
        Create a deep copy of the input data to prevent modification between runs.
        
        Args:
            input_data: The input data to copy
            
        Returns:
            A deep copy of the input data
        """
        if isinstance(input_data, list):
            return [self._copy_input(item) for item in input_data]
        elif isinstance(input_data, dict):
            return {k: self._copy_input(v) for k, v in input_data.items()}
        elif isinstance(input_data, tuple):
            return tuple(self._copy_input(item) for item in input_data)
        elif isinstance(input_data, set):
            return {self._copy_input(item) for item in input_data}
        else:
            # For primitive types, no deep copy needed
            return input_data
    
    def _estimate_theoretical_complexity(self, code: str, function_name: str) -> str:
        """
        Estimate the theoretical time complexity by analyzing the code structure.
        This is a heuristic approach and may not be accurate for all algorithms.
        
        Args:
            code: The code to analyze
            function_name: The name of the main function
            
        Returns:
            A string representing the estimated big-O notation
        """
        # Simple heuristic approach based on loop nesting and common patterns
        # In a real implementation, this would be much more sophisticated
        
        lines = code.split('\n')
        function_lines = []
        in_function = False
        
        # Extract the main function lines
        for line in lines:
            if line.strip().startswith(f"def {function_name}"):
                in_function = True
                function_lines.append(line)
            elif in_function:
                if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                    # Start of a new function or class
                    in_function = False
                else:
                    function_lines.append(line)
        
        function_code = '\n'.join(function_lines)
        
        # Check for common sorting algorithm names
        if 'merge_sort' in function_name.lower():
            return "O(n log n)"
        elif 'quick_sort' in function_name.lower():
            return "O(n log n)"  # Average case
        elif 'heap_sort' in function_name.lower():
            return "O(n log n)"
        elif 'bubble_sort' in function_name.lower() or 'insertion_sort' in function_name.lower():
            return "O(n²)"
        
        # Count nested loops
        max_nesting_level = 0
        current_nesting_level = 0
        
        for line in function_lines:
            line = line.strip()
            
            # Check for loop statements
            if any(loop_keyword in line for loop_keyword in ['for ', 'while ']):
                current_nesting_level += 1
                max_nesting_level = max(max_nesting_level, current_nesting_level)
            
            # Check for potential end of a loop block
            elif line and line[0] not in [' ', '\t'] and not line.startswith('def '):
                current_nesting_level = max(0, current_nesting_level - 1)
        
        # Map nesting level to complexity class
        if max_nesting_level == 0:
            return "O(1)"
        elif max_nesting_level == 1:
            return "O(n)"
        elif max_nesting_level == 2:
            return "O(n²)"
        else:
            return f"O(n^{max_nesting_level})"
    
    def _estimate_measured_complexity(self, execution_times: Dict[int, float]) -> str:
        """
        Estimate the time complexity class based on measured execution times.
        
        Args:
            execution_times: Dictionary mapping input sizes to execution times
            
        Returns:
            A string representing the estimated complexity class
        """
        # Convert to lists for curve fitting
        sizes = list(execution_times.keys())
        times = list(execution_times.values())
        
        if len(sizes) < 2:
            return "Unknown"
        
        # Try fitting to different complexity classes
        # O(1)
        constant_error = self._calculate_fit_error(sizes, times, lambda n: 1)
        
        # O(log n)
        log_error = self._calculate_fit_error(sizes, times, lambda n: math.log(n))
        
        # O(n)
        linear_error = self._calculate_fit_error(sizes, times, lambda n: n)
        
        # O(n log n)
        linearithmic_error = self._calculate_fit_error(sizes, times, lambda n: n * math.log(n))
        
        # O(n²)
        quadratic_error = self._calculate_fit_error(sizes, times, lambda n: n ** 2)
        
        # O(n³)
        cubic_error = self._calculate_fit_error(sizes, times, lambda n: n ** 3)
        
        # O(2^n)
        exponential_error = float('inf')  # Avoid for large inputs
        if max(sizes) <= 100:
            exponential_error = self._calculate_fit_error(sizes, times, lambda n: 2 ** n)
        
        # Find the best fit
        errors = [
            (constant_error, "O(1)"),
            (log_error, "O(log n)"),
            (linear_error, "O(n)"),
            (linearithmic_error, "O(n log n)"),
            (quadratic_error, "O(n²)"),
            (cubic_error, "O(n³)"),
            (exponential_error, "O(2^n)")
        ]
        
        errors.sort(key=lambda x: x[0])
        return errors[0][1]
    
    def _calculate_fit_error(self, sizes: List[int], times: List[float], complexity_func: Callable) -> float:
        """
        Calculate the error when fitting measured times to a complexity function.
        
        Args:
            sizes: List of input sizes
            times: List of execution times
            complexity_func: Function that models a complexity class
            
        Returns:
            The mean squared error of the fit
        """
        # Calculate function values for each size
        func_values = [complexity_func(size) for size in sizes]
        
        # Find the best scaling factor
        if sum(func_values) == 0:
            return float('inf')
        
        scaling_factor = sum(t * f for t, f in zip(times, func_values)) / sum(f * f for f in func_values)
        
        # Calculate error
        errors = [(times[i] - scaling_factor * func_values[i]) ** 2 for i in range(len(sizes))]
        mse = sum(errors) / len(errors)
        
        return mse
    
    def _calculate_improvement(self, execution_times: Dict[int, float], original_execution_times: Dict[int, float]) -> Dict[str, Any]:
        """
        Calculate the improvement of the new algorithm over the original one.
        
        Args:
            execution_times: Dictionary mapping input sizes to execution times for the new algorithm
            original_execution_times: Dictionary mapping input sizes to execution times for the original algorithm
            
        Returns:
            A dictionary containing improvement metrics
        """
        improvement_metrics = {}
        
        # Calculate speedup for each input size
        speedups = {}
        for size in execution_times:
            if size in original_execution_times and original_execution_times[size] > 0:
                speedups[size] = original_execution_times[size] / execution_times[size]
        
        if not speedups:
            return {"average_speedup": 1.0, "improvement_percentage": 0.0}
        
        # Calculate average speedup
        avg_speedup = sum(speedups.values()) / len(speedups)
        
        # Calculate improvement percentage
        improvement_percentage = (avg_speedup - 1) * 100
        
        # Create improvement metrics
        improvement_metrics["speedups"] = speedups
        improvement_metrics["average_speedup"] = avg_speedup
        improvement_metrics["improvement_percentage"] = improvement_percentage
        
        return improvement_metrics
    
    def _calculate_score(
        self, 
        theoretical_complexity: str, 
        measured_complexity: str, 
        execution_times: Dict[int, float], 
        original_execution_times: Optional[Dict[int, float]] = None
    ) -> float:
        """
        Calculate an overall score for the algorithm based on complexity and execution times.
        
        Args:
            theoretical_complexity: Estimated big-O notation
            measured_complexity: Complexity class based on measurements
            execution_times: Dictionary mapping input sizes to execution times
            original_execution_times: Optional execution times for the original algorithm
            
        Returns:
            A score between 0.0 and 1.0
        """
        # Define complexity class scores (higher is better)
        complexity_scores = {
            "O(1)": 1.0,
            "O(log n)": 0.9,
            "O(n)": 0.8,
            "O(n log n)": 0.7,
            "O(n²)": 0.5,
            "O(n³)": 0.3,
            "O(2^n)": 0.1,
            "Unknown": 0.0
        }
        
        # Get complexity score
        measured_score = complexity_scores.get(measured_complexity, 0.0)
        
        # If original code is provided, factor in improvement
        if original_execution_times:
            improvement = self._calculate_improvement(execution_times, original_execution_times)
            avg_speedup = improvement.get("average_speedup", 1.0)
            
            # Cap speedup score to prevent extreme values
            speedup_score = min(avg_speedup / 10.0, 1.0)
            
            # Combine complexity and speedup scores
            score = 0.7 * measured_score + 0.3 * speedup_score
        else:
            # Use complexity score alone
            score = measured_score
        
        return score
    
    def _default_input_generator(self, size: int) -> List[int]:
        """
        Default function to generate input of a given size.
        Generates a list of random integers.
        
        Args:
            size: The size of the input to generate
            
        Returns:
            A list of random integers
        """
        return [random.randint(0, 1000) for _ in range(size)]
