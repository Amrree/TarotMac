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

from app.app_delegate import TarotAppDelegate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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