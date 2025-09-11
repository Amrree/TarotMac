"""
Home Screen for Android TarotMac App
Main dashboard with navigation to all features.
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.app import MDApp
from kivy.metrics import dp


class HomeScreen(Screen):
    """
    Home screen with dashboard and navigation.
    Mobile-optimized with Material Design components.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.core_modules = {}
        self._build_ui()
    
    def set_core_modules(self, deck=None, spread_manager=None, 
                        influence_engine=None, ai_manager=None):
        """Set core modules for this screen."""
        self.core_modules = {
            'deck': deck,
            'spread_manager': spread_manager,
            'influence_engine': influence_engine,
            'ai_manager': ai_manager
        }
    
    def _build_ui(self):
        """Build the home screen UI."""
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=dp(16)
        )
        
        # Top app bar
        toolbar = MDTopAppBar(
            title="TarotMac",
            elevation=4,
            md_bg_color=(0.2, 0.6, 0.8, 1),  # Blue theme
            specific_text_color=(1, 1, 1, 1)
        )
        main_layout.add_widget(toolbar)
        
        # Scrollable content
        scroll_view = MDScrollView()
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            size_hint_y=None,
            height=dp(800)  # Adjust based on content
        )
        
        # Welcome section
        welcome_card = self._create_welcome_card()
        content_layout.add_widget(welcome_card)
        
        # Quick actions grid
        actions_card = self._create_actions_card()
        content_layout.add_widget(actions_card)
        
        # Recent readings card
        recent_card = self._create_recent_readings_card()
        content_layout.add_widget(recent_card)
        
        # App status card
        status_card = self._create_status_card()
        content_layout.add_widget(status_card)
        
        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)
        
        self.add_widget(main_layout)
    
    def _create_welcome_card(self):
        """Create welcome card with app introduction."""
        card = MDCard(
            size_hint_y=None,
            height=dp(120),
            padding=dp(16),
            elevation=2,
            radius=[dp(12)]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8)
        )
        
        title = MDLabel(
            text="Welcome to TarotMac",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(32),
            font_style="H5"
        )
        
        subtitle = MDLabel(
            text="Your personal tarot companion with AI insights",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(24),
            font_style="Body1"
        )
        
        layout.add_widget(title)
        layout.add_widget(subtitle)
        card.add_widget(layout)
        
        return card
    
    def _create_actions_card(self):
        """Create quick actions card with navigation buttons."""
        card = MDCard(
            size_hint_y=None,
            height=dp(200),
            padding=dp(16),
            elevation=2,
            radius=[dp(12)]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(12)
        )
        
        title = MDLabel(
            text="Quick Actions",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(32),
            font_style="H6"
        )
        layout.add_widget(title)
        
        # Action buttons grid
        actions_grid = MDGridLayout(
            cols=2,
            spacing=dp(12),
            size_hint_y=None,
            height=dp(120)
        )
        
        # Single card reading
        single_card_btn = MDRaisedButton(
            text="Single Card",
            size_hint_y=None,
            height=dp(48),
            md_bg_color=(0.2, 0.6, 0.8, 1),
            on_press=self._navigate_to_readings
        )
        actions_grid.add_widget(single_card_btn)
        
        # Three card spread
        three_card_btn = MDRaisedButton(
            text="Three Card",
            size_hint_y=None,
            height=dp(48),
            md_bg_color=(0.2, 0.6, 0.8, 1),
            on_press=self._navigate_to_readings
        )
        actions_grid.add_widget(three_card_btn)
        
        # Chat with AI
        chat_btn = MDRaisedButton(
            text="Chat with AI",
            size_hint_y=None,
            height=dp(48),
            md_bg_color=(0.6, 0.2, 0.8, 1),
            on_press=self._navigate_to_chat
        )
        actions_grid.add_widget(chat_btn)
        
        # View history
        history_btn = MDRaisedButton(
            text="View History",
            size_hint_y=None,
            height=dp(48),
            md_bg_color=(0.8, 0.6, 0.2, 1),
            on_press=self._navigate_to_history
        )
        actions_grid.add_widget(history_btn)
        
        layout.add_widget(actions_grid)
        card.add_widget(layout)
        
        return card
    
    def _create_recent_readings_card(self):
        """Create recent readings card."""
        card = MDCard(
            size_hint_y=None,
            height=dp(150),
            padding=dp(16),
            elevation=2,
            radius=[dp(12)]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8)
        )
        
        title = MDLabel(
            text="Recent Readings",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(32),
            font_style="H6"
        )
        layout.add_widget(title)
        
        # Placeholder for recent readings
        recent_text = MDLabel(
            text="No recent readings yet.\nStart with a single card reading!",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(80),
            font_style="Body2",
            halign="center"
        )
        layout.add_widget(recent_text)
        
        card.add_widget(layout)
        
        return card
    
    def _create_status_card(self):
        """Create app status card."""
        card = MDCard(
            size_hint_y=None,
            height=dp(100),
            padding=dp(16),
            elevation=2,
            radius=[dp(12)]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8)
        )
        
        title = MDLabel(
            text="App Status",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(24),
            font_style="H6"
        )
        layout.add_widget(title)
        
        # Status indicators
        status_text = self._get_status_text()
        status_label = MDLabel(
            text=status_text,
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(48),
            font_style="Body2"
        )
        layout.add_widget(status_label)
        
        card.add_widget(layout)
        
        return card
    
    def _get_status_text(self):
        """Get current app status text."""
        status_parts = []
        
        if self.core_modules.get('deck'):
            status_parts.append("✅ Deck loaded")
        else:
            status_parts.append("❌ Deck not loaded")
        
        if self.core_modules.get('ai_manager'):
            status_parts.append("✅ AI ready")
        else:
            status_parts.append("❌ AI not ready")
        
        return "\n".join(status_parts)
    
    def _navigate_to_readings(self, instance):
        """Navigate to readings screen."""
        app = MDApp.get_running_app()
        if app and hasattr(app, 'screen_manager'):
            app.screen_manager.current = 'readings'
    
    def _navigate_to_chat(self, instance):
        """Navigate to chat screen."""
        app = MDApp.get_running_app()
        if app and hasattr(app, 'screen_manager'):
            app.screen_manager.current = 'chat'
    
    def _navigate_to_history(self, instance):
        """Navigate to history screen."""
        app = MDApp.get_running_app()
        if app and hasattr(app, 'screen_manager'):
            app.screen_manager.current = 'history'