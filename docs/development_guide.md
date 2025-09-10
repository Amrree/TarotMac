# Development Guide - macOS Tarot App

## Getting Started

### Prerequisites

- **macOS 12.0+** (Monterey or later)
- **Python 3.10+**
- **Xcode Command Line Tools**
- **Ollama** (for AI functionality)

### Initial Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd tarot-app
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Ollama**:
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ollama pull llama3.2:3b
   ```

5. **Run the application**:
   ```bash
   python -m app.main
   ```

## Project Structure

```
tarot-app/
├── app/                    # PyObjC UI layer
│   ├── main.py            # Application entry point
│   ├── views/             # View controllers
│   └── assets/            # Images, icons, fonts
├── core/                  # Business logic
│   ├── cards/             # Card management
│   ├── spreads/           # Spread definitions
│   ├── influence/         # Influence engine
│   └── journal/           # Readings journal
├── ai/                    # AI integration
│   ├── ollama_client.py   # Ollama client
│   ├── prompts.py         # AI prompts
│   └── memory.py          # Memory management
├── db/                    # Data persistence
│   ├── models.py          # SQLAlchemy models
│   ├── canonical_deck.json # Complete deck data
│   └── migrations/        # Database migrations
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   └── integration/        # Integration tests
├── packaging/             # Build scripts
│   ├── build_app.py       # Py2app script
│   └── codesign.sh        # Code signing
└── docs/                  # Documentation
    ├── architecture.md    # Technical architecture
    ├── ollama_setup.md    # Ollama installation
    └── qa_checklist.md    # Quality assurance
```

## Development Workflow

### 1. Feature Development

1. **Create feature branch**:
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Implement feature**:
   - Write code following the architecture patterns
   - Add unit tests for new functionality
   - Update documentation as needed

3. **Test locally**:
   ```bash
   pytest tests/unit/
   pytest tests/integration/
   python -m app.main  # Manual testing
   ```

4. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

### 2. Testing Strategy

#### Unit Tests
- Test individual components in isolation
- Focus on business logic and algorithms
- Mock external dependencies
- Aim for >90% code coverage

#### Integration Tests
- Test complete workflows
- Verify database operations
- Test AI integration
- Validate data flow

#### Manual Testing
- Test all user workflows
- Verify UI/UX behavior
- Test on different macOS versions
- Validate accessibility features

### 3. Code Quality

#### Style Guidelines
- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write descriptive docstrings
- Keep functions focused and small

#### Architecture Principles
- Separation of concerns
- Dependency injection
- Clean interfaces
- Testable design

### 4. Database Management

#### Schema Changes
1. Create migration script in `db/migrations/`
2. Update models in `db/models.py`
3. Test migration on sample data
4. Update tests accordingly

#### Data Seeding
```bash
# Load canonical deck
python -c "from db.seed import load_canonical_deck; load_canonical_deck()"
```

### 5. AI Integration

#### Model Management
```bash
# List available models
ollama list

# Pull new model
ollama pull llama3.2:8b

# Test model
ollama run llama3.2:3b "Test prompt"
```

#### Prompt Development
- Test prompts with different models
- Validate JSON schema compliance
- Optimize for response quality
- Document prompt strategies

## Building and Packaging

### Development Build

```bash
# Run in development mode
python -m app.main
```

### Production Build

```bash
# Create .app bundle
python packaging/build_app.py py2app

# Code sign (requires developer certificate)
chmod +x packaging/codesign.sh
./packaging/codesign.sh
```

### Distribution

1. **Test the .app bundle**:
   ```bash
   open dist/Tarot.app
   ```

2. **Verify code signing**:
   ```bash
   codesign --verify --verbose dist/Tarot.app
   spctl --assess --verbose dist/Tarot.app
   ```

3. **Create installer** (optional):
   ```bash
   # Use tools like Packages or create a DMG
   ```

## Debugging

### Common Issues

#### Ollama Connection Problems
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

#### Database Issues
```bash
# Reset database
rm tarot.db
python -c "from db.init import create_database; create_database()"
```

#### UI Issues
- Check PyObjC imports
- Verify NSView hierarchy
- Check Auto Layout constraints
- Test on different screen sizes

### Logging

```python
import logging
logger = logging.getLogger(__name__)
logger.info("Debug message")
```

### Performance Profiling

```python
import cProfile
cProfile.run('your_function()')
```

## Contributing

### Pull Request Process

1. **Fork the repository**
2. **Create feature branch**
3. **Implement changes**
4. **Add tests**
5. **Update documentation**
6. **Submit pull request**

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Performance impact considered
- [ ] Security implications reviewed

### Issue Reporting

When reporting issues, include:
- macOS version
- Python version
- Ollama version and model
- Steps to reproduce
- Expected vs actual behavior
- Log files (if applicable)

## Architecture Decisions

### Why PyObjC?
- Most native macOS experience
- Direct access to AppKit
- Better performance than alternatives
- Seamless integration with macOS features

### Why SQLite?
- No external dependencies
- Excellent performance
- ACID compliance
- Cross-platform compatibility
- Built-in encryption support

### Why Ollama?
- Local AI processing
- Privacy-first approach
- Multiple model support
- Easy integration
- Active development

### Why Influence Engine?
- Deterministic results
- Explainable AI
- Customizable rules
- No dependency on external APIs
- Educational value

## Performance Optimization

### Database Optimization
- Use proper indexes
- Batch operations
- Connection pooling
- Query optimization

### UI Optimization
- Lazy loading
- Efficient redraws
- Memory management
- Responsive design

### AI Optimization
- Model selection
- Prompt optimization
- Caching strategies
- Streaming responses

## Security Considerations

### Data Protection
- Encrypt sensitive fields
- Use macOS Keychain
- Implement access controls
- Regular security audits

### Privacy
- Local processing only
- No telemetry
- User-controlled data
- Clear privacy policy

### Code Security
- Regular dependency updates
- Secure coding practices
- Input validation
- Error handling

## Future Enhancements

### Planned Features
- Advanced learning modes
- Custom deck creation
- Cloud sync (opt-in)
- Plugin system
- Multi-language support

### Technical Improvements
- Performance optimization
- Accessibility enhancements
- Cross-platform support
- Advanced AI features
- Better error handling

## Resources

### Documentation
- [PyObjC Documentation](https://pyobjc.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Ollama Documentation](https://ollama.ai/docs)
- [macOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)

### Tools
- [Xcode](https://developer.apple.com/xcode/)
- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Ollama](https://ollama.ai/)
- [SQLite Browser](https://sqlitebrowser.org/)

### Community
- [PyObjC Mailing List](https://mail.python.org/mailman3/lists/pyobjc-dev.python.org/)
- [Ollama Discord](https://discord.gg/ollama)
- [macOS Developer Forums](https://developer.apple.com/forums/)

## Support

For development support:
- Check the documentation
- Review existing issues
- Ask questions in discussions
- Contribute improvements

Remember: This is a privacy-first, offline-capable application. All design decisions should prioritize user privacy and local functionality.