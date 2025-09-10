"""History view controller."""

try:
    from AppKit import (
        NSView, NSViewController, NSMakeRect, NSColor, NSTextField, NSTextView,
        NSButton, NSFont, NSTableView, NSTableColumn, NSTableViewDataSource,
        NSTableViewDelegate, NSLayoutConstraint, NSLayoutAttributeTop,
        NSLayoutAttributeLeading, NSLayoutAttributeTrailing, NSLayoutAttributeBottom,
        NSLayoutAttributeCenterX, NSLayoutAttributeCenterY, NSLayoutRelationEqual
    )
except ImportError:
    # Use mock for testing when AppKit is not available
    from ..mock_appkit import appkit_module
    NSView = appkit_module.NSView
    NSViewController = appkit_module.NSViewController
    NSMakeRect = appkit_module.NSMakeRect
    NSColor = appkit_module.NSColor
    NSTextField = appkit_module.NSTextField
    NSTextView = appkit_module.NSTextView
    NSButton = appkit_module.NSButton
    NSFont = appkit_module.NSFont
    NSTableView = appkit_module.NSTableView
    NSTableColumn = appkit_module.NSTableColumn
    NSTableViewDataSource = appkit_module.NSTableViewDataSource
    NSTableViewDelegate = appkit_module.NSTableViewDelegate
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

from app.history_manager import HistoryManager

logger = logging.getLogger(__name__)


class HistoryViewController(NSViewController):
    """Controller for the history tab."""
    
    def init(self):
        self = super(HistoryViewController, self).init()
        if self is None:
            return None
        
        # Initialize history manager
        self.history_manager = HistoryManager()
        
        self.setupView()
        return self
    
    def setupView(self):
        """Set up the history view."""
        view_rect = NSMakeRect(0, 0, 800, 600)
        view = NSView.alloc().initWithFrame_(view_rect)
        view.setWantsLayer_(True)
        view.layer().setBackgroundColor_(NSColor.blackColor().CGColor())
        
        # Create search area
        self.createSearchArea(view)
        
        # Create readings table
        self.createReadingsTable(view)
        
        # Create control buttons
        self.createControlButtons(view)
        
        # Load initial data
        self.loadReadings()
        
        self.setView_(view)
    
    def createSearchArea(self, parent_view):
        """Create the search area."""
        # Search field
        search_rect = NSMakeRect(50, 550, 400, 30)
        self.search_field = NSTextField.alloc().initWithFrame_(search_rect)
        self.search_field.setPlaceholderString_("Search readings...")
        self.search_field.setBackgroundColor_(NSColor.darkGrayColor())
        self.search_field.setTextColor_(NSColor.lightGrayColor())
        self.search_field.setFont_(NSFont.fontWithName_size_("Monaco", 12))
        
        # Set up search action
        self.search_field.setTarget_(self)
        self.search_field.setAction_("searchReadings:")
        
        parent_view.addSubview_(self.search_field)
        
        # Search button
        search_button = NSButton.alloc().initWithFrame_(
            NSMakeRect(460, 550, 90, 30)
        )
        search_button.setTitle_("Search")
        search_button.setTarget_(self)
        search_button.setAction_("searchReadings:")
        search_button.setBordered_(True)
        search_button.setBezelStyle_(NSButton.RoundedBezelStyle)
        parent_view.addSubview_(search_button)
    
    def createReadingsTable(self, parent_view):
        """Create the readings table."""
        table_rect = NSMakeRect(50, 100, 700, 400)
        self.readings_table = NSTableView.alloc().initWithFrame_(table_rect)
        self.readings_table.setDataSource_(self)
        self.readings_table.setDelegate_(self)
        
        # Create columns
        self.createTableColumns()
        
        parent_view.addSubview_(self.readings_table)
    
    def createTableColumns(self):
        """Create table columns."""
        # Date column
        date_column = NSTableColumn.alloc().initWithIdentifier_("date")
        date_column.setTitle_("Date")
        date_column.setWidth_(150)
        self.readings_table.addTableColumn_(date_column)
        
        # Spread type column
        spread_column = NSTableColumn.alloc().initWithIdentifier_("spread")
        spread_column.setTitle_("Spread")
        spread_column.setWidth_(120)
        self.readings_table.addTableColumn_(spread_column)
        
        # Cards column
        cards_column = NSTableColumn.alloc().initWithIdentifier_("cards")
        cards_column.setTitle_("Cards")
        cards_column.setWidth_(200)
        self.readings_table.addTableColumn_(cards_column)
        
        # Summary column
        summary_column = NSTableColumn.alloc().initWithIdentifier_("summary")
        summary_column.setTitle_("Summary")
        summary_column.setWidth_(230)
        self.readings_table.addTableColumn_(summary_column)
    
    def createControlButtons(self, parent_view):
        """Create control buttons."""
        # Refresh button
        refresh_button = NSButton.alloc().initWithFrame_(
            NSMakeRect(50, 50, 90, 30)
        )
        refresh_button.setTitle_("Refresh")
        refresh_button.setTarget_(self)
        refresh_button.setAction_("refreshReadings:")
        refresh_button.setBordered_(True)
        refresh_button.setBezelStyle_(NSButton.RoundedBezelStyle)
        parent_view.addSubview_(refresh_button)
        
        # Delete button
        delete_button = NSButton.alloc().initWithFrame_(
            NSMakeRect(150, 50, 90, 30)
        )
        delete_button.setTitle_("Delete")
        delete_button.setTarget_(self)
        delete_button.setAction_("deleteReading:")
        delete_button.setBordered_(True)
        delete_button.setBezelStyle_(NSButton.RoundedBezelStyle)
        parent_view.addSubview_(delete_button)
        
        # Export button
        export_button = NSButton.alloc().initWithFrame_(
            NSMakeRect(250, 50, 90, 30)
        )
        export_button.setTitle_("Export")
        export_button.setTarget_(self)
        export_button.setAction_("exportReadings:")
        export_button.setBordered_(True)
        export_button.setBezelStyle_(NSButton.RoundedBezelStyle)
        parent_view.addSubview_(export_button)
    
    def loadReadings(self):
        """Load readings from storage."""
        self.readings = self.history_manager.getAllReadings()
        self.readings_table.reloadData()
        logger.info(f"Loaded {len(self.readings)} readings")
    
    def searchReadings_(self, sender):
        """Handle search button press."""
        query = self.search_field.stringValue()
        results = self.history_manager.searchReadings(query)
        self.readings = results
        self.readings_table.reloadData()
        logger.info(f"Search returned {len(results)} results")
    
    def refreshReadings_(self, sender):
        """Handle refresh button press."""
        self.loadReadings()
        logger.info("Readings refreshed")
    
    def deleteReading_(self, sender):
        """Handle delete button press."""
        selected_row = self.readings_table.selectedRow()
        if selected_row >= 0 and selected_row < len(self.readings):
            reading = self.readings[selected_row]
            reading_id = reading.get('id')
            if reading_id:
                success = self.history_manager.deleteReading(reading_id)
                if success:
                    self.loadReadings()
                    logger.info(f"Deleted reading: {reading_id}")
                else:
                    logger.error(f"Failed to delete reading: {reading_id}")
    
    def exportReadings_(self, sender):
        """Handle export button press."""
        # TODO: Implement file dialog for export path
        success = self.history_manager.exportReadings("readings_export.json")
        if success:
            logger.info("Readings exported successfully")
        else:
            logger.error("Failed to export readings")
    
    # NSTableViewDataSource methods
    def numberOfRowsInTableView_(self, tableView):
        """Return number of rows in table."""
        return len(self.readings) if hasattr(self, 'readings') else 0
    
    def tableView_objectValueForTableColumn_row_(self, tableView, column, row):
        """Return value for table cell."""
        if row >= len(self.readings):
            return ""
        
        reading = self.readings[row]
        column_id = column.identifier()
        
        if column_id == "date":
            return reading.get('timestamp', 'Unknown')[:10]  # Just date part
        elif column_id == "spread":
            return reading.get('spread_type', 'Unknown')
        elif column_id == "cards":
            cards = reading.get('cards', [])
            return f"{len(cards)} cards"
        elif column_id == "summary":
            return reading.get('summary', 'No summary')[:50] + "..." if len(reading.get('summary', '')) > 50 else reading.get('summary', 'No summary')
        
        return ""