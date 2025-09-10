"""
AI Manager for TarotMac

This module provides the main interface for AI functionality,
integrating Ollama client, chat memory, and model configuration.
"""

import asyncio
from typing import Dict, List, Any, Optional, AsyncGenerator, Tuple
from datetime import datetime
import logging

from .ollama_client import OllamaClient, InfluencedReadingResponse
from .chat_memory import ChatMemoryManager, ChatSession, ChatMessage
from .model_config import ModelConfigManager, ModelConfig, ModelPurpose

logger = logging.getLogger(__name__)


class AIManager:
    """Main AI manager integrating all AI functionality."""
    
    def __init__(self, host: str = "localhost", port: int = 11434):
        """
        Initialize the AI manager.
        
        Args:
            host: Ollama server host
            port: Ollama server port
        """
        self.host = host
        self.port = port
        self.ollama_client: Optional[OllamaClient] = None
        self.memory_manager = ChatMemoryManager()
        self.model_manager = ModelConfigManager()
        self.is_connected = False
        self.connection_checked = False
    
    async def initialize(self) -> bool:
        """Initialize the AI manager and check connection."""
        try:
            # Get current model
            current_model = self.model_manager.get_current_model()
            if not current_model:
                # Set default model
                default_model = self.model_manager.get_recommended_models(ModelPurpose.GENERAL)[0]
                self.model_manager.set_current_model(default_model.name)
                current_model = default_model
            
            # Initialize Ollama client
            self.ollama_client = OllamaClient(
                model=current_model.name,
                host=self.host,
                port=self.port
            )
            
            # Check connection
            self.is_connected = await self.ollama_client.check_connection()
            self.connection_checked = True
            
            if not self.is_connected:
                logger.warning("Ollama connection failed, AI features will be limited")
            
            return True
            
        except Exception as e:
            logger.error(f"Error initializing AI manager: {e}")
            self.is_connected = False
            self.connection_checked = True
            return False
    
    async def check_connection(self) -> bool:
        """Check connection to Ollama server."""
        if not self.ollama_client:
            return False
        
        try:
            self.is_connected = await self.ollama_client.check_connection()
            return self.is_connected
        except Exception as e:
            logger.error(f"Connection check failed: {e}")
            self.is_connected = False
            return False
    
    async def get_available_models(self) -> List[str]:
        """Get list of available Ollama models."""
        if not self.ollama_client:
            return []
        
        try:
            return await self.ollama_client.get_available_models()
        except Exception as e:
            logger.error(f"Error getting available models: {e}")
            return []
    
    async def update_model_availability(self) -> None:
        """Update model availability based on Ollama server."""
        if not self.ollama_client:
            return
        
        try:
            available_models = await self.get_available_models()
            
            # Update all models
            for model_name in self.model_manager.models:
                is_available = model_name in available_models
                self.model_manager.update_model_availability(model_name, is_available)
            
            # Update custom models
            for model_name in self.model_manager.custom_configs:
                is_available = model_name in available_models
                self.model_manager.update_model_availability(model_name, is_available)
                
        except Exception as e:
            logger.error(f"Error updating model availability: {e}")
    
    async def set_model(self, model_name: str) -> bool:
        """Set the current AI model."""
        try:
            # Check if model is available
            available_models = await self.get_available_models()
            if model_name not in available_models:
                logger.warning(f"Model {model_name} not available on Ollama server")
                return False
            
            # Update model manager
            if not self.model_manager.set_current_model(model_name):
                logger.error(f"Model {model_name} not found in configuration")
                return False
            
            # Update Ollama client
            self.ollama_client.model = model_name
            self.model_manager.update_model_availability(model_name, True)
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting model: {e}")
            return False
    
    def get_current_model(self) -> Optional[ModelConfig]:
        """Get current model configuration."""
        return self.model_manager.get_current_model()
    
    def get_model_recommendations(self, use_case: str) -> List[ModelConfig]:
        """Get model recommendations for specific use cases."""
        return self.model_manager.get_model_recommendations(use_case)
    
    # Chat Memory Management
    
    def create_chat_session(self, title: str = "", context: Optional[Dict[str, Any]] = None) -> ChatSession:
        """Create a new chat session."""
        return self.memory_manager.create_session(title, context)
    
    def get_current_session(self) -> Optional[ChatSession]:
        """Get current chat session."""
        return self.memory_manager.get_current_session()
    
    def set_current_session(self, session_id: str) -> bool:
        """Set current chat session."""
        return self.memory_manager.set_current_session(session_id)
    
    def list_sessions(self, include_inactive: bool = False) -> List[ChatSession]:
        """List chat sessions."""
        return self.memory_manager.list_sessions(include_inactive)
    
    def end_session(self, session_id: Optional[str] = None) -> bool:
        """End a chat session."""
        return self.memory_manager.end_session(session_id)
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a chat session."""
        return self.memory_manager.delete_session(session_id)
    
    # Chat Functionality
    
    async def chat_stream(self, message: str, 
                         session_id: Optional[str] = None,
                         context: Optional[Dict[str, Any]] = None) -> AsyncGenerator[str, None]:
        """Stream chat response."""
        if not self.is_connected or not self.ollama_client:
            yield "AI service is currently unavailable. Please check your Ollama connection."
            return
        
        try:
            # Add user message to session
            self.memory_manager.add_message("user", message, session_id)
            
            # Get conversation context
            messages, session_context = self.memory_manager.get_conversation_context(session_id)
            
            # Merge contexts
            merged_context = session_context.copy()
            if context:
                merged_context.update(context)
            
            # Stream response
            response_chunks = []
            async for chunk in self.ollama_client.chat_stream(messages, merged_context):
                response_chunks.append(chunk)
                yield chunk
            
            # Add assistant response to session
            full_response = "".join(response_chunks)
            self.memory_manager.add_message("assistant", full_response, session_id)
            
        except Exception as e:
            logger.error(f"Error in chat stream: {e}")
            yield "I'm sorry, I encountered an error. Please try again."
    
    async def chat(self, message: str, 
                   session_id: Optional[str] = None,
                   context: Optional[Dict[str, Any]] = None) -> str:
        """Get complete chat response."""
        if not self.is_connected or not self.ollama_client:
            return "AI service is currently unavailable. Please check your Ollama connection."
        
        try:
            # Add user message to session
            self.memory_manager.add_message("user", message, session_id)
            
            # Get conversation context
            messages, session_context = self.memory_manager.get_conversation_context(session_id)
            
            # Merge contexts
            merged_context = session_context.copy()
            if context:
                merged_context.update(context)
            
            # Get response
            response = await self.ollama_client.chat(messages, merged_context)
            
            # Add assistant response to session
            self.memory_manager.add_message("assistant", response, session_id)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return "I'm sorry, I encountered an error. Please try again."
    
    # Tarot-Specific AI Features
    
    async def generate_influenced_reading(self, reading_context: Dict[str, Any]) -> InfluencedReadingResponse:
        """Generate influenced reading interpretation."""
        if not self.is_connected or not self.ollama_client:
            return self.ollama_client._create_fallback_response(reading_context)
        
        try:
            return await self.ollama_client.generate_influenced_meanings(reading_context)
        except Exception as e:
            logger.error(f"Error generating influenced reading: {e}")
            return self.ollama_client._create_fallback_response(reading_context)
    
    async def chat_about_reading(self, reading_data: Dict[str, Any], 
                               question: str = "Tell me about this reading") -> str:
        """Chat about a specific reading."""
        context = {
            "reading": reading_data,
            "type": "reading_discussion"
        }
        
        return await self.chat(question, context=context)
    
    async def chat_about_card(self, card_data: Dict[str, Any], 
                            question: str = "Tell me about this card") -> str:
        """Chat about a specific card."""
        context = {
            "card": card_data,
            "type": "card_discussion"
        }
        
        return await self.chat(question, context=context)
    
    # Utility Methods
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory manager statistics."""
        return self.memory_manager.get_statistics()
    
    def get_model_stats(self) -> Dict[str, Any]:
        """Get model manager statistics."""
        return self.model_manager.get_model_stats()
    
    def cleanup_old_messages(self, keep_recent: int = 20) -> int:
        """Cleanup old messages in all sessions."""
        return self.memory_manager.cleanup_old_messages(keep_recent=keep_recent)
    
    def export_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Export a chat session."""
        return self.memory_manager.export_session(session_id)
    
    def import_session(self, session_data: Dict[str, Any]) -> Optional[ChatSession]:
        """Import a chat session."""
        return self.memory_manager.import_session(session_data)
    
    def get_status(self) -> Dict[str, Any]:
        """Get overall AI manager status."""
        return {
            "is_connected": self.is_connected,
            "connection_checked": self.connection_checked,
            "current_model": self.get_current_model().name if self.get_current_model() else None,
            "memory_stats": self.get_memory_stats(),
            "model_stats": self.get_model_stats()
        }