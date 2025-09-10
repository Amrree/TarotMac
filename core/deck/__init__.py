"""
Deck Module for the Tarot Application.

This module provides the core functionality for managing tarot decks,
including card representation, deck operations, and data loading.

Classes:
    Card: Represents a single tarot card with metadata and orientation
    Deck: Manages a collection of tarot cards with shuffle/draw operations
    DeckLoader: Loads card data from various sources

Enums:
    ArcanaType: Major or Minor Arcana classification
    Suit: Minor Arcana suit types (Wands, Cups, Swords, Pentacles)
    Orientation: Card orientation (Upright or Reversed)

Example:
    from core.deck import DeckLoader, Orientation
    
    # Load the canonical deck
    deck = DeckLoader.load_canonical_deck()
    
    # Shuffle and draw cards
    deck.shuffle()
    card = deck.draw_card(Orientation.UPRIGHT)
    
    # Check deck state
    print(f"Remaining cards: {deck.count}")
    print(f"Card drawn: {card}")
"""

from .card import Card, CardMetadata, ArcanaType, Suit, Orientation
from .deck import Deck, DrawResult
from .loader import DeckLoader

__all__ = [
    'Card',
    'CardMetadata', 
    'ArcanaType',
    'Suit',
    'Orientation',
    'Deck',
    'DrawResult',
    'DeckLoader'
]

__version__ = '1.0.0'
__author__ = 'Tarot App Team'
__description__ = 'Core deck management for tarot applications'