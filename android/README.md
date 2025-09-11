# TarotMac Android App

A mobile-optimized Android version of the TarotMac tarot application, built with Python and Kivy for cross-platform compatibility.

## Features

- **Complete Tarot Deck**: Full 78-card deck with upright and reversed meanings
- **Multiple Spreads**: Single card, three-card, and Celtic Cross spreads
- **AI-Powered Insights**: Local Ollama LLM integration for personalized interpretations
- **Reading History**: Persistent storage and searchable reading history
- **Mobile-Optimized UI**: Material Design components with touch-friendly interface
- **Offline-First**: All functionality works without internet connection

## Architecture

### Core Modules (Reused from macOS version)
- **Deck Module**: Card management and canonical deck loading
- **Influence Engine**: Rule-based card interpretation system
- **Spreads Module**: Reading creation and interpretation
- **AI Module**: Ollama integration with chat memory
- **History Module**: Reading persistence and search
- **Settings Module**: Application configuration

### Android-Specific Components
- **Kivy Framework**: Cross-platform mobile development
- **KivyMD**: Material Design components for Android
- **Screen Management**: Navigation between app sections
- **Mobile UI**: Touch-optimized interface design

## Project Structure

```
android/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── buildozer.spec         # Android build configuration
├── screens/               # Screen implementations
│   ├── home_screen.py     # Dashboard and navigation
│   ├── readings_screen.py # Tarot readings interface
│   ├── chat_screen.py     # AI chat interface
│   ├── history_screen.py  # Reading history management
│   └── settings_screen.py # App settings and preferences
├── assets/                # App assets
│   ├── icon.png          # App icon
│   └── presplash.png     # Splash screen
└── README.md             # This file
```

## Installation

### Prerequisites
- Python 3.10+
- Android SDK
- Buildozer (for Android builds)

### Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Buildozer:
   ```bash
   pip install buildozer
   ```

3. Initialize Buildozer:
   ```bash
   buildozer init
   ```

### Development
Run the app in development mode:
```bash
python main.py
```

### Android Build
Build APK for Android:
```bash
buildozer android debug
```

## Usage

### Home Screen
- Dashboard with app status
- Quick action buttons for common tasks
- Navigation to all app features

### Readings Screen
- Select spread type (Single Card, Three Card, Celtic Cross)
- Draw cards for readings
- View card interpretations
- Clear readings

### Chat Screen
- AI-powered tarot conversations
- Chat history management
- Context-aware responses
- Session management

### History Screen
- View past readings
- Search and filter readings
- Export reading data
- Delete individual readings

### Settings Screen
- App configuration
- User preferences
- AI settings
- Data management

## Core Module Integration

The Android app reuses all core modules from the macOS version:

### Deck Integration
```python
from deck.deck_loader import DeckLoader
deck = DeckLoader.load_canonical_deck()
```

### Spreads Integration
```python
from spreads.spread_manager import SpreadManager, SpreadType
spread_manager = SpreadManager()
reading = spread_manager.create_reading(SpreadType.SINGLE_CARD, "Question")
```

### AI Integration
```python
from ai.ai_manager import AIManager
ai_manager = AIManager()
session = ai_manager.create_chat_session()
```

### Influence Engine Integration
```python
from influence.tarot_influence_engine import TarotInfluenceEngine
influence_engine = TarotInfluenceEngine()
interpretation = spread_manager.interpret_reading(reading, influence_engine)
```

## Mobile Optimizations

### Touch Interface
- Large touch targets (48dp minimum)
- Swipe gestures for navigation
- Touch-friendly card displays
- Responsive layouts

### Material Design
- Consistent color scheme
- Material Design components
- Proper elevation and shadows
- Android-standard navigation patterns

### Performance
- Efficient scrolling with MDScrollView
- Lazy loading of content
- Optimized card rendering
- Memory management

## Testing

### Unit Tests
```bash
python -m pytest tests/
```

### Android Testing
- Test on Android devices
- Verify touch interactions
- Test different screen sizes
- Validate Material Design compliance

## Deployment

### Google Play Store
1. Build release APK:
   ```bash
   buildozer android release
   ```

2. Sign the APK
3. Upload to Google Play Console
4. Configure store listing
5. Submit for review

### Requirements
- Android API 21+ (Android 5.0)
- Minimum 2GB RAM
- 100MB storage space
- Internet connection for AI features (optional)

## Troubleshooting

### Common Issues
- **Import Errors**: Ensure all core modules are in Python path
- **Build Errors**: Check Android SDK and NDK versions
- **UI Issues**: Verify KivyMD version compatibility
- **AI Errors**: Check Ollama installation and model availability

### Debug Mode
Enable debug mode in settings for detailed logging and error information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test on Android device
5. Submit pull request

## License

Same license as the main TarotMac project.

## Support

For issues and questions:
- Check the main TarotMac documentation
- Review Android-specific troubleshooting
- Test core module functionality
- Verify mobile UI components