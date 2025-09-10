# Technical Architecture

## Overview

The macOS Python Tarot App follows a clean architecture pattern with clear separation between UI, business logic, AI integration, and data persistence layers. The application is designed for offline-first operation with local Ollama LLM integration.

## Architecture Layers

### 1. UI Layer (`app/`)

**Technology**: PyObjC with AppKit
**Responsibility**: Native macOS user interface

```
app/
├── main.py              # Application entry point and main window
├── views/               # View controllers
│   ├── home_view.py     # Dashboard/home screen
│   ├── readings_view.py # Readings management
│   ├── chat_view.py     # Chat interface
│   ├── history_view.py  # Readings journal
│   └── settings_view.py # Configuration
├── models/              # UI data models
│   ├── reading_model.py # Reading display model
│   └── card_model.py    # Card display model
└── assets/              # Images, icons, fonts
```

**Key Design Principles**:
- Zed-inspired minimalist aesthetic
- Dark theme with cyan-blue accents
- Monospaced typography
- Generous spacing and clean layouts

### 2. Core Layer (`core/`)

**Responsibility**: Business logic for tarot functionality

```
core/
├── cards/               # Card management
│   ├── deck.py          # Deck operations
│   ├── card.py          # Individual card logic
│   └── canonical.py     # Canonical card data
├── spreads/             # Spread definitions
│   ├── spread_types.py  # Built-in spread types
│   ├── custom_spread.py # Custom spread editor
│   └── layout.py        # Spread layout logic
├── influence/           # Card influence engine
│   ├── engine.py        # Main influence computation
│   ├── rules.py         # Influence rules
│   └── vectors.py       # Influence vector math
└── journal/             # Readings journal
    ├── storage.py       # Reading persistence
    ├── search.py        # Search and filtering
    └── export.py        # Export/import functionality
```

**Card Influence Engine**:
- Rule-based system computing card interactions
- Influence vectors: polarity (-2..+2), intensity (0..1), themes
- Deterministic and fully unit-tested
- Supports adjacency weighting, major arcana dominance, suit interactions

### 3. AI Layer (`ai/`)

**Technology**: Ollama Python client
**Responsibility**: Local LLM integration and conversation management

```
ai/
├── ollama_client.py     # Ollama API client
├── prompts.py           # AI prompt templates
├── memory.py            # Conversation memory
├── schema.py            # JSON schema validation
└── streaming.py         # Streaming response handling
```

**Key Features**:
- Streaming responses for UI responsiveness
- JSON schema validation for structured outputs
- Memory management with user-controlled privacy
- Graceful fallback when Ollama unavailable

### 4. Data Layer (`db/`)

**Technology**: SQLite with SQLAlchemy ORM
**Responsibility**: Data persistence and management

```
db/
├── models.py            # SQLAlchemy models
├── migrations/          # Database migrations
├── canonical_deck.json  # Complete 78-card database
└── session.py           # Database session management
```

**Data Models**:
- Cards: Complete tarot deck with metadata
- Readings: Saved readings with positions and orientations
- Conversations: Chat history linked to readings
- Memory: AI conversation memory with privacy controls

## Data Flow

### Reading Creation Flow

1. **User Action**: User selects spread type and draws cards
2. **Core Processing**: Influence engine computes card interactions
3. **AI Enhancement**: Ollama generates influenced meanings and advice
4. **Storage**: Reading saved to SQLite with metadata
5. **UI Update**: Interface displays results with influence breakdown

### Chat Flow

1. **Context Seeding**: Chat initialized with card or reading context
2. **User Input**: User types question or request
3. **AI Processing**: Ollama generates response with memory context
4. **Response Display**: Streaming response shown in chat interface
5. **Memory Update**: Conversation stored with privacy controls

## Security and Privacy

### Data Encryption
- Sensitive fields encrypted at rest using user passphrase
- Integration with macOS Keychain for convenience
- Optional encrypted export/import functionality

### Privacy Controls
- All AI processing happens locally via Ollama
- User controls what AI can "remember" per conversation
- No telemetry or analytics by default
- Clear privacy documentation at first launch

## Performance Considerations

### Model Selection
- Default to lightweight models (3B parameters) for responsiveness
- User-configurable model selection based on hardware
- Streaming responses for real-time UI updates

### Database Optimization
- SQLite with proper indexing for search performance
- Local embeddings for semantic search capabilities
- Efficient query patterns for large reading collections

## Error Handling

### Graceful Degradation
- Fallback to static interpretations when Ollama unavailable
- Clear user feedback on AI status and errors
- Robust retry mechanisms with exponential backoff

### Validation
- All AI outputs validated against JSON schema
- Fallback responses when validation fails
- Comprehensive error logging for debugging

## Testing Strategy

### Unit Tests
- Influence engine rules and calculations
- Card database operations
- AI adapter schema validation
- Database model operations

### Integration Tests
- End-to-end reading creation and storage
- Chat functionality with AI integration
- Export/import functionality
- Error handling scenarios

### Acceptance Tests
- macOS .app packaging and launch
- Offline functionality verification
- Privacy controls validation
- Performance benchmarks

## Deployment Architecture

### macOS .app Packaging
- Py2app for native macOS application bundle
- Code signing for distribution
- Proper entitlements for Keychain access

### Distribution
- Self-contained application bundle
- No external dependencies beyond Ollama
- Clear installation and setup instructions

## Future Extensibility

### Cross-Platform Support
- Clean architecture enables alternative UI implementations
- Toga or PySide options for cross-platform deployment
- Shared core logic across platforms

### Advanced Features
- Cloud sync (opt-in) for reading backup
- Advanced learning modes with spaced repetition
- Plugin system for custom influence rules
- Multi-language support with localization

## Monitoring and Maintenance

### Logging
- Structured logging for debugging and monitoring
- Privacy-conscious logging (no sensitive data)
- Performance metrics collection

### Updates
- Self-updating mechanism for core application
- Model updates through Ollama integration
- Database migration system for schema changes