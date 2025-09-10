"""Settings view controller."""

from AppKit import NSView, NSViewController, NSMakeRect, NSColor, NSTextField
from Foundation import NSObject
import logging

logger = logging.getLogger(__name__)


class SettingsViewController(NSViewController):
    """Controller for the settings tab."""
    
    def init(self):
        self = super(SettingsViewController, self).init()
        if self is None:
            return None
        
        view_rect = NSMakeRect(0, 0, 800, 600)
        view = NSView.alloc().initWithFrame_(view_rect)
        view.setWantsLayer_(True)
        view.layer().setBackgroundColor_(NSColor.blackColor().CGColor())
        
        # Add settings placeholder
        settings_text = NSTextField.alloc().initWithFrame_(
            NSMakeRect(300, 300, 200, 50)
        )
        settings_text.setStringValue_("Settings")
        settings_text.setEditable_(False)
        settings_text.setBordered_(False)
        settings_text.setBackgroundColor_(NSColor.clearColor())
        settings_text.setTextColor_(NSColor.lightGrayColor())
        
        view.addSubview_(settings_text)
        self.setView_(view)
        return self