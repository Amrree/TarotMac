"""
Readings view controller for drawing and managing tarot readings.
"""

try:
    from AppKit import (
        NSView, NSViewController, NSRect, NSMakeRect,
        NSButton, NSTextField, NSTextView, NSColor,
        NSFont, NSFontManager, NSLayoutConstraint,
        NSLayoutAttributeTop, NSLayoutAttributeLeading,
        NSLayoutAttributeTrailing, NSLayoutAttributeBottom,
        NSLayoutAttributeCenterX, NSLayoutAttributeCenterY,
        NSLayoutRelationEqual, NSLayoutConstraintOrientationHorizontal,
        NSLayoutConstraintOrientationVertical
    )
except ImportError:
    # Use mock for testing when AppKit is not available
    from ..mock_appkit import appkit_module
    NSView = appkit_module.NSView
    NSViewController = appkit_module.NSViewController
    NSRect = appkit_module.NSRect
    NSMakeRect = appkit_module.NSMakeRect
    NSButton = appkit_module.NSButton
    NSTextField = appkit_module.NSTextField
    NSTextView = appkit_module.NSTextView
    NSColor = appkit_module.NSColor
    NSFont = appkit_module.NSFont
    NSFontManager = appkit_module.NSFontManager
    NSLayoutConstraint = appkit_module.NSLayoutConstraint
    NSLayoutAttributeTop = appkit_module.NSLayoutConstraint.LayoutAttributeTop
    NSLayoutAttributeLeading = appkit_module.NSLayoutConstraint.LayoutAttributeLeading
    NSLayoutAttributeTrailing = appkit_module.NSLayoutConstraint.LayoutAttributeTrailing
    NSLayoutAttributeBottom = appkit_module.NSLayoutConstraint.LayoutAttributeBottom
    NSLayoutAttributeCenterX = appkit_module.NSLayoutConstraint.LayoutAttributeCenterX
    NSLayoutAttributeCenterY = appkit_module.NSLayoutConstraint.LayoutAttributeCenterY
    NSLayoutRelationEqual = appkit_module.NSLayoutConstraint.LayoutRelationEqual
    NSLayoutConstraintOrientationHorizontal = appkit_module.NSLayoutConstraint.LayoutConstraintOrientationHorizontal
    NSLayoutConstraintOrientationVertical = appkit_module.NSLayoutConstraint.LayoutConstraintOrientationVertical

try:
    from Foundation import NSObject
except ImportError:
    # Use mock for testing when Foundation is not available
    from ..mock_foundation import foundation_module
    NSObject = foundation_module.NSObject

import logging

from app.readings_manager import ReadingsManager
from app.views.card_display import CardSpreadView

logger = logging.getLogger(__name__)


class ReadingsViewController(NSViewController):
    """Controller for the readings tab."""
    
    def init(self):
        """Initialize the readings view controller."""
        self = super(ReadingsViewController, self).init()
        if self is None:
            return None
        
        # Initialize readings manager
        self.readings_manager = ReadingsManager()
        
        self.setupView()
        return self
    
    def setupView(self):
        """Set up the readings view."""
        # Create main view
        view_rect = NSMakeRect(0, 0, 800, 600)
        view = NSView.alloc().initWithFrame_(view_rect)
        view.setWantsLayer_(True)
        view.layer().setBackgroundColor_(NSColor.blackColor().CGColor())
        
        # Create spread selection buttons
        self.createSpreadButtons(view)
        
        # Create card display area
        self.createCardDisplayArea(view)
        
        # Create interpretation area
        self.createInterpretationArea(view)
        
        # Create control buttons
        self.createControlButtons(view)
        
        self.setView_(view)
    
    def createSpreadButtons(self, parent_view):
        """Create spread selection buttons."""
        # Single card button
        single_button = NSButton.alloc().initWithFrame_(
            NSMakeRect(50, 500, 120, 40)
        )
        single_button.setTitle_("Single")
        single_button.setTarget_(self)
        single_button.setAction_("singleCardPressed:")
        single_button.setBordered_(True)
        single_button.setBezelStyle_(NSButton.RoundedBezelStyle)
        parent_view.addSubview_(single_button)
        
        # Three card button
        three_button = NSButton.alloc().initWithFrame_(
            NSMakeRect(180, 500, 120, 40)
        )
        three_button.setTitle_("Three-Card")
        three_button.setTarget_(self)
        three_button.setAction_("threeCardPressed:")
        three_button.setBordered_(True)
        three_button.setBezelStyle_(NSButton.RoundedBezelStyle)
        parent_view.addSubview_(three_button)
        
        # Celtic Cross button
        celtic_button = NSButton.alloc().initWithFrame_(
            NSMakeRect(310, 500, 120, 40)
        )
        celtic_button.setTitle_("Celtic Cross")
        celtic_button.setTarget_(self)
        celtic_button.setAction_("celticCrossPressed:")
        celtic_button.setBordered_(True)
        celtic_button.setBezelStyle_(NSButton.RoundedBezelStyle)
        parent_view.addSubview_(celtic_button)
    
    def createCardDisplayArea(self, parent_view):
        """Create area for displaying drawn cards."""
        # Create card spread view
        spread_rect = NSMakeRect(50, 200, 700, 300)
        self.card_spread_view = CardSpreadView.alloc().initWithFrame_(spread_rect)
        parent_view.addSubview_(self.card_spread_view)
    
    def createInterpretationArea(self, parent_view):
        """Create interpretation text area."""
        interpretation_rect = NSMakeRect(50, 50, 700, 200)
        interpretation_view = NSTextView.alloc().initWithFrame_(interpretation_rect)
        interpretation_view.setString_("The cards await your interpretation...")
        interpretation_view.setEditable_(False)
        interpretation_view.setSelectable_(True)
        interpretation_view.setBackgroundColor_(NSColor.blackColor())
        interpretation_view.setTextColor_(NSColor.lightGrayColor())
        
        # Set monospaced font
        font = NSFont.fontWithName_size_("Monaco", 12)
        interpretation_view.setFont_(font)
        
        parent_view.addSubview_(interpretation_view)
        self.interpretation_view = interpretation_view
    
    def createControlButtons(self, parent_view):
        """Create control buttons for the reading."""
        # Draw cards button
        draw_button = NSButton.alloc().initWithFrame_(
            NSMakeRect(50, 150, 120, 40)
        )
        draw_button.setTitle_("Draw Cards")
        draw_button.setTarget_(self)
        draw_button.setAction_("drawCardsPressed:")
        draw_button.setBordered_(True)
        draw_button.setBezelStyle_(NSButton.RoundedBezelStyle)
        parent_view.addSubview_(draw_button)
        
        # Clear reading button
        clear_button = NSButton.alloc().initWithFrame_(
            NSMakeRect(180, 150, 120, 40)
        )
        clear_button.setTitle_("Clear Reading")
        clear_button.setTarget_(self)
        clear_button.setAction_("clearReadingPressed:")
        clear_button.setBordered_(True)
        clear_button.setBezelStyle_(NSButton.RoundedBezelStyle)
        parent_view.addSubview_(clear_button)
    
    # Button actions
    def singleCardPressed_(self, sender):
        """Handle single card spread selection."""
        logger.info("Single card spread selected")
        self.createReading("single")
    
    def threeCardPressed_(self, sender):
        """Handle three card spread selection."""
        logger.info("Three card spread selected")
        self.createReading("three")
    
    def celticCrossPressed_(self, sender):
        """Handle Celtic Cross spread selection."""
        logger.info("Celtic Cross spread selected")
        self.createReading("celtic_cross")
    
    def drawCardsPressed_(self, sender):
        """Handle draw cards button press."""
        logger.info("Draw cards button pressed")
        self.drawCards()
    
    def clearReadingPressed_(self, sender):
        """Handle clear reading button press."""
        logger.info("Clear reading button pressed")
        self.clearReading()
    
    def createReading(self, spread_type):
        """Create a new reading with the specified spread type."""
        success = self.readings_manager.createReading(spread_type)
        if success:
            logger.info(f"Created {spread_type} reading")
            self.updateInterpretation("Reading created. Click 'Draw Cards' to begin.")
        else:
            logger.error(f"Failed to create {spread_type} reading")
            self.updateInterpretation("Failed to create reading. Please try again.")
    
    def drawCards(self):
        """Draw cards for the current reading."""
        success = self.readings_manager.drawCards()
        if success:
            # Update card display
            cards_data = self.readings_manager.getReadingCards()
            spread_type = self.readings_manager.getCurrentSpreadType()
            self.card_spread_view.setSpread(cards_data, spread_type)
            
            # Update interpretation
            interpretation = self.readings_manager.getReadingInterpretation()
            self.updateInterpretation(interpretation)
            
            logger.info("Cards drawn successfully")
        else:
            logger.error("Failed to draw cards")
            self.updateInterpretation("Failed to draw cards. Please try again.")
    
    def clearReading(self):
        """Clear the current reading."""
        self.readings_manager.clearReading()
        self.card_spread_view.setSpread([], "single")
        self.updateInterpretation("Reading cleared. Select a spread to begin.")
        logger.info("Reading cleared")
    
    def updateInterpretation(self, text):
        """Update the interpretation text."""
        self.interpretation_view.setString_(text)