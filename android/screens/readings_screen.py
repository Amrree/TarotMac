"""
Readings Screen for Android TarotMac App
Handles tarot card readings with mobile-optimized interface.
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDSegmentedControl, MDSegmentedControlItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.clock import Clock

# Import core modules
from spreads.spread_manager import SpreadManager, SpreadType
from influence.tarot_influence_engine import TarotInfluenceEngine


class ReadingsScreen(Screen):
    """
    Readings screen for tarot card readings.
    Mobile-optimized with touch-friendly controls.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.core_modules = {}
        self.current_reading = None
        self.current_spread_type = SpreadType.SINGLE_CARD
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
        """Build the readings screen UI."""
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=dp(16)
        )
        
        # Top app bar
        toolbar = MDTopAppBar(
            title="Tarot Readings",
            elevation=4,
            md_bg_color=(0.2, 0.6, 0.8, 1),
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
        
        # Spread selection card
        spread_card = self._create_spread_selection_card()
        content_layout.add_widget(spread_card)
        
        # Reading area card
        reading_card = self._create_reading_area_card()
        content_layout.add_widget(reading_card)
        
        # Interpretation card
        interpretation_card = self._create_interpretation_card()
        content_layout.add_widget(interpretation_card)
        
        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)
        
        self.add_widget(main_layout)
    
    def _create_spread_selection_card(self):
        """Create spread selection card."""
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
            text="Choose Your Spread",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(32),
            font_style="H6"
        )
        layout.add_widget(title)
        
        # Spread type selection
        spread_control = MDSegmentedControl(
            size_hint_y=None,
            height=dp(48)
        )
        
        # Single card option
        single_item = MDSegmentedControlItem(
            text="Single Card",
            on_press=lambda x: self._select_spread_type(SpreadType.SINGLE_CARD)
        )
        spread_control.add_widget(single_item)
        
        # Three card option
        three_item = MDSegmentedControlItem(
            text="Three Card",
            on_press=lambda x: self._select_spread_type(SpreadType.THREE_CARD)
        )
        spread_control.add_widget(three_item)
        
        # Celtic cross option
        celtic_item = MDSegmentedControlItem(
            text="Celtic Cross",
            on_press=lambda x: self._select_spread_type(SpreadType.CELTIC_CROSS)
        )
        spread_control.add_widget(celtic_item)
        
        layout.add_widget(spread_control)
        
        # Draw cards button
        draw_btn = MDRaisedButton(
            text="Draw Cards",
            size_hint_y=None,
            height=dp(48),
            md_bg_color=(0.2, 0.6, 0.8, 1),
            on_press=self._draw_cards
        )
        layout.add_widget(draw_btn)
        
        card.add_widget(layout)
        
        return card
    
    def _create_reading_area_card(self):
        """Create reading area card for displaying cards."""
        card = MDCard(
            size_hint_y=None,
            height=dp(300),
            padding=dp(16),
            elevation=2,
            radius=[dp(12)]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16)
        )
        
        title = MDLabel(
            text="Your Reading",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(32),
            font_style="H6"
        )
        layout.add_widget(title)
        
        # Card display area
        self.card_display = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(200)
        )
        
        # Placeholder text
        placeholder = MDLabel(
            text="Select a spread and draw cards to begin your reading",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(200),
            font_style="Body1",
            halign="center"
        )
        self.card_display.add_widget(placeholder)
        
        layout.add_widget(self.card_display)
        
        # Clear reading button
        clear_btn = MDFlatButton(
            text="Clear Reading",
            size_hint_y=None,
            height=dp(36),
            on_press=self._clear_reading
        )
        layout.add_widget(clear_btn)
        
        card.add_widget(layout)
        
        return card
    
    def _create_interpretation_card(self):
        """Create interpretation card."""
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
            text="Interpretation",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(32),
            font_style="H6"
        )
        layout.add_widget(title)
        
        # Interpretation text area
        self.interpretation_text = MDLabel(
            text="Draw cards to see your interpretation here",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(150),
            font_style="Body2",
            halign="left",
            valign="top"
        )
        layout.add_widget(self.interpretation_text)
        
        card.add_widget(layout)
        
        return card
    
    def _select_spread_type(self, spread_type):
        """Select spread type."""
        self.current_spread_type = spread_type
        print(f"Selected spread type: {spread_type}")
    
    def _draw_cards(self, instance):
        """Draw cards for the selected spread."""
        try:
            spread_manager = self.core_modules.get('spread_manager')
            deck = self.core_modules.get('deck')
            
            if not spread_manager or not deck:
                self._show_error("Core modules not available")
                return
            
            # Create reading
            reading = spread_manager.create_reading(
                spread_type=self.current_spread_type,
                question="What guidance do the cards offer?"
            )
            
            if not reading:
                self._show_error("Failed to create reading")
                return
            
            # Draw cards
            success = spread_manager.draw_cards_for_reading(reading, deck)
            
            if not success:
                self._show_error("Failed to draw cards")
                return
            
            self.current_reading = reading
            self._update_card_display()
            self._update_interpretation()
            
        except Exception as e:
            print(f"Error drawing cards: {e}")
            self._show_error(f"Error: {str(e)}")
    
    def _update_card_display(self):
        """Update the card display area."""
        if not self.current_reading:
            return
        
        # Clear existing cards
        self.card_display.clear_widgets()
        
        # Get positioned cards
        positioned_cards = self.current_reading.positioned_cards
        
        if not positioned_cards:
            placeholder = MDLabel(
                text="No cards drawn yet",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(200),
                font_style="Body1",
                halign="center"
            )
            self.card_display.add_widget(placeholder)
            return
        
        # Create card display grid
        card_grid = MDGridLayout(
            cols=min(len(positioned_cards), 3),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(200)
        )
        
        for card_pos in positioned_cards:
            card = card_pos.card
            position = card_pos.position
            
            # Create card widget
            card_widget = self._create_card_widget(card, position)
            card_grid.add_widget(card_widget)
        
        self.card_display.add_widget(card_grid)
    
    def _create_card_widget(self, card, position):
        """Create a card widget for display."""
        card_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(4),
            size_hint_y=None,
            height=dp(180)
        )
        
        # Card name
        name_label = MDLabel(
            text=card.name,
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(24),
            font_style="Caption",
            halign="center"
        )
        card_container.add_widget(name_label)
        
        # Card position
        position_label = MDLabel(
            text=f"Position: {position.name}",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(20),
            font_style="Caption",
            halign="center"
        )
        card_container.add_widget(position_label)
        
        # Card orientation
        orientation_label = MDLabel(
            text=f"{'Upright' if card.is_upright else 'Reversed'}",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(20),
            font_style="Caption",
            halign="center"
        )
        card_container.add_widget(orientation_label)
        
        # Card meaning preview
        meaning_preview = card.upright_meaning[:50] + "..." if len(card.upright_meaning) > 50 else card.upright_meaning
        meaning_label = MDLabel(
            text=meaning_preview,
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(60),
            font_style="Caption",
            halign="center",
            valign="top"
        )
        card_container.add_widget(meaning_label)
        
        return card_container
    
    def _update_interpretation(self):
        """Update the interpretation text."""
        if not self.current_reading:
            return
        
        try:
            spread_manager = self.core_modules.get('spread_manager')
            influence_engine = self.core_modules.get('influence_engine')
            
            if not spread_manager:
                return
            
            # Get interpretation
            interpretation = spread_manager.interpret_reading(
                self.current_reading, influence_engine
            )
            
            if isinstance(interpretation, dict):
                # Extract overall summary
                summary = interpretation.get('overall_summary', 'No interpretation available')
            else:
                summary = str(interpretation)
            
            self.interpretation_text.text = summary
            
        except Exception as e:
            print(f"Error updating interpretation: {e}")
            self.interpretation_text.text = f"Error generating interpretation: {str(e)}"
    
    def _clear_reading(self, instance):
        """Clear the current reading."""
        self.current_reading = None
        self._update_card_display()
        self.interpretation_text.text = "Draw cards to see your interpretation here"
    
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