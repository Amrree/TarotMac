"""Home view controller."""

from AppKit import NSView, NSViewController, NSMakeRect, NSColor, NSTextField
from Foundation import NSObject
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