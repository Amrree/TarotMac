"""History view controller."""

from AppKit import NSView, NSViewController, NSMakeRect, NSColor, NSTextField
from Foundation import NSObject
import logging

logger = logging.getLogger(__name__)


class HistoryViewController(NSViewController):
    """Controller for the history tab."""
    
    def init(self):
        self = super(HistoryViewController, self).init()
        if self is None:
            return None
        
        view_rect = NSMakeRect(0, 0, 800, 600)
        view = NSView.alloc().initWithFrame_(view_rect)
        view.setWantsLayer_(True)
        view.layer().setBackgroundColor_(NSColor.blackColor().CGColor())
        
        # Add history placeholder
        history_text = NSTextField.alloc().initWithFrame_(
            NSMakeRect(300, 300, 200, 50)
        )
        history_text.setStringValue_("Reading History")
        history_text.setEditable_(False)
        history_text.setBordered_(False)
        history_text.setBackgroundColor_(NSColor.clearColor())
        history_text.setTextColor_(NSColor.lightGrayColor())
        
        view.addSubview_(history_text)
        self.setView_(view)
        return self