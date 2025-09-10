# QA Checklist - macOS Tarot App

## Pre-Release Testing Checklist

### ✅ Core Functionality

#### Card Database
- [ ] All 78 cards loaded correctly
- [ ] Major Arcana (22 cards) present
- [ ] Minor Arcana (56 cards) present
- [ ] All suits (Wands, Cups, Swords, Pentacles) complete
- [ ] Card metadata (keywords, polarity, intensity) valid
- [ ] Upright and reversed meanings present

#### Spread System
- [ ] Single card spread works
- [ ] Three-card spread (Past/Present/Future) works
- [ ] Celtic Cross spread works
- [ ] Custom spread creation works
- [ ] Card positioning and orientation correct
- [ ] Spread layouts display properly

#### Influence Engine
- [ ] Adjacency calculations correct
- [ ] Major Arcana multiplier applied
- [ ] Same suit amplification works
- [ ] Reversal effects applied
- [ ] Numeric progression detection works
- [ ] Polarity and intensity within valid ranges
- [ ] Influence factors properly explained

#### AI Integration
- [ ] Ollama connection established
- [ ] Model selection works
- [ ] Streaming responses functional
- [ ] JSON schema validation works
- [ ] Fallback responses when AI unavailable
- [ ] Context seeding for conversations
- [ ] Memory management functional

#### Reading Management
- [ ] Readings save correctly
- [ ] Reading metadata (title, tags, notes) preserved
- [ ] Card positions and orientations saved
- [ ] Reading search and filtering works
- [ ] Reading export/import functional
- [ ] Reading history accessible

#### Chat System
- [ ] Chat with individual cards works
- [ ] Chat with complete readings works
- [ ] Standalone conversations work
- [ ] Memory toggle functional
- [ ] Conversation history preserved
- [ ] Context linking works

### ✅ User Interface

#### Visual Design
- [ ] Zed-inspired dark theme applied
- [ ] Monospaced fonts used throughout
- [ ] Cyan-blue accents visible
- [ ] Generous spacing and clean layouts
- [ ] No decorative elements (as specified)
- [ ] High contrast for accessibility

#### Navigation
- [ ] All tabs accessible (Home, Readings, Chat, History, Settings)
- [ ] Tab switching smooth
- [ ] Active tab highlighted correctly
- [ ] Back navigation works where applicable

#### Responsiveness
- [ ] UI scales properly on different screen sizes
- [ ] Minimum window size enforced
- [ ] Resizing works smoothly
- [ ] No layout breaking on resize

### ✅ Performance

#### Startup
- [ ] App launches within 3 seconds
- [ ] Database initialization fast
- [ ] UI loads without delay
- [ ] No memory leaks on startup

#### Runtime
- [ ] Card drawing responsive (< 1 second)
- [ ] Influence computation fast (< 2 seconds)
- [ ] AI responses reasonable (< 10 seconds)
- [ ] UI remains responsive during AI processing
- [ ] Memory usage stable

#### Database
- [ ] SQLite queries optimized
- [ ] Large reading collections perform well
- [ ] Search operations fast
- [ ] No database corruption

### ✅ Privacy & Security

#### Local Operation
- [ ] App works fully offline
- [ ] No network requests without user consent
- [ ] All data stored locally
- [ ] No telemetry or analytics

#### Data Protection
- [ ] Sensitive fields encrypted at rest
- [ ] User passphrase integration works
- [ ] macOS Keychain integration functional
- [ ] Encrypted export/import works

#### AI Privacy
- [ ] All AI processing local via Ollama
- [ ] No data sent to external servers
- [ ] Memory controls functional
- [ ] User controls what AI remembers

### ✅ Compatibility

#### macOS Versions
- [ ] macOS 12.0 (Monterey) - minimum supported
- [ ] macOS 13.0 (Ventura) - recommended
- [ ] macOS 14.0 (Sonoma) - latest
- [ ] macOS 15.0 (Sequoia) - future compatibility

#### Hardware
- [ ] Intel Macs supported
- [ ] Apple Silicon (M1/M2/M3) optimized
- [ ] Various RAM configurations (8GB+)
- [ ] Different storage types

#### Ollama Integration
- [ ] Ollama 0.1.0+ supported
- [ ] Multiple model types work
- [ ] Model switching functional
- [ ] Graceful degradation when Ollama unavailable

### ✅ Accessibility

#### VoiceOver
- [ ] All UI elements have labels
- [ ] Navigation order logical
- [ ] Dynamic content announced
- [ ] Custom controls accessible

#### Visual Accessibility
- [ ] High contrast mode supported
- [ ] Font size adjustable
- [ ] Color not only way to convey information
- [ ] Sufficient color contrast ratios

#### Keyboard Navigation
- [ ] All functions accessible via keyboard
- [ ] Tab order logical
- [ ] Keyboard shortcuts work
- [ ] Focus indicators visible

### ✅ Error Handling

#### Graceful Degradation
- [ ] Ollama unavailable - fallback to static interpretations
- [ ] Database errors - user-friendly messages
- [ ] Network issues - clear error messages
- [ ] File system errors - proper handling

#### User Feedback
- [ ] Loading indicators during AI processing
- [ ] Progress bars for long operations
- [ ] Clear error messages
- [ ] Recovery suggestions provided

#### Logging
- [ ] Comprehensive error logging
- [ ] No sensitive data in logs
- [ ] Log levels appropriate
- [ ] Log rotation implemented

### ✅ Packaging & Distribution

#### App Bundle
- [ ] .app bundle created successfully
- [ ] All dependencies included
- [ ] Resources properly bundled
- [ ] App launches from bundle

#### Code Signing
- [ ] Developer ID certificate applied
- [ ] App notarized (if distributing)
- [ ] Gatekeeper accepts app
- [ ] Signature verification passes

#### Installation
- [ ] App installs without issues
- [ ] First launch experience smooth
- [ ] Privacy documentation shown
- [ ] Ollama setup guidance provided

### ✅ Documentation

#### User Documentation
- [ ] README comprehensive
- [ ] Ollama setup guide complete
- [ ] Architecture documentation present
- [ ] Research report included

#### Developer Documentation
- [ ] Code comments adequate
- [ ] API documentation present
- [ ] Testing instructions clear
- [ ] Build instructions complete

### ✅ Testing

#### Unit Tests
- [ ] Influence engine tests pass
- [ ] Database model tests pass
- [ ] AI adapter tests pass
- [ ] Utility function tests pass

#### Integration Tests
- [ ] Complete reading flow test passes
- [ ] Chat integration test passes
- [ ] Export/import test passes
- [ ] Error handling tests pass

#### Manual Testing
- [ ] All user workflows tested
- [ ] Edge cases explored
- [ ] Performance benchmarks met
- [ ] Accessibility verified

## Release Criteria

### Must Pass (Blocking)
- [ ] All core functionality works
- [ ] App launches and runs offline
- [ ] Influence engine produces valid results
- [ ] AI integration functional
- [ ] Privacy requirements met
- [ ] No critical bugs

### Should Pass (Important)
- [ ] Performance benchmarks met
- [ ] UI/UX polished
- [ ] Accessibility standards met
- [ ] Documentation complete
- [ ] Code signing successful

### Nice to Have (Optional)
- [ ] Advanced features working
- [ ] Performance optimized
- [ ] UI animations smooth
- [ ] Additional model support

## Post-Release Monitoring

### User Feedback
- [ ] Feedback collection system in place
- [ ] Bug report process defined
- [ ] Feature request tracking
- [ ] User satisfaction metrics

### Performance Monitoring
- [ ] App launch time tracking
- [ ] Memory usage monitoring
- [ ] AI response time tracking
- [ ] Error rate monitoring

### Security Monitoring
- [ ] Privacy compliance verification
- [ ] Security vulnerability scanning
- [ ] Data protection audit
- [ ] Access control verification

## Sign-off

### Development Team
- [ ] Lead Developer: ________________
- [ ] AI Integration Lead: ________________
- [ ] UI/UX Designer: ________________
- [ ] QA Lead: ________________

### Release Manager
- [ ] Release Manager: ________________
- [ ] Date: ________________
- [ ] Version: ________________

### Final Approval
- [ ] Technical Lead: ________________
- [ ] Product Manager: ________________
- [ ] Security Review: ________________