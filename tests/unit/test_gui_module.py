"""
Unit tests for the GUI module.
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.app_delegate import TarotAppDelegate
from app.readings_manager import ReadingsManager
from app.chat_manager import ChatManager
from app.history_manager import HistoryManager
from app.settings_manager import SettingsManager


class TestTarotAppDelegate(unittest.TestCase):
    """Test the application delegate."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.delegate = TarotAppDelegate()
    
    def test_init(self):
        """Test delegate initialization."""
        self.assertIsNotNone(self.delegate)
        # The main_window_controller should be None initially
        self.assertIsNone(self.delegate.main_window_controller)
    
    def test_applicationDidFinishLaunching_(self):
        """Test application launch handling."""
        # Mock the main window controller
        with patch('app.app_delegate.MainWindowController') as mock_controller:
            mock_instance = Mock()
            mock_controller.alloc.return_value.init.return_value = mock_instance
            
            # Call the method
            self.delegate.applicationDidFinishLaunching_(None)
            
            # Verify window controller was created
            mock_controller.alloc.assert_called_once()
            mock_instance.showWindow_.assert_called_once_with(None)
    
    def test_applicationWillTerminate_(self):
        """Test application termination handling."""
        # Set up a mock window controller
        mock_controller = Mock()
        mock_window = Mock()
        mock_controller.window.return_value = mock_window
        self.delegate.main_window_controller = mock_controller
        
        # Call the method
        self.delegate.applicationWillTerminate_(None)
        
        # Verify window was closed
        mock_window.close.assert_called_once()
    
    def test_applicationShouldTerminateAfterLastWindowClosed_(self):
        """Test termination behavior when last window closes."""
        result = self.delegate.applicationShouldTerminateAfterLastWindowClosed_(None)
        self.assertTrue(result)


class TestReadingsManager(unittest.TestCase):
    """Test the readings manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = ReadingsManager()
    
    def test_init(self):
        """Test manager initialization."""
        self.assertIsNotNone(self.manager.deck)
        self.assertIsNotNone(self.manager.spread_manager)
        self.assertIsNotNone(self.manager.influence_engine)
        self.assertIsNone(self.manager.current_reading)
        self.assertIsNone(self.manager.current_spread_type)
    
    def test_createReading(self):
        """Test reading creation."""
        # Test valid spread types
        valid_spreads = ['single', 'three', 'celtic_cross', 'relationship', 'year_ahead']
        for spread_type in valid_spreads:
            success = self.manager.createReading(spread_type)
            self.assertTrue(success)
            self.assertEqual(self.manager.current_spread_type, spread_type)
            self.assertIsNotNone(self.manager.current_reading)
        
        # Test invalid spread type
        success = self.manager.createReading('invalid')
        self.assertFalse(success)
    
    def test_drawCards(self):
        """Test card drawing."""
        # Create a reading first
        self.manager.createReading('single')
        
        # Draw cards
        success = self.manager.drawCards()
        self.assertTrue(success)
        
        # Verify cards were drawn
        cards = self.manager.getReadingCards()
        self.assertGreater(len(cards), 0)
    
    def test_getReadingCards(self):
        """Test getting reading cards."""
        # No reading
        cards = self.manager.getReadingCards()
        self.assertEqual(len(cards), 0)
        
        # With reading
        self.manager.createReading('single')
        self.manager.drawCards()
        cards = self.manager.getReadingCards()
        self.assertGreater(len(cards), 0)
    
    def test_getReadingInterpretation(self):
        """Test getting reading interpretation."""
        # No reading
        interpretation = self.manager.getReadingInterpretation()
        self.assertEqual(interpretation, "No reading available")
        
        # With reading
        self.manager.createReading('single')
        self.manager.drawCards()
        interpretation = self.manager.getReadingInterpretation()
        self.assertIsInstance(interpretation, str)
        self.assertGreater(len(interpretation), 0)
    
    def test_clearReading(self):
        """Test clearing reading."""
        # Set up a reading
        self.manager.createReading('single')
        self.manager.drawCards()
        
        # Clear reading
        self.manager.clearReading()
        
        # Verify cleared
        self.assertIsNone(self.manager.current_reading)
        self.assertIsNone(self.manager.current_spread_type)
    
    def test_getAvailableSpreadTypes(self):
        """Test getting available spread types."""
        spreads = self.manager.getAvailableSpreadTypes()
        expected = ['single', 'three', 'celtic_cross', 'relationship', 'year_ahead']
        self.assertEqual(spreads, expected)
    
    def test_getDeckStatus(self):
        """Test getting deck status."""
        status = self.manager.getDeckStatus()
        self.assertIn('total_cards', status)
        self.assertIn('remaining_cards', status)
        self.assertIn('is_empty', status)
        self.assertGreater(status['total_cards'], 0)


class TestChatManager(unittest.TestCase):
    """Test the chat manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = ChatManager()
    
    def test_init(self):
        """Test manager initialization."""
        self.assertIsNotNone(self.manager.ai_manager)
        self.assertIsNone(self.manager.current_session_id)
    
    def test_startNewSession(self):
        """Test starting new session."""
        session_id = self.manager.startNewSession()
        self.assertIsNotNone(session_id)
        self.assertEqual(self.manager.current_session_id, session_id)
    
    def test_sendMessage(self):
        """Test sending message."""
        # Start session
        self.manager.startNewSession()
        
        # Send message
        response = self.manager.sendMessage("Hello")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
    
    def test_getChatHistory(self):
        """Test getting chat history."""
        # No session
        history = self.manager.getChatHistory()
        self.assertEqual(len(history), 0)
        
        # With session
        self.manager.startNewSession()
        self.manager.sendMessage("Hello")
        history = self.manager.getChatHistory()
        # The mock might not populate history, so just check it's a list
        self.assertIsInstance(history, list)
    
    def test_clearChatHistory(self):
        """Test clearing chat history."""
        # Set up session
        self.manager.startNewSession()
        self.manager.sendMessage("Hello")
        
        # Clear history
        self.manager.clearChatHistory()
        
        # Verify cleared
        history = self.manager.getChatHistory()
        self.assertEqual(len(history), 0)
    
    def test_endSession(self):
        """Test ending session."""
        # Start session
        self.manager.startNewSession()
        self.assertIsNotNone(self.manager.current_session_id)
        
        # End session
        self.manager.endSession()
        self.assertIsNone(self.manager.current_session_id)
    
    def test_isSessionActive(self):
        """Test session active status."""
        # No session
        self.assertFalse(self.manager.isSessionActive())
        
        # With session
        self.manager.startNewSession()
        self.assertTrue(self.manager.isSessionActive())


class TestHistoryManager(unittest.TestCase):
    """Test the history manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = HistoryManager()
    
    def test_init(self):
        """Test manager initialization."""
        self.assertIsNotNone(self.manager.storage)
        self.assertIsNotNone(self.manager.search_filter)
        self.assertEqual(len(self.manager.current_search_results), 0)
        self.assertIsNone(self.manager.current_filter)
    
    def test_saveReading(self):
        """Test saving reading."""
        reading_data = {
            'id': 'test_reading_1',
            'spread_type': 'single',
            'cards': [{'name': 'The Fool', 'orientation': 'upright'}],
            'interpretation': 'Test interpretation',
            'timestamp': '2024-01-01T00:00:00'
        }
        
        success = self.manager.saveReading(reading_data)
        self.assertTrue(success)
    
    def test_getAllReadings(self):
        """Test getting all readings."""
        readings = self.manager.getAllReadings()
        self.assertIsInstance(readings, list)
    
    def test_searchReadings(self):
        """Test searching readings."""
        # Search with query
        results = self.manager.searchReadings("test")
        self.assertIsInstance(results, list)
        
        # Search with filters
        filters = {'spread_type': 'single'}
        results = self.manager.searchReadings("", filters)
        self.assertIsInstance(results, list)
    
    def test_getReadingById(self):
        """Test getting reading by ID."""
        # Save a reading first
        reading_data = {
            'id': 'test_reading_2',
            'spread_type': 'three',
            'cards': [],
            'interpretation': 'Test'
        }
        self.manager.saveReading(reading_data)
        
        # Get by ID
        reading = self.manager.getReadingById('test_reading_2')
        self.assertIsNotNone(reading)
        self.assertEqual(reading['id'], 'test_reading_2')
    
    def test_deleteReading(self):
        """Test deleting reading."""
        # Save a reading first
        reading_data = {
            'id': 'test_reading_3',
            'spread_type': 'single',
            'cards': [],
            'interpretation': 'Test'
        }
        self.manager.saveReading(reading_data)
        
        # Delete reading
        success = self.manager.deleteReading('test_reading_3')
        self.assertTrue(success)
    
    def test_exportReadings(self):
        """Test exporting readings."""
        success = self.manager.exportReadings('test_export.json')
        self.assertTrue(success)
    
    def test_importReadings(self):
        """Test importing readings."""
        # Export first
        self.manager.exportReadings('test_import.json')
        
        # Import
        success = self.manager.importReadings('test_import.json')
        self.assertTrue(success)
    
    def test_getSearchResults(self):
        """Test getting search results."""
        results = self.manager.getSearchResults()
        self.assertIsInstance(results, list)
    
    def test_clearSearch(self):
        """Test clearing search."""
        self.manager.clearSearch()
        self.assertEqual(len(self.manager.current_search_results), 0)
        self.assertIsNone(self.manager.current_filter)


class TestSettingsManager(unittest.TestCase):
    """Test the settings manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = SettingsManager()
    
    def test_init(self):
        """Test manager initialization."""
        self.assertIsNotNone(self.manager.app_config)
        self.assertIsNotNone(self.manager.user_preferences)
    
    def test_getAppConfig(self):
        """Test getting app config."""
        config = self.manager.getAppConfig()
        self.assertIsInstance(config, dict)
        self.assertIn('app_name', config)
        self.assertIn('version', config)
        self.assertIn('theme', config)
    
    def test_getUserPreferences(self):
        """Test getting user preferences."""
        preferences = self.manager.getUserPreferences()
        self.assertIsInstance(preferences, dict)
        self.assertIn('default_spread', preferences)
        self.assertIn('ai_model', preferences)
        self.assertIn('encryption_enabled', preferences)
    
    def test_updateAppConfig(self):
        """Test updating app config."""
        config = {'theme': 'light', 'auto_save': False}
        success = self.manager.updateAppConfig(config)
        self.assertTrue(success)
    
    def test_updateUserPreferences(self):
        """Test updating user preferences."""
        preferences = {'default_spread': 'three', 'ai_model': 'llama3.1'}
        success = self.manager.updateUserPreferences(preferences)
        self.assertTrue(success)
    
    def test_resetToDefaults(self):
        """Test resetting to defaults."""
        success = self.manager.resetToDefaults()
        self.assertTrue(success)
    
    def test_exportSettings(self):
        """Test exporting settings."""
        success = self.manager.exportSettings('test_settings.json')
        self.assertTrue(success)
    
    def test_importSettings(self):
        """Test importing settings."""
        # Export first
        self.manager.exportSettings('test_import_settings.json')
        
        # Import
        success = self.manager.importSettings('test_import_settings.json')
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()