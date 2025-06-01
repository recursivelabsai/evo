"""
DialogueManager - Core component for managing conversation flow in EvoChat.

This module provides the DialogueManager class, which orchestrates the conversation flow
between the user and the evolutionary system. It tracks conversation state, processes
user inputs, coordinates with NLU components, and generates appropriate responses.
"""

import logging
import uuid
from typing import Dict, List, Any, Optional, Union, Callable, Tuple
from datetime import datetime

from evochat.dialogue.state_tracker import StateTracker
from evochat.nlu.intent_detector import IntentDetector
from evochat.nlu.entity_extractor import EntityExtractor
from evochat.nlu.context_analyzer import ContextAnalyzer
from evoops.orchestrator.engine import Engine
from evointel.blueprints import BlueprintRegistry


# Configure logging
logger = logging.getLogger(__name__)


class DialogueManager:
    """
    Core component for managing conversation flow in EvoChat.
    
    The DialogueManager orchestrates the entire conversation flow, tracking state,
    processing user inputs, and generating appropriate responses. It acts as the
    central hub connecting various components of the EvoChat system, including NLU,
    orchestration, and interface components.
    """
    
    def __init__(self, orchestrator: Optional[Engine] = None):
        """
        Initialize the DialogueManager.
        
        Args:
            orchestrator: Optional orchestration engine to use for evolution tasks
        """
        self.state_tracker = StateTracker()
        self.intent_detector = IntentDetector()
        self.entity_extractor = EntityExtractor()
        self.context_analyzer = ContextAnalyzer()
        self.orchestrator = orchestrator or Engine()
        
        # Initialize response templates
        self._init_response_templates()
        
        # Initialize wizard registry
        self.active_wizards = {}
    
    async def process_message(self, user_id: str, message: str) -> Dict[str, Any]:
        """
        Process an incoming user message and generate a response.
        
        This is the main entry point for handling user messages. It performs intent
        detection, entity extraction, context analysis, state tracking, and response
        generation in a single cohesive flow.
        
        Args:
            user_id: Unique identifier for the user
            message: The user's message text
            
        Returns:
            A response object containing:
            - text: The response text
            - state: The updated conversation state
            - actions: Any actions to be performed (e.g., start evolution, show results)
            - meta: Additional metadata for the interface
        """
        # Initialize response object
        response = {
            "text": "",
            "state": {},
            "actions": [],
            "meta": {}
        }
        
        # Get current state
        state = self.state_tracker.get_state(user_id)
        
        # Check if a wizard is active for this user
        if user_id in self.active_wizards:
            # Let the wizard process the message
            wizard_response = await self._process_wizard_message(user_id, message, state)
            if wizard_response:
                return wizard_response
        
        # Get conversation context
        context = self.state_tracker.get_context(user_id)
        
        # Detect intent
        intent = self.intent_detector.detect(message, context)
        logger.info(f"Detected intent: {intent}")
        
        # Extract entities
        entities = self.entity_extractor.extract(message, intent, context)
        logger.info(f"Extracted entities: {entities}")
        
        # Analyze context
        context_analysis = self.context_analyzer.analyze(message, intent, entities, context)
        logger.info(f"Context analysis: {context_analysis}")
        
        # Update state with new information
        state.update({
            "last_intent": intent,
            "entities": entities,
            "last_message": message,
            "last_updated": datetime.now().isoformat(),
            "context_analysis": context_analysis
        })
        
        # Process the intent
        processed_response = await self._process_intent(user_id, intent, entities, state)
        response.update(processed_response)
        
        # Update state
        self.state_tracker.update_state(user_id, state)
        response["state"] = state
        
        return response
    
    async def _process_intent(
        self, 
        user_id: str, 
        intent: str, 
        entities: Dict[str, Any], 
        state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process a detected intent and generate an appropriate response.
        
        Args:
            user_id: Unique identifier for the user
            intent: The detected intent
            entities: Extracted entities
            state: Current conversation state
            
        Returns:
            A response object
        """
        # Initialize response
        response = {
            "text": "",
            "actions": [],
            "meta": {}
        }
        
        # Process different intents
        if intent == "greeting":
            response["text"] = self._get_template("greeting")
            
        elif intent == "help":
            response["text"] = self._get_template("help")
            
        elif intent == "evolve_code":
            # Start the evolution wizard
            from evochat.wizards.evolution_wizard import EvolutionWizard
            wizard = EvolutionWizard(self.orchestrator)
            self.active_wizards[user_id] = wizard
            
            # Get initial wizard response
            wizard_response = await wizard.start()
            response.update(wizard_response)
            
        elif intent == "evolve_prompt":
            # Start the prompt evolution wizard
            from evochat.wizards.evolution_wizard import EvolutionWizard
            wizard = EvolutionWizard(self.orchestrator, artifact_type="prompt")
            self.active_wizards[user_id] = wizard
            
            # Get initial wizard response
            wizard_response = await wizard.start()
            response.update(wizard_response)
            
        elif intent == "blueprint_info":
            # Check if a specific blueprint was mentioned
            blueprint_id = entities.get("blueprint_id")
            if blueprint_id:
                response.update(await self._get_blueprint_info(blueprint_id))
            else:
                response["text"] = self._get_template("blueprint_list_intro")
                response["actions"].append({
                    "type": "list_blueprints",
                    "data": await self._get_blueprint_list()
                })
                
        elif intent == "task_status":
            # Check if a specific task was mentioned
            task_id = entities.get("task_id")
            if task_id:
                response.update(await self._get_task_status(task_id))
            else:
                # Check if there's a recent task in the state
                recent_task = state.get("recent_task_id")
                if recent_task:
                    response.update(await self._get_task_status(recent_task))
                else:
                    response["text"] = self._get_template("task_id_missing")
                    
        elif intent == "provide_feedback":
            # Start the feedback wizard
            from evochat.wizards.feedback_wizard import FeedbackWizard
            
            # Check if a task ID was provided
            task_id = entities.get("task_id") or state.get("recent_task_id")
            if not task_id:
                response["text"] = self._get_template("feedback_task_missing")
                return response
                
            wizard = FeedbackWizard(self.orchestrator, task_id)
            self.active_wizards[user_id] = wizard
            
            # Get initial wizard response
            wizard_response = await wizard.start()
            response.update(wizard_response)
            
        elif intent == "cancel":
            # Check if there's an active wizard
            if user_id in self.active_wizards:
                # Get cancellation response from wizard
                wizard = self.active_wizards[user_id]
                cancellation_response = wizard.cancel()
                
                # Remove the wizard
                del self.active_wizards[user_id]
                
                response.update(cancellation_response)
            else:
                response["text"] = self._get_template("cancel_nothing")
                
        else:
            # Default response for unknown intent
            response["text"] = self._get_template("unknown_intent")
        
        return response
    
    async def _process_wizard_message(
        self, 
        user_id: str, 
        message: str, 
        state: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Process a message in the context of an active wizard.
        
        Args:
            user_id: Unique identifier for the user
            message: The user's message
            state: Current conversation state
            
        Returns:
            A response object if the wizard handled the message, None otherwise
        """
        wizard = self.active_wizards[user_id]
        
        # Check if the message is a command to exit the wizard
        if message.lower() in ["exit", "quit", "cancel"]:
            # Get cancellation response from wizard
            response = wizard.cancel()
            
            # Remove the wizard
            del self.active_wizards[user_id]
            
            return response
        
        # Process the message with the wizard
        wizard_response = await wizard.process_step(message, state)
        
        # Check if the wizard is complete
        if wizard.is_complete():
            # Remove the wizard
            del self.active_wizards[user_id]
            
            # Update state with wizard results
            state.update(wizard.get_results())
            self.state_tracker.update_state(user_id, state)
            
            # Include the updated state in the response
            wizard_response["state"] = state
        
        return wizard_response
    
    async def _get_blueprint_info(self, blueprint_id: str) -> Dict[str, Any]:
        """
        Get information about a specific blueprint.
        
        Args:
            blueprint_id: The ID of the blueprint
            
        Returns:
            A response object with blueprint information
        """
        blueprint = BlueprintRegistry.get(blueprint_id)
        
        if not blueprint:
            return {
                "text": self._get_template("blueprint_not_found").format(blueprint_id=blueprint_id),
                "actions": [],
                "meta": {}
            }
        
        # Get blueprint details
        blueprint_data = blueprint.to_dict()
        
        # Format response
        text = self._get_template("blueprint_info").format(
            name=blueprint_data["name"],
            description=blueprint_data["description"],
            version=blueprint_data["version"],
            author=blueprint_data["author"]
        )
        
        return {
            "text": text,
            "actions": [{
                "type": "display_blueprint",
                "data": blueprint_data
            }],
            "meta": {}
        }
    
    async def _get_blueprint_list(self) -> List[Dict[str, Any]]:
        """
        Get a list of available blueprints.
        
        Returns:
            A list of blueprint data objects
        """
        blueprints = BlueprintRegistry.list_all()
        
        # Format blueprint data
        blueprint_list = []
        for blueprint in blueprints:
            blueprint_list.append({
                "id": blueprint.id,
                "name": blueprint.name,
                "description": blueprint.description,
                "version": blueprint.version,
                "tags": blueprint.tags
            })
        
        return blueprint_list
    
    async def _get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of an evolution task.
        
        Args:
            task_id: The ID of the task
            
        Returns:
            A response object with task status information
        """
        try:
            # Get task status from orchestrator
            status = await self.orchestrator.get_task_status(task_id)
            
            # Format response based on status
            if status["status"] == "completed":
                text = self._get_template("task_completed").format(
                    task_id=task_id,
                    progress=status["progress"]
                )
                
                return {
                    "text": text,
                    "actions": [{
                        "type": "show_results",
                        "data": {"task_id": task_id}
                    }],
                    "meta": {}
                }
                
            elif status["status"] == "failed":
                text = self._get_template("task_failed").format(
                    task_id=task_id,
                    stage=status["stage"],
                    error=status.get("error", "Unknown error")
                )
                
                return {
                    "text": text,
                    "actions": [],
                    "meta": {}
                }
                
            else:  # In progress
                text = self._get_template("task_in_progress").format(
                    task_id=task_id,
                    status=status["status"],
                    stage=status["stage"],
                    progress=status["progress"]
                )
                
                return {
                    "text": text,
                    "actions": [{
                        "type": "show_progress",
                        "data": status
                    }],
                    "meta": {}
                }
                
        except Exception as e:
            logger.error(f"Error getting task status: {e}")
            
            text = self._get_template("task_status_error").format(
                task_id=task_id,
                error=str(e)
            )
            
            return {
                "text": text,
                "actions": [],
                "meta": {}
            }
    
    def _init_response_templates(self):
        """
        Initialize response templates.
        
        In a real implementation, these would be loaded from files or a database.
        """
        self.templates = {
            "greeting": "Hello! I'm EvoChat, your evolutionary AI assistant. I can help you evolve code, prompts, and other artifacts through AI-driven evolution. What would you like to evolve today?",
            
            "help": "I can help you with the following:\n\n"
                   "- Evolve code: I can optimize algorithms, refactor code, and improve performance\n"
                   "- Evolve prompts: I can enhance LLM prompts for better results\n"
                   "- Blueprint info: I can provide information about evolution blueprints\n"
                   "- Task status: I can check the status of ongoing evolution tasks\n"
                   "- Provide feedback: You can guide the evolution process with your feedback\n\n"
                   "Just let me know what you'd like to do!",
            
            "unknown_intent": "I'm not sure what you're asking for. You can ask me to evolve code, check task status, or get information about blueprints. Type 'help' for more options.",
            
            "blueprint_list_intro": "Here are the available evolution blueprints:",
            
            "blueprint_info": "**{name}** (v{version})\n\n"
                             "{description}\n\n"
                             "Created by: {author}",
            
            "blueprint_not_found": "I couldn't find a blueprint with ID '{blueprint_id}'. Type 'list blueprints' to see available blueprints.",
            
            "task_id_missing": "Please provide a task ID to check status. You can say something like 'check status of task ABC123'.",
            
            "task_completed": "Task {task_id} has completed successfully! The evolution process is 100% complete.",
            
            "task_failed": "Task {task_id} has failed at stage '{stage}'. Error: {error}",
            
            "task_in_progress": "Task {task_id} is currently {status} at stage '{stage}'. Progress: {progress}%",
            
            "task_status_error": "I encountered an error while checking the status of task {task_id}: {error}",
            
            "feedback_task_missing": "Please specify which evolution task you'd like to provide feedback for. You can say something like 'provide feedback for task ABC123'.",
            
            "cancel_nothing": "There's nothing active to cancel. You can start a new evolution task by saying something like 'evolve this code' or 'optimize this algorithm'."
        }
    
    def _get_template(self, template_name: str) -> str:
        """
        Get a response template by name.
        
        Args:
            template_name: The name of the template
            
        Returns:
            The template text, or a default message if not found
        """
        return self.templates.get(
            template_name, 
            "I'm not sure how to respond to that. Type 'help' for assistance."
        )
