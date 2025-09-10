"""
Main application entry point for macOS Tarot App.
"""

import sys
import os
from AppKit import NSApplication, NSWindow, NSView, NSRect, NSMakeRect
from Foundation import NSObject
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.views.main_window import MainWindowController

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TarotAppDelegate(NSObject):
    """Main application delegate."""
    
    def applicationDidFinishLaunching_(self, notification):
        """Called when application finishes launching."""
        logger.info("Tarot App launching...")
        
        # Create and show main window
        self.main_window = MainWindowController.alloc().init()
        self.main_window.showWindow_(None)
        
        logger.info("Tarot App launched successfully")


def main():
    """Main entry point."""
    # Create application
    app = NSApplication.sharedApplication()
    
    # Set up delegate
    delegate = TarotAppDelegate.alloc().init()
    app.setDelegate_(delegate)
    
    # Run application
    app.run()


if __name__ == "__main__":
    main()