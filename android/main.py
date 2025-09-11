#!/usr/bin/env python3
"""
Android TarotMac Application
Main entry point for the Android version of the tarot application.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to Python path to access core modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.utils import platform

# Import our Android-specific screens
from android.screens.home_screen import HomeScreen
from android.screens.readings_screen import ReadingsScreen
from android.screens.chat_screen import ChatScreen
from android.screens.history_screen import HistoryScreen
from android.screens.settings_screen import SettingsScreen

# Import core modules
from deck.deck_loader import DeckLoader
from spreads.spread_manager import SpreadManager
from influence.tarot_influence_engine import TarotInfluenceEngine
from ai.ai_manager import AIManager


class TarotMacAndroidApp(App):
    """
    Main Android application class for TarotMac.
    Integrates all core modules with mobile-optimized UI.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "TarotMac"
        self.icon = "assets/icon.png"
        
        # Initialize core modules
        self.deck = None
        self.spread_manager = None
        self.influence_engine = None
        self.ai_manager = None
        
        # Screen manager for navigation
        self.screen_manager = None
        
        # Initialize core modules
        self._initialize_core_modules()
    
    def _initialize_core_modules(self):
        """Initialize all core modules for the Android app."""
        try:
            # Load the canonical deck
            self.deck = DeckLoader.load_canonical_deck()
            print(f"✅ Deck loaded: {self.deck.total_count} cards")
            
            # Initialize spread manager
            self.spread_manager = SpreadManager()
            print("✅ Spread manager initialized")
            
            # Initialize influence engine
            self.influence_engine = TarotInfluenceEngine()
            print("✅ Influence engine initialized")
            
            # Initialize AI manager
            self.ai_manager = AIManager()
            print("✅ AI manager initialized")
            
        except Exception as e:
            print(f"❌ Error initializing core modules: {e}")
            # Continue with None values - screens will handle gracefully
    
    def build(self):
        """Build the Android application UI."""
        # Configure window for mobile
        if platform == 'android':
            Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Light gray background
        else:
            # For testing on desktop
            Window.size = (360, 640)  # Mobile-like dimensions
        
        # Create screen manager
        self.screen_manager = ScreenManager()
        
        # Add all screens
        screens = [
            ('home', HomeScreen(name='home')),
            ('readings', ReadingsScreen(name='readings')),
            ('chat', ChatScreen(name='chat')),
            ('history', HistoryScreen(name='history')),
            ('settings', SettingsScreen(name='settings'))
        ]
        
        for screen_id, screen in screens:
            self.screen_manager.add_widget(screen)
        
        # Set initial screen
        self.screen_manager.current = 'home'
        
        return self.screen_manager
    
    def on_start(self):
        """Called when the app starts."""
        print("🚀 TarotMac Android app started")
        
        # Pass core modules to screens
        for screen in self.screen_manager.screens:
            if hasattr(screen, 'set_core_modules'):
                screen.set_core_modules(
                    deck=self.deck,
                    spread_manager=self.spread_manager,
                    influence_engine=self.influence_engine,
                    ai_manager=self.ai_manager
                )
    
    def on_pause(self):
        """Called when the app is paused (Android lifecycle)."""
        print("⏸️ App paused")
        return True
    
    def on_resume(self):
        """Called when the app is resumed (Android lifecycle)."""
        print("▶️ App resumed")
    
    def on_stop(self):
        """Called when the app is stopped."""
        print("🛑 App stopped")


def main():
    """Main entry point for the Android application."""
    try:
        app = TarotMacAndroidApp()
        app.run()
    except Exception as e:
        print(f"❌ Fatal error starting Android app: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()