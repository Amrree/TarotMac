"""
Chat Screen for Android TarotMac App
AI chat interface with mobile-optimized design.
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
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.clock import Clock
import asyncio

# Import core modules
from ai.ai_manager import AIManager
from ai.chat_memory import ChatMessage, MessageRole


class ChatScreen(Screen):
    """
    Chat screen for AI conversations.
    Mobile-optimized with touch-friendly interface.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.core_modules = {}
        self.chat_session = None
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
        
        # Initialize chat session
        self._initialize_chat_session()
    
    def _build_ui(self):
        """Build the chat screen UI."""
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=dp(16)
        )
        
        # Top app bar
        toolbar = MDTopAppBar(
            title="AI Chat",
            elevation=4,
            md_bg_color=(0.6, 0.2, 0.8, 1),  # Purple theme
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["arrow-left", lambda x: self._navigate_back()]],
            right_action_items=[["chat-plus", lambda x: self._start_new_session()]]
        )
        main_layout.add_widget(toolbar)
        
        # Chat history area
        chat_card = self._create_chat_history_card()
        main_layout.add_widget(chat_card)
        
        # Input area
        input_card = self._create_input_card()
        main_layout.add_widget(input_card)
        
        self.add_widget(main_layout)
    
    def _create_chat_history_card(self):
        """Create chat history card."""
        card = MDCard(
            size_hint_y=0.7,
            padding=dp(16),
            elevation=2,
            radius=[dp(12)]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8)
        )
        
        # Chat history scroll view
        self.chat_scroll = MDScrollView()
        self.chat_content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(400)
        )
        
        # Welcome message
        welcome_msg = self._create_message_widget(
            "AI Assistant",
            "Hello! I'm your tarot AI assistant. Ask me about cards, readings, or anything tarot-related!",
            "assistant"
        )
        self.chat_content.add_widget(welcome_msg)
        
        self.chat_scroll.add_widget(self.chat_content)
        layout.add_widget(self.chat_scroll)
        
        card.add_widget(layout)
        
        return card
    
    def _create_input_card(self):
        """Create input area card."""
        card = MDCard(
            size_hint_y=0.25,
            padding=dp(16),
            elevation=2,
            radius=[dp(12)]
        )
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(12)
        )
        
        # Message input
        self.message_input = MDTextField(
            hint_text="Type your message here...",
            multiline=True,
            max_text_length=500,
            size_hint_y=0.6
        )
        layout.add_widget(self.message_input)
        
        # Action buttons
        button_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=0.4
        )
        
        # Send button
        send_btn = MDRaisedButton(
            text="Send",
            size_hint_x=0.7,
            md_bg_color=(0.6, 0.2, 0.8, 1),
            on_press=self._send_message
        )
        button_layout.add_widget(send_btn)
        
        # Clear button
        clear_btn = MDFlatButton(
            text="Clear",
            size_hint_x=0.3,
            on_press=self._clear_chat
        )
        button_layout.add_widget(clear_btn)
        
        layout.add_widget(button_layout)
        card.add_widget(layout)
        
        return card
    
    def _create_message_widget(self, sender, message, role):
        """Create a message widget."""
        message_card = MDCard(
            size_hint_y=None,
            height=dp(80),
            padding=dp(12),
            elevation=1,
            radius=[dp(8)]
        )
        
        # Set colors based on role
        if role == "user":
            message_card.md_bg_color = (0.2, 0.6, 0.8, 0.1)  # Light blue
        else:
            message_card.md_bg_color = (0.6, 0.2, 0.8, 0.1)  # Light purple
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(4)
        )
        
        # Sender name
        sender_label = MDLabel(
            text=sender,
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(20),
            font_style="Caption",
            bold=True
        )
        layout.add_widget(sender_label)
        
        # Message text
        message_label = MDLabel(
            text=message,
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(40),
            font_style="Body2",
            text_size=(None, None),
            halign="left",
            valign="top"
        )
        layout.add_widget(message_label)
        
        message_card.add_widget(layout)
        
        return message_card
    
    def _initialize_chat_session(self):
        """Initialize chat session with AI manager."""
        try:
            ai_manager = self.core_modules.get('ai_manager')
            if ai_manager:
                self.chat_session = ai_manager.create_chat_session()
                print("✅ Chat session initialized")
            else:
                print("❌ AI manager not available")
        except Exception as e:
            print(f"❌ Error initializing chat session: {e}")
    
    def _send_message(self, instance):
        """Send message to AI."""
        message_text = self.message_input.text.strip()
        
        if not message_text:
            return
        
        # Clear input
        self.message_input.text = ""
        
        # Add user message to chat
        user_msg = self._create_message_widget("You", message_text, "user")
        self.chat_content.add_widget(user_msg)
        
        # Scroll to bottom
        self._scroll_to_bottom()
        
        # Show typing indicator
        typing_msg = self._create_message_widget(
            "AI Assistant", 
            "Thinking...", 
            "assistant"
        )
        self.chat_content.add_widget(typing_msg)
        self._scroll_to_bottom()
        
        # Send to AI (async)
        Clock.schedule_once(lambda dt: self._process_ai_response(message_text), 0.1)
    
    def _process_ai_response(self, user_message):
        """Process AI response asynchronously."""
        try:
            ai_manager = self.core_modules.get('ai_manager')
            if not ai_manager or not self.chat_session:
                self._show_error("AI not available")
                return
            
            # Add user message to session
            ai_manager.memory_manager.add_message(
                self.chat_session.session_id,
                MessageRole.USER.value,
                user_message
            )
            
            # Get AI response
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                response = loop.run_until_complete(
                    ai_manager.chat(user_message)
                )
                
                # Remove typing indicator
                self.chat_content.remove_widget(self.chat_content.children[0])
                
                # Add AI response
                ai_msg = self._create_message_widget("AI Assistant", response, "assistant")
                self.chat_content.add_widget(ai_msg)
                
                # Scroll to bottom
                self._scroll_to_bottom()
                
            finally:
                loop.close()
                
        except Exception as e:
            print(f"Error processing AI response: {e}")
            # Remove typing indicator
            if self.chat_content.children:
                self.chat_content.remove_widget(self.chat_content.children[0])
            
            # Show error message
            error_msg = self._create_message_widget(
                "AI Assistant", 
                f"Sorry, I encountered an error: {str(e)}", 
                "assistant"
            )
            self.chat_content.add_widget(error_msg)
            self._scroll_to_bottom()
    
    def _scroll_to_bottom(self):
        """Scroll chat to bottom."""
        # Update chat content height
        total_height = sum(child.height for child in self.chat_content.children)
        self.chat_content.height = max(total_height, dp(400))
        
        # Scroll to bottom
        Clock.schedule_once(lambda dt: self.chat_scroll.scroll_to(self.chat_content.children[0]), 0.1)
    
    def _clear_chat(self, instance):
        """Clear chat history."""
        dialog = MDDialog(
            title="Clear Chat",
            text="Are you sure you want to clear the chat history?",
            buttons=[
                MDFlatButton(text="Cancel", on_press=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="Clear", 
                    on_press=lambda x: self._confirm_clear_chat(dialog)
                )
            ]
        )
        dialog.open()
    
    def _confirm_clear_chat(self, dialog):
        """Confirm clearing chat history."""
        dialog.dismiss()
        
        # Clear chat content
        self.chat_content.clear_widgets()
        
        # Add welcome message back
        welcome_msg = self._create_message_widget(
            "AI Assistant",
            "Hello! I'm your tarot AI assistant. Ask me about cards, readings, or anything tarot-related!",
            "assistant"
        )
        self.chat_content.add_widget(welcome_msg)
        
        # Clear AI session
        try:
            ai_manager = self.core_modules.get('ai_manager')
            if ai_manager and self.chat_session:
                ai_manager.end_session(self.chat_session.session_id)
                self._initialize_chat_session()
        except Exception as e:
            print(f"Error clearing AI session: {e}")
    
    def _start_new_session(self, instance):
        """Start a new chat session."""
        self._confirm_clear_chat(None)
    
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