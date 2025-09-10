#!/usr/bin/env python3
"""
Example usage of the Deck Module.

This script demonstrates how other modules (like spreads, influence engine, etc.)
would interact with the deck module to perform common tarot operations.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.deck import (
    Card, CardMetadata, ArcanaType, Suit, Orientation,
    Deck, DrawResult, DeckLoader
)


def example_spread_usage():
    """Example of how the Spreads module would use the deck."""
    print("=== Spreads Module Example ===")
    
    # Load deck
    deck = DeckLoader.load_canonical_deck(seed=42)
    print(f"Loaded deck with {deck.count} cards")
    
    # Three-card spread
    print("\nDrawing three-card spread...")
    deck.shuffle()
    result = deck.draw_cards(3, Orientation.UPRIGHT)
    
    spread = {
        "past": result.cards[0],
        "present": result.cards[1],
        "future": result.cards[2]
    }
    
    for position, card in spread.items():
        print(f"{position.title()}: {card.get_display_name()}")
        print(f"  Meaning: {card.get_meaning()[:100]}...")
    
    print(f"\nRemaining cards: {result.remaining_count}")


def example_influence_engine_usage():
    """Example of how the Influence Engine would use the deck."""
    print("\n=== Influence Engine Example ===")
    
    # Load deck
    deck = DeckLoader.load_canonical_deck(seed=123)
    deck.shuffle()
    
    # Draw cards for influence analysis
    result = deck.draw_cards(3, Orientation.UPRIGHT)
    cards = result.cards
    
    print(f"Drew {len(cards)} cards for influence analysis:")
    
    # Extract card data for influence engine
    card_data = []
    for i, card in enumerate(cards):
        card_info = {
            "position_id": f"position_{i}",
            "card_id": card.id,
            "name": card.name,
            "arcana": card.arcana.value,
            "suit": card.suit.value if card.suit else None,
            "element": card.element,
            "orientation": card.orientation.value,
            "polarity_baseline": card.polarity_baseline,
            "intensity_baseline": card.intensity_baseline,
            "themes": card.themes,
            "keywords": card.keywords,
            "x_coordinate": float(i),
            "y_coordinate": 0.0
        }
        card_data.append(card_info)
        
        print(f"  {card.get_display_name()}: {card.element} element, polarity={card.polarity_baseline:.2f}")
    
    # This data would be passed to the influence engine
    print(f"\nCard data ready for influence engine:")
    for card_info in card_data:
        print(f"  {card_info['name']}: {card_info['element']} element")


def example_deck_management():
    """Example of deck management operations."""
    print("\n=== Deck Management Example ===")
    
    # Load deck
    deck = DeckLoader.load_canonical_deck(seed=456)
    
    # Show initial state
    stats = deck.get_card_statistics()
    print(f"Initial deck state:")
    print(f"  Total cards: {stats['total_cards']}")
    print(f"  Major Arcana: {stats['major_arcana']}")
    print(f"  Minor Arcana: {stats['minor_arcana']}")
    print(f"  Court Cards: {stats['court_cards']}")
    print(f"  Numbered Cards: {stats['numbered_cards']}")
    
    # Filter cards
    print(f"\nCard filtering examples:")
    major_cards = deck.get_major_arcana()
    print(f"  Major Arcana cards: {len(major_cards)}")
    
    wands_cards = deck.get_cards_by_suit(Suit.WANDS)
    print(f"  Wands cards: {len(wands_cards)}")
    
    court_cards = deck.get_court_cards()
    print(f"  Court cards: {len(court_cards)}")
    
    # Show some examples
    if major_cards:
        print(f"  Example Major Arcana: {major_cards[0].get_display_name()}")
    if wands_cards:
        print(f"  Example Wands card: {wands_cards[0].get_display_name()}")
    if court_cards:
        print(f"  Example Court card: {court_cards[0].get_display_name()}")


def example_card_operations():
    """Example of individual card operations."""
    print("\n=== Card Operations Example ===")
    
    # Create a custom card
    metadata = CardMetadata(
        name="The Fool",
        arcana=ArcanaType.MAJOR,
        element="air",
        keywords=["new beginnings", "innocence", "spontaneity"],
        upright_text="The Fool represents new beginnings and innocence.",
        reversed_text="Reversed, The Fool warns of recklessness.",
        themes={"new_beginnings": 0.9, "innocence": 0.8},
        polarity_baseline=0.5,
        intensity_baseline=0.7
    )
    
    card = Card(metadata, Orientation.UPRIGHT)
    
    print(f"Card: {card.get_display_name()}")
    print(f"  ID: {card.id}")
    print(f"  Arcana: {card.arcana.value}")
    print(f"  Element: {card.element}")
    print(f"  Orientation: {card.orientation.value}")
    print(f"  Keywords: {', '.join(card.keywords)}")
    print(f"  Polarity: {card.polarity_baseline:.2f}")
    print(f"  Intensity: {card.intensity_baseline:.2f}")
    
    # Test orientation changes
    print(f"\nUpright meaning: {card.get_meaning()[:80]}...")
    
    card.flip()
    print(f"After flip - Orientation: {card.orientation.value}")
    print(f"Reversed meaning: {card.get_meaning()[:80]}...")
    
    # Convert to dictionary
    card_dict = card.to_dict()
    print(f"\nCard as dictionary:")
    print(f"  Keys: {list(card_dict.keys())}")
    print(f"  Current meaning: {card_dict['current_meaning'][:60]}...")


def example_data_loading():
    """Example of data loading operations."""
    print("\n=== Data Loading Example ===")
    
    # Get canonical deck info
    canonical_path = DeckLoader.get_canonical_deck_path()
    info = DeckLoader.get_deck_info(canonical_path)
    
    print(f"Canonical deck information:")
    print(f"  File: {os.path.basename(info['file_path'])}")
    print(f"  Name: {info['deck_name']}")
    print(f"  Description: {info['description']}")
    print(f"  Total cards: {info['total_cards']}")
    print(f"  Major Arcana: {info['major_arcana']}")
    print(f"  Minor Arcana: {info['minor_arcana']}")
    print(f"  Complete: {info['is_complete']}")
    
    # Show suit distribution
    print(f"  Suit distribution:")
    for suit, count in info['suit_counts'].items():
        print(f"    {suit.title()}: {count}")


def main():
    """Run all examples."""
    print("🎴 Deck Module Usage Examples")
    print("=" * 50)
    
    try:
        example_card_operations()
        example_deck_management()
        example_data_loading()
        example_spread_usage()
        example_influence_engine_usage()
        
        print("\n" + "=" * 50)
        print("✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Example failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()