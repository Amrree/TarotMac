"""
Example Usage of the AI Module

This file demonstrates how to use the AI module for chat functionality,
tarot reading interpretation, and memory management.
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai.ai_manager import AIManager
from ai.chat_memory import ChatSession
from ai.model_config import ModelPurpose


async def example_basic_chat():
    """Example of basic chat functionality."""
    print("=== Basic Chat Example ===")
    
    # Initialize AI manager
    ai_manager = AIManager()
    await ai_manager.initialize()
    
    # Check connection status
    print(f"AI Connected: {ai_manager.is_connected}")
    print(f"Current Model: {ai_manager.get_current_model().display_name if ai_manager.get_current_model() else 'None'}")
    
    # Create a chat session
    session = ai_manager.create_chat_session("Basic Chat Example")
    print(f"Created session: {session.title}")
    
    # Have a conversation
    print("\n--- Conversation ---")
    
    response = await ai_manager.chat("Hello! Can you tell me about tarot cards?")
    print(f"User: Hello! Can you tell me about tarot cards?")
    print(f"AI: {response}")
    
    response = await ai_manager.chat("What is The Fool card about?")
    print(f"\nUser: What is The Fool card about?")
    print(f"AI: {response}")
    
    # Show session statistics
    print(f"\n--- Session Statistics ---")
    print(f"Messages in session: {len(session.messages)}")
    print(f"Session context: {session.get_context_summary()}")


async def example_streaming_chat():
    """Example of streaming chat functionality."""
    print("\n=== Streaming Chat Example ===")
    
    ai_manager = AIManager()
    await ai_manager.initialize()
    
    if not ai_manager.is_connected:
        print("AI not connected, skipping streaming example")
        return
    
    # Create session
    session = ai_manager.create_chat_session("Streaming Chat Example")
    
    print("User: Tell me a story about The Magician card")
    print("AI: ", end="", flush=True)
    
    # Stream response
    async for chunk in ai_manager.chat_stream("Tell me a story about The Magician card"):
        print(chunk, end="", flush=True)
    
    print("\n")  # New line after streaming


async def example_reading_discussion():
    """Example of discussing a tarot reading."""
    print("\n=== Reading Discussion Example ===")
    
    ai_manager = AIManager()
    await ai_manager.initialize()
    
    if not ai_manager.is_connected:
        print("AI not connected, skipping reading discussion example")
        return
    
    # Create a mock reading context
    reading_data = {
        "title": "Career Guidance Reading",
        "spread_name": "Three Card Spread",
        "date": "2024-01-01",
        "cards": [
            {
                "card_name": "The Fool",
                "orientation": "upright",
                "position": "Past",
                "meaning": "New beginnings and fresh starts"
            },
            {
                "card_name": "The Magician",
                "orientation": "upright", 
                "position": "Present",
                "meaning": "Taking action and using your skills"
            },
            {
                "card_name": "The World",
                "orientation": "upright",
                "position": "Future",
                "meaning": "Completion and success"
            }
        ]
    }
    
    # Create session with reading context
    session = ai_manager.create_chat_session("Career Reading Discussion", {"reading": reading_data})
    
    # Discuss the reading
    print("--- Reading Discussion ---")
    
    response = await ai_manager.chat_about_reading(reading_data, "What does this reading tell me about my career?")
    print(f"User: What does this reading tell me about my career?")
    print(f"AI: {response}")
    
    response = await ai_manager.chat("How should I interpret The Fool in the past position?")
    print(f"\nUser: How should I interpret The Fool in the past position?")
    print(f"AI: {response}")


async def example_card_discussion():
    """Example of discussing a specific card."""
    print("\n=== Card Discussion Example ===")
    
    ai_manager = AIManager()
    await ai_manager.initialize()
    
    if not ai_manager.is_connected:
        print("AI not connected, skipping card discussion example")
        return
    
    # Card data
    card_data = {
        "name": "The High Priestess",
        "orientation": "reversed",
        "position": "Present",
        "keywords": ["intuition", "mystery", "inner wisdom", "secrets"],
        "meaning": "The High Priestess represents intuition and inner wisdom"
    }
    
    # Discuss the card
    print("--- Card Discussion ---")
    
    response = await ai_manager.chat_about_card(card_data, "What does The High Priestess reversed mean?")
    print(f"User: What does The High Priestess reversed mean?")
    print(f"AI: {response}")
    
    response = await ai_manager.chat("How can I work with this energy?")
    print(f"\nUser: How can I work with this energy?")
    print(f"AI: {response}")


async def example_memory_management():
    """Example of memory management functionality."""
    print("\n=== Memory Management Example ===")
    
    ai_manager = AIManager()
    await ai_manager.initialize()
    
    # Create multiple sessions
    print("--- Creating Multiple Sessions ---")
    
    session1 = ai_manager.create_chat_session("Tarot Learning Session")
    session2 = ai_manager.create_chat_session("Card Meanings Session")
    session3 = ai_manager.create_chat_session("Reading Practice Session")
    
    # Add messages to sessions
    await ai_manager.chat("What is tarot?", session1.session_id)
    await ai_manager.chat("Tell me about Major Arcana", session2.session_id)
    await ai_manager.chat("How do I do a reading?", session3.session_id)
    
    # List sessions
    print("\n--- Session List ---")
    sessions = ai_manager.list_sessions()
    for session in sessions:
        print(f"- {session.title}: {len(session.messages)} messages")
    
    # Switch between sessions
    print("\n--- Switching Sessions ---")
    ai_manager.set_current_session(session2.session_id)
    current = ai_manager.get_current_session()
    print(f"Current session: {current.title}")
    
    # Add more messages to current session
    await ai_manager.chat("What about Minor Arcana?", session2.session_id)
    print(f"Session now has {len(session2.messages)} messages")
    
    # Show memory statistics
    print("\n--- Memory Statistics ---")
    stats = ai_manager.get_memory_stats()
    print(f"Total sessions: {stats['total_sessions']}")
    print(f"Active sessions: {stats['active_sessions']}")
    print(f"Total messages: {stats['total_messages']}")


async def example_model_management():
    """Example of model management functionality."""
    print("\n=== Model Management Example ===")
    
    ai_manager = AIManager()
    await ai_manager.initialize()
    
    # Show current model
    current_model = ai_manager.get_current_model()
    if current_model:
        print(f"Current model: {current_model.display_name}")
        print(f"Size: {current_model.size.value}")
        print(f"Purpose: {current_model.purpose.value}")
        print(f"Parameters: {current_model.parameters:,}")
    
    # Get model recommendations
    print("\n--- Model Recommendations ---")
    
    quick_models = ai_manager.get_model_recommendations("quick_reading")
    print(f"Quick reading models: {len(quick_models)}")
    for model in quick_models[:3]:  # Show first 3
        print(f"  - {model.display_name} ({model.size.value})")
    
    detailed_models = ai_manager.get_model_recommendations("detailed_analysis")
    print(f"Detailed analysis models: {len(detailed_models)}")
    for model in detailed_models[:3]:  # Show first 3
        print(f"  - {model.display_name} ({model.size.value})")
    
    # Show model statistics
    print("\n--- Model Statistics ---")
    model_stats = ai_manager.get_model_stats()
    print(f"Total models: {model_stats['total_models']}")
    print(f"Available models: {model_stats['available_models']}")
    print(f"Custom models: {model_stats['custom_models']}")


async def example_session_export_import():
    """Example of session export/import functionality."""
    print("\n=== Session Export/Import Example ===")
    
    ai_manager = AIManager()
    await ai_manager.initialize()
    
    # Create a session with some content
    session = ai_manager.create_chat_session("Export Test Session")
    await ai_manager.chat("Hello, this is a test message", session.session_id)
    await ai_manager.chat("This is another message", session.session_id)
    
    print(f"Original session: {session.title} with {len(session.messages)} messages")
    
    # Export session
    exported_data = ai_manager.export_session(session.session_id)
    print(f"Exported session data keys: {list(exported_data.keys())}")
    
    # Import session
    imported_session = ai_manager.import_session(exported_data)
    if imported_session:
        print(f"Imported session: {imported_session.title} with {len(imported_session.messages)} messages")
        print(f"Import successful: {imported_session.session_id != session.session_id}")


async def example_error_handling():
    """Example of error handling when AI is not available."""
    print("\n=== Error Handling Example ===")
    
    # Create AI manager with invalid host to simulate connection failure
    ai_manager = AIManager(host="invalid-host", port=9999)
    await ai_manager.initialize()
    
    print(f"AI Connected: {ai_manager.is_connected}")
    
    # Try to chat when not connected
    session = ai_manager.create_chat_session("Error Test Session")
    response = await ai_manager.chat("Hello, are you there?")
    print(f"Response when not connected: {response}")
    
    # Memory management still works without AI
    print(f"Memory still works: {len(session.messages)} messages")
    print(f"Session management still works: {ai_manager.get_current_session().title}")


async def example_complete_workflow():
    """Example of a complete AI workflow."""
    print("\n=== Complete AI Workflow Example ===")
    
    ai_manager = AIManager()
    await ai_manager.initialize()
    
    if not ai_manager.is_connected:
        print("AI not connected, demonstrating fallback behavior")
        return
    
    # 1. Create a tarot learning session
    session = ai_manager.create_chat_session("Tarot Learning Journey", {
        "topic": "tarot_learning",
        "level": "beginner"
    })
    
    # 2. Start learning conversation
    print("--- Learning Conversation ---")
    
    await ai_manager.chat("I'm new to tarot. Where should I start?")
    await ai_manager.chat("What's the difference between Major and Minor Arcana?")
    await ai_manager.chat("Can you explain The Fool card?")
    
    # 3. Switch to a reading session
    reading_session = ai_manager.create_chat_session("My First Reading", {
        "reading_type": "three_card",
        "question": "What should I focus on today?"
    })
    
    # 4. Discuss a reading
    reading_data = {
        "title": "Daily Guidance",
        "cards": [
            {"name": "The Sun", "position": "Past", "meaning": "Joy and success"},
            {"name": "The Moon", "position": "Present", "meaning": "Intuition and mystery"},
            {"name": "The Star", "position": "Future", "meaning": "Hope and inspiration"}
        ]
    }
    
    await ai_manager.chat_about_reading(reading_data, "What does this reading mean?")
    
    # 5. Show final statistics
    print("\n--- Final Statistics ---")
    memory_stats = ai_manager.get_memory_stats()
    print(f"Total sessions: {memory_stats['total_sessions']}")
    print(f"Total messages: {memory_stats['total_messages']}")
    
    model_stats = ai_manager.get_model_stats()
    print(f"Current model: {model_stats['current_model']}")
    print(f"Available models: {model_stats['available_models']}")


async def main():
    """Run all examples."""
    print("TarotMac AI Module - Example Usage")
    print("=" * 50)
    
    try:
        await example_basic_chat()
        await example_streaming_chat()
        await example_reading_discussion()
        await example_card_discussion()
        await example_memory_management()
        await example_model_management()
        await example_session_export_import()
        await example_error_handling()
        await example_complete_workflow()
        
        print("\n" + "=" * 50)
        print("All AI examples completed successfully!")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())