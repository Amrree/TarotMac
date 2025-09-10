# Spreads Module

The Spreads Module provides comprehensive functionality for creating, managing, and interpreting tarot card spreads. It integrates seamlessly with the Deck Module for card drawing and the Influence Engine for advanced card interpretation.

## Overview

This module implements a complete spread management system that supports:
- Multiple predefined spread layouts (Single Card, Three Card, Celtic Cross, Relationship, Year Ahead)
- Custom spread creation and management
- Card placement and position management
- Integration with influence engine for enhanced interpretations
- Reading validation and statistics
- Multiple export formats

## Architecture

### Core Components

1. **SpreadLayout**: Defines the structure and positions of a tarot spread
2. **SpreadPosition**: Represents a single position within a spread
3. **SpreadReading**: Manages a complete reading with cards and interpretations
4. **SpreadManager**: Main interface for spread operations and integration

### Key Classes

#### SpreadLayout
Defines the structure of a tarot spread including:
- Spread type and metadata
- Position definitions with meanings and coordinates
- Card count constraints (min/max)
- Validation and utility methods

#### SpreadPosition
Represents a single position in a spread:
- Position ID and human-readable name
- Meaning (past, present, future, etc.)
- Description and coordinates for visual layout
- Optional flag for flexible spreads

#### SpreadReading
Manages a complete tarot reading:
- Card placement in specific positions
- Interpretation management
- Reading validation and statistics
- Serialization and export capabilities

#### SpreadManager
Main interface for spread operations:
- Reading creation and management
- Card drawing integration
- Influence engine integration
- Export and validation utilities

## Supported Spreads

### 1. Single Card Spread
- **Purpose**: Quick insights or daily guidance
- **Positions**: 1 (The Answer)
- **Use case**: Simple questions, daily draws, quick guidance

### 2. Three Card Spread
- **Purpose**: Understanding the flow of events
- **Positions**: 3 (Past, Present, Future)
- **Use case**: General life guidance, decision making, timeline analysis

### 3. Celtic Cross Spread
- **Purpose**: Deep insight into complex situations
- **Positions**: 10 (Current Situation, Challenge, Distant Past, Recent Past, Possible Outcome, Near Future, Your Approach, External Influences, Hopes & Fears, Final Outcome)
- **Use case**: Complex life situations, major decisions, comprehensive analysis

### 4. Relationship Spread
- **Purpose**: Understanding relationship dynamics
- **Positions**: 4 (You, Partner, Relationship, Advice)
- **Use case**: Relationship analysis, partnership guidance, communication insights

### 5. Year Ahead Spread
- **Purpose**: Monthly guidance throughout the year
- **Positions**: 12 (January through December)
- **Use case**: Annual planning, monthly focus, long-term guidance

## API Reference

### Creating a Reading

```python
from core.spreads.manager import SpreadManager
from core.spreads.layout import SpreadType
from core.deck.loader import DeckLoader

# Load deck and create manager
deck = DeckLoader.load_canonical_deck(seed=42)
manager = SpreadManager(deck=deck)

# Create reading
reading = manager.create_reading(
    SpreadType.THREE_CARD,
    question="What does the future hold?",
    shuffle_seed=123
)
```

### Drawing Cards

```python
# Draw cards for the reading
manager.draw_cards_for_reading(reading)

# Check if reading is complete
if reading.is_complete():
    print("Reading is complete!")
```

### Getting Interpretations

```python
# Get interpretation
interpretation = manager.interpret_reading(reading)

# Access individual card interpretations
for pc in reading.positioned_cards:
    position_id = pc.position.position_id
    if position_id in interpretation["interpretations"]:
        card_data = interpretation["interpretations"][position_id]
        print(f"{pc.position.name}: {card_data['influenced_text']}")
```

### Reading Statistics

```python
# Get reading statistics
stats = manager.get_reading_statistics(reading)

print(f"Total cards: {stats['total_cards']}")
print(f"Major Arcana: {stats['major_arcana']}")
print(f"Minor Arcana: {stats['minor_arcana']}")
print(f"Upright: {stats['upright_cards']}")
print(f"Reversed: {stats['reversed_cards']}")
```

### Exporting Readings

```python
# Export in different formats
json_export = manager.export_reading(reading, "json")
text_export = manager.export_reading(reading, "text")
summary_export = manager.export_reading(reading, "summary")
```

## Integration

### With Deck Module

The Spreads Module integrates with the Deck Module for:
- Card drawing with orientation control
- Deck state management
- Shuffling and randomization
- Card filtering and statistics

### With Influence Engine

The Spreads Module integrates with the Influence Engine for:
- Enhanced card interpretations
- Influence factor analysis
- Confidence scoring
- Contextual meaning generation

### Example Integration

```python
from core.spreads.manager import SpreadManager
from core.deck.loader import DeckLoader
from core.influence.advanced_engine import TarotInfluenceEngine

# Create integrated manager
deck = DeckLoader.load_canonical_deck(seed=42)
influence_engine = TarotInfluenceEngine()
manager = SpreadManager(deck=deck, influence_engine=influence_engine)

# Create and interpret reading
reading = manager.create_reading(SpreadType.CELTIC_CROSS)
manager.draw_cards_for_reading(reading)
interpretation = manager.interpret_reading(reading)
```

## Data Format

### Spread Layout JSON Structure

```json
{
  "spread_type": "three_card",
  "name": "Three Card Spread",
  "description": "A classic past-present-future reading",
  "positions": [
    {
      "position_id": "past",
      "name": "Past",
      "meaning": "past",
      "description": "What has led to your current situation",
      "coordinates": [0.2, 0.5],
      "is_optional": false
    }
  ],
  "min_cards": 3,
  "max_cards": 3
}
```

### Reading JSON Structure

```json
{
  "reading_id": "uuid-string",
  "layout": { /* spread layout data */ },
  "positioned_cards": [
    {
      "card": { /* card data */ },
      "position": { /* position data */ },
      "drawn_at": "2024-01-01T12:00:00"
    }
  ],
  "question": "What does the future hold?",
  "created_at": "2024-01-01T12:00:00",
  "interpretations": {
    "past": "Interpretation text for past position"
  },
  "notes": "Additional notes"
}
```

## Usage Examples

### Basic Single Card Reading

```python
# Create simple reading
reading = manager.create_reading(SpreadType.SINGLE_CARD, "What should I focus on?")
manager.draw_cards_for_reading(reading)

# Display results
for pc in reading.positioned_cards:
    print(f"{pc.position.name}: {pc.card.get_display_name()}")
    print(f"Meaning: {pc.card.get_meaning()}")
```

### Complex Celtic Cross Reading

```python
# Create comprehensive reading
reading = manager.create_reading(
    SpreadType.CELTIC_CROSS,
    "What do I need to know about my current situation?"
)

# Draw all cards
manager.draw_cards_for_reading(reading)

# Get detailed interpretation
interpretation = manager.interpret_reading(reading)

# Display comprehensive results
for pc in reading.positioned_cards:
    position_id = pc.position.position_id
    if position_id in interpretation["interpretations"]:
        data = interpretation["interpretations"][position_id]
        print(f"\n{pc.position.name}:")
        print(f"  Card: {data['card_name']} ({data['orientation']})")
        print(f"  Meaning: {data['influenced_text']}")
        print(f"  Confidence: {data['confidence']}")
```

### Reading Validation

```python
# Validate reading
is_valid, issues = manager.validate_reading(reading)

if not is_valid:
    print("Reading has issues:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("Reading is valid!")
```

## Testing

The module includes comprehensive unit tests covering:
- Layout creation and validation
- Reading management
- Card placement and removal
- Integration with deck and influence engine
- Export functionality
- Error handling

Run tests with:
```bash
python -m pytest tests/unit/test_spreads_module.py -v
```

## Error Handling

The module provides robust error handling for:
- Invalid spread types
- Incomplete readings
- Duplicate card placements
- Insufficient deck cards
- Invalid position references
- Export format errors

## Future Enhancements

Planned enhancements include:
- Custom spread creation tools
- Visual layout rendering
- Reading templates and presets
- Advanced statistics and analytics
- Integration with AI chat features
- Reading comparison and analysis tools

## Dependencies

- **Deck Module**: For card drawing and management
- **Influence Engine**: For enhanced interpretations
- **Standard Library**: datetime, uuid, typing, dataclasses
- **External**: None (self-contained)

## Files

- `layout.py`: Spread layout definitions and position management
- `reading.py`: Reading management and card placement
- `manager.py`: Main interface and integration logic
- `__init__.py`: Module initialization and exports
- `example_usage.py`: Comprehensive usage examples
- `README.md`: This documentation