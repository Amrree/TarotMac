"""
Example usage of the GUI module components.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import mock modules if needed
try:
    from AppKit import NSApplication, NSApp
except ImportError:
    # Use mock for testing when AppKit is not available
    from app.mock_appkit import appkit_module
    NSApplication = appkit_module.NSApplication
    NSApp = appkit_module.NSApp

from app.app_delegate import TarotAppDelegate
from app.readings_manager import ReadingsManager
from app.chat_manager import ChatManager
from app.history_manager import HistoryManager
from app.settings_manager import SettingsManager


def demonstrate_readings_manager():
    """Demonstrate the readings manager functionality."""
    print("=== Readings Manager Demo ===")
    
    manager = ReadingsManager()
    
    # Create a reading
    print("Creating single card reading...")
    success = manager.createReading("single")
    print(f"Reading created: {success}")
    
    if success:
        # Draw cards
        print("Drawing cards...")
        success = manager.drawCards()
        print(f"Cards drawn: {success}")
        
        if success:
            # Get cards
            cards = manager.getReadingCards()
            print(f"Cards drawn: {len(cards)}")
            for card in cards:
                print(f"  - {card['name']} ({card['orientation']})")
            
            # Get interpretation
            interpretation = manager.getReadingInterpretation()
            print(f"Interpretation: {interpretation[:100]}...")
    
    # Test other spread types
    print("\nTesting other spread types...")
    for spread_type in manager.getAvailableSpreadTypes():
        print(f"Testing {spread_type} spread...")
        success = manager.createReading(spread_type)
        print(f"  Created: {success}")
        if success:
            success = manager.drawCards()
            print(f"  Cards drawn: {success}")
            if success:
                cards = manager.getReadingCards()
                print(f"  Cards: {len(cards)}")
    
    # Get deck status
    status = manager.getDeckStatus()
    print(f"\nDeck status: {status}")
    
    print("=== End Readings Manager Demo ===\n")


def demonstrate_chat_manager():
    """Demonstrate the chat manager functionality."""
    print("=== Chat Manager Demo ===")
    
    manager = ChatManager()
    
    # Start new session
    print("Starting new chat session...")
    session_id = manager.startNewSession()
    print(f"Session ID: {session_id}")
    
    # Send messages
    messages = [
        "Hello, can you help me with a tarot reading?",
        "What does The Fool card mean?",
        "Can you explain the Celtic Cross spread?"
    ]
    
    for message in messages:
        print(f"\nSending: {message}")
        response = manager.sendMessage(message)
        print(f"Response: {response[:100]}...")
    
    # Get chat history
    print("\nChat history:")
    history = manager.getChatHistory()
    for entry in history:
        print(f"  {entry['role']}: {entry['content'][:50]}...")
    
    # Test session management
    print(f"\nSession active: {manager.isSessionActive()}")
    print(f"Current session ID: {manager.getCurrentSessionId()}")
    
    # Clear history
    print("Clearing chat history...")
    manager.clearChatHistory()
    history = manager.getChatHistory()
    print(f"History after clear: {len(history)} messages")
    
    print("=== End Chat Manager Demo ===\n")


def demonstrate_history_manager():
    """Demonstrate the history manager functionality."""
    print("=== History Manager Demo ===")
    
    manager = HistoryManager()
    
    # Save some readings
    readings_data = [
        {
            'id': 'demo_reading_1',
            'spread_type': 'single',
            'cards': [{'name': 'The Fool', 'orientation': 'upright'}],
            'interpretation': 'A new beginning awaits you.',
            'summary': 'New beginning reading'
        },
        {
            'id': 'demo_reading_2',
            'spread_type': 'three',
            'cards': [
                {'name': 'The Magician', 'orientation': 'upright'},
                {'name': 'The High Priestess', 'orientation': 'reversed'},
                {'name': 'The Empress', 'orientation': 'upright'}
            ],
            'interpretation': 'You have the power to manifest your desires.',
            'summary': 'Power and manifestation reading'
        }
    ]
    
    print("Saving readings...")
    for reading_data in readings_data:
        success = manager.saveReading(reading_data)
        print(f"  Saved {reading_data['id']}: {success}")
    
    # Get all readings
    print("\nAll readings:")
    all_readings = manager.getAllReadings()
    print(f"Total readings: {len(all_readings)}")
    for reading in all_readings:
        print(f"  - {reading['id']}: {reading['spread_type']} spread")
    
    # Search readings
    print("\nSearching readings...")
    search_results = manager.searchReadings("beginning")
    print(f"Search results for 'beginning': {len(search_results)}")
    for result in search_results:
        print(f"  - {result['id']}: {result['summary']}")
    
    # Get specific reading
    print("\nGetting specific reading...")
    reading = manager.getReadingById('demo_reading_1')
    if reading:
        print(f"Found reading: {reading['id']}")
        print(f"  Spread: {reading['spread_type']}")
        print(f"  Cards: {len(reading['cards'])}")
        print(f"  Summary: {reading['summary']}")
    
    # Export readings
    print("\nExporting readings...")
    success = manager.exportReadings('demo_readings.json')
    print(f"Export successful: {success}")
    
    # Import readings
    print("Importing readings...")
    success = manager.importReadings('demo_readings.json')
    print(f"Import successful: {success}")
    
    print("=== End History Manager Demo ===\n")


def demonstrate_settings_manager():
    """Demonstrate the settings manager functionality."""
    print("=== Settings Manager Demo ===")
    
    manager = SettingsManager()
    
    # Get current settings
    print("Current app config:")
    app_config = manager.getAppConfig()
    for key, value in app_config.items():
        print(f"  {key}: {value}")
    
    print("\nCurrent user preferences:")
    user_preferences = manager.getUserPreferences()
    for key, value in user_preferences.items():
        print(f"  {key}: {value}")
    
    # Update settings
    print("\nUpdating app config...")
    new_config = {
        'theme': 'light',
        'auto_save': False,
        'log_level': 'DEBUG'
    }
    success = manager.updateAppConfig(new_config)
    print(f"Config updated: {success}")
    
    print("Updating user preferences...")
    new_preferences = {
        'default_spread': 'three',
        'ai_model': 'llama3.1',
        'encryption_enabled': True
    }
    success = manager.updateUserPreferences(new_preferences)
    print(f"Preferences updated: {success}")
    
    # Save settings
    print("Saving settings...")
    success = manager.saveSettings()
    print(f"Settings saved: {success}")
    
    # Export settings
    print("Exporting settings...")
    success = manager.exportSettings('demo_settings.json')
    print(f"Settings exported: {success}")
    
    # Import settings
    print("Importing settings...")
    success = manager.importSettings('demo_settings.json')
    print(f"Settings imported: {success}")
    
    # Reset to defaults
    print("Resetting to defaults...")
    success = manager.resetToDefaults()
    print(f"Reset successful: {success}")
    
    print("=== End Settings Manager Demo ===\n")


def main():
    """Main demonstration function."""
    print("GUI Module Demonstration")
    print("=" * 50)
    
    try:
        # Demonstrate each manager
        demonstrate_readings_manager()
        demonstrate_chat_manager()
        demonstrate_history_manager()
        demonstrate_settings_manager()
        
        print("All demonstrations completed successfully!")
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()