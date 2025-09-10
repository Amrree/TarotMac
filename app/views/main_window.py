"""
Main window controller for the Tarot application.
"""

try:
    from AppKit import (
        NSWindow, NSWindowController, NSRect, NSMakeRect,
        NSTabView, NSTabViewItem, NSView, NSColor,
        NSLayoutConstraint, NSLayoutAttributeTop, NSLayoutAttributeLeading,
        NSLayoutAttributeTrailing, NSLayoutAttributeBottom
    )
except ImportError:
    # Use mock for testing when AppKit is not available
    from ..mock_appkit import appkit_module
    NSWindow = appkit_module.NSWindow
    NSWindowController = appkit_module.NSWindowController
    NSRect = appkit_module.NSRect
    NSMakeRect = appkit_module.NSMakeRect
    NSTabView = appkit_module.NSTabView
    NSTabViewItem = appkit_module.NSTabViewItem
    NSView = appkit_module.NSView
    NSColor = appkit_module.NSColor
    NSLayoutConstraint = appkit_module.NSLayoutConstraint
    NSLayoutAttributeTop = appkit_module.NSLayoutConstraint.LayoutAttributeTop
    NSLayoutAttributeLeading = appkit_module.NSLayoutConstraint.LayoutAttributeLeading
    NSLayoutAttributeTrailing = appkit_module.NSLayoutConstraint.LayoutAttributeTrailing
    NSLayoutAttributeBottom = appkit_module.NSLayoutConstraint.LayoutAttributeBottom

try:
    from Foundation import NSObject
except ImportError:
    # Use mock for testing when Foundation is not available
    from ..mock_foundation import foundation_module
    NSObject = foundation_module.NSObject

import logging

from app.views.home_view import HomeViewController
from app.views.readings_view import ReadingsViewController
from app.views.chat_view import ChatViewController
from app.views.history_view import HistoryViewController
from app.views.settings_view import SettingsViewController

logger = logging.getLogger(__name__)


class MainWindowController(NSWindowController):
    """Main window controller with tabbed interface."""
    
    def init(self):
        """Initialize the main window."""
        # Create window
        window_rect = NSMakeRect(100, 100, 1200, 800)
        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            window_rect,
            NSWindow.TitledWindowMask | NSWindow.ClosableWindowMask | 
            NSWindow.MiniaturizableWindowMask | NSWindow.ResizableWindowMask,
            NSWindow.Buffered,
            False
        )
        
        # Set window properties
        window.setTitle_("Tarot")
        window.setMinSize_((800, 600))
        
        # Set dark theme colors
        window.setBackgroundColor_(NSColor.blackColor())
        
        # Initialize controller
        self = super(MainWindowController, self).initWithWindow_(window)
        if self is None:
            return None
        
        self.setupUI()
        return self
    
    def setupUI(self):
        """Set up the main UI with tabs."""
        window = self.window()
        content_view = window.contentView()
        
        # Create tab view
        tab_view = NSTabView.alloc().initWithFrame_(content_view.bounds())
        tab_view.setAutoresizingMask_(
            NSView.WidthSizable | NSView.HeightSizable
        )
        
        # Create tab items
        self.createTabItems(tab_view)
        
        # Add tab view to window
        content_view.addSubview_(tab_view)
        
        # Center window on screen
        window.center()
    
    def createTabItems(self, tab_view):
        """Create all tab items."""
        
        # Home tab
        home_item = NSTabViewItem.alloc().initWithIdentifier_("home")
        home_item.setLabel_("Home")
        home_view_controller = HomeViewController.alloc().init()
        home_item.setView_(home_view_controller.view())
        tab_view.addTabViewItem_(home_item)
        
        # Readings tab
        readings_item = NSTabViewItem.alloc().initWithIdentifier_("readings")
        readings_item.setLabel_("Readings")
        readings_view_controller = ReadingsViewController.alloc().init()
        readings_item.setView_(readings_view_controller.view())
        tab_view.addTabViewItem_(readings_item)
        
        # Chat tab
        chat_item = NSTabViewItem.alloc().initWithIdentifier_("chat")
        chat_item.setLabel_("Chat")
        chat_view_controller = ChatViewController.alloc().init()
        chat_item.setView_(chat_view_controller.view())
        tab_view.addTabViewItem_(chat_item)
        
        # History tab
        history_item = NSTabViewItem.alloc().initWithIdentifier_("history")
        history_item.setLabel_("History")
        history_view_controller = HistoryViewController.alloc().init()
        history_item.setView_(history_view_controller.view())
        tab_view.addTabViewItem_(history_item)
        
        # Settings tab
        settings_item = NSTabViewItem.alloc().initWithIdentifier_("settings")
        settings_item.setLabel_("Settings")
        settings_view_controller = SettingsViewController.alloc().init()
        settings_item.setView_(settings_view_controller.view())
        tab_view.addTabViewItem_(settings_item)
    
    def showWindow_(self, sender):
        """Show the main window."""
        self.window().makeKeyAndOrderFront_(None)