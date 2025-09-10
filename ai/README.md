# AI Module

The AI Module provides comprehensive AI functionality for TarotMac, including Ollama integration, chat memory management, model configuration, and tarot-specific AI features.

## Overview

This module implements a complete AI system that supports:
- Local LLM integration via Ollama
- Persistent chat memory and session management
- Model configuration and selection
- Tarot-specific AI features (reading interpretation, card discussion)
- Streaming and non-streaming chat responses
- Fallback behavior when AI is unavailable

## Architecture

### Core Components

1. **AIManager**: Main interface integrating all AI functionality
2. **OllamaClient**: Client for Ollama LLM integration
3. **ChatMemoryManager**: Manages chat sessions and memory
4. **ModelConfigManager**: Manages model configurations and selection

### Key Classes

#### AIManager
Main AI manager providing unified interface:
- AI initialization and connection management
- Chat functionality (streaming and non-streaming)
- Tarot-specific AI features
- Session and memory management
- Model configuration integration

#### OllamaClient
Client for Ollama LLM integration:
- Connection management and health checks
- Chat streaming and non-streaming
- Tarot reading interpretation
- Model availability checking
- Error handling and fallbacks

#### ChatMemoryManager
Manages chat sessions and memory:
- Session creation and management
- Message history and context
- Conversation memory with token limits
- Session export/import
- Automatic cleanup of old data

#### ModelConfigManager
Manages model configurations:
- Predefined model configurations
- Custom model support
- Model recommendations by use case
- Availability tracking
- Configuration persistence

## Supported Models

### Default Models
- **Llama 3.2 3B**: Fast, efficient model for general conversations
- **Llama 3.2 1B**: Ultra-fast model for quick responses
- **Llama 3.1 8B**: Balanced model with good reasoning capabilities
- **Mistral 7B**: Analytical model for complex interpretations
- **Gemma 2 9B**: Creative model for imaginative interpretations

### Model Categories
- **Tiny** (< 1B): Ultra-fast, lightweight
- **Small** (1-3B): Fast, efficient
- **Medium** (3-7B): Balanced performance
- **Large** (7-13B): High-quality responses
- **XLarge** (13B+): Maximum quality

### Use Case Recommendations
- **Quick Reading**: Tiny/Small models for fast interpretations
- **Detailed Analysis**: Medium/Large models for comprehensive analysis
- **Creative Interpretation**: Creative-focused models
- **Analytical Advice**: Analytical models for practical guidance

## API Reference

### Basic AI Initialization

```python
from ai.ai_manager import AIManager

# Initialize AI manager
ai_manager = AIManager()
await ai_manager.initialize()

# Check connection status
if ai_manager.is_connected:
    print("AI is ready!")
else:
    print("AI not available, using fallback mode")
```

### Chat Functionality

```python
# Create a chat session
session = ai_manager.create_chat_session("My Chat Session")

# Non-streaming chat
response = await ai_manager.chat("Tell me about tarot cards")
print(response)

# Streaming chat
async for chunk in ai_manager.chat_stream("Tell me a story"):
    print(chunk, end="", flush=True)
```

### Tarot-Specific Features

```python
# Discuss a reading
reading_data = {
    "title": "Career Reading",
    "cards": [
        {"name": "The Fool", "position": "Past", "meaning": "New beginnings"},
        {"name": "The Magician", "position": "Present", "meaning": "Taking action"},
        {"name": "The World", "position": "Future", "meaning": "Success"}
    ]
}

response = await ai_manager.chat_about_reading(reading_data, "What does this reading mean?")

# Discuss a specific card
card_data = {
    "name": "The High Priestess",
    "orientation": "reversed",
    "keywords": ["intuition", "mystery", "inner wisdom"]
}

response = await ai_manager.chat_about_card(card_data, "What does this card mean?")
```

### Memory Management

```python
# Create multiple sessions
session1 = ai_manager.create_chat_session("Learning Session")
session2 = ai_manager.create_chat_session("Reading Session")

# Switch between sessions
ai_manager.set_current_session(session1.session_id)

# List all sessions
sessions = ai_manager.list_sessions()
for session in sessions:
    print(f"{session.title}: {len(session.messages)} messages")

# Export/import sessions
exported_data = ai_manager.export_session(session1.session_id)
imported_session = ai_manager.import_session(exported_data)
```

### Model Management

```python
# Get current model
current_model = ai_manager.get_current_model()
print(f"Current model: {current_model.display_name}")

# Get model recommendations
quick_models = ai_manager.get_model_recommendations("quick_reading")
detailed_models = ai_manager.get_model_recommendations("detailed_analysis")

# Switch models (if available)
await ai_manager.set_model("llama3.2:3b")

# Get model statistics
stats = ai_manager.get_model_stats()
print(f"Available models: {stats['available_models']}")
```

## Integration

### With Spreads Module

The AI Module integrates with the Spreads Module for enhanced reading interpretations:

```python
from core.spreads.manager import SpreadManager
from core.deck.loader import DeckLoader
from ai.ai_manager import AIManager

# Create spread reading
deck = DeckLoader.load_canonical_deck()
spread_manager = SpreadManager(deck=deck)
reading = spread_manager.create_reading(SpreadType.THREE_CARD)
spread_manager.draw_cards_for_reading(reading)

# Get AI interpretation
ai_manager = AIManager()
await ai_manager.initialize()

# Convert reading to AI format
reading_data = {
    "title": reading.question or "Tarot Reading",
    "spread_name": reading.layout.name,
    "cards": [
        {
            "name": pc.card.name,
            "position": pc.position.name,
            "orientation": pc.card.orientation.value,
            "meaning": pc.card.get_meaning()
        }
        for pc in reading.positioned_cards
    ]
}

# Get AI interpretation
response = await ai_manager.chat_about_reading(reading_data)
print(response)
```

### With History Module

The AI Module integrates with the History Module for persistent chat storage:

```python
# Sessions are automatically managed in memory
# Integration with database persistence would be handled by History Module
```

## Configuration

### Model Configuration File

The AI Module uses a JSON configuration file for custom models:

```json
{
  "current_model": "llama3.2:3b",
  "custom_models": [
    {
      "name": "custom-tarot-model",
      "display_name": "Custom Tarot Model",
      "size": "medium",
      "purpose": "tarot",
      "description": "Custom model trained for tarot",
      "parameters": 5000000000,
      "context_length": 8000,
      "recommended_temperature": 0.7,
      "recommended_top_p": 0.9,
      "max_tokens": 2000,
      "download_size_gb": 3.0,
      "tags": ["custom", "tarot"]
    }
  ]
}
```

### Memory Configuration

Memory management can be configured:

```python
# Create memory manager with custom settings
memory_manager = ChatMemoryManager(
    max_sessions=100,           # Maximum sessions to keep
    max_session_age_days=60     # Maximum age before cleanup
)

# Configure cleanup
ai_manager.cleanup_old_messages(keep_recent=50)  # Keep 50 recent messages per session
```

## Error Handling

### Connection Failures

The AI Module gracefully handles connection failures:

```python
# Check connection status
if not ai_manager.is_connected:
    print("AI not available, using fallback responses")

# Fallback responses are automatically provided
response = await ai_manager.chat("Hello")  # Returns fallback message
```

### Model Unavailability

When models are not available:

```python
# Check model availability
available_models = await ai_manager.get_available_models()
if "llama3.2:3b" not in available_models:
    print("Model not available, using alternative")

# Switch to available model
await ai_manager.set_model("llama3.2:1b")  # Smaller, more likely to be available
```

## Performance Considerations

### Memory Management

- Sessions are kept in memory for fast access
- Old messages are automatically cleaned up
- Token limits prevent excessive memory usage
- Export/import allows for persistence

### Model Selection

- Smaller models provide faster responses
- Larger models provide better quality
- Recommendations help choose appropriate models
- Availability checking prevents errors

### Streaming vs Non-Streaming

- Streaming provides real-time responses
- Non-streaming provides complete responses
- Choose based on UI requirements
- Both support the same features

## Testing

The module includes comprehensive unit tests covering:
- AI manager initialization and connection
- Chat functionality (streaming and non-streaming)
- Memory management and session handling
- Model configuration and selection
- Error handling and fallbacks
- Integration scenarios

Run tests with:
```bash
python -m pytest tests/unit/test_ai_module.py -v
```

## Dependencies

- **ollama**: Ollama Python client for LLM integration
- **pydantic**: Data validation and serialization
- **asyncio**: Asynchronous programming support
- **Standard Library**: datetime, json, logging, typing

## Files

- `ai_manager.py`: Main AI manager and integration interface
- `ollama_client.py`: Ollama client for LLM integration
- `chat_memory.py`: Chat memory and session management
- `model_config.py`: Model configuration and selection
- `__init__.py`: Module initialization and exports
- `example_usage.py`: Comprehensive usage examples
- `README.md`: This documentation