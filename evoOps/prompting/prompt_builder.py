"""
PromptBuilder - Utility for constructing prompts for AI agents.

This module provides functionality for building prompts for AI agents based on templates,
context, and residue from past evolutions. It supports both template-based prompt generation
and dynamic construction of prompts based on the current evolutionary context.
"""

import logging
import re
from string import Template
from typing import Dict, List, Any, Optional, Union

from evointel.meta_prompts import MetaPromptRegistry
from evointel.residue import ResidueRegistry


# Configure logging
logger = logging.getLogger(__name__)


class PromptBuilder:
    """
    Utility for constructing prompts for AI agents.
    
    This class provides methods for building prompts based on templates, context,
    and residue from past evolutions. It supports simple template substitution,
    conditional sections based on available context, and dynamic residue injection.
    """
    
    def __init__(self):
        """
        Initialize the PromptBuilder.
        """
        pass
    
    def build(self, template_id: str, **variables) -> str:
        """
        Build a prompt using a template from the MetaPromptRegistry.
        
        Args:
            template_id: The ID of the template to use
            **variables: Variables to fill in the template
            
        Returns:
            A prompt string
        """
        # Get template from registry
        template = MetaPromptRegistry.get(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")
        
        # Process special variables
        variables = self._process_special_variables(variables)
        
        # Fill template
        return self._fill_template(template, variables)
    
    def build_from_string(self, template_string: str, **variables) -> str:
        """
        Build a prompt using a template string.
        
        Args:
            template_string: The template string to use
            **variables: Variables to fill in the template
            
        Returns:
            A prompt string
        """
        # Process special variables
        variables = self._process_special_variables(variables)
        
        # Fill template
        return self._fill_template(template_string, variables)
    
    def build_default_prompt(self, stage: str, **variables) -> str:
        """
        Build a default prompt for a specific evolution stage.
        
        Args:
            stage: The evolution stage (e.g., "initial_optimization", "code_review")
            **variables: Variables to fill in the template
            
        Returns:
            A prompt string
        """
        # Get default template for the stage
        template_id = self._get_default_template_id(stage)
        
        # Build prompt using the template
        return self.build(template_id, **variables)
    
    def _process_special_variables(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process special variables that require additional handling.
        
        Args:
            variables: Dictionary of variables
            
        Returns:
            Processed dictionary of variables
        """
        processed_variables = variables.copy()
        
        # Process residue if available
        if "residue" in processed_variables and processed_variables["residue"]:
            # Format residue for inclusion in the prompt
            residue_patterns = self._format_residue(processed_variables["residue"])
            processed_variables["residue_patterns"] = residue_patterns
        
        # Process previous reflections if available
        if "previous_reflections" in processed_variables and processed_variables["previous_reflections"]:
            # Format reflections for inclusion in the prompt
            reflection_summary = self._format_reflections(processed_variables["previous_reflections"])
            processed_variables["reflection_summary"] = reflection_summary
        
        # Process user guidance if available
        if "user_guidance" in processed_variables and processed_variables["user_guidance"]:
            # Format user guidance for inclusion in the prompt
            guidance_summary = self._format_user_guidance(processed_variables["user_guidance"])
            processed_variables["guidance_summary"] = guidance_summary
        
        return processed_variables
    
    def _fill_template(self, template: str, variables: Dict[str, Any]) -> str:
        """
        Fill a template with variables, handling conditional sections and undefined variables.
        
        Args:
            template: The template string
            variables: Dictionary of variables
            
        Returns:
            The filled template
        """
        # Handle conditional sections
        template = self._process_conditionals(template, variables)
        
        # Use string.Template for variable substitution
        try:
            template_obj = Template(template)
            result = template_obj.safe_substitute(variables)
            return result
        except Exception as e:
            logger.error(f"Error filling template: {e}")
            # Fallback: basic replacement
            for key, value in variables.items():
                if isinstance(value, str):
                    template = template.replace(f"${key}", value)
            return template
    
    def _process_conditionals(self, template: str, variables: Dict[str, Any]) -> str:
        """
        Process conditional sections in the template based on available variables.
        
        Args:
            template: The template string
            variables: Dictionary of variables
            
        Returns:
            The processed template with conditional sections handled
        """
        # Pattern for conditional sections: {{#if variable_name}}...{{/if}}
        pattern = r'{{#if ([^}]+)}}(.*?){{/if}}'
        
        # Function to handle each match
        def replace(match):
            condition = match.group(1).strip()
            content = match.group(2)
            
            # Check if condition is satisfied (variable exists and is truthy)
            if condition in variables and variables[condition]:
                return content
            else:
                return ''
        
        # Replace all conditional sections
        result = re.sub(pattern, replace, template, flags=re.DOTALL)
        return result
    
    def _format_residue(self, residue: List[Dict[str, Any]]) -> str:
        """
        Format residue patterns for inclusion in the prompt.
        
        Args:
            residue: List of residue pattern dictionaries
            
        Returns:
            A formatted string representing the residue patterns
        """
        if not residue:
            return ""
        
        # Group residue by type
        residue_by_type = {}
        for item in residue:
            residue_type = item.get("type", "unknown")
            if residue_type not in residue_by_type:
                residue_by_type[residue_type] = []
            residue_by_type[residue_type].append(item)
        
        # Format each type of residue
        formatted_residue = []
        for residue_type, items in residue_by_type.items():
            formatted_residue.append(f"### {residue_type.title()} Patterns")
            for item in items:
                pattern = item.get("pattern", "")
                value = item.get("potential_value", "")
                formatted_residue.append(f"- **Pattern**: {pattern}")
                if value:
                    formatted_residue.append(f"  **Potential Value**: {value}")
            formatted_residue.append("")
        
        return "\n".join(formatted_residue)
    
    def _format_reflections(self, reflections: List[Dict[str, Any]]) -> str:
        """
        Format reflections for inclusion in the prompt.
        
        Args:
            reflections: List of reflection dictionaries
            
        Returns:
            A formatted string representing the reflections
        """
        if not reflections:
            return ""
        
        formatted_reflections = ["### Previous Reflections"]
        for reflection in reflections:
            stage = reflection.get("stage", "")
            agent = reflection.get("agent", "")
            content = reflection.get("content", "")
            
            if stage and agent:
                formatted_reflections.append(f"#### {stage.title()} (by {agent})")
            elif stage:
                formatted_reflections.append(f"#### {stage.title()}")
            elif agent:
                formatted_reflections.append(f"#### Reflection by {agent}")
            else:
                formatted_reflections.append("#### Reflection")
            
            # Extract key insights from the content
            if content:
                # Try to find key insights or summary section
                insights_match = re.search(r'(?:key insights|summary):\s*(.*?)(?:\n\n|\Z)', content, re.IGNORECASE | re.DOTALL)
                if insights_match:
                    insights = insights_match.group(1).strip()
                    formatted_reflections.append(insights)
                else:
                    # Use the first paragraph as a summary
                    summary = content.split('\n\n')[0].strip()
                    formatted_reflections.append(summary)
            
            formatted_reflections.append("")
        
        return "\n".join(formatted_reflections)
    
    def _format_user_guidance(self, guidance_history: List[Dict[str, Any]]) -> str:
        """
        Format user guidance for inclusion in the prompt.
        
        Args:
            guidance_history: List of guidance dictionaries
            
        Returns:
            A formatted string representing the user guidance
        """
        if not guidance_history:
            return ""
        
        formatted_guidance = ["### User Guidance"]
        
        # Use only the most recent guidance entries (limit to last 3)
        recent_guidance = guidance_history[-3:]
        
        for entry in recent_guidance:
            timestamp = entry.get("timestamp", "")
            guidance = entry.get("guidance", "")
            
            if timestamp:
                formatted_guidance.append(f"**At {timestamp}**: {guidance}")
            else:
                formatted_guidance.append(f"**Guidance**: {guidance}")
        
        return "\n".join(formatted_guidance)
    
    def _get_default_template_id(self, stage: str) -> str:
        """
        Get the default template ID for a specific evolution stage.
        
        Args:
            stage: The evolution stage
            
        Returns:
            The default template ID for the stage
        """
        # Map stages to default templates
        stage_templates = {
            "initial_optimization": "code_optimization_initial",
            "code_review": "code_review_standard",
            "edge_case_testing": "edge_case_analysis",
            "final_synthesis": "final_synthesis_standard",
            "iteration_1": "evolution_iteration_first",
            "iteration_2": "evolution_iteration_middle",
            "iteration_3": "evolution_iteration_middle",
            "iteration_4": "evolution_iteration_middle",
            "iteration_5": "evolution_iteration_final"
        }
        
        # Return the template ID for the stage, or a generic template if not found
        return stage_templates.get(stage, "generic_evolution")
    
    def build_recursive_prompt(self, depth: int, context: Dict[str, Any]) -> str:
        """
        Build a recursive prompt that implements multi-layer reasoning.
        
        This special prompt construction method creates a prompt with explicit recursive 
        reasoning instructions, where each recursion depth addresses different aspects
        of the evolution task.
        
        Args:
            depth: The maximum recursion depth
            context: The evolution context
            
        Returns:
            A recursive prompt string
        """
        # Base template
        base_template = """
# Recursive Evolution Task

You are tasked with evolving the following code through recursive optimization:

```{language}
{code}
```

## Evolution Goal
{goal}

## Recursive Reasoning Process

I want you to think through this evolution task recursively, with each layer addressing 
different aspects of the optimization process. Follow these {depth} reasoning layers:

{recursive_layers}

## Final Output

After completing all reasoning layers, provide your final evolved solution in the following format:

```{language}
// Evolved solution
// Time Complexity: O(?)
// Space Complexity: O(?)

[Your evolved code here]
```

Then provide a brief summary of how your solution addresses the evolution goal and the key insights 
from your recursive reasoning process.
        """
        
        # Define recursive layer templates based on depth
        layer_templates = [
            "### Layer 1: Problem Analysis\nAnalyze the current implementation, identifying its purpose, algorithm type, and current performance characteristics (time complexity, space complexity, efficiency bottlenecks).",
            "### Layer 2: Solution Strategy\nDevelop a high-level optimization strategy. What approaches, algorithms, or techniques would address the identified bottlenecks while preserving correctness?",
            "### Layer 3: Implementation Planning\nPlan the specific implementation changes required. How will you restructure the code to implement your optimization strategy?",
            "### Layer 4: Edge Case Analysis\nIdentify potential edge cases and failure modes in your planned implementation. How will you ensure robustness in these scenarios?",
            "### Layer 5: Optimization Refinement\nRefine your optimization approach based on the identified edge cases. Are there further optimizations or simplifications possible?",
            "### Layer 6: Code Generation\nImplement your optimized solution, ensuring clarity, correctness, and performance improvements.",
            "### Layer 7: Verification & Validation\nVerify that your implementation correctly addresses the original requirements and achieves the desired performance improvements.",
            "### Layer 8: Meta-Reflection\nReflect on the evolution process itself. What patterns, insights, or principles emerged that could be applied to similar optimization tasks?"
        ]
        
        # Include layers up to the specified depth
        actual_depth = min(depth, len(layer_templates))
        selected_layers = layer_templates[:actual_depth]
        recursive_layers = "\n\n".join(selected_layers)
        
        # Build the prompt
        variables = {
            "depth": actual_depth,
            "recursive_layers": recursive_layers,
            **context
        }
        
        return self._fill_template(base_template, variables)
    
    def build_symbolic_residue_prompt(self, context: Dict[str, Any]) -> str:
        """
        Build a prompt that explicitly focuses on leveraging symbolic residue
        from past evolution attempts.
        
        This method creates a prompt that instructs the AI agent to utilize patterns
        from past failures and near-misses to guide the current evolution.
        
        Args:
            context: The evolution context, including residue patterns
            
        Returns:
            A symbolic residue-focused prompt string
        """
        # Get relevant residue for the context
        code = context.get("code", "")
        goal = context.get("goal", "")
        domain = context.get("domain", "general")
        
        residue = ResidueRegistry.get_relevant(code, goal, domain)
        
        # Format residue for the prompt
        residue_patterns = self._format_residue(residue) if residue else ""
        
        # Add residue to context
        enhanced_context = {
            **context,
            "residue_patterns": residue_patterns
        }
        
        # Template with focus on residue utilization
        template = """
# Evolution with Symbolic Residue Utilization

You are tasked with evolving the following code:

```{language}
{code}
```

## Evolution Goal
{goal}

{{#if residue_patterns}}
## Symbolic Residue Patterns
The following patterns represent valuable insights from past evolution attempts.
These include near-misses, innovative fragments, and common failure modes that
can guide your approach:

{residue_patterns}

Your task is to leverage these patterns to inform your evolution strategy. Pay
special attention to:
1. Avoiding known failure modes
2. Incorporating promising innovative fragments
3. Learning from near-miss approaches
{{/if}}

## Your Task
1. Analyze the current implementation and its limitations
2. Develop an optimization strategy that incorporates insights from symbolic residue
3. Implement your evolved solution
4. Explain how your solution addresses the goal and utilizes the residue patterns

## Output Format
Provide your solution in the following format:

```{language}
// Evolved solution

[Your evolved code here]
```

Then explain:
1. How your solution addresses the evolution goal
2. Which symbolic residue patterns influenced your approach
3. How you avoided known failure modes
4. Any new patterns or insights that emerged during this evolution
        """
        
        return self._fill_template(template, enhanced_context)
    
    def build_coherence_focused_prompt(self, context: Dict[str, Any]) -> str:
        """
        Build a prompt that focuses on maintaining coherence during evolution.
        
        This method creates a prompt that guides the AI agent to maintain
        structural coherence while making evolutionary changes.
        
        Args:
            context: The evolution context
            
        Returns:
            A coherence-focused prompt string
        """
        template = """
# Evolution with Coherence Focus

You are tasked with evolving the following code while maintaining coherence:

```{language}
{code}
```

## Evolution Goal
{goal}

## Coherence Guidelines
Coherence in evolution means maintaining the essential structure and meaning of the code
while improving its performance or functionality. This includes:

1. **Logical Coherence**: Preserve the logical flow and intent of the algorithm
2. **Structural Coherence**: Maintain appropriate abstractions and code organization
3. **Functional Coherence**: Ensure all functionality is preserved during optimization
4. **Style Coherence**: Keep consistent coding style and naming conventions
5. **Comment Coherence**: Update comments to reflect changes while preserving explanatory value

## Your Task
1. Analyze the current implementation to understand its structure and intent
2. Identify optimization opportunities that preserve coherence
3. Implement changes in a way that maintains logical and structural integrity
4. Ensure the evolved solution preserves all functionality of the original
5. Update comments and documentation to reflect changes

## Output Format
Provide your solution in the following format:

```{language}
// Evolved solution

[Your evolved code here]
```

Then explain:
1. How your solution addresses the evolution goal
2. How you maintained coherence during the evolution
3. Any trade-offs you made between optimization and coherence
        """
        
        return self._fill_template(template, context)
