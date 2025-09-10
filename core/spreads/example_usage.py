"""
Example Usage of the Spreads Module

This file demonstrates how to use the spreads module for creating and managing
tarot spread readings. It shows integration with the deck module and influence engine.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from core.spreads.manager import SpreadManager
from core.spreads.layout import SpreadType
from core.deck.loader import DeckLoader
from core.influence.advanced_engine import TarotInfluenceEngine


def example_basic_reading():
    """Example of creating a basic single card reading."""
    print("=== Basic Single Card Reading ===")
    
    # Load deck and create manager
    deck = DeckLoader.load_canonical_deck(seed=42)
    manager = SpreadManager(deck=deck)
    
    # Create reading
    reading = manager.create_reading(
        SpreadType.SINGLE_CARD,
        question="What should I focus on today?",
        shuffle_seed=123
    )
    
    # Draw cards
    manager.draw_cards_for_reading(reading)
    
    # Get interpretation
    interpretation = manager.interpret_reading(reading)
    
    # Display results
    print(f"Question: {reading.question}")
    print(f"Layout: {reading.layout.name}")
    print(f"Cards drawn: {len(reading.positioned_cards)}")
    
    for pc in reading.positioned_cards:
        print(f"\n{pc.position.name}:")
        print(f"  Card: {pc.card.get_display_name()}")
        print(f"  Meaning: {pc.card.get_meaning()}")
    
    print(f"\nOverall Summary: {interpretation['overall_summary']}")
    print(f"Advice: {interpretation['advice']}")
    print(f"Confidence: {interpretation['confidence']}")


def example_three_card_reading():
    """Example of creating a three-card past-present-future reading."""
    print("\n=== Three Card Reading ===")
    
    # Load deck and create manager
    deck = DeckLoader.load_canonical_deck(seed=456)
    manager = SpreadManager(deck=deck)
    
    # Create reading
    reading = manager.create_reading(
        SpreadType.THREE_CARD,
        question="How will my career develop over time?",
        shuffle_seed=789
    )
    
    # Draw cards
    manager.draw_cards_for_reading(reading)
    
    # Get interpretation
    interpretation = manager.interpret_reading(reading)
    
    # Display results
    print(f"Question: {reading.question}")
    print(f"Layout: {reading.layout.name}")
    
    for pc in reading.positioned_cards:
        print(f"\n{pc.position.name} ({pc.position.meaning.value}):")
        print(f"  Card: {pc.card.get_display_name()}")
        print(f"  Position meaning: {pc.position.description}")
        print(f"  Card meaning: {pc.card.get_meaning()}")
    
    # Get statistics
    stats = manager.get_reading_statistics(reading)
    print(f"\nReading Statistics:")
    print(f"  Total cards: {stats['total_cards']}")
    print(f"  Major Arcana: {stats['major_arcana']}")
    print(f"  Minor Arcana: {stats['minor_arcana']}")
    print(f"  Upright: {stats['upright_cards']}")
    print(f"  Reversed: {stats['reversed_cards']}")


def example_celtic_cross_reading():
    """Example of creating a Celtic Cross reading."""
    print("\n=== Celtic Cross Reading ===")
    
    # Load deck and create manager
    deck = DeckLoader.load_canonical_deck(seed=999)
    manager = SpreadManager(deck=deck)
    
    # Create reading
    reading = manager.create_reading(
        SpreadType.CELTIC_CROSS,
        question="What do I need to know about my current life situation?",
        shuffle_seed=111
    )
    
    # Draw cards
    manager.draw_cards_for_reading(reading)
    
    # Get interpretation
    interpretation = manager.interpret_reading(reading)
    
    # Display results
    print(f"Question: {reading.question}")
    print(f"Layout: {reading.layout.name}")
    print(f"Description: {reading.layout.description}")
    
    # Group cards by their position in the spread
    for pc in reading.positioned_cards:
        print(f"\n{pc.position.name}:")
        print(f"  Card: {pc.card.get_display_name()}")
        print(f"  Meaning: {pc.position.description}")
        print(f"  Card interpretation: {pc.card.get_meaning()}")
    
    # Get detailed statistics
    stats = manager.get_reading_statistics(reading)
    print(f"\nDetailed Statistics:")
    print(f"  Total cards: {stats['total_cards']}")
    print(f"  Major Arcana: {stats['major_arcana']}")
    print(f"  Minor Arcana: {stats['minor_arcana']}")
    print(f"  Upright cards: {stats['upright_cards']}")
    print(f"  Reversed cards: {stats['reversed_cards']}")
    
    if stats['suit_distribution']:
        print(f"  Suit distribution: {stats['suit_distribution']}")
    
    if stats['element_distribution']:
        print(f"  Element distribution: {stats['element_distribution']}")


def example_relationship_reading():
    """Example of creating a relationship reading."""
    print("\n=== Relationship Reading ===")
    
    # Load deck and create manager
    deck = DeckLoader.load_canonical_deck(seed=222)
    manager = SpreadManager(deck=deck)
    
    # Create reading
    reading = manager.create_reading(
        SpreadType.RELATIONSHIP,
        question="What is the current state of my relationship?",
        shuffle_seed=333
    )
    
    # Draw cards
    manager.draw_cards_for_reading(reading)
    
    # Get interpretation
    interpretation = manager.interpret_reading(reading)
    
    # Display results
    print(f"Question: {reading.question}")
    print(f"Layout: {reading.layout.name}")
    
    for pc in reading.positioned_cards:
        print(f"\n{pc.position.name}:")
        print(f"  Card: {pc.card.get_display_name()}")
        print(f"  Focus: {pc.position.description}")
        print(f"  Meaning: {pc.card.get_meaning()}")
    
    print(f"\nOverall Summary: {interpretation['overall_summary']}")
    print(f"Advice: {interpretation['advice']}")


def example_reading_export():
    """Example of exporting readings in different formats."""
    print("\n=== Reading Export Examples ===")
    
    # Create a simple reading
    deck = DeckLoader.load_canonical_deck(seed=444)
    manager = SpreadManager(deck=deck)
    
    reading = manager.create_reading(
        SpreadType.THREE_CARD,
        question="What should I know about my current situation?",
        shuffle_seed=555
    )
    
    manager.draw_cards_for_reading(reading)
    
    # Export in different formats
    print("JSON Export:")
    json_export = manager.export_reading(reading, "json")
    print(json_export[:200] + "..." if len(json_export) > 200 else json_export)
    
    print("\nText Export:")
    text_export = manager.export_reading(reading, "text")
    print(text_export)
    
    print("\nSummary Export:")
    summary_export = manager.export_reading(reading, "summary")
    print(summary_export)


def example_reading_validation():
    """Example of reading validation and error handling."""
    print("\n=== Reading Validation Examples ===")
    
    deck = DeckLoader.load_canonical_deck(seed=666)
    manager = SpreadManager(deck=deck)
    
    # Create incomplete reading
    reading = manager.create_reading(SpreadType.THREE_CARD)
    
    # Validate incomplete reading
    is_valid, issues = manager.validate_reading(reading)
    print(f"Incomplete reading valid: {is_valid}")
    print(f"Issues: {issues}")
    
    # Complete the reading
    manager.draw_cards_for_reading(reading)
    
    # Validate complete reading
    is_valid, issues = manager.validate_reading(reading)
    print(f"\nComplete reading valid: {is_valid}")
    print(f"Issues: {issues}")
    
    # Test reading statistics
    stats = manager.get_reading_statistics(reading)
    print(f"\nReading Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


def example_available_spreads():
    """Example of exploring available spreads."""
    print("\n=== Available Spreads ===")
    
    manager = SpreadManager()
    
    # Get available spreads
    available_spreads = manager.get_available_spreads()
    print(f"Available spread types: {len(available_spreads)}")
    
    for spread_type in available_spreads:
        layout = manager.create_spread_layout(spread_type)
        print(f"\n{layout.name} ({spread_type.value}):")
        print(f"  Description: {layout.description}")
        print(f"  Positions: {len(layout.positions)}")
        print(f"  Min cards: {layout.min_cards}")
        print(f"  Max cards: {layout.max_cards}")
        
        # Show position meanings
        meanings = [pos.meaning.value for pos in layout.positions]
        print(f"  Position meanings: {meanings}")


def example_integration_with_influence_engine():
    """Example of using spreads with the influence engine."""
    print("\n=== Integration with Influence Engine ===")
    
    # Load deck and create influence engine
    deck = DeckLoader.load_canonical_deck(seed=777)
    influence_engine = TarotInfluenceEngine()
    manager = SpreadManager(deck=deck, influence_engine=influence_engine)
    
    # Create reading
    reading = manager.create_reading(
        SpreadType.THREE_CARD,
        question="How do the cards influence each other?",
        shuffle_seed=888
    )
    
    # Draw cards
    manager.draw_cards_for_reading(reading)
    
    # Get interpretation with influence engine
    interpretation = manager.interpret_reading(reading)
    
    print(f"Question: {reading.question}")
    print(f"Layout: {reading.layout.name}")
    
    # Display detailed interpretation with influence factors
    for pc in reading.positioned_cards:
        position_id = pc.position.position_id
        if position_id in interpretation["interpretations"]:
            interp_data = interpretation["interpretations"][position_id]
            print(f"\n{pc.position.name}:")
            print(f"  Card: {interp_data['card_name']} ({interp_data['orientation']})")
            print(f"  Influenced meaning: {interp_data['influenced_text']}")
            print(f"  Confidence: {interp_data['confidence']}")
            
            # Show influence factors
            if interp_data['influence_factors']:
                print(f"  Influence factors:")
                for factor in interp_data['influence_factors']:
                    print(f"    - {factor['source']}: {factor['explanation']}")
    
    print(f"\nOverall Summary: {interpretation['overall_summary']}")
    print(f"Advice: {interpretation['advice']}")


if __name__ == "__main__":
    """Run all examples."""
    print("TarotMac Spreads Module - Example Usage")
    print("=" * 50)
    
    try:
        example_basic_reading()
        example_three_card_reading()
        example_celtic_cross_reading()
        example_relationship_reading()
        example_reading_export()
        example_reading_validation()
        example_available_spreads()
        example_integration_with_influence_engine()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()