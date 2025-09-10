"""Chat view controller."""

try:
    from AppKit import (
        NSView, NSViewController, NSMakeRect, NSColor, NSTextField, NSTextView,
        NSButton, NSFont, NSLayoutConstraint, NSLayoutAttributeTop,
        NSLayoutAttributeLeading, NSLayoutAttributeTrailing, NSLayoutAttributeBottom,
        NSLayoutAttributeCenterX, NSLayoutAttributeCenterY, NSLayoutRelationEqual
    )
except ImportError:
    # Use mock for testing when AppKit is not available
    from ..mock_appkit import appkit_module
    NSView = appkit_module.NSView
    NSViewController = appkit_module.NSViewController
    NSMakeRect = appkit_module.NSMakeRect
    NSColor = appkit_module.NSColor
    NSTextField = appkit_module.NSTextField
    NSTextView = appkit_module.NSTextView
    NSButton = appkit_module.NSButton
    NSFont = appkit_module.NSFont
    NSLayoutConstraint = appkit_module.NSLayoutConstraint
    NSLayoutAttributeTop = appkit_module.NSLayoutConstraint.LayoutAttributeTop
    NSLayoutAttributeLeading = appkit_module.NSLayoutConstraint.LayoutAttributeLeading
    NSLayoutAttributeTrailing = appkit_module.NSLayoutConstraint.LayoutAttributeTrailing
    NSLayoutAttributeBottom = appkit_module.NSLayoutConstraint.LayoutAttributeBottom
    NSLayoutAttributeCenterX = appkit_module.NSLayoutConstraint.LayoutAttributeCenterX
    NSLayoutAttributeCenterY = appkit_module.NSLayoutConstraint.LayoutAttributeCenterY
    NSLayoutRelationEqual = appkit_module.NSLayoutConstraint.LayoutRelationEqual

try:
    from Foundation import NSObject
except ImportError:
    # Use mock for testing when Foundation is not available
    from ..mock_foundation import foundation_module
    NSObject = foundation_module.NSObject

import logging

from app.chat_manager import ChatManager

logger = logging.getLogger(__name__)


class ChatViewController(NSViewController):
    """Controller for the chat tab."""
    
    def init(self):
        self = super(ChatViewController, self).init()
        if self is None:
            return None
        
        # Initialize chat manager
        self.chat_manager = ChatManager()
        
        self.setupView()
        return self
    
    def setupView(self):
        """Set up the chat view."""
        view_rect = NSMakeRect(0, 0, 800, 600)
        view = NSView.alloc().initWithFrame_(view_rect)
        view.setWantsLayer_(True)
        view.layer().setBackgroundColor_(NSColor.blackColor().CGColor())
        
        # Create chat history area
        self.createChatHistoryArea(view)
        
        # Create input area
        self.createInputArea(view)
        
        # Create control buttons
        self.createControlButtons(view)
        
        self.setView_(view)
    
    def createChatHistoryArea(self, parent_view):
        """Create the chat history display area."""
        history_rect = NSMakeRect(50, 100, 700, 400)
        self.chat_history_view = NSTextView.alloc().initWithFrame_(history_rect)
        self.chat_history_view.setString_("Welcome! Start a conversation with the AI.\n")
        self.chat_history_view.setEditable_(False)
        self.chat_history_view.setSelectable_(True)
        self.chat_history_view.setBackgroundColor_(NSColor.blackColor())
        self.chat_history_view.setTextColor_(NSColor.lightGrayColor())
        
        # Set monospaced font
        font = NSFont.fontWithName_size_("Monaco", 12)
        self.chat_history_view.setFont_(font)
        
        parent_view.addSubview_(self.chat_history_view)
    
    def createInputArea(self, parent_view):
        """Create the message input area."""
        # Input field
        input_rect = NSMakeRect(50, 50, 600, 30)
        self.message_input = NSTextField.alloc().initWithFrame_(input_rect)
        self.message_input.setPlaceholderString_("Type your message here...")
        self.message_input.setBackgroundColor_(NSColor.darkGrayColor())
        self.message_input.setTextColor_(NSColor.lightGrayColor())
        self.message_input.setFont_(NSFont.fontWithName_size_("Monaco", 12))
        
        # Set up enter key action
        self.message_input.setTarget_(self)
        self.message_input.setAction_("sendMessagePressed:")
        
        parent_view.addSubview_(self.message_input)
    
    def createControlButtons(self, parent_view):
        """Create control buttons."""
        # Send button
        send_button = NSButton.alloc().initWithFrame_(
            NSMakeRect(660, 50, 90, 30)
        )
        send_button.setTitle_("Send")
        send_button.setTarget_(self)
        send_button.setAction_("sendMessagePressed:")
        send_button.setBordered_(True)
        send_button.setBezelStyle_(NSButton.RoundedBezelStyle)
        parent_view.addSubview_(send_button)
        
        # Clear button
        clear_button = NSButton.alloc().initWithFrame_(
            NSMakeRect(50, 20, 90, 30)
        )
        clear_button.setTitle_("Clear Chat")
        clear_button.setTarget_(self)
        clear_button.setAction_("clearChatPressed:")
        clear_button.setBordered_(True)
        clear_button.setBezelStyle_(NSButton.RoundedBezelStyle)
        parent_view.addSubview_(clear_button)
    
    def sendMessagePressed_(self, sender):
        """Handle send message button press."""
        message = self.message_input.stringValue()
        if not message.strip():
            return
        
        # Clear input
        self.message_input.setStringValue_("")
        
        # Add user message to history
        self.appendToHistory(f"You: {message}\n")
        
        # Send to AI
        response = self.chat_manager.sendMessage(message)
        if response:
            self.appendToHistory(f"AI: {response}\n\n")
        else:
            self.appendToHistory("AI: Sorry, I couldn't generate a response.\n\n")
    
    def clearChatPressed_(self, sender):
        """Handle clear chat button press."""
        self.chat_manager.clearChatHistory()
        self.chat_history_view.setString_("Chat cleared. Start a new conversation!\n")
        logger.info("Chat cleared")
    
    def appendToHistory(self, text):
        """Append text to chat history."""
        current_text = self.chat_history_view.string()
        self.chat_history_view.setString_(current_text + text)
        
        # Scroll to bottom
        self.chat_history_view.scrollToEndOfDocument_(None)