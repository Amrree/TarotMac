"""Home view controller."""

try:
    from AppKit import NSView, NSViewController, NSMakeRect, NSColor, NSTextField
except ImportError:
    # Use mock for testing when AppKit is not available
    from ..mock_appkit import appkit_module
    NSView = appkit_module.NSView
    NSViewController = appkit_module.NSViewController
    NSMakeRect = appkit_module.NSMakeRect
    NSColor = appkit_module.NSColor
    NSTextField = appkit_module.NSTextField

try:
    from Foundation import NSObject
except ImportError:
    # Use mock for testing when Foundation is not available
    from ..mock_foundation import foundation_module
    NSObject = foundation_module.NSObject

import logging

logger = logging.getLogger(__name__)


class HomeViewController(NSViewController):
    """Controller for the home/dashboard tab."""
    
    def init(self):
        self = super(HomeViewController, self).init()
        if self is None:
            return None
        
        view_rect = NSMakeRect(0, 0, 800, 600)
        view = NSView.alloc().initWithFrame_(view_rect)
        view.setWantsLayer_(True)
        view.layer().setBackgroundColor_(NSColor.blackColor().CGColor())
        
        # Add welcome text
        welcome_text = NSTextField.alloc().initWithFrame_(
            NSMakeRect(300, 300, 200, 50)
        )
        welcome_text.setStringValue_("Welcome to Tarot")
        welcome_text.setEditable_(False)
        welcome_text.setBordered_(False)
        welcome_text.setBackgroundColor_(NSColor.clearColor())
        welcome_text.setTextColor_(NSColor.lightGrayColor())
        
        view.addSubview_(welcome_text)
        self.setView_(view)
        return self