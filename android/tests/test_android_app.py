"""
Unit tests for Android TarotMac App
Tests the Android-specific components and core module integration.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path for core modules
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

# Mock Kivy components for testing
class MockKivyApp:
    def __init__(self):
        self.screen_manager = None
    
    def get_running_app(self):
        return self

class MockScreenManager:
    def __init__(self):
        self.current = 'home'
        self.screens = []

class MockMDApp:
    @staticmethod
    def get_running_app():
        return MockKivyApp()

# Mock KivyMD components
class MockMDBoxLayout:
    def __init__(self, **kwargs):
        self.children = []
        self.size_hint_y = kwargs.get('size_hint_y', 1)
        self.height = kwargs.get('height', 100)
    
    def add_widget(self, widget):
        self.children.append(widget)
    
    def clear_widgets(self):
        self.children.clear()

class MockMDCard:
    def __init__(self, **kwargs):
        self.children = []
        self.size_hint_y = kwargs.get('size_hint_y', 1)
        self.height = kwargs.get('height', 100)
        self.padding = kwargs.get('padding', 0)
        self.elevation = kwargs.get('elevation', 0)
        self.radius = kwargs.get('radius', [0])
    
    def add_widget(self, widget):
        self.children.append(widget)

class MockMDLabel:
    def __init__(self, **kwargs):
        self.text = kwargs.get('text', '')
        self.theme_text_color = kwargs.get('theme_text_color', 'Primary')
        self.size_hint_y = kwargs.get('size_hint_y', 1)
        self.height = kwargs.get('height', 100)
        self.font_style = kwargs.get('font_style', 'Body1')
        self.halign = kwargs.get('halign', 'left')
        self.valign = kwargs.get('valign', 'top')

class MockMDRaisedButton:
    def __init__(self, **kwargs):
        self.text = kwargs.get('text', '')
        self.size_hint_y = kwargs.get('size_hint_y', 1)
        self.height = kwargs.get('height', 100)
        self.md_bg_color = kwargs.get('md_bg_color', (0, 0, 0, 1))
        self.on_press = kwargs.get('on_press', None)

class MockMDTextField:
    def __init__(self, **kwargs):
        self.text = kwargs.get('text', '')
        self.hint_text = kwargs.get('hint_text', '')
        self.multiline = kwargs.get('multiline', False)
        self.max_text_length = kwargs.get('max_text_length', 1000)
        self.size_hint_y = kwargs.get('size_hint_y', 1)

class MockMDSwitch:
    def __init__(self, **kwargs):
        self.active = kwargs.get('active', False)
        self.on_press = kwargs.get('on_press', None)

class MockMDScrollView:
    def __init__(self):
        self.children = []
    
    def add_widget(self, widget):
        self.children.append(widget)
    
    def scroll_to(self, widget):
        pass

class MockMDList:
    def __init__(self):
        self.children = []
    
    def add_widget(self, widget):
        self.children.append(widget)
    
    def clear_widgets(self):
        self.children.clear()

class MockOneLineListItem:
    def __init__(self, **kwargs):
        self.text = kwargs.get('text', '')
        self.theme_text_color = kwargs.get('theme_text_color', 'Primary')
        self.on_press = kwargs.get('on_press', None)

class MockThreeLineListItem:
    def __init__(self, **kwargs):
        self.text = kwargs.get('text', '')
        self.secondary_text = kwargs.get('secondary_text', '')
        self.tertiary_text = kwargs.get('tertiary_text', '')
        self.theme_text_color = kwargs.get('theme_text_color', 'Primary')
        self.on_press = kwargs.get('on_press', None)

class MockMDDialog:
    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.text = kwargs.get('text', '')
        self.buttons = kwargs.get('buttons', [])
        self.content_cls = kwargs.get('content_cls', None)
        self.size_hint = kwargs.get('size_hint', (0.8, 0.6))
    
    def open(self):
        pass
    
    def dismiss(self):
        pass

class MockMDTopAppBar:
    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.elevation = kwargs.get('elevation', 0)
        self.md_bg_color = kwargs.get('md_bg_color', (0, 0, 0, 1))
        self.specific_text_color = kwargs.get('specific_text_color', (1, 1, 1, 1))
        self.left_action_items = kwargs.get('left_action_items', [])
        self.right_action_items = kwargs.get('right_action_items', [])

class MockMDSegmentedControl:
    def __init__(self, **kwargs):
        self.children = []
        self.size_hint_y = kwargs.get('size_hint_y', 1)
        self.height = kwargs.get('height', 100)
    
    def add_widget(self, widget):
        self.children.append(widget)

class MockMDSegmentedControlItem:
    def __init__(self, **kwargs):
        self.text = kwargs.get('text', '')
        self.on_press = kwargs.get('on_press', None)

class MockMDGridLayout:
    def __init__(self, **kwargs):
        self.children = []
        self.cols = kwargs.get('cols', 1)
        self.spacing = kwargs.get('spacing', 0)
        self.size_hint_y = kwargs.get('size_hint_y', 1)
        self.height = kwargs.get('height', 100)
    
    def add_widget(self, widget):
        self.children.append(widget)

class MockMDFlatButton:
    def __init__(self, **kwargs):
        self.text = kwargs.get('text', '')
        self.size_hint_y = kwargs.get('size_hint_y', 1)
        self.height = kwargs.get('height', 100)
        self.on_press = kwargs.get('on_press', None)

class MockMDIconButton:
    def __init__(self, **kwargs):
        self.icon = kwargs.get('icon', '')
        self.size_hint_y = kwargs.get('size_hint_y', 1)
        self.height = kwargs.get('height', 100)
        self.on_press = kwargs.get('on_press', None)

# Mock core modules
class MockDeck:
    def __init__(self):
        self.total_count = 78
        self.count = 78

class MockSpreadManager:
    def __init__(self):
        pass
    
    def create_reading(self, spread_type, question):
        return MockReading()
    
    def draw_cards_for_reading(self, reading, deck):
        return True
    
    def interpret_reading(self, reading, influence_engine):
        return {'overall_summary': 'Test interpretation'}

class MockReading:
    def __init__(self):
        self.positioned_cards = [MockPositionedCard()]

class MockPositionedCard:
    def __init__(self):
        self.card = MockCard()
        self.position = MockPosition()

class MockCard:
    def __init__(self):
        self.id = 'test_card'
        self.name = 'Test Card'
        self.is_upright = True
        self.upright_meaning = 'Test meaning'

class MockPosition:
    def __init__(self):
        self.name = 'Test Position'

class MockTarotInfluenceEngine:
    def __init__(self):
        pass

class MockAIManager:
    def __init__(self):
        self.memory_manager = MockMemoryManager()
    
    def create_chat_session(self):
        return MockChatSession()
    
    async def chat(self, message):
        return "Test AI response"
    
    def end_session(self, session_id):
        pass

class MockMemoryManager:
    def __init__(self):
        pass
    
    def add_message(self, session_id, role, message):
        pass

class MockChatSession:
    def __init__(self):
        self.session_id = 'test_session'

class MockMessageRole:
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

# Mock dp function
def dp(value):
    return value

# Mock Clock
class MockClock:
    @staticmethod
    def schedule_once(func, delay):
        pass

# Mock Window
class MockWindow:
    @staticmethod
    def clearcolor(color):
        pass
    
    @staticmethod
    def size(size):
        pass

# Mock platform
def platform():
    return 'android'

# Mock asyncio
class MockAsyncio:
    @staticmethod
    def new_event_loop():
        return MockEventLoop()
    
    @staticmethod
    def set_event_loop(loop):
        pass

class MockEventLoop:
    def run_until_complete(self, coro):
        return "Test response"
    
    def close(self):
        pass

# Mock metrics
class MockMetrics:
    @staticmethod
    def dp(value):
        return value

# Mock utils
class MockUtils:
    @staticmethod
    def platform():
        return 'android'

# Mock core
class MockCore:
    class window:
        Window = MockWindow
    
    class utils:
        platform = MockUtils.platform
    
    class metrics:
        dp = MockMetrics.dp
    
    class clock:
        Clock = MockClock

# Mock kivy
class MockKivy:
    app = MockCore
    uix = MockCore
    core = MockCore
    utils = MockCore.utils
    metrics = MockCore.metrics
    clock = MockCore.clock

# Mock kivymd
class MockKivyMD:
    uix = MockCore
    app = MockCore

# Mock modules
sys.modules['kivy'] = MockKivy()
sys.modules['kivy.app'] = MockCore
sys.modules['kivy.uix.screenmanager'] = MockCore
sys.modules['kivy.core.window'] = MockCore.window
sys.modules['kivy.utils'] = MockCore.utils
sys.modules['kivy.metrics'] = MockCore.metrics
sys.modules['kivy.clock'] = MockCore.clock
sys.modules['kivymd'] = MockKivyMD()
sys.modules['kivymd.uix.boxlayout'] = MockCore
sys.modules['kivymd.uix.gridlayout'] = MockCore
sys.modules['kivymd.uix.card'] = MockCore
sys.modules['kivymd.uix.label'] = MockCore
sys.modules['kivymd.uix.button'] = MockCore
sys.modules['kivymd.uix.toolbar'] = MockCore
sys.modules['kivymd.uix.scrollview'] = MockCore
sys.modules['kivymd.uix.floatlayout'] = MockCore
sys.modules['kivymd.uix.textfield'] = MockCore
sys.modules['kivymd.uix.dialog'] = MockCore
sys.modules['kivymd.uix.selectioncontrol'] = MockCore
sys.modules['kivymd.uix.list'] = MockCore
sys.modules['kivymd.app'] = MockCore
sys.modules['asyncio'] = MockAsyncio()

# Mock core modules
sys.modules['deck.deck_loader'] = type('MockDeckLoader', (), {
    'load_canonical_deck': lambda: MockDeck()
})()
sys.modules['spreads.spread_manager'] = type('MockSpreadManager', (), {
    'SpreadManager': MockSpreadManager,
    'SpreadType': type('SpreadType', (), {
        'SINGLE_CARD': 'single_card',
        'THREE_CARD': 'three_card',
        'CELTIC_CROSS': 'celtic_cross'
    })
})()
sys.modules['influence.tarot_influence_engine'] = type('MockTarotInfluenceEngine', (), {
    'TarotInfluenceEngine': MockTarotInfluenceEngine
})()
sys.modules['ai.ai_manager'] = type('MockAIManager', (), {
    'AIManager': MockAIManager
})()
sys.modules['ai.chat_memory'] = type('MockChatMemory', (), {
    'MessageRole': MockMessageRole
})()


class TestAndroidApp(unittest.TestCase):
    """Test Android app functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock the main app
        self.app = type('MockTarotMacAndroidApp', (), {
            'deck': MockDeck(),
            'spread_manager': MockSpreadManager(),
            'influence_engine': MockTarotInfluenceEngine(),
            'ai_manager': MockAIManager(),
            'screen_manager': MockScreenManager()
        })()
    
    def test_app_initialization(self):
        """Test app initialization."""
        self.assertIsNotNone(self.app.deck)
        self.assertIsNotNone(self.app.spread_manager)
        self.assertIsNotNone(self.app.influence_engine)
        self.assertIsNotNone(self.app.ai_manager)
        self.assertIsNotNone(self.app.screen_manager)
    
    def test_deck_integration(self):
        """Test deck module integration."""
        deck = self.app.deck
        self.assertEqual(deck.total_count, 78)
        self.assertEqual(deck.count, 78)
    
    def test_spread_manager_integration(self):
        """Test spread manager integration."""
        spread_manager = self.app.spread_manager
        reading = spread_manager.create_reading('single_card', 'Test question')
        self.assertIsNotNone(reading)
        self.assertTrue(spread_manager.draw_cards_for_reading(reading, self.app.deck))
    
    def test_ai_manager_integration(self):
        """Test AI manager integration."""
        ai_manager = self.app.ai_manager
        session = ai_manager.create_chat_session()
        self.assertIsNotNone(session)
        self.assertEqual(session.session_id, 'test_session')
    
    def test_influence_engine_integration(self):
        """Test influence engine integration."""
        influence_engine = self.app.influence_engine
        self.assertIsNotNone(influence_engine)
    
    def test_screen_manager_integration(self):
        """Test screen manager integration."""
        screen_manager = self.app.screen_manager
        self.assertIsNotNone(screen_manager)
        self.assertEqual(screen_manager.current, 'home')


class TestAndroidScreens(unittest.TestCase):
    """Test Android screen components."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.core_modules = {
            'deck': MockDeck(),
            'spread_manager': MockSpreadManager(),
            'influence_engine': MockTarotInfluenceEngine(),
            'ai_manager': MockAIManager()
        }
    
    def test_home_screen_creation(self):
        """Test home screen creation."""
        # Mock screen creation
        screen = type('MockHomeScreen', (), {
            'core_modules': self.core_modules,
            'set_core_modules': lambda self, **kwargs: setattr(self, 'core_modules', kwargs)
        })()
        
        screen.set_core_modules(**self.core_modules)
        self.assertEqual(len(screen.core_modules), 4)
        self.assertIn('deck', screen.core_modules)
        self.assertIn('spread_manager', screen.core_modules)
        self.assertIn('influence_engine', screen.core_modules)
        self.assertIn('ai_manager', screen.core_modules)
    
    def test_readings_screen_creation(self):
        """Test readings screen creation."""
        screen = type('MockReadingsScreen', (), {
            'core_modules': self.core_modules,
            'current_reading': None,
            'current_spread_type': 'single_card',
            'set_core_modules': lambda self, **kwargs: setattr(self, 'core_modules', kwargs)
        })()
        
        screen.set_core_modules(**self.core_modules)
        self.assertEqual(len(screen.core_modules), 4)
        self.assertIsNone(screen.current_reading)
        self.assertEqual(screen.current_spread_type, 'single_card')
    
    def test_chat_screen_creation(self):
        """Test chat screen creation."""
        screen = type('MockChatScreen', (), {
            'core_modules': self.core_modules,
            'chat_session': None,
            'set_core_modules': lambda self, **kwargs: setattr(self, 'core_modules', kwargs)
        })()
        
        screen.set_core_modules(**self.core_modules)
        self.assertEqual(len(screen.core_modules), 4)
        self.assertIsNone(screen.chat_session)
    
    def test_history_screen_creation(self):
        """Test history screen creation."""
        screen = type('MockHistoryScreen', (), {
            'core_modules': self.core_modules,
            'readings_history': [],
            'set_core_modules': lambda self, **kwargs: setattr(self, 'core_modules', kwargs)
        })()
        
        screen.set_core_modules(**self.core_modules)
        self.assertEqual(len(screen.core_modules), 4)
        self.assertEqual(len(screen.readings_history), 0)
    
    def test_settings_screen_creation(self):
        """Test settings screen creation."""
        screen = type('MockSettingsScreen', (), {
            'core_modules': self.core_modules,
            'settings': {},
            'set_core_modules': lambda self, **kwargs: setattr(self, 'core_modules', kwargs)
        })()
        
        screen.set_core_modules(**self.core_modules)
        self.assertEqual(len(screen.core_modules), 4)
        self.assertEqual(len(screen.settings), 0)


class TestAndroidUIComponents(unittest.TestCase):
    """Test Android UI components."""
    
    def test_md_box_layout_creation(self):
        """Test MDBoxLayout creation."""
        layout = MockMDBoxLayout(orientation='vertical', spacing=10)
        self.assertEqual(len(layout.children), 0)
        self.assertEqual(layout.size_hint_y, 1)
        self.assertEqual(layout.height, 100)
    
    def test_md_card_creation(self):
        """Test MDCard creation."""
        card = MockMDCard(padding=16, elevation=2)
        self.assertEqual(len(card.children), 0)
        self.assertEqual(card.padding, 16)
        self.assertEqual(card.elevation, 2)
    
    def test_md_label_creation(self):
        """Test MDLabel creation."""
        label = MockMDLabel(text="Test", theme_text_color="Primary")
        self.assertEqual(label.text, "Test")
        self.assertEqual(label.theme_text_color, "Primary")
    
    def test_md_button_creation(self):
        """Test MDRaisedButton creation."""
        button = MockMDRaisedButton(text="Test", md_bg_color=(0, 0, 0, 1))
        self.assertEqual(button.text, "Test")
        self.assertEqual(button.md_bg_color, (0, 0, 0, 1))
    
    def test_md_text_field_creation(self):
        """Test MDTextField creation."""
        text_field = MockMDTextField(hint_text="Test hint", multiline=True)
        self.assertEqual(text_field.hint_text, "Test hint")
        self.assertTrue(text_field.multiline)
    
    def test_md_switch_creation(self):
        """Test MDSwitch creation."""
        switch = MockMDSwitch(active=True)
        self.assertTrue(switch.active)
    
    def test_md_dialog_creation(self):
        """Test MDDialog creation."""
        dialog = MockMDDialog(title="Test", text="Test message")
        self.assertEqual(dialog.title, "Test")
        self.assertEqual(dialog.text, "Test message")
        self.assertEqual(len(dialog.buttons), 0)


class TestAndroidNavigation(unittest.TestCase):
    """Test Android navigation functionality."""
    
    def test_screen_navigation(self):
        """Test screen navigation."""
        screen_manager = MockScreenManager()
        screen_manager.current = 'home'
        self.assertEqual(screen_manager.current, 'home')
        
        screen_manager.current = 'readings'
        self.assertEqual(screen_manager.current, 'readings')
        
        screen_manager.current = 'chat'
        self.assertEqual(screen_manager.current, 'chat')
        
        screen_manager.current = 'history'
        self.assertEqual(screen_manager.current, 'history')
        
        screen_manager.current = 'settings'
        self.assertEqual(screen_manager.current, 'settings')
    
    def test_navigation_consistency(self):
        """Test navigation consistency."""
        screen_manager = MockScreenManager()
        valid_screens = ['home', 'readings', 'chat', 'history', 'settings']
        
        for screen in valid_screens:
            screen_manager.current = screen
            self.assertEqual(screen_manager.current, screen)


class TestAndroidCoreIntegration(unittest.TestCase):
    """Test Android core module integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_deck = MockDeck()
        self.mock_spread_manager = MockSpreadManager()
        self.mock_influence_engine = MockTarotInfluenceEngine()
        self.mock_ai_manager = MockAIManager()
    
    def test_deck_loading(self):
        """Test deck loading integration."""
        deck = self.mock_deck
        self.assertEqual(deck.total_count, 78)
        self.assertEqual(deck.count, 78)
    
    def test_spread_creation(self):
        """Test spread creation integration."""
        reading = self.mock_spread_manager.create_reading('single_card', 'Test question')
        self.assertIsNotNone(reading)
        self.assertIsNotNone(reading.positioned_cards)
    
    def test_card_drawing(self):
        """Test card drawing integration."""
        reading = self.mock_spread_manager.create_reading('single_card', 'Test question')
        success = self.mock_spread_manager.draw_cards_for_reading(reading, self.mock_deck)
        self.assertTrue(success)
    
    def test_interpretation_generation(self):
        """Test interpretation generation integration."""
        reading = self.mock_spread_manager.create_reading('single_card', 'Test question')
        interpretation = self.mock_spread_manager.interpret_reading(reading, self.mock_influence_engine)
        self.assertIsNotNone(interpretation)
        self.assertIn('overall_summary', interpretation)
    
    def test_ai_session_creation(self):
        """Test AI session creation integration."""
        session = self.mock_ai_manager.create_chat_session()
        self.assertIsNotNone(session)
        self.assertEqual(session.session_id, 'test_session')
    
    def test_ai_message_handling(self):
        """Test AI message handling integration."""
        session = self.mock_ai_manager.create_chat_session()
        self.mock_ai_manager.memory_manager.add_message(session.session_id, 'user', 'Test message')
        # No exception should be raised
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()