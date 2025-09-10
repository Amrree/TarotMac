"""
Unit tests for the AI Module

Tests all components of the AI module including Ollama client,
chat memory management, model configuration, and AI manager.
"""

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, List, Any

from ai.ai_manager import AIManager
from ai.ollama_client import OllamaClient, InfluencedReadingResponse
from ai.chat_memory import ChatMemoryManager, ChatSession, ChatMessage
from ai.model_config import ModelConfigManager, ModelConfig, ModelSize, ModelPurpose


class TestChatMessage:
    """Test ChatMessage functionality."""
    
    def test_chat_message_creation(self):
        """Test ChatMessage creation."""
        message = ChatMessage(
            role="user",
            content="Hello, world!",
            metadata={"test": "value"}
        )
        
        assert message.role == "user"
        assert message.content == "Hello, world!"
        assert message.metadata["test"] == "value"
        assert message.message_id is not None
        assert isinstance(message.timestamp, datetime)
    
    def test_chat_message_serialization(self):
        """Test ChatMessage serialization."""
        message = ChatMessage(
            role="assistant",
            content="Test response",
            metadata={"key": "value"}
        )
        
        data = message.to_dict()
        assert data["role"] == "assistant"
        assert data["content"] == "Test response"
        assert data["metadata"]["key"] == "value"
        assert "message_id" in data
        assert "timestamp" in data
    
    def test_chat_message_deserialization(self):
        """Test ChatMessage deserialization."""
        data = {
            "message_id": "test-id",
            "role": "user",
            "content": "Test message",
            "timestamp": "2024-01-01T12:00:00",
            "metadata": {"test": "value"}
        }
        
        message = ChatMessage.from_dict(data)
        assert message.message_id == "test-id"
        assert message.role == "user"
        assert message.content == "Test message"
        assert message.metadata["test"] == "value"


class TestChatSession:
    """Test ChatSession functionality."""
    
    def test_chat_session_creation(self):
        """Test ChatSession creation."""
        session = ChatSession(
            title="Test Session",
            context={"test": "value"}
        )
        
        assert session.title == "Test Session"
        assert session.context["test"] == "value"
        assert session.is_active is True
        assert len(session.messages) == 0
        assert session.session_id is not None
    
    def test_add_message(self):
        """Test adding messages to session."""
        session = ChatSession()
        
        message = session.add_message("user", "Hello!")
        assert len(session.messages) == 1
        assert message.role == "user"
        assert message.content == "Hello!"
        assert message in session.messages
    
    def test_get_recent_messages(self):
        """Test getting recent messages."""
        session = ChatSession()
        
        # Add multiple messages
        for i in range(5):
            session.add_message("user", f"Message {i}")
        
        recent = session.get_recent_messages(3)
        assert len(recent) == 3
        assert recent[0].content == "Message 2"
        assert recent[2].content == "Message 4"
    
    def test_get_messages_for_llm(self):
        """Test getting messages formatted for LLM."""
        session = ChatSession()
        
        session.add_message("user", "Hello")
        session.add_message("assistant", "Hi there!")
        
        messages = session.get_messages_for_llm()
        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "Hello"
        assert messages[1]["role"] == "assistant"
        assert messages[1]["content"] == "Hi there!"
    
    def test_clear_old_messages(self):
        """Test clearing old messages."""
        session = ChatSession()
        
        # Add many messages
        for i in range(25):
            session.add_message("user", f"Message {i}")
        
        removed = session.clear_old_messages(keep_recent=10)
        assert removed == 15
        assert len(session.messages) == 10
        assert session.messages[0].content == "Message 15"
    
    def test_update_context(self):
        """Test updating session context."""
        session = ChatSession()
        
        session.update_context("reading_id", "test-123")
        assert session.context["reading_id"] == "test-123"
        
        session.update_context("card_name", "The Fool")
        assert session.context["card_name"] == "The Fool"
    
    def test_context_summary(self):
        """Test context summary generation."""
        session = ChatSession()
        
        # Test empty context
        summary = session.get_context_summary()
        assert summary == "No specific context"
        
        # Test with reading context
        session.update_context("reading", {"title": "Test Reading"})
        summary = session.get_context_summary()
        assert "Test Reading" in summary
        
        # Test with card context
        session.update_context("card", {"name": "The Fool"})
        summary = session.get_context_summary()
        assert "The Fool" in summary


class TestChatMemoryManager:
    """Test ChatMemoryManager functionality."""
    
    def test_memory_manager_creation(self):
        """Test ChatMemoryManager creation."""
        manager = ChatMemoryManager(max_sessions=10, max_session_age_days=7)
        
        assert manager.max_sessions == 10
        assert manager.max_session_age_days == 7
        assert len(manager.sessions) == 0
        assert manager.current_session_id is None
    
    def test_create_session(self):
        """Test creating a new session."""
        manager = ChatMemoryManager()
        
        session = manager.create_session("Test Session", {"test": "value"})
        
        assert session.title == "Test Session"
        assert session.context["test"] == "value"
        assert session.session_id in manager.sessions
        assert manager.current_session_id == session.session_id
    
    def test_get_current_session(self):
        """Test getting current session."""
        manager = ChatMemoryManager()
        
        # No current session
        assert manager.get_current_session() is None
        
        # Create session
        session = manager.create_session("Test")
        current = manager.get_current_session()
        assert current == session
    
    def test_set_current_session(self):
        """Test setting current session."""
        manager = ChatMemoryManager()
        
        session1 = manager.create_session("Session 1")
        session2 = manager.create_session("Session 2")
        
        # Set current session
        assert manager.set_current_session(session1.session_id)
        assert manager.get_current_session() == session1
        
        # Set to non-existent session
        assert not manager.set_current_session("non-existent")
    
    def test_add_message(self):
        """Test adding messages to sessions."""
        manager = ChatMemoryManager()
        
        session = manager.create_session("Test")
        
        message = manager.add_message("user", "Hello!")
        assert message is not None
        assert message.role == "user"
        assert message.content == "Hello!"
        assert len(session.messages) == 1
    
    def test_get_conversation_context(self):
        """Test getting conversation context."""
        manager = ChatMemoryManager()
        
        session = manager.create_session("Test", {"key": "value"})
        session.add_message("user", "Hello")
        session.add_message("assistant", "Hi")
        
        messages, context = manager.get_conversation_context()
        
        assert len(messages) == 2
        assert context["key"] == "value"
    
    def test_end_session(self):
        """Test ending a session."""
        manager = ChatMemoryManager()
        
        session = manager.create_session("Test")
        assert session.is_active is True
        
        manager.end_session()
        assert session.is_active is False
        assert manager.current_session_id is None
    
    def test_delete_session(self):
        """Test deleting a session."""
        manager = ChatMemoryManager()
        
        session = manager.create_session("Test")
        session_id = session.session_id
        
        assert session_id in manager.sessions
        assert manager.delete_session(session_id)
        assert session_id not in manager.sessions
    
    def test_cleanup_old_messages(self):
        """Test cleaning up old messages."""
        manager = ChatMemoryManager()
        
        session = manager.create_session("Test")
        
        # Add many messages
        for i in range(25):
            manager.add_message("user", f"Message {i}")
        
        removed = manager.cleanup_old_messages(keep_recent=10)
        assert removed == 15
        assert len(session.messages) == 10


class TestModelConfig:
    """Test ModelConfig functionality."""
    
    def test_model_config_creation(self):
        """Test ModelConfig creation."""
        config = ModelConfig(
            name="test-model",
            display_name="Test Model",
            size=ModelSize.SMALL,
            purpose=ModelPurpose.GENERAL,
            description="A test model",
            parameters=1000000000,
            context_length=4000
        )
        
        assert config.name == "test-model"
        assert config.display_name == "Test Model"
        assert config.size == ModelSize.SMALL
        assert config.purpose == ModelPurpose.GENERAL
        assert config.parameters == 1000000000
    
    def test_model_config_serialization(self):
        """Test ModelConfig serialization."""
        config = ModelConfig(
            name="test-model",
            display_name="Test Model",
            size=ModelSize.MEDIUM,
            purpose=ModelPurpose.TAROT,
            description="A test model",
            parameters=3000000000,
            context_length=8000
        )
        
        data = config.to_dict()
        assert data["name"] == "test-model"
        assert data["size"] == "medium"
        assert data["purpose"] == "tarot"
        assert data["parameters"] == 3000000000
    
    def test_model_config_deserialization(self):
        """Test ModelConfig deserialization."""
        data = {
            "name": "test-model",
            "display_name": "Test Model",
            "size": "small",
            "purpose": "general",
            "description": "A test model",
            "parameters": 1000000000,
            "context_length": 4000,
            "recommended_temperature": 0.7,
            "recommended_top_p": 0.9,
            "max_tokens": 2000,
            "is_available": True,
            "download_size_gb": 1.0,
            "tags": ["test", "small"]
        }
        
        config = ModelConfig.from_dict(data)
        assert config.name == "test-model"
        assert config.size == ModelSize.SMALL
        assert config.purpose == ModelPurpose.GENERAL
        assert config.tags == ["test", "small"]


class TestModelConfigManager:
    """Test ModelConfigManager functionality."""
    
    def test_model_manager_creation(self):
        """Test ModelConfigManager creation."""
        manager = ModelConfigManager()
        
        assert len(manager.models) > 0  # Should have default models
        assert manager.current_model is None
    
    def test_get_available_models(self):
        """Test getting available models."""
        manager = ModelConfigManager()
        
        # Set some models as available
        manager.update_model_availability("llama3.2:3b", True)
        manager.update_model_availability("llama3.2:1b", True)
        
        available = manager.get_available_models()
        assert len(available) >= 2
    
    def test_get_models_by_size(self):
        """Test getting models by size."""
        manager = ModelConfigManager()
        
        small_models = manager.get_models_by_size(ModelSize.SMALL)
        assert len(small_models) > 0
        assert all(model.size == ModelSize.SMALL for model in small_models)
    
    def test_get_models_by_purpose(self):
        """Test getting models by purpose."""
        manager = ModelConfigManager()
        
        general_models = manager.get_models_by_purpose(ModelPurpose.GENERAL)
        assert len(general_models) > 0
        assert all(model.purpose == ModelPurpose.GENERAL for model in general_models)
    
    def test_get_recommended_models(self):
        """Test getting recommended models."""
        manager = ModelConfigManager()
        
        recommendations = manager.get_recommended_models(ModelPurpose.GENERAL)
        assert len(recommendations) > 0
        
        # Should be sorted by parameters
        for i in range(len(recommendations) - 1):
            assert recommendations[i].parameters <= recommendations[i + 1].parameters
    
    def test_set_current_model(self):
        """Test setting current model."""
        manager = ModelConfigManager()
        
        # Set a valid model
        assert manager.set_current_model("llama3.2:3b")
        assert manager.get_current_model().name == "llama3.2:3b"
        
        # Set invalid model
        assert not manager.set_current_model("non-existent-model")
    
    def test_add_custom_model(self):
        """Test adding custom model."""
        manager = ModelConfigManager()
        
        custom_config = ModelConfig(
            name="custom-model",
            display_name="Custom Model",
            size=ModelSize.SMALL,
            purpose=ModelPurpose.TAROT,
            description="A custom model",
            parameters=2000000000,
            context_length=6000
        )
        
        assert manager.add_custom_model(custom_config)
        assert "custom-model" in manager.custom_configs
    
    def test_get_model_recommendations(self):
        """Test getting model recommendations for use cases."""
        manager = ModelConfigManager()
        
        # Test different use cases
        quick_models = manager.get_model_recommendations("quick_reading")
        assert len(quick_models) > 0
        
        detailed_models = manager.get_model_recommendations("detailed_analysis")
        assert len(detailed_models) > 0


class TestOllamaClient:
    """Test OllamaClient functionality."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock Ollama client."""
        with patch('ai.ollama_client.ollama.Client') as mock:
            client_instance = Mock()
            mock.return_value = client_instance
            client_instance.list.return_value = {'models': [{'name': 'llama3.2:3b'}]}
            client_instance.generate.return_value = {'response': '{"reading_id": "test", "summary": "test", "cards": [], "advice": [], "follow_up_questions": []}'}
            client_instance.chat.return_value = {'message': {'content': 'Test response'}}
            yield client_instance
    
    def test_ollama_client_creation(self, mock_client):
        """Test OllamaClient creation."""
        client = OllamaClient(model="llama3.2:3b")
        
        assert client.model == "llama3.2:3b"
        assert client.host == "localhost"
        assert client.port == 11434
    
    @pytest.mark.asyncio
    async def test_check_connection(self, mock_client):
        """Test connection check."""
        client = OllamaClient(model="llama3.2:3b")
        
        result = await client.check_connection()
        assert result is True
    
    @pytest.mark.asyncio
    async def test_check_connection_failure(self, mock_client):
        """Test connection check failure."""
        mock_client.list.side_effect = Exception("Connection failed")
        client = OllamaClient(model="llama3.2:3b")
        
        result = await client.check_connection()
        assert result is False
    
    @pytest.mark.asyncio
    async def test_generate_influenced_meanings(self, mock_client):
        """Test generating influenced meanings."""
        client = OllamaClient(model="llama3.2:3b")
        
        reading_context = {
            "reading_id": "test-123",
            "spread_name": "Three Card",
            "cards": []
        }
        
        result = await client.generate_influenced_meanings(reading_context)
        assert isinstance(result, InfluencedReadingResponse)
        assert result.reading_id == "test"
    
    @pytest.mark.asyncio
    async def test_chat_stream(self, mock_client):
        """Test chat streaming."""
        client = OllamaClient(model="llama3.2:3b")
        
        messages = [{"role": "user", "content": "Hello"}]
        
        chunks = []
        async for chunk in client.chat_stream(messages):
            chunks.append(chunk)
        
        assert len(chunks) > 0
        assert "Test response" in "".join(chunks)
    
    @pytest.mark.asyncio
    async def test_chat(self, mock_client):
        """Test chat functionality."""
        client = OllamaClient(model="llama3.2:3b")
        
        messages = [{"role": "user", "content": "Hello"}]
        response = await client.chat(messages)
        
        assert response == "Test response"
    
    @pytest.mark.asyncio
    async def test_get_available_models(self, mock_client):
        """Test getting available models."""
        client = OllamaClient(model="llama3.2:3b")
        
        models = await client.get_available_models()
        assert "llama3.2:3b" in models


class TestAIManager:
    """Test AIManager functionality."""
    
    @pytest.fixture
    def mock_ollama_client(self):
        """Create a mock Ollama client for AIManager."""
        with patch('ai.ai_manager.OllamaClient') as mock:
            client_instance = Mock()
            mock.return_value = client_instance
            client_instance.check_connection = AsyncMock(return_value=True)
            client_instance.get_available_models = AsyncMock(return_value=["llama3.2:3b"])
            client_instance.chat_stream = AsyncMock()
            client_instance.chat = AsyncMock(return_value="Test response")
            client_instance.generate_influenced_meanings = AsyncMock()
            yield client_instance
    
    @pytest.mark.asyncio
    async def test_ai_manager_initialization(self, mock_ollama_client):
        """Test AIManager initialization."""
        manager = AIManager()
        
        result = await manager.initialize()
        assert result is True
        assert manager.is_connected is True
        assert manager.ollama_client is not None
    
    @pytest.mark.asyncio
    async def test_check_connection(self, mock_ollama_client):
        """Test connection check."""
        manager = AIManager()
        await manager.initialize()
        
        result = await manager.check_connection()
        assert result is True
    
    @pytest.mark.asyncio
    async def test_get_available_models(self, mock_ollama_client):
        """Test getting available models."""
        manager = AIManager()
        await manager.initialize()
        
        models = await manager.get_available_models()
        assert "llama3.2:3b" in models
    
    @pytest.mark.asyncio
    async def test_set_model(self, mock_ollama_client):
        """Test setting model."""
        manager = AIManager()
        await manager.initialize()
        
        result = await manager.set_model("llama3.2:3b")
        assert result is True
        assert manager.ollama_client.model == "llama3.2:3b"
    
    def test_create_chat_session(self, mock_ollama_client):
        """Test creating chat session."""
        manager = AIManager()
        
        session = manager.create_chat_session("Test Session", {"test": "value"})
        assert session.title == "Test Session"
        assert session.context["test"] == "value"
        assert manager.get_current_session() == session
    
    @pytest.mark.asyncio
    async def test_chat_stream(self, mock_ollama_client):
        """Test chat streaming."""
        manager = AIManager()
        await manager.initialize()
        
        manager.create_chat_session("Test")
        
        chunks = []
        async for chunk in manager.chat_stream("Hello!"):
            chunks.append(chunk)
        
        assert len(chunks) > 0
        assert "Test response" in "".join(chunks)
    
    @pytest.mark.asyncio
    async def test_chat(self, mock_ollama_client):
        """Test chat functionality."""
        manager = AIManager()
        await manager.initialize()
        
        manager.create_chat_session("Test")
        
        response = await manager.chat("Hello!")
        assert response == "Test response"
    
    def test_get_status(self, mock_ollama_client):
        """Test getting AI manager status."""
        manager = AIManager()
        
        status = manager.get_status()
        assert "is_connected" in status
        assert "current_model" in status
        assert "memory_stats" in status
        assert "model_stats" in status


class TestAIIntegration:
    """Integration tests for AI module."""
    
    @pytest.mark.asyncio
    async def test_complete_chat_workflow(self, mock_ollama_client):
        """Test complete chat workflow."""
        manager = AIManager()
        await manager.initialize()
        
        # Create session
        session = manager.create_chat_session("Test Chat")
        
        # Add messages
        await manager.chat("What is tarot?", session.session_id)
        await manager.chat("Tell me about The Fool card", session.session_id)
        
        # Check session state
        assert len(session.messages) == 4  # 2 user + 2 assistant
        assert session.messages[0].role == "user"
        assert session.messages[1].role == "assistant"
    
    def test_memory_cleanup_workflow(self, mock_ollama_client):
        """Test memory cleanup workflow."""
        manager = AIManager()
        
        # Create multiple sessions
        for i in range(5):
            session = manager.create_chat_session(f"Session {i}")
            for j in range(10):
                manager.add_message("user", f"Message {j}", session.session_id)
        
        # Cleanup old messages
        removed = manager.cleanup_old_messages(keep_recent=5)
        assert removed > 0
        
        # Check all sessions have limited messages
        for session in manager.list_sessions():
            assert len(session.messages) <= 5
    
    def test_model_recommendation_workflow(self, mock_ollama_client):
        """Test model recommendation workflow."""
        manager = AIManager()
        
        # Get recommendations for different use cases
        quick_models = manager.get_model_recommendations("quick_reading")
        detailed_models = manager.get_model_recommendations("detailed_analysis")
        
        assert len(quick_models) > 0
        assert len(detailed_models) > 0
        
        # Quick models should generally be smaller
        if quick_models and detailed_models:
            avg_quick_params = sum(m.parameters for m in quick_models) / len(quick_models)
            avg_detailed_params = sum(m.parameters for m in detailed_models) / len(detailed_models)
            assert avg_quick_params <= avg_detailed_params


if __name__ == "__main__":
    pytest.main([__file__])