"""
AI Module for TarotMac

This module provides AI functionality including Ollama integration,
chat memory management, model configuration, and tarot-specific AI features.

Classes:
    AIManager: Main AI manager integrating all functionality
    OllamaClient: Client for Ollama LLM integration
    ChatMemoryManager: Manages chat sessions and memory
    ModelConfigManager: Manages model configurations and selection
    ChatSession: Represents a chat session with memory
    ChatMessage: Represents a single chat message
    ModelConfig: Configuration for a specific model

Enums:
    ModelSize: Enumeration of model sizes
    ModelPurpose: Enumeration of model purposes
"""

from .ai_manager import AIManager
from .ollama_client import OllamaClient, InfluencedReadingResponse
from .chat_memory import ChatMemoryManager, ChatSession, ChatMessage
from .model_config import ModelConfigManager, ModelConfig, ModelSize, ModelPurpose

__all__ = [
    'AIManager',
    'OllamaClient',
    'InfluencedReadingResponse',
    'ChatMemoryManager',
    'ChatSession',
    'ChatMessage',
    'ModelConfigManager',
    'ModelConfig',
    'ModelSize',
    'ModelPurpose'
]