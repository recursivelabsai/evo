"""
ClaudeAgent - Implementation of BaseAgent for Anthropic's Claude models.

This module provides a concrete implementation of the BaseAgent abstract class
for interacting with Anthropic's Claude models (Claude 3 Opus, Claude 3 Sonnet, etc.).
It handles API client initialization, request formatting, and response processing.
"""

import json
import logging
import asyncio
import time
from typing import Dict, List, Any, Optional, Union, Callable

from anthropic import AsyncAnthropic, APIStatusError, APITimeoutError, APIConnectionError
from anthropic.types import Message
from anthropic.types.completion import Completion

from evoops.agents.base_agent import BaseAgent


# Configure logging
logger = logging.getLogger(__name__)


class ClaudeAgent(BaseAgent):
    """
    Implementation of BaseAgent for Anthropic's Claude models.
    
    This class provides methods for generating responses from Claude models,
    streaming responses, and reflecting on text. It handles Claude-specific
    request formatting, token counting, and error handling.
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-opus-20240229",
        temperature: float = 0.7,
        max_tokens: int = 4000,
        top_p: float = 0.9,
        timeout: float = 60.0,
        retry_count: int = 3,
        retry_delay: float = 2.0,
        **kwargs
    ):
        """
        Initialize a ClaudeAgent.
        
        Args:
            api_key: Anthropic API key
            model: Claude model identifier (e.g., "claude-3-opus-20240229")
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            top_p: Nucleus sampling parameter (0.0 to 1.0)
            timeout: Timeout for API calls in seconds
            retry_count: Number of times to retry failed API calls
            retry_delay: Delay between retries in seconds
            **kwargs: Additional model-specific parameters
        """
        super().__init__(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            timeout=timeout,
            retry_count=retry_count,
            retry_delay=retry_delay,
            **kwargs
        )
    
    def _init_client(self):
        """
        Initialize the Anthropic API client.
        """
        self.client = AsyncAnthropic(api_key=self.api_key)
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from Claude.
        
        Args:
            prompt: The prompt to generate a response to
            **kwargs: Additional generation parameters
            
        Returns:
            The generated response text
            
        Raises:
            Exception: If generation fails
        """
        # Merge parameters
        params = self._merge_params(kwargs)
        
        # Extract Claude-specific parameters
        max_tokens = params.pop("max_tokens", self.max_tokens)
        system_prompt = params.pop("system_prompt", None)
        
        try:
            # Create message object
            messages = [{"role": "user", "content": prompt}]
            
            # Prepare request
            request = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": messages,
                "temperature": params.get("temperature", self.temperature),
                "top_p": params.get("top_p", self.top_p),
            }
            
            # Add system prompt if provided
            if system_prompt:
                request["system"] = system_prompt
            
            # Make request
            start_time = time.time()
            response: Message = await self.client.messages.create(**request)
            end_time = time.time()
            
            # Update telemetry
            self.telemetry["total_tokens_used"] += response.usage.input_tokens + response.usage.output_tokens
            self.telemetry["total_latency"] += (end_time - start_time)
            
            # Extract text from response
            return response.content[0].text
            
        except (APIStatusError, APITimeoutError, APIConnectionError) as e:
            logger.error(f"Claude API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error calling Claude API: {e}")
            raise
    
    async def stream(self, prompt: str, callback: Callable[[str], None], **kwargs):
        """
        Stream a response from Claude, calling the callback for each chunk.
        
        Args:
            prompt: The prompt to generate a response to
            callback: Function to call with each response chunk
            **kwargs: Additional generation parameters
            
        Raises:
            Exception: If streaming fails
        """
        # Merge parameters
        params = self._merge_params(kwargs)
        
        # Extract Claude-specific parameters
        max_tokens = params.pop("max_tokens", self.max_tokens)
        system_prompt = params.pop("system_prompt", None)
        
        try:
            # Create message object
            messages = [{"role": "user", "content": prompt}]
            
            # Prepare request
            request = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": messages,
                "temperature": params.get("temperature", self.temperature),
                "top_p": params.get("top_p", self.top_p),
                "stream": True
            }
            
            # Add system prompt if provided
            if system_prompt:
                request["system"] = system_prompt
            
            # Make streaming request
            start_time = time.time()
            input_tokens = 0
            output_tokens = 0
            
            async with self.client.messages.stream(**request) as stream:
                async for chunk in stream:
                    if chunk.usage:
                        input_tokens = chunk.usage.input_tokens
                        output_tokens = chunk.usage.output_tokens
                    
                    if chunk.delta.text:
                        callback(chunk.delta.text)
            
            end_time = time.time()
            
            # Update telemetry
            self.telemetry["total_tokens_used"] += input_tokens + output_tokens
            self.telemetry["total_latency"] += (end_time - start_time)
            
        except (APIStatusError, APITimeoutError, APIConnectionError) as e:
            logger.error(f"Claude API streaming error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error streaming from Claude API: {e}")
            raise
    
    async def reflect(self, text: str, **kwargs) -> Dict[str, Any]:
        """
        Generate a reflection on a text using Claude.
        
        This method prompts Claude to analyze the given text and provide structured feedback.
        
        Args:
            text: The text to reflect on
            **kwargs: Additional reflection parameters
            
        Returns:
            A dictionary containing reflection results
            
        Raises:
            Exception: If reflection fails
        """
        # Build reflection prompt
        reflection_type = kwargs.get("reflection_type", "general")
        
        # Get prompt template based on reflection type
        prompt_template = self._get_reflection_prompt_template(reflection_type)
        
        # Fill in the template
        prompt = prompt_template.format(text=text)
        
        # Add formatting instructions for JSON output
        prompt += "\nProvide your reflection as a JSON object with appropriate fields for your analysis."
        
        try:
            # Generate response
            response = await self.generate(prompt, **kwargs)
            
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                try:
                    reflection = json.loads(json_str)
                    return reflection
                except json.JSONDecodeError:
                    logger.warning("Failed to parse JSON from reflection response")
            
            # Fallback if JSON parsing fails: return the whole response
            return {"raw_reflection": response}
            
        except Exception as e:
            logger.error(f"Error generating reflection: {e}")
            raise
    
    def _get_reflection_prompt_template(self, reflection_type: str) -> str:
        """
        Get a prompt template for a specific type of reflection.
        
        Args:
            reflection_type: The type of reflection to generate
            
        Returns:
            A prompt template string
        """
        templates = {
            "general": """
                Please analyze the following text and provide a structured reflection:
                
                ```
                {text}
                ```
                
                In your reflection, please consider:
                1. Overall quality and coherence
                2. Key strengths and weaknesses
                3. Suggestions for improvement
                4. Any notable patterns or characteristics
            """,
            
            "code": """
                Please analyze the following code and provide a structured reflection:
                
                ```
                {text}
                ```
                
                In your reflection, please consider:
                1. Code quality and readability
                2. Potential bugs or edge cases
                3. Performance characteristics
                4. Suggestions for optimization
                5. Overall architecture and design
            """,
            
            "algorithm": """
                Please analyze the following algorithm implementation and provide a structured reflection:
                
                ```
                {text}
                ```
                
                In your reflection, please consider:
                1. Time complexity (Big O notation)
                2. Space complexity (Big O notation)
                3. Correctness and edge case handling
                4. Optimization opportunities
                5. Alternative approaches that might be more efficient
            """,
            
            "prompt": """
                Please analyze the following prompt and provide a structured reflection:
                
                ```
                {text}
                ```
                
                In your reflection, please consider:
                1. Clarity and specificity
                2. Potential ambiguities or inconsistencies
                3. Effectiveness for its intended purpose
                4. Suggestions for improvement
                5. Potential failure modes or limitations
            """
        }
        
        # Return the requested template or fall back to general
        return templates.get(reflection_type, templates["general"])
    
    @staticmethod
    def count_tokens(text: str) -> int:
        """
        Count the number of tokens in a text using Anthropic's tokenizer.
        
        Note: This is a rough approximation, as we don't have direct access to Anthropic's tokenizer.
        
        Args:
            text: The text to count tokens for
            
        Returns:
            An estimated token count
        """
        # Rough approximation: 1 token ≈ 4 characters for English text
        return len(text) // 4
