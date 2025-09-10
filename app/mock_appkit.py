"""
Mock AppKit module for testing when PyObjC is not available.
"""

import sys
from unittest.mock import Mock

# Create mock AppKit module
appkit_module = type(sys)('AppKit')

# Mock NSApplication
class NSApplication:
    @staticmethod
    def sharedApplication():
        return Mock()
    
    def setDelegate_(self, delegate):
        pass
    
    def run(self):
        pass

# Mock NSObject
class NSObject:
    @classmethod
    def alloc(cls):
        return cls()
    
    def init(self):
        return self
    
    def __init__(self):
        pass

# Mock NSApp
NSApp = Mock()

# Mock NSWindow
class NSWindow:
    TitledWindowMask = 1
    ClosableWindowMask = 2
    MiniaturizableWindowMask = 4
    ResizableWindowMask = 8
    Buffered = 1
    
    def __init__(self):
        self.title = ""
        self.min_size = (800, 600)
        self.background_color = None
    
    def initWithContentRect_styleMask_backing_defer_(self, rect, style, backing, defer):
        return self
    
    def setTitle_(self, title):
        self.title = title
    
    def setMinSize_(self, size):
        self.min_size = size
    
    def setBackgroundColor_(self, color):
        self.background_color = color
    
    def center(self):
        pass
    
    def makeKeyAndOrderFront_(self, sender):
        pass
    
    def close(self):
        pass

# Mock NSWindowController
class NSWindowController:
    def __init__(self):
        self.window_instance = None
    
    def initWithWindow_(self, window):
        self.window_instance = window
        return self
    
    def window(self):
        return self.window_instance
    
    def showWindow_(self, sender):
        pass

# Mock NSView
class NSView:
    WidthSizable = 1
    HeightSizable = 2
    
    def __init__(self):
        self.frame_instance = None
        self.subviews = []
        self.layer_instance = None
    
    def initWithFrame_(self, frame):
        self.frame_instance = frame
        return self
    
    def frame(self):
        return self.frame_instance
    
    def setWantsLayer_(self, wants):
        if wants:
            self.layer_instance = Mock()
    
    def layer(self):
        return self.layer_instance
    
    def setAutoresizingMask_(self, mask):
        pass
    
    def addSubview_(self, view):
        self.subviews.append(view)
    
    def removeFromSuperview(self):
        pass

# Mock NSColor
class NSColor:
    @staticmethod
    def blackColor():
        return Mock()
    
    @staticmethod
    def whiteColor():
        return Mock()
    
    @staticmethod
    def lightGrayColor():
        return Mock()
    
    @staticmethod
    def darkGrayColor():
        return Mock()
    
    @staticmethod
    def clearColor():
        return Mock()
    
    def CGColor(self):
        return Mock()

# Mock NSRect and NSMakeRect
class NSRect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def size(self):
        return Mock(width=self.width, height=self.height)

def NSMakeRect(x, y, width, height):
    return NSRect(x, y, width, height)

# Mock NSButton
class NSButton:
    RoundedBezelStyle = 1
    SwitchButton = 1
    
    def __init__(self):
        self.title = ""
        self.target = None
        self.action = None
        self.bordered = True
        self.bezel_style = None
        self.state = 0
    
    def initWithFrame_(self, frame):
        return self
    
    def setTitle_(self, title):
        self.title = title
    
    def setTarget_(self, target):
        self.target = target
    
    def setAction_(self, action):
        self.action = action
    
    def setBordered_(self, bordered):
        self.bordered = bordered
    
    def setBezelStyle_(self, style):
        self.bezel_style = style
    
    def setButtonType_(self, button_type):
        pass
    
    def setState_(self, state):
        self.state = state
    
    def state(self):
        return self.state

# Mock NSTextField
class NSTextField:
    CenterTextAlignment = 1
    
    def __init__(self):
        self.string_value = ""
        self.editable = True
        self.bordered = True
        self.background_color = None
        self.text_color = None
        self.font = None
        self.placeholder_string = ""
        self.target = None
        self.action = None
    
    def initWithFrame_(self, frame):
        return self
    
    def setStringValue_(self, value):
        self.string_value = value
    
    def stringValue(self):
        return self.string_value
    
    def setEditable_(self, editable):
        self.editable = editable
    
    def setBordered_(self, bordered):
        self.bordered = bordered
    
    def setBackgroundColor_(self, color):
        self.background_color = color
    
    def setTextColor_(self, color):
        self.text_color = color
    
    def setFont_(self, font):
        self.font = font
    
    def setPlaceholderString_(self, placeholder):
        self.placeholder_string = placeholder
    
    def setTarget_(self, target):
        self.target = target
    
    def setAction_(self, action):
        self.action = action
    
    def setAlignment_(self, alignment):
        pass

# Mock NSTextView
class NSTextView:
    def __init__(self):
        self.string_value = ""
        self.editable = True
        self.selectable = True
        self.background_color = None
        self.text_color = None
        self.font = None
    
    def initWithFrame_(self, frame):
        return self
    
    def setString_(self, value):
        self.string_value = value
    
    def string(self):
        return self.string_value
    
    def setEditable_(self, editable):
        self.editable = editable
    
    def setSelectable_(self, selectable):
        self.selectable = selectable
    
    def setBackgroundColor_(self, color):
        self.background_color = color
    
    def setTextColor_(self, color):
        self.text_color = color
    
    def setFont_(self, font):
        self.font = font
    
    def scrollToEndOfDocument_(self, sender):
        pass

# Mock NSFont
class NSFont:
    @staticmethod
    def fontWithName_size_(name, size):
        return Mock()

# Mock NSTableView
class NSTableView:
    def __init__(self):
        self.data_source = None
        self.delegate = None
        self.columns = []
        self.selected_row = -1
    
    def initWithFrame_(self, frame):
        return self
    
    def setDataSource_(self, data_source):
        self.data_source = data_source
    
    def setDelegate_(self, delegate):
        self.delegate = delegate
    
    def addTableColumn_(self, column):
        self.columns.append(column)
    
    def reloadData(self):
        pass
    
    def selectedRow(self):
        return self.selected_row

# Mock NSTableColumn
class NSTableColumn:
    def __init__(self):
        self.identifier = ""
        self.title = ""
        self.width = 100
    
    def initWithIdentifier_(self, identifier):
        self.identifier = identifier
        return self
    
    def setTitle_(self, title):
        self.title = title
    
    def setWidth_(self, width):
        self.width = width

# Mock NSTabView
class NSTabView:
    def __init__(self):
        self.tab_items = []
    
    def initWithFrame_(self, frame):
        return self
    
    def setAutoresizingMask_(self, mask):
        pass
    
    def addTabViewItem_(self, item):
        self.tab_items.append(item)

# Mock NSTabViewItem
class NSTabViewItem:
    def __init__(self):
        self.identifier = ""
        self.label = ""
        self.view = None
    
    def initWithIdentifier_(self, identifier):
        self.identifier = identifier
        return self
    
    def setLabel_(self, label):
        self.label = label
    
    def setView_(self, view):
        self.view = view

# Mock NSViewController
class NSViewController:
    def __init__(self):
        self.view_instance = None
    
    def init(self):
        return self
    
    def setView_(self, view):
        self.view_instance = view
    
    def view(self):
        return self.view_instance

# Mock NSImageView
class NSImageView:
    ScaleProportionallyUpOrDown = 1
    
    def __init__(self):
        self.image = None
        self.image_scaling = None
    
    def initWithFrame_(self, frame):
        return self
    
    def setImage_(self, image):
        self.image = image
    
    def setImageScaling_(self, scaling):
        self.image_scaling = scaling

# Mock NSImage
class NSImage:
    ScaleProportionallyUpOrDown = 1

# Mock NSLayoutConstraint
class NSLayoutConstraint:
    LayoutAttributeTop = 1
    LayoutAttributeLeading = 2
    LayoutAttributeTrailing = 3
    LayoutAttributeBottom = 4
    LayoutAttributeCenterX = 5
    LayoutAttributeCenterY = 6
    LayoutRelationEqual = 1
    LayoutConstraintOrientationHorizontal = 1
    LayoutConstraintOrientationVertical = 2

# Mock NSFontManager
class NSFontManager:
    pass

# Mock NSTableViewDataSource
class NSTableViewDataSource:
    pass

# Mock NSTableViewDelegate
class NSTableViewDelegate:
    pass

# Add all mocks to the module
appkit_module.NSApplication = NSApplication
appkit_module.NSObject = NSObject
appkit_module.NSApp = NSApp
appkit_module.NSWindow = NSWindow
appkit_module.NSWindowController = NSWindowController
appkit_module.NSView = NSView
appkit_module.NSColor = NSColor
appkit_module.NSRect = NSRect
appkit_module.NSMakeRect = NSMakeRect
appkit_module.NSButton = NSButton
appkit_module.NSTextField = NSTextField
appkit_module.NSTextView = NSTextView
appkit_module.NSFont = NSFont
appkit_module.NSTableView = NSTableView
appkit_module.NSTableColumn = NSTableColumn
appkit_module.NSTabView = NSTabView
appkit_module.NSTabViewItem = NSTabViewItem
appkit_module.NSViewController = NSViewController
appkit_module.NSImageView = NSImageView
appkit_module.NSImage = NSImage
appkit_module.NSLayoutConstraint = NSLayoutConstraint
appkit_module.NSFontManager = NSFontManager
appkit_module.NSTableViewDataSource = NSTableViewDataSource
appkit_module.NSTableViewDelegate = NSTableViewDelegate

# Add to sys.modules
sys.modules['AppKit'] = appkit_module

# Export the module
__all__ = ['appkit_module']