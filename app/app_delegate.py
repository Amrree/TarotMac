"""
Application delegate for the Tarot application.
Handles application lifecycle and coordinates between GUI and core modules.
"""

try:
    from AppKit import NSApplication, NSObject, NSApp
except ImportError:
    # Use mock for testing when AppKit is not available
    from .mock_appkit import appkit_module
    NSApplication = appkit_module.NSApplication
    NSObject = appkit_module.NSObject
    NSApp = appkit_module.NSApp

try:
    from Foundation import NSObject
except ImportError:
    # Use mock for testing when Foundation is not available
    from .mock_foundation import foundation_module
    NSObject = foundation_module.NSObject

import logging

from app.views.main_window import MainWindowController

logger = logging.getLogger(__name__)


class TarotAppDelegate(NSObject):
    """Application delegate for the Tarot app."""
    
    def __init__(self):
        """Initialize the app delegate."""
        super().__init__()
        self.main_window_controller = None
    
    def init(self):
        """Initialize the app delegate."""
        self = super(TarotAppDelegate, self).init()
        if self is None:
            return None
        
        self.main_window_controller = None
        return self
    
    def applicationDidFinishLaunching_(self, notification):
        """Called when the application finishes launching."""
        logger.info("Tarot application launched")
        
        # Create and show main window
        self.main_window_controller = MainWindowController.alloc().init()
        self.main_window_controller.showWindow_(None)
        
        # Set up logging
        self.setupLogging()
    
    def applicationWillTerminate_(self, notification):
        """Called when the application is about to terminate."""
        logger.info("Tarot application terminating")
        
        # Clean up resources
        if self.main_window_controller:
            self.main_window_controller.window().close()
    
    def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
        """Return True to quit when the last window is closed."""
        return True
    
    def setupLogging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )