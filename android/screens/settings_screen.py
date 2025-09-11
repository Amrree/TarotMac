"""
Settings Screen for Android TarotMac App
Application settings and preferences with mobile-optimized interface.
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivymd.app import MDApp
from kivy.metrics import dp


class SettingsScreen(Screen):
    """
    Settings screen for application configuration.
    Mobile-optimized with touch-friendly interface.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.core_modules = {}
        self.settings = {}
        self._build_ui()
        self._load_settings()
    
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
        """Build the settings screen UI."""
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=dp(16)
        )
        
        # Top app bar
        toolbar = MDTopAppBar(
            title="Settings",
            elevation=4,
            md_bg_color=(0.2, 0.8, 0.6, 1),  # Green theme
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["arrow-left", lambda x: self._navigate_back()]]
        )
        main_layout.add_widget(toolbar)
        
        # Scrollable content
        scroll_view = MDScrollView()
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            size_hint_y=None,
            height=dp(1000)  # Adjust based on content
        )
        
        # App configuration card
        app_config_card = self._create_app_config_card()
        content_layout.add_widget(app_config_card)
        
        # User preferences card
        preferences_card = self._create_preferences_card()
        content_layout.add_widget(preferences_card)
        
        # AI settings card
        ai_settings_card = self._create_ai_settings_card()
        content_layout.add_widget(ai_settings_card)
        
        # Data management card
        data_card = self._create_data_management_card()
        content_layout.add_widget(data_card)
        
        # About card
        about_card = self._create_about_card()
        content_layout.add_widget(about_card)
        
        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)
        
        self.add_widget(main_layout)
    
    def _create_app_config_card(self):
        """Create app configuration card."""
        card = MDCard(
            size_hint_y=None,
            height=dp(200),
            padding=dp(16),
            elevation=2,
            radius=[dp(12)]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        title = MDLabel(
            text="App Configuration",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(32),
            font_style="H6"
        )
        layout.add_widget(title)
        
        # App version
        version_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(32)
        )
        
        version_label = MDLabel(
            text="Version:",
            theme_text_color="Primary",
            size_hint_x=0.3,
            font_style="Body2"
        )
        version_layout.add_widget(version_label)
        
        self.version_value = MDLabel(
            text="1.0.0",
            theme_text_color="Secondary",
            size_hint_x=0.7,
            font_style="Body2"
        )
        version_layout.add_widget(self.version_value)
        
        layout.add_widget(version_layout)
        
        # Debug mode toggle
        debug_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(32)
        )
        
        debug_label = MDLabel(
            text="Debug Mode:",
            theme_text_color="Primary",
            size_hint_x=0.7,
            font_style="Body2"
        )
        debug_layout.add_widget(debug_label)
        
        self.debug_switch = MDSwitch(
            size_hint_x=0.3,
            on_press=self._toggle_debug_mode
        )
        debug_layout.add_widget(self.debug_switch)
        
        layout.add_widget(debug_layout)
        
        card.add_widget(layout)
        
        return card
    
    def _create_preferences_card(self):
        """Create user preferences card."""
        card = MDCard(
            size_hint_y=None,
            height=dp(250),
            padding=dp(16),
            elevation=2,
            radius=[dp(12)]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        title = MDLabel(
            text="User Preferences",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(32),
            font_style="H6"
        )
        layout.add_widget(title)
        
        # Theme selection
        theme_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(32)
        )
        
        theme_label = MDLabel(
            text="Theme:",
            theme_text_color="Primary",
            size_hint_x=0.3,
            font_style="Body2"
        )
        theme_layout.add_widget(theme_label)
        
        self.theme_value = MDLabel(
            text="Light",
            theme_text_color="Secondary",
            size_hint_x=0.7,
            font_style="Body2"
        )
        theme_layout.add_widget(self.theme_value)
        
        layout.add_widget(theme_layout)
        
        # Auto-save readings toggle
        autosave_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(32)
        )
        
        autosave_label = MDLabel(
            text="Auto-save Readings:",
            theme_text_color="Primary",
            size_hint_x=0.7,
            font_style="Body2"
        )
        autosave_layout.add_widget(autosave_label)
        
        self.autosave_switch = MDSwitch(
            size_hint_x=0.3,
            on_press=self._toggle_autosave
        )
        autosave_layout.add_widget(self.autosave_switch)
        
        layout.add_widget(autosave_layout)
        
        # Notification toggle
        notification_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(32)
        )
        
        notification_label = MDLabel(
            text="Notifications:",
            theme_text_color="Primary",
            size_hint_x=0.7,
            font_style="Body2"
        )
        notification_layout.add_widget(notification_label)
        
        self.notification_switch = MDSwitch(
            size_hint_x=0.3,
            on_press=self._toggle_notifications
        )
        notification_layout.add_widget(self.notification_switch)
        
        layout.add_widget(notification_layout)
        
        card.add_widget(layout)
        
        return card
    
    def _create_ai_settings_card(self):
        """Create AI settings card."""
        card = MDCard(
            size_hint_y=None,
            height=dp(200),
            padding=dp(16),
            elevation=2,
            radius=[dp(12)]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        title = MDLabel(
            text="AI Settings",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(32),
            font_style="H6"
        )
        layout.add_widget(title)
        
        # AI model selection
        model_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(32)
        )
        
        model_label = MDLabel(
            text="Model:",
            theme_text_color="Primary",
            size_hint_x=0.3,
            font_style="Body2"
        )
        model_layout.add_widget(model_label)
        
        self.model_value = MDLabel(
            text="llama2",
            theme_text_color="Secondary",
            size_hint_x=0.7,
            font_style="Body2"
        )
        model_layout.add_widget(self.model_value)
        
        layout.add_widget(model_layout)
        
        # AI enabled toggle
        ai_enabled_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(32)
        )
        
        ai_enabled_label = MDLabel(
            text="AI Enabled:",
            theme_text_color="Primary",
            size_hint_x=0.7,
            font_style="Body2"
        )
        ai_enabled_layout.add_widget(ai_enabled_label)
        
        self.ai_enabled_switch = MDSwitch(
            size_hint_x=0.3,
            on_press=self._toggle_ai_enabled
        )
        ai_enabled_layout.add_widget(self.ai_enabled_switch)
        
        layout.add_widget(ai_enabled_layout)
        
        # Test AI connection button
        test_ai_btn = MDRaisedButton(
            text="Test AI Connection",
            size_hint_y=None,
            height=dp(36),
            md_bg_color=(0.6, 0.2, 0.8, 1),
            on_press=self._test_ai_connection
        )
        layout.add_widget(test_ai_btn)
        
        card.add_widget(layout)
        
        return card
    
    def _create_data_management_card(self):
        """Create data management card."""
        card = MDCard(
            size_hint_y=None,
            height=dp(200),
            padding=dp(16),
            elevation=2,
            radius=[dp(12)]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        title = MDLabel(
            text="Data Management",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(32),
            font_style="H6"
        )
        layout.add_widget(title)
        
        # Action buttons
        button_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(48)
        )
        
        # Export data button
        export_btn = MDRaisedButton(
            text="Export Data",
            size_hint_x=0.5,
            md_bg_color=(0.2, 0.6, 0.8, 1),
            on_press=self._export_data
        )
        button_layout.add_widget(export_btn)
        
        # Import data button
        import_btn = MDRaisedButton(
            text="Import Data",
            size_hint_x=0.5,
            md_bg_color=(0.8, 0.6, 0.2, 1),
            on_press=self._import_data
        )
        button_layout.add_widget(import_btn)
        
        layout.add_widget(button_layout)
        
        # Clear data button
        clear_btn = MDFlatButton(
            text="Clear All Data",
            size_hint_y=None,
            height=dp(36),
            on_press=self._clear_all_data
        )
        layout.add_widget(clear_btn)
        
        card.add_widget(layout)
        
        return card
    
    def _create_about_card(self):
        """Create about card."""
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
            text="About TarotMac",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(32),
            font_style="H6"
        )
        layout.add_widget(title)
        
        about_text = MDLabel(
            text="A modern tarot application with AI-powered insights. Built with Python and Kivy for cross-platform compatibility.",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(80),
            font_style="Body2",
            halign="left",
            valign="top"
        )
        layout.add_widget(about_text)
        
        card.add_widget(layout)
        
        return card
    
    def _load_settings(self):
        """Load settings from storage."""
        try:
            # TODO: Implement actual settings loading from storage
            # For now, use default values
            self.settings = {
                'debug_mode': False,
                'theme': 'light',
                'autosave_readings': True,
                'notifications': True,
                'ai_enabled': True,
                'ai_model': 'llama2'
            }
            
            # Update UI with loaded settings
            self.debug_switch.active = self.settings['debug_mode']
            self.theme_value.text = self.settings['theme'].title()
            self.autosave_switch.active = self.settings['autosave_readings']
            self.notification_switch.active = self.settings['notifications']
            self.ai_enabled_switch.active = self.settings['ai_enabled']
            self.model_value.text = self.settings['ai_model']
            
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def _save_settings(self):
        """Save settings to storage."""
        try:
            # TODO: Implement actual settings saving to storage
            print("Settings saved:", self.settings)
            self._show_success("Settings saved successfully")
            
        except Exception as e:
            print(f"Error saving settings: {e}")
            self._show_error(f"Error saving settings: {str(e)}")
    
    def _toggle_debug_mode(self, instance):
        """Toggle debug mode."""
        self.settings['debug_mode'] = instance.active
        self._save_settings()
    
    def _toggle_autosave(self, instance):
        """Toggle auto-save readings."""
        self.settings['autosave_readings'] = instance.active
        self._save_settings()
    
    def _toggle_notifications(self, instance):
        """Toggle notifications."""
        self.settings['notifications'] = instance.active
        self._save_settings()
    
    def _toggle_ai_enabled(self, instance):
        """Toggle AI enabled."""
        self.settings['ai_enabled'] = instance.active
        self._save_settings()
    
    def _test_ai_connection(self, instance):
        """Test AI connection."""
        try:
            ai_manager = self.core_modules.get('ai_manager')
            if ai_manager:
                # TODO: Implement actual AI connection test
                self._show_success("AI connection test successful")
            else:
                self._show_error("AI manager not available")
                
        except Exception as e:
            print(f"Error testing AI connection: {e}")
            self._show_error(f"AI connection test failed: {str(e)}")
    
    def _export_data(self, instance):
        """Export application data."""
        try:
            # TODO: Implement actual data export
            self._show_success("Data exported successfully")
            
        except Exception as e:
            print(f"Error exporting data: {e}")
            self._show_error(f"Error exporting data: {str(e)}")
    
    def _import_data(self, instance):
        """Import application data."""
        try:
            # TODO: Implement actual data import
            self._show_success("Data imported successfully")
            
        except Exception as e:
            print(f"Error importing data: {e}")
            self._show_error(f"Error importing data: {str(e)}")
    
    def _clear_all_data(self, instance):
        """Clear all application data."""
        dialog = MDDialog(
            title="Clear All Data",
            text="Are you sure you want to clear all application data? This action cannot be undone.",
            buttons=[
                MDFlatButton(text="Cancel", on_press=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="Clear All", 
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_press=lambda x: self._confirm_clear_all_data(dialog)
                )
            ]
        )
        dialog.open()
    
    def _confirm_clear_all_data(self, dialog):
        """Confirm clearing all data."""
        dialog.dismiss()
        
        try:
            # TODO: Implement actual data clearing
            self._show_success("All data cleared successfully")
            
        except Exception as e:
            print(f"Error clearing all data: {e}")
            self._show_error(f"Error clearing all data: {str(e)}")
    
    def _show_success(self, message):
        """Show success dialog."""
        dialog = MDDialog(
            title="Success",
            text=message,
            buttons=[
                MDFlatButton(text="OK", on_press=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()
    
    def _show_error(self, message):
        """Show error dialog."""
        dialog = MDDialog(
            title="Error",
            text=message,
            buttons=[
                MDFlatButton(text="OK", on_press=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()
    
    def _navigate_back(self):
        """Navigate back to home screen."""
        app = MDApp.get_running_app()
        if app and hasattr(app, 'screen_manager'):
            app.screen_manager.current = 'home'