"""
History Screen for Android TarotMac App
Reading history management with mobile-optimized interface.
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
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.app import MDApp
from kivy.metrics import dp
from datetime import datetime


class HistoryScreen(Screen):
    """
    History screen for managing reading history.
    Mobile-optimized with touch-friendly interface.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.core_modules = {}
        self.readings_history = []
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
        
        # Load readings history
        self._load_readings_history()
    
    def _build_ui(self):
        """Build the history screen UI."""
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=dp(16)
        )
        
        # Top app bar
        toolbar = MDTopAppBar(
            title="Reading History",
            elevation=4,
            md_bg_color=(0.8, 0.6, 0.2, 1),  # Orange theme
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["arrow-left", lambda x: self._navigate_back()]],
            right_action_items=[["refresh", lambda x: self._refresh_history()]]
        )
        main_layout.add_widget(toolbar)
        
        # Search and filter area
        search_card = self._create_search_card()
        main_layout.add_widget(search_card)
        
        # History list area
        history_card = self._create_history_card()
        main_layout.add_widget(history_card)
        
        self.add_widget(main_layout)
    
    def _create_search_card(self):
        """Create search and filter card."""
        card = MDCard(
            size_hint_y=None,
            height=dp(120),
            padding=dp(16),
            elevation=2,
            radius=[dp(12)]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(12)
        )
        
        title = MDLabel(
            text="Search & Filter",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(24),
            font_style="H6"
        )
        layout.add_widget(title)
        
        # Search input
        self.search_input = MDTextField(
            hint_text="Search readings...",
            size_hint_y=None,
            height=dp(48)
        )
        layout.add_widget(self.search_input)
        
        # Search button
        search_btn = MDRaisedButton(
            text="Search",
            size_hint_y=None,
            height=dp(36),
            md_bg_color=(0.8, 0.6, 0.2, 1),
            on_press=self._search_readings
        )
        layout.add_widget(search_btn)
        
        card.add_widget(layout)
        
        return card
    
    def _create_history_card(self):
        """Create history list card."""
        card = MDCard(
            size_hint_y=0.8,
            padding=dp(16),
            elevation=2,
            radius=[dp(12)]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8)
        )
        
        # History title
        title = MDLabel(
            text="Your Readings",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(32),
            font_style="H6"
        )
        layout.add_widget(title)
        
        # History scroll view
        self.history_scroll = MDScrollView()
        self.history_list = MDList()
        
        # Add placeholder if no readings
        if not self.readings_history:
            placeholder = OneLineListItem(
                text="No readings found. Start with a reading to see your history here!",
                theme_text_color="Secondary"
            )
            self.history_list.add_widget(placeholder)
        
        self.history_scroll.add_widget(self.history_list)
        layout.add_widget(self.history_scroll)
        
        # Action buttons
        button_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(48)
        )
        
        # Export button
        export_btn = MDRaisedButton(
            text="Export",
            size_hint_x=0.5,
            md_bg_color=(0.2, 0.6, 0.8, 1),
            on_press=self._export_readings
        )
        button_layout.add_widget(export_btn)
        
        # Clear all button
        clear_btn = MDFlatButton(
            text="Clear All",
            size_hint_x=0.5,
            on_press=self._clear_all_readings
        )
        button_layout.add_widget(clear_btn)
        
        layout.add_widget(button_layout)
        card.add_widget(layout)
        
        return card
    
    def _load_readings_history(self):
        """Load readings history from storage."""
        try:
            # TODO: Implement actual history loading from storage
            # For now, create sample data
            self.readings_history = [
                {
                    'id': '1',
                    'spread_type': 'Single Card',
                    'question': 'What guidance do I need today?',
                    'cards': ['The Fool'],
                    'date': '2024-01-15',
                    'interpretation': 'A new beginning awaits you...'
                },
                {
                    'id': '2',
                    'spread_type': 'Three Card',
                    'question': 'What does my future hold?',
                    'cards': ['The Magician', 'The High Priestess', 'The Empress'],
                    'date': '2024-01-14',
                    'interpretation': 'You have the power to manifest your desires...'
                }
            ]
            
            self._update_history_display()
            
        except Exception as e:
            print(f"Error loading readings history: {e}")
    
    def _update_history_display(self):
        """Update the history display."""
        self.history_list.clear_widgets()
        
        if not self.readings_history:
            placeholder = OneLineListItem(
                text="No readings found. Start with a reading to see your history here!",
                theme_text_color="Secondary"
            )
            self.history_list.add_widget(placeholder)
            return
        
        for reading in self.readings_history:
            # Create reading item
            reading_item = ThreeLineListItem(
                text=f"{reading['spread_type']} Reading",
                secondary_text=f"Question: {reading['question']}",
                tertiary_text=f"Date: {reading['date']} | Cards: {', '.join(reading['cards'])}",
                on_press=lambda x, r=reading: self._show_reading_details(r)
            )
            self.history_list.add_widget(reading_item)
    
    def _search_readings(self, instance):
        """Search readings based on input."""
        search_term = self.search_input.text.lower().strip()
        
        if not search_term:
            self._update_history_display()
            return
        
        # Filter readings
        filtered_readings = []
        for reading in self.readings_history:
            if (search_term in reading['question'].lower() or
                search_term in reading['spread_type'].lower() or
                any(search_term in card.lower() for card in reading['cards'])):
                filtered_readings.append(reading)
        
        # Update display with filtered results
        self.history_list.clear_widgets()
        
        if not filtered_readings:
            no_results = OneLineListItem(
                text=f"No readings found for '{search_term}'",
                theme_text_color="Secondary"
            )
            self.history_list.add_widget(no_results)
            return
        
        for reading in filtered_readings:
            reading_item = ThreeLineListItem(
                text=f"{reading['spread_type']} Reading",
                secondary_text=f"Question: {reading['question']}",
                tertiary_text=f"Date: {reading['date']} | Cards: {', '.join(reading['cards'])}",
                on_press=lambda x, r=reading: self._show_reading_details(r)
            )
            self.history_list.add_widget(reading_item)
    
    def _show_reading_details(self, reading):
        """Show detailed reading information."""
        # Create detailed reading dialog
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            size_hint_y=None,
            height=dp(400)
        )
        
        # Reading info
        info_text = f"""
Spread Type: {reading['spread_type']}
Question: {reading['question']}
Date: {reading['date']}
Cards: {', '.join(reading['cards'])}

Interpretation:
{reading['interpretation']}
        """.strip()
        
        info_label = MDLabel(
            text=info_text,
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(300),
            font_style="Body2",
            halign="left",
            valign="top"
        )
        content.add_widget(info_label)
        
        # Action buttons
        button_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(48)
        )
        
        # Delete button
        delete_btn = MDRaisedButton(
            text="Delete",
            size_hint_x=0.5,
            md_bg_color=(0.8, 0.2, 0.2, 1),
            on_press=lambda x: self._delete_reading(reading, content)
        )
        button_layout.add_widget(delete_btn)
        
        # Close button
        close_btn = MDFlatButton(
            text="Close",
            size_hint_x=0.5,
            on_press=lambda x: self._close_dialog(content)
        )
        button_layout.add_widget(close_btn)
        
        content.add_widget(button_layout)
        
        # Create dialog
        dialog = MDDialog(
            title="Reading Details",
            type="custom",
            content_cls=content,
            size_hint=(0.9, 0.8)
        )
        dialog.open()
        
        # Store dialog reference for closing
        self.current_dialog = dialog
    
    def _delete_reading(self, reading, content):
        """Delete a reading."""
        try:
            # Remove from history
            self.readings_history = [r for r in self.readings_history if r['id'] != reading['id']]
            
            # Update display
            self._update_history_display()
            
            # Close dialog
            self._close_dialog(content)
            
            # Show success message
            self._show_success("Reading deleted successfully")
            
        except Exception as e:
            print(f"Error deleting reading: {e}")
            self._show_error(f"Error deleting reading: {str(e)}")
    
    def _close_dialog(self, content):
        """Close the current dialog."""
        if hasattr(self, 'current_dialog'):
            self.current_dialog.dismiss()
    
    def _refresh_history(self, instance):
        """Refresh readings history."""
        self._load_readings_history()
        self._show_success("History refreshed")
    
    def _export_readings(self, instance):
        """Export readings to file."""
        try:
            if not self.readings_history:
                self._show_error("No readings to export")
                return
            
            # TODO: Implement actual export functionality
            # For now, show success message
            self._show_success(f"Exported {len(self.readings_history)} readings")
            
        except Exception as e:
            print(f"Error exporting readings: {e}")
            self._show_error(f"Error exporting readings: {str(e)}")
    
    def _clear_all_readings(self, instance):
        """Clear all readings."""
        dialog = MDDialog(
            title="Clear All Readings",
            text="Are you sure you want to delete all readings? This action cannot be undone.",
            buttons=[
                MDFlatButton(text="Cancel", on_press=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="Clear All", 
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_press=lambda x: self._confirm_clear_all(dialog)
                )
            ]
        )
        dialog.open()
    
    def _confirm_clear_all(self, dialog):
        """Confirm clearing all readings."""
        dialog.dismiss()
        
        try:
            # Clear all readings
            self.readings_history = []
            self._update_history_display()
            
            # Show success message
            self._show_success("All readings cleared")
            
        except Exception as e:
            print(f"Error clearing all readings: {e}")
            self._show_error(f"Error clearing all readings: {str(e)}")
    
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