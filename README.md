# macOS Python Tarot App

A production-quality macOS native tarot application with local Ollama LLM integration, featuring a complete 78-card deck, configurable spreads, rule-driven card influence engine, and conversational AI capabilities.

## Features

- **Complete Tarot Deck**: All 78 cards (Major & Minor Arcana) with upright/reversed meanings
- **Configurable Spreads**: Single, Three-card, Celtic Cross, Relationship, Year-Ahead, and custom spreads
- **Card Influence Engine**: Rule-based system that computes how neighboring cards modify meanings
- **Conversational AI**: Chat with individual cards or entire readings using local Ollama LLM
- **Readings Journal**: Persistent, searchable storage of past readings with tags and metadata
- **Privacy-First**: Fully offline operation with optional encrypted export/import
- **Native macOS**: PyObjC-based UI with Zed-inspired minimalist aesthetic

## Quick Start

### Prerequisites

- macOS 12.0+ (Monterey or later)
- Python 3.10+
- Ollama installed and running locally

### Installation

1. **Install Ollama**:
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull recommended model
   ollama pull llama3.2:3b  # Lightweight model for good performance
   ```

2. **Clone and Setup**:
   ```bash
   git clone <repository-url>
   cd tarot-app
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python -m app.main
   ```

## Project Structure

```
tarot-app/
├── app/                    # PyObjC UI components
│   ├── main.py            # Application entry point
│   ├── views/             # View controllers
│   ├── models/            # UI data models
│   └── assets/            # Images, icons, etc.
├── core/                  # Core business logic
│   ├── cards/             # Card database and management
│   ├── spreads/           # Spread definitions and logic
│   ├── influence/         # Card influence engine
│   └── journal/           # Readings journal management
├── ai/                    # Ollama integration
│   ├── ollama_client.py   # Ollama API client
│   ├── prompts.py         # AI prompt templates
│   └── memory.py          # Conversation memory management
├── db/                    # Database and migrations
│   ├── models.py          # SQLAlchemy models
│   ├── migrations/        # Database migrations
│   └── canonical_deck.json # Complete 78-card database
├── tests/                 # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── fixtures/          # Test data
├── packaging/             # macOS .app packaging
│   ├── build_app.py       # Py2app build script
│   └── codesign.sh        # Code signing script
└── docs/                  # Documentation
    ├── architecture.md    # Technical architecture
    ├── ollama_setup.md    # Ollama installation guide
    ├── prompts.md         # AI prompt documentation
    └── research.md        # Competitive analysis report
```

## Development Roadmap

### MVP (Current Focus)
- [x] Research and competitive analysis
- [ ] Canonical card database (JSON + SQLite)
- [ ] Minimal PyObjC UI with 3-card draw flow
- [ ] Influence engine core API + unit tests
- [ ] Ollama adapter skeleton with JSON schema validation

### v1 (Full Feature Set)
- [ ] Complete UI (all tabs and functionality)
- [ ] Chat integration with memory management
- [ ] Deck manager and card editor
- [ ] Packaging scripts for macOS .app
- [ ] Comprehensive test suite

### v2 (Polish and Extensions)
- [ ] Alternative cross-platform UI option
- [ ] Advanced learning mode with spaced repetition
- [ ] Optional cloud sync (opt-in)
- [ ] Accessibility improvements and polish

## Architecture Overview

The application follows a clean architecture pattern with clear separation of concerns:

- **UI Layer** (`app/`): PyObjC-based native macOS interface
- **Core Layer** (`core/`): Business logic for cards, spreads, and influence engine
- **AI Layer** (`ai/`): Ollama integration and conversation management
- **Data Layer** (`db/`): SQLite persistence with SQLAlchemy ORM

## Key Design Decisions

1. **Privacy-First**: All data processing happens locally; no remote authentication or telemetry
2. **Offline-First**: Application works fully without internet connectivity
3. **Native macOS**: PyObjC provides the most mac-native user experience
4. **Modular Architecture**: Clean separation enables testing and future platform support
5. **Zed-Inspired UI**: Minimalist, terminal-like aesthetic for clarity and focus

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the minimalist aesthetic of Zed editor
- Built with privacy-first principles using Ollama for local AI
- Card meanings based on traditional tarot interpretations