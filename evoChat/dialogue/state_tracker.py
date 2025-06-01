"""
StateTracker - Component for maintaining conversation state across interactions.

This module provides the StateTracker class, which manages and persists conversation
state for users interacting with EvoChat. It handles state initialization, updates,
context management, and persistence across sessions.
"""

import logging
import json
import os
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import uuid


# Configure logging
logger = logging.getLogger(__name__)


class StateTracker:
    """
    Component for maintaining conversation state across interactions.
    
    The StateTracker manages conversation state for users, including:
    - User information and preferences
    - Conversation history and context
    - Active tasks and their status
    - Session information and persistence
    
    It provides methods for initializing, updating, retrieving, and persisting state.
    """
    
    def __init__(self, persistence_dir: Optional[str] = None):
        """
        Initialize the StateTracker.
        
        Args:
            persistence_dir: Optional directory for persisting state to disk
        """
        self.states = {}  # In-memory state storage
        self.persistence_dir = persistence_dir
        
        # Create persistence directory if specified and doesn't exist
        if self.persistence_dir and not os.path.exists(self.persistence_dir):
            os.makedirs(self.persistence_dir)
    
    def get_state(self, user_id: str) -> Dict[str, Any]:
        """
        Get the current state for a user.
        
        If the user doesn't have a state yet, a new one is initialized.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            The user's current state
        """
        # Check if user state exists in memory
        if user_id not in self.states:
            # Try to load from disk if persistence is enabled
            if self.persistence_dir:
                loaded_state = self._load_state_from_disk(user_id)
                if loaded_state:
                    self.states[user_id] = loaded_state
                    return self.states[user_id]
            
            # Initialize new state
            self.states[user_id] = self._initialize_state(user_id)
        
        return self.states[user_id]
    
    def update_state(self, user_id: str, state: Dict[str, Any]) -> None:
        """
        Update the state for a user.
        
        Args:
            user_id: Unique identifier for the user
            state: The new state to set
        """
        # Update state in memory
        self.states[user_id] = state
        
        # Update session info
        state["session"]["last_activity"] = datetime.now().isoformat()
        state["session"]["interaction_count"] += 1
        
        # Persist to disk if enabled
        if self.persistence_dir:
            self._persist_state_to_disk(user_id, state)
    
    def get_context(self, user_id: str) -> Dict[str, Any]:
        """
        Get the conversation context for a user.
        
        The context is a subset of the state that includes information relevant
        for intent detection, entity extraction, and response generation.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            The user's conversation context
        """
        state = self.get_state(user_id)
        
        # Extract relevant context from state
        context = {
            "recent_messages": state.get("recent_messages", []),
            "last_intent": state.get("last_intent"),
            "recent_intents": state.get("recent_intents", []),
            "entities": state.get("entities", {}),
            "preferences": state.get("preferences", {}),
            "active_task": state.get("active_task"),
            "recent_task_id": state.get("recent_task_id"),
            "ongoing_evolution": state.get("ongoing_evolution"),
            "session": state.get("session", {})
        }
        
        return context
    
    def clear_state(self, user_id: str) -> None:
        """
        Clear the state for a user.
        
        Args:
            user_id: Unique identifier for the user
        """
        if user_id in self.states:
            del self.states[user_id]
        
        # Remove persisted state if enabled
        if self.persistence_dir:
            file_path = os.path.join(self.persistence_dir, f"{user_id}.json")
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    logger.error(f"Error removing persisted state for user {user_id}: {e}")
    
    def update_conversation_history(self, user_id: str, message: str, response: str) -> None:
        """
        Update the conversation history for a user.
        
        Args:
            user_id: Unique identifier for the user
            message: The user's message
            response: The system's response
        """
        state = self.get_state(user_id)
        
        # Initialize conversation history if it doesn't exist
        if "conversation_history" not in state:
            state["conversation_history"] = []
        
        # Initialize recent messages if they don't exist
        if "recent_messages" not in state:
            state["recent_messages"] = []
        
        # Add message and response to history
        timestamp = datetime.now().isoformat()
        history_entry = {
            "timestamp": timestamp,
            "user_message": message,
            "system_response": response
        }
        
        state["conversation_history"].append(history_entry)
        
        # Update recent messages (keep last 10)
        state["recent_messages"].append({"role": "user", "content": message, "timestamp": timestamp})
        state["recent_messages"].append({"role": "system", "content": response, "timestamp": timestamp})
        state["recent_messages"] = state["recent_messages"][-10:]
        
        # Update state
        self.update_state(user_id, state)
    
    def track_intent(self, user_id: str, intent: str) -> None:
        """
        Track an intent for a user.
        
        Args:
            user_id: Unique identifier for the user
            intent: The detected intent
        """
        state = self.get_state(user_id)
        
        # Update last intent
        state["last_intent"] = intent
        
        # Initialize recent intents if they don't exist
        if "recent_intents" not in state:
            state["recent_intents"] = []
        
        # Add intent to recent intents (keep last 5)
        state["recent_intents"].append({
            "intent": intent,
            "timestamp": datetime.now().isoformat()
        })
        state["recent_intents"] = state["recent_intents"][-5:]
        
        # Update state
        self.update_state(user_id, state)
    
    def update_task_info(self, user_id: str, task_id: str, status: Dict[str, Any]) -> None:
        """
        Update task information for a user.
        
        Args:
            user_id: Unique identifier for the user
            task_id: The ID of the task
            status: The task status information
        """
        state = self.get_state(user_id)
        
        # Initialize tasks if they don't exist
        if "tasks" not in state:
            state["tasks"] = {}
        
        # Update task status
        state["tasks"][task_id] = {
            "status": status,
            "last_updated": datetime.now().isoformat()
        }
        
        # Update recent task ID
        state["recent_task_id"] = task_id
        
        # Update active task if the task is in progress
        if status.get("status") == "in_progress":
            state["active_task"] = task_id
        elif task_id == state.get("active_task"):
            # Clear active task if it's completed or failed
            state.pop("active_task", None)
        
        # Update state
        self.update_state(user_id, state)
    
    def set_preference(self, user_id: str, preference_name: str, preference_value: Any) -> None:
        """
        Set a preference for a user.
        
        Args:
            user_id: Unique identifier for the user
            preference_name: The name of the preference
            preference_value: The value of the preference
        """
        state = self.get_state(user_id)
        
        # Initialize preferences if they don't exist
        if "preferences" not in state:
            state["preferences"] = {}
        
        # Set preference
        state["preferences"][preference_name] = preference_value
        
        # Update state
        self.update_state(user_id, state)
    
    def _initialize_state(self, user_id: str) -> Dict[str, Any]:
        """
        Initialize a new state for a user.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            A new state dictionary
        """
        return {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "session": {
                "id": str(uuid.uuid4()),
                "started_at": datetime.now().isoformat(),
                "last_activity": datetime.now().isoformat(),
                "interaction_count": 0
            },
            "conversation_history": [],
            "recent_messages": [],
            "recent_intents": [],
            "tasks": {},
            "preferences": {
                "language": "en",
                "expertise_level": "intermediate",
                "response_style": "balanced"
            }
        }
    
    def _persist_state_to_disk(self, user_id: str, state: Dict[str, Any]) -> None:
        """
        Persist a user's state to disk.
        
        Args:
            user_id: Unique identifier for the user
            state: The state to persist
        """
        if not self.persistence_dir:
            return
        
        file_path = os.path.join(self.persistence_dir, f"{user_id}.json")
        
        try:
            with open(file_path, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error(f"Error persisting state for user {user_id}: {e}")
    
    def _load_state_from_disk(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a user's state from disk.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            The loaded state, or None if it doesn't exist or can't be loaded
        """
        if not self.persistence_dir:
            return None
        
        file_path = os.path.join(self.persistence_dir, f"{user_id}.json")
        
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r') as f:
                state = json.load(f)
            return state
        except Exception as e:
            logger.error(f"Error loading state for user {user_id}: {e}")
            return None
