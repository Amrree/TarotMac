# GUI Module

The GUI module provides the macOS native user interface for the Tarot application, built using PyObjC and AppKit.

## Overview

This module implements a complete macOS application with:
- Native macOS window management
- Tabbed interface for different features
- Integration with all core modules
- Dark theme with Zed-inspired aesthetics
- Responsive UI components

## Architecture

### Core Components

#### App Delegate (`app_delegate.py`)
- `TarotAppDelegate`: Main application delegate
- Handles application lifecycle events
- Coordinates between GUI and core modules
- Manages main window creation and display

#### View Controllers
- `HomeViewController`: Dashboard and welcome screen
- `ReadingsViewController`: Tarot reading interface
- `ChatViewController`: AI chat interface
- `HistoryViewController`: Reading history management
- `SettingsViewController`: Application settings

#### Managers
- `ReadingsManager`: Integrates GUI with core readings functionality
- `ChatManager`: Integrates GUI with AI chat functionality
- `HistoryManager`: Integrates GUI with history management
- `SettingsManager`: Integrates GUI with settings management

#### Custom Views
- `CardDisplayView`: Displays individual tarot cards
- `CardSpreadView`: Displays card spreads (single, three-card, Celtic Cross)

## Features

### Readings Interface
- **Spread Selection**: Choose from single card, three-card, Celtic Cross, relationship, and year-ahead spreads
- **Card Drawing**: Draw cards with optional shuffle seed for reproducibility
- **Card Display**: Visual representation of drawn cards with orientation
- **Interpretation**: Real-time interpretation using the influence engine
- **Reading Management**: Create, clear, and manage readings

### Chat Interface
- **AI Integration**: Chat with the AI about tarot cards and readings
- **Session Management**: Persistent chat sessions with memory
- **Message History**: View and manage conversation history
- **Real-time Responses**: Stream responses from the AI

### History Interface
- **Reading Storage**: View all saved readings
- **Search Functionality**: Search readings by content, spread type, or date
- **Reading Management**: Delete, export, and import readings
- **Table View**: Sortable table with reading details

### Settings Interface
- **App Configuration**: Theme, auto-save, logging settings
- **User Preferences**: Default spread, AI model, encryption settings
- **Settings Management**: Save, reset, export, and import settings
- **Real-time Updates**: Settings applied immediately

## Usage

### Basic Application Launch

```python
from app.main import main

if __name__ == "__main__":
    main()
```

### Using Individual Managers

```python
from app.readings_manager import ReadingsManager
from app.chat_manager import ChatManager
from app.history_manager import HistoryManager
from app.settings_manager import SettingsManager

# Readings
readings_manager = ReadingsManager()
readings_manager.createReading("single")
readings_manager.drawCards()
cards = readings_manager.getReadingCards()

# Chat
chat_manager = ChatManager()
chat_manager.startNewSession()
response = chat_manager.sendMessage("Hello")

# History
history_manager = HistoryManager()
readings = history_manager.getAllReadings()
results = history_manager.searchReadings("query")

# Settings
settings_manager = SettingsManager()
config = settings_manager.getAppConfig()
preferences = settings_manager.getUserPreferences()
```

### Custom View Usage

```python
from app.views.card_display import CardDisplayView, CardSpreadView

# Single card display
card_view = CardDisplayView.alloc().initWithFrame_(frame)
card_view.setCard(card_data, is_reversed=False)

# Card spread display
spread_view = CardSpreadView.alloc().initWithFrame_(frame)
spread_view.setSpread(cards_data, "three")
```

## Integration

### Core Module Integration

The GUI module integrates with all core modules:

- **Deck Module**: Card drawing and management
- **Spreads Module**: Spread creation and interpretation
- **Influence Engine**: Card influence calculations
- **AI Module**: Chat functionality and AI responses
- **History Module**: Reading storage and retrieval
- **Settings Module**: Configuration management

### Data Flow

1. **User Input**: User interacts with GUI components
2. **Manager Processing**: Managers process input and call core modules
3. **Core Module Execution**: Core modules perform business logic
4. **Response Handling**: Managers handle responses and update UI
5. **UI Update**: View controllers update display

## Testing

### Unit Tests

Run the GUI module tests:

```bash
python3 -m pytest tests/unit/test_gui_module.py
```

### Test Coverage

Tests cover:
- App delegate functionality
- Manager integration
- View controller behavior
- Custom view components
- Error handling and edge cases

### Example Usage

Run the example usage script:

```bash
python3 app/example_usage.py
```

## Dependencies

### Required
- `PyObjC`: macOS native UI framework
- `AppKit`: macOS application framework
- `Foundation`: Core macOS framework

### Core Module Dependencies
- `core.deck`: Card and deck management
- `core.spreads`: Spread layouts and readings
- `core.influence`: Card influence engine
- `ai`: AI chat functionality
- `history`: Reading storage and retrieval
- `settings`: Configuration management

## File Structure

```
app/
├── main.py                 # Application entry point
├── app_delegate.py         # Application delegate
├── readings_manager.py     # Readings integration
├── chat_manager.py         # Chat integration
├── history_manager.py      # History integration
├── settings_manager.py     # Settings integration
├── example_usage.py        # Usage examples
├── README.md              # This file
└── views/
    ├── main_window.py      # Main window controller
    ├── home_view.py        # Home view controller
    ├── readings_view.py    # Readings view controller
    ├── chat_view.py        # Chat view controller
    ├── history_view.py     # History view controller
    ├── settings_view.py    # Settings view controller
    └── card_display.py     # Custom card display views
```

## Future Enhancements

### Planned Features
- **Card Images**: Load and display actual tarot card images
- **Animations**: Smooth transitions and card flip animations
- **Drag & Drop**: Drag cards between positions
- **Custom Spreads**: User-defined spread layouts
- **Export Options**: Multiple export formats (PDF, HTML, etc.)
- **Accessibility**: VoiceOver support and keyboard navigation

### UI Improvements
- **Responsive Layout**: Better handling of different window sizes
- **Theme Customization**: Multiple theme options
- **Font Options**: Customizable fonts and sizes
- **Layout Options**: Customizable UI layouts

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all core modules are properly installed
2. **UI Not Displaying**: Check that PyObjC is correctly installed
3. **Manager Errors**: Verify core module dependencies are available
4. **Memory Issues**: Ensure proper cleanup of view controllers

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Optimization

- Use lazy loading for large datasets
- Implement view recycling for table views
- Cache frequently accessed data
- Optimize image loading and display

## Contributing

When contributing to the GUI module:

1. Follow macOS Human Interface Guidelines
2. Maintain consistent dark theme
3. Test on different macOS versions
4. Ensure accessibility compliance
5. Update documentation for new features
6. Add tests for new functionality

## License

This module is part of the Tarot application and follows the same license terms.