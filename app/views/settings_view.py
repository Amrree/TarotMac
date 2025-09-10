"""Settings view controller."""

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

from app.settings_manager import SettingsManager

logger = logging.getLogger(__name__)


class SettingsViewController(NSViewController):
    """Controller for the settings tab."""
    
    def init(self):
        self = super(SettingsViewController, self).init()
        if self is None:
            return None
        
        # Initialize settings manager
        self.settings_manager = SettingsManager()
        
        self.setupView()
        return self
    
    def setupView(self):
        """Set up the settings view."""
        view_rect = NSMakeRect(0, 0, 800, 600)
        view = NSView.alloc().initWithFrame_(view_rect)
        view.setWantsLayer_(True)
        view.layer().setBackgroundColor_(NSColor.blackColor().CGColor())
        
        # Create settings sections
        self.createAppConfigSection(view)
        self.createUserPreferencesSection(view)
        
        # Create control buttons
        self.createControlButtons(view)
        
        self.setView_(view)
    
    def createAppConfigSection(self, parent_view):
        """Create application configuration section."""
        # Section title
        title_rect = NSMakeRect(50, 500, 200, 30)
        title_label = NSTextField.alloc().initWithFrame_(title_rect)
        title_label.setStringValue_("Application Configuration")
        title_label.setEditable_(False)
        title_label.setBordered_(False)
        title_label.setBackgroundColor_(NSColor.clearColor())
        title_label.setTextColor_(NSColor.lightGrayColor())
        title_label.setFont_(NSFont.fontWithName_size_("Helvetica-Bold", 14))
        parent_view.addSubview_(title_label)
        
        # App name field
        name_label = NSTextField.alloc().initWithFrame_(NSMakeRect(50, 470, 100, 20))
        name_label.setStringValue_("App Name:")
        name_label.setEditable_(False)
        name_label.setBordered_(False)
        name_label.setBackgroundColor_(NSColor.clearColor())
        name_label.setTextColor_(NSColor.lightGrayColor())
        parent_view.addSubview_(name_label)
        
        self.app_name_field = NSTextField.alloc().initWithFrame_(NSMakeRect(160, 470, 200, 20))
        self.app_name_field.setStringValue_("Tarot")
        self.app_name_field.setBackgroundColor_(NSColor.darkGrayColor())
        self.app_name_field.setTextColor_(NSColor.lightGrayColor())
        parent_view.addSubview_(self.app_name_field)
        
        # Theme field
        theme_label = NSTextField.alloc().initWithFrame_(NSMakeRect(50, 440, 100, 20))
        theme_label.setStringValue_("Theme:")
        theme_label.setEditable_(False)
        theme_label.setBordered_(False)
        theme_label.setBackgroundColor_(NSColor.clearColor())
        theme_label.setTextColor_(NSColor.lightGrayColor())
        parent_view.addSubview_(theme_label)
        
        self.theme_field = NSTextField.alloc().initWithFrame_(NSMakeRect(160, 440, 200, 20))
        self.theme_field.setStringValue_("dark")
        self.theme_field.setBackgroundColor_(NSColor.darkGrayColor())
        self.theme_field.setTextColor_(NSColor.lightGrayColor())
        parent_view.addSubview_(self.theme_field)
        
        # Auto save checkbox
        self.auto_save_checkbox = NSButton.alloc().initWithFrame_(NSMakeRect(50, 410, 200, 20))
        self.auto_save_checkbox.setTitle_("Auto Save Readings")
        self.auto_save_checkbox.setButtonType_(NSButton.SwitchButton)
        self.auto_save_checkbox.setState_(1)  # On
        parent_view.addSubview_(self.auto_save_checkbox)
    
    def createUserPreferencesSection(self, parent_view):
        """Create user preferences section."""
        # Section title
        title_rect = NSMakeRect(50, 350, 200, 30)
        title_label = NSTextField.alloc().initWithFrame_(title_rect)
        title_label.setStringValue_("User Preferences")
        title_label.setEditable_(False)
        title_label.setBordered_(False)
        title_label.setBackgroundColor_(NSColor.clearColor())
        title_label.setTextColor_(NSColor.lightGrayColor())
        title_label.setFont_(NSFont.fontWithName_size_("Helvetica-Bold", 14))
        parent_view.addSubview_(title_label)
        
        # Default spread field
        spread_label = NSTextField.alloc().initWithFrame_(NSMakeRect(50, 320, 100, 20))
        spread_label.setStringValue_("Default Spread:")
        spread_label.setEditable_(False)
        spread_label.setBordered_(False)
        spread_label.setBackgroundColor_(NSColor.clearColor())
        spread_label.setTextColor_(NSColor.lightGrayColor())
        parent_view.addSubview_(spread_label)
        
        self.default_spread_field = NSTextField.alloc().initWithFrame_(NSMakeRect(160, 320, 200, 20))
        self.default_spread_field.setStringValue_("single")
        self.default_spread_field.setBackgroundColor_(NSColor.darkGrayColor())
        self.default_spread_field.setTextColor_(NSColor.lightGrayColor())
        parent_view.addSubview_(self.default_spread_field)
        
        # AI model field
        model_label = NSTextField.alloc().initWithFrame_(NSMakeRect(50, 290, 100, 20))
        model_label.setStringValue_("AI Model:")
        model_label.setEditable_(False)
        model_label.setBordered_(False)
        model_label.setBackgroundColor_(NSColor.clearColor())
        model_label.setTextColor_(NSColor.lightGrayColor())
        parent_view.addSubview_(model_label)
        
        self.ai_model_field = NSTextField.alloc().initWithFrame_(NSMakeRect(160, 290, 200, 20))
        self.ai_model_field.setStringValue_("llama3.2")
        self.ai_model_field.setBackgroundColor_(NSColor.darkGrayColor())
        self.ai_model_field.setTextColor_(NSColor.lightGrayColor())
        parent_view.addSubview_(self.ai_model_field)
        
        # Encryption checkbox
        self.encryption_checkbox = NSButton.alloc().initWithFrame_(NSMakeRect(50, 260, 200, 20))
        self.encryption_checkbox.setTitle_("Enable Encryption")
        self.encryption_checkbox.setButtonType_(NSButton.SwitchButton)
        self.encryption_checkbox.setState_(0)  # Off
        parent_view.addSubview_(self.encryption_checkbox)
    
    def createControlButtons(self, parent_view):
        """Create control buttons."""
        # Save button
        save_button = NSButton.alloc().initWithFrame_(
            NSMakeRect(50, 50, 90, 30)
        )
        save_button.setTitle_("Save")
        save_button.setTarget_(self)
        save_button.setAction_("saveSettings:")
        save_button.setBordered_(True)
        save_button.setBezelStyle_(NSButton.RoundedBezelStyle)
        parent_view.addSubview_(save_button)
        
        # Reset button
        reset_button = NSButton.alloc().initWithFrame_(
            NSMakeRect(150, 50, 90, 30)
        )
        reset_button.setTitle_("Reset")
        reset_button.setTarget_(self)
        reset_button.setAction_("resetSettings:")
        reset_button.setBordered_(True)
        reset_button.setBezelStyle_(NSButton.RoundedBezelStyle)
        parent_view.addSubview_(reset_button)
        
        # Export button
        export_button = NSButton.alloc().initWithFrame_(
            NSMakeRect(250, 50, 90, 30)
        )
        export_button.setTitle_("Export")
        export_button.setTarget_(self)
        export_button.setAction_("exportSettings:")
        export_button.setBordered_(True)
        export_button.setBezelStyle_(NSButton.RoundedBezelStyle)
        parent_view.addSubview_(export_button)
        
        # Import button
        import_button = NSButton.alloc().initWithFrame_(
            NSMakeRect(350, 50, 90, 30)
        )
        import_button.setTitle_("Import")
        import_button.setTarget_(self)
        import_button.setAction_("importSettings:")
        import_button.setBordered_(True)
        import_button.setBezelStyle_(NSButton.RoundedBezelStyle)
        parent_view.addSubview_(import_button)
    
    def saveSettings_(self, sender):
        """Handle save settings button press."""
        # Collect settings from UI
        app_config = {
            'app_name': self.app_name_field.stringValue(),
            'theme': self.theme_field.stringValue(),
            'auto_save': self.auto_save_checkbox.state() == 1
        }
        
        user_preferences = {
            'default_spread': self.default_spread_field.stringValue(),
            'ai_model': self.ai_model_field.stringValue(),
            'encryption_enabled': self.encryption_checkbox.state() == 1
        }
        
        # Update settings
        self.settings_manager.updateAppConfig(app_config)
        self.settings_manager.updateUserPreferences(user_preferences)
        
        # Save to storage
        success = self.settings_manager.saveSettings()
        if success:
            logger.info("Settings saved successfully")
        else:
            logger.error("Failed to save settings")
    
    def resetSettings_(self, sender):
        """Handle reset settings button press."""
        success = self.settings_manager.resetToDefaults()
        if success:
            self.loadSettings()
            logger.info("Settings reset to defaults")
        else:
            logger.error("Failed to reset settings")
    
    def exportSettings_(self, sender):
        """Handle export settings button press."""
        # TODO: Implement file dialog for export path
        success = self.settings_manager.exportSettings("settings_export.json")
        if success:
            logger.info("Settings exported successfully")
        else:
            logger.error("Failed to export settings")
    
    def importSettings_(self, sender):
        """Handle import settings button press."""
        # TODO: Implement file dialog for import path
        success = self.settings_manager.importSettings("settings_export.json")
        if success:
            self.loadSettings()
            logger.info("Settings imported successfully")
        else:
            logger.error("Failed to import settings")
    
    def loadSettings(self):
        """Load settings into UI fields."""
        app_config = self.settings_manager.getAppConfig()
        user_preferences = self.settings_manager.getUserPreferences()
        
        # Update UI fields
        self.app_name_field.setStringValue_(app_config.get('app_name', 'Tarot'))
        self.theme_field.setStringValue_(app_config.get('theme', 'dark'))
        self.auto_save_checkbox.setState_(1 if app_config.get('auto_save', True) else 0)
        
        self.default_spread_field.setStringValue_(user_preferences.get('default_spread', 'single'))
        self.ai_model_field.setStringValue_(user_preferences.get('ai_model', 'llama3.2'))
        self.encryption_checkbox.setState_(1 if user_preferences.get('encryption_enabled', False) else 0)