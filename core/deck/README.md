# Deck Module

The Deck Module provides the core functionality for managing tarot decks in the tarot application. It includes classes for representing individual cards, managing complete decks, and loading card data from various sources.

## Overview

The Deck Module consists of three main components:

- **Card**: Represents a single tarot card with metadata and orientation
- **Deck**: Manages a collection of tarot cards with shuffle/draw operations
- **DeckLoader**: Loads card data from JSON files and creates Deck instances

## Features

### Card Management
- Full 78-card tarot deck support (22 Major Arcana + 56 Minor Arcana)
- Upright and reversed orientation handling
- Rich metadata including keywords, themes, and elemental associations
- Flexible card identification and display

### Deck Operations
- Shuffling with configurable random seeds
- Drawing single or multiple cards
- Peeking at cards without removing them
- Filtering cards by suit, arcana type, or other criteria
- Deck statistics and state management

### Data Loading
- JSON file support for card data
- Canonical deck loading
- Validation of card data structure
- Flexible JSON format support

## Usage Examples

### Basic Card Creation

```python
from core.deck import Card, CardMetadata, ArcanaType, Suit, Orientation

# Create a Major Arcana card
metadata = CardMetadata(
    name="The Fool",
    arcana=ArcanaType.MAJOR,
    element="air",
    keywords=["new beginnings", "innocence"],
    upright_text="The Fool represents new beginnings and innocence.",
    reversed_text="Reversed, The Fool warns of recklessness.",
    themes={"new_beginnings": 0.9, "innocence": 0.8},
    polarity_baseline=0.5,
    intensity_baseline=0.7
)

card = Card(metadata, Orientation.UPRIGHT)
print(card.get_display_name())  # "The Fool"
print(card.get_meaning())       # Upright meaning text
```

### Deck Operations

```python
from core.deck import DeckLoader, Orientation

# Load the canonical deck
deck = DeckLoader.load_canonical_deck(seed=42)

# Shuffle and draw cards
deck.shuffle()
card = deck.draw_card(Orientation.UPRIGHT)

# Draw multiple cards
result = deck.draw_cards(3, Orientation.REVERSED)
print(f"Drew {result.drawn_count} cards, {result.remaining_count} remaining")

# Check deck state
print(f"Deck has {deck.count} cards remaining")
print(f"Complete deck: {deck.is_complete}")
```

### Card Filtering

```python
# Filter cards by various criteria
major_cards = deck.get_major_arcana()
minor_cards = deck.get_minor_arcana()
wands_cards = deck.get_cards_by_suit(Suit.WANDS)
court_cards = deck.get_court_cards()
numbered_cards = deck.get_numbered_cards()

# Get deck statistics
stats = deck.get_card_statistics()
print(f"Major Arcana: {stats['major_arcana']}")
print(f"Minor Arcana: {stats['minor_arcana']}")
print(f"Court Cards: {stats['court_cards']}")
```

### Data Loading

```python
from core.deck import DeckLoader

# Load from JSON file
deck = DeckLoader.create_deck_from_json("my_deck.json", seed=42)

# Load canonical deck
deck = DeckLoader.load_canonical_deck()

# Get deck information
info = DeckLoader.get_deck_info("my_deck.json")
print(f"Deck: {info['deck_name']}")
print(f"Total cards: {info['total_cards']}")
print(f"Complete: {info['is_complete']}")
```

## Integration with Other Modules

### Spreads Module
The Deck Module provides the foundation for the Spreads Module:

```python
# Example of how spreads module would use deck
from core.deck import DeckLoader, Orientation

def draw_spread(deck, spread_type):
    """Draw cards for a specific spread type."""
    deck.shuffle()
    
    if spread_type == "three_card":
        cards = deck.draw_cards(3, Orientation.UPRIGHT)
        return {
            "past": cards.cards[0],
            "present": cards.cards[1], 
            "future": cards.cards[2]
        }
    elif spread_type == "celtic_cross":
        cards = deck.draw_cards(10, Orientation.UPRIGHT)
        return {
            "center": cards.cards[0],
            "cross": cards.cards[1],
            "past": cards.cards[2],
            # ... etc
        }
```

### Influence Engine Integration
The Deck Module provides card metadata for the Influence Engine:

```python
# Example of how influence engine would use deck
def get_card_for_influence(card):
    """Extract card data for influence calculations."""
    return {
        "card_id": card.id,
        "name": card.name,
        "arcana": card.arcana.value,
        "suit": card.suit.value if card.suit else None,
        "element": card.element,
        "orientation": card.orientation.value,
        "polarity_baseline": card.polarity_baseline,
        "intensity_baseline": card.intensity_baseline,
        "themes": card.themes,
        "keywords": card.keywords
    }
```

## Data Format

### Card Data Structure
Cards are represented as dictionaries with the following structure:

```json
{
  "id": "fool",
  "name": "The Fool",
  "arcana": "major",
  "suit": null,
  "number": null,
  "rank": null,
  "element": "air",
  "keywords": ["new beginnings", "innocence"],
  "upright_text": "The Fool represents new beginnings and innocence.",
  "reversed_text": "Reversed, The Fool warns of recklessness.",
  "themes": {"new_beginnings": 0.9, "innocence": 0.8},
  "polarity_baseline": 0.5,
  "intensity_baseline": 0.7
}
```

### Deck File Structure
Deck files can have different structures:

```json
{
  "deck_info": {
    "name": "Rider-Waite-Smith Tarot",
    "version": "1.0",
    "description": "Complete 78-card tarot deck"
  },
  "cards": [
    // ... card data
  ]
}
```

Or:

```json
{
  "deck_name": "My Custom Deck",
  "description": "A custom tarot deck",
  "total_cards": 78,
  "cards": [
    // ... card data
  ]
}
```

## Testing

The module includes comprehensive unit tests covering:

- Card creation and metadata handling
- Orientation management (upright/reversed)
- Deck operations (shuffle, draw, peek)
- Card filtering and statistics
- Data loading and validation
- Error handling and edge cases

Run tests with:
```bash
python3 test_deck.py
```

## Error Handling

The module includes robust error handling for:

- Invalid card data structure
- Missing required fields
- File not found errors
- Invalid JSON format
- Empty or corrupted deck files

## Performance Considerations

- Deck operations are optimized for typical tarot reading scenarios
- Shuffling uses Fisher-Yates algorithm for uniform distribution
- Card filtering uses efficient list comprehensions
- Memory usage scales linearly with deck size

## Future Enhancements

Potential future enhancements include:

- Support for custom deck layouts
- Card image and artwork management
- Deck comparison and analysis tools
- Export functionality for different formats
- Advanced filtering and search capabilities