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
    
    def _format_residue(self, residue: List
