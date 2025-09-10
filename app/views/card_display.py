"""
Card display component for showing tarot cards in the GUI.
"""

try:
    from AppKit import (
        NSView, NSRect, NSMakeRect, NSColor, NSImage, NSImageView,
        NSTextField, NSFont, NSLayoutConstraint, NSLayoutAttributeTop,
        NSLayoutAttributeLeading, NSLayoutAttributeTrailing, NSLayoutAttributeBottom,
        NSLayoutAttributeCenterX, NSLayoutAttributeCenterY, NSLayoutRelationEqual
    )
except ImportError:
    # Use mock for testing when AppKit is not available
    from ..mock_appkit import appkit_module
    NSView = appkit_module.NSView
    NSRect = appkit_module.NSRect
    NSMakeRect = appkit_module.NSMakeRect
    NSColor = appkit_module.NSColor
    NSImage = appkit_module.NSImage
    NSImageView = appkit_module.NSImageView
    NSTextField = appkit_module.NSTextField
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

logger = logging.getLogger(__name__)


class CardDisplayView(NSView):
    """Custom view for displaying a single tarot card."""
    
    def __init__(self, frame):
        """Initialize the card display view."""
        super(CardDisplayView, self).__init__(frame)
        self.card_data = None
        self.is_reversed = False
        self.setupView()
    
    def setupView(self):
        """Set up the card display view."""
        self.setWantsLayer_(True)
        self.layer().setBackgroundColor_(NSColor.darkGrayColor().CGColor())
        self.layer().setBorderWidth_(1.0)
        self.layer().setBorderColor_(NSColor.lightGrayColor().CGColor())
        self.layer().setCornerRadius_(8.0)
        
        # Create card image view
        image_rect = NSMakeRect(10, 10, self.frame().size.width - 20, self.frame().size.height - 40)
        self.card_image_view = NSImageView.alloc().initWithFrame_(image_rect)
        self.card_image_view.setImageScaling_(NSImage.ScaleProportionallyUpOrDown)
        self.addSubview_(self.card_image_view)
        
        # Create card name label
        name_rect = NSMakeRect(10, self.frame().size.height - 30, self.frame().size.width - 20, 20)
        self.card_name_label = NSTextField.alloc().initWithFrame_(name_rect)
        self.card_name_label.setStringValue_("Card Name")
        self.card_name_label.setEditable_(False)
        self.card_name_label.setBordered_(False)
        self.card_name_label.setBackgroundColor_(NSColor.clearColor())
        self.card_name_label.setTextColor_(NSColor.lightGrayColor())
        self.card_name_label.setFont_(NSFont.fontWithName_size_("Helvetica", 12))
        self.card_name_label.setAlignment_(NSTextField.CenterTextAlignment)
        self.addSubview_(self.card_name_label)
    
    def setCard(self, card_data, is_reversed=False):
        """Set the card data to display."""
        self.card_data = card_data
        self.is_reversed = is_reversed
        
        if card_data:
            # Update card name
            name = card_data.name
            if is_reversed:
                name += " (Reversed)"
            self.card_name_label.setStringValue_(name)
            
            # TODO: Load card image when available
            # For now, just show placeholder
            self.showPlaceholder()
        else:
            self.showPlaceholder()
    
    def showPlaceholder(self):
        """Show placeholder for missing card."""
        self.card_name_label.setStringValue_("No Card")
        # TODO: Set placeholder image
        self.card_image_view.setImage_(None)
    
    def getCardData(self):
        """Get the current card data."""
        return self.card_data
    
    def getIsReversed(self):
        """Get whether the card is reversed."""
        return self.is_reversed


class CardSpreadView(NSView):
    """View for displaying a spread of cards."""
    
    def __init__(self, frame):
        """Initialize the card spread view."""
        super(CardSpreadView, self).__init__(frame)
        self.card_views = []
        self.setupView()
    
    def setupView(self):
        """Set up the card spread view."""
        self.setWantsLayer_(True)
        self.layer().setBackgroundColor_(NSColor.blackColor().CGColor())
    
    def setSpread(self, cards_data, spread_type="single"):
        """Set the cards to display in the spread."""
        # Clear existing cards
        for card_view in self.card_views:
            card_view.removeFromSuperview()
        self.card_views = []
        
        if not cards_data:
            return
        
        # Create card views based on spread type
        if spread_type == "single":
            self.createSingleCardLayout(cards_data)
        elif spread_type == "three":
            self.createThreeCardLayout(cards_data)
        elif spread_type == "celtic_cross":
            self.createCelticCrossLayout(cards_data)
        else:
            self.createSingleCardLayout(cards_data)
    
    def createSingleCardLayout(self, cards_data):
        """Create layout for single card spread."""
        if not cards_data:
            return
        
        card_width = 120
        card_height = 180
        x = (self.frame().size.width - card_width) / 2
        y = (self.frame().size.height - card_height) / 2
        
        card_view = CardDisplayView.alloc().initWithFrame_(
            NSMakeRect(x, y, card_width, card_height)
        )
        card_view.setCard(cards_data[0])
        self.addSubview_(card_view)
        self.card_views.append(card_view)
    
    def createThreeCardLayout(self, cards_data):
        """Create layout for three card spread."""
        if len(cards_data) < 3:
            return
        
        card_width = 100
        card_height = 150
        card_spacing = 20
        total_width = 3 * card_width + 2 * card_spacing
        start_x = (self.frame().size.width - total_width) / 2
        y = (self.frame().size.height - card_height) / 2
        
        for i, card_data in enumerate(cards_data[:3]):
            x = start_x + i * (card_width + card_spacing)
            card_view = CardDisplayView.alloc().initWithFrame_(
                NSMakeRect(x, y, card_width, card_height)
            )
            card_view.setCard(card_data)
            self.addSubview_(card_view)
            self.card_views.append(card_view)
    
    def createCelticCrossLayout(self, cards_data):
        """Create layout for Celtic Cross spread."""
        if len(cards_data) < 10:
            return
        
        card_width = 80
        card_height = 120
        card_spacing = 15
        
        # Position cards in Celtic Cross pattern
        positions = [
            (200, 200),  # Center cross
            (200, 320),  # Cross
            (200, 80),   # Above
            (200, 440),  # Below
            (80, 200),   # Left
            (320, 200),  # Right
            (440, 200),  # Staff
            (440, 320),  # Staff
            (440, 440),  # Staff
            (440, 560)   # Staff
        ]
        
        for i, (x, y) in enumerate(positions):
            if i < len(cards_data):
                card_view = CardDisplayView.alloc().initWithFrame_(
                    NSMakeRect(x, y, card_width, card_height)
                )
                card_view.setCard(cards_data[i])
                self.addSubview_(card_view)
                self.card_views.append(card_view)
    
    def getCardViews(self):
        """Get all card views in the spread."""
        return self.card_views