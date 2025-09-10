"""
Tarot Deck representation for the Deck Module.

This module defines the Deck class that manages a collection of tarot cards,
providing functionality for shuffling, drawing, and managing card states.
"""

import random
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
from .card import Card, CardMetadata, ArcanaType, Suit, Orientation


@dataclass
class DrawResult:
    """Result of drawing cards from the deck."""
    cards: List[Card]
    remaining_count: int
    drawn_count: int


class Deck:
    """
    Represents a complete tarot deck with 78 cards.
    
    The Deck class manages a collection of tarot cards and provides methods
    for shuffling, drawing cards, and managing the deck state.
    """
    
    def __init__(self, card_metadata: List[Dict[str, Any]], seed: Optional[int] = None):
        """
        Initialize a deck with card metadata.
        
        Args:
            card_metadata: List of dictionaries containing card information
            seed: Optional random seed for reproducible shuffling
        """
        self._cards: List[Card] = []
        self._original_cards: List[Card] = []
        self._seed = seed
        self._random = random.Random(seed) if seed else random.Random()
        
        # Create cards from metadata
        self._create_cards(card_metadata)
        
        # Store original state for reset
        self._original_cards = [Card(card.metadata, card.orientation) for card in self._cards]
    
    def _create_cards(self, card_metadata: List[Dict[str, Any]]) -> None:
        """
        Create Card objects from metadata.
        
        Args:
            card_metadata: List of dictionaries containing card information
        """
        for card_data in card_metadata:
            # Convert string enums to proper enum values
            arcana = ArcanaType(card_data.get('arcana', 'major'))
            suit = Suit(card_data['suit']) if card_data.get('suit') else None
            
            # Create metadata object
            metadata = CardMetadata(
                name=card_data['name'],
                arcana=arcana,
                suit=suit,
                number=card_data.get('number'),
                rank=card_data.get('rank'),
                element=card_data.get('element'),
                keywords=card_data.get('keywords', []),
                upright_text=card_data.get('upright_text', ''),
                reversed_text=card_data.get('reversed_text', ''),
                themes=card_data.get('themes', {}),
                polarity_baseline=card_data.get('polarity_baseline', 0.0),
                intensity_baseline=card_data.get('intensity_baseline', 0.5)
            )
            
            # Create card with upright orientation by default
            card = Card(metadata, Orientation.UPRIGHT)
            self._cards.append(card)
    
    @property
    def count(self) -> int:
        """Get the current number of cards in the deck."""
        return len(self._cards)
    
    @property
    def total_count(self) -> int:
        """Get the total number of cards in the complete deck."""
        return len(self._original_cards)
    
    @property
    def is_empty(self) -> bool:
        """Check if the deck is empty."""
        return len(self._cards) == 0
    
    @property
    def is_complete(self) -> bool:
        """Check if the deck has all 78 cards."""
        return len(self._cards) == 78
    
    def shuffle(self) -> None:
        """
        Shuffle the deck using the configured random number generator.
        
        This method shuffles the cards in place using the Fisher-Yates algorithm.
        """
        self._random.shuffle(self._cards)
    
    def draw_card(self, orientation: Optional[Orientation] = None) -> Optional[Card]:
        """
        Draw a single card from the top of the deck.
        
        Args:
            orientation: Optional orientation to set for the drawn card.
                        If None, the card keeps its current orientation.
        
        Returns:
            The drawn card, or None if the deck is empty
        """
        if self.is_empty:
            return None
        
        card = self._cards.pop(0)
        
        if orientation is not None:
            card.set_orientation(orientation)
        
        return card
    
    def draw_cards(self, count: int, orientation: Optional[Orientation] = None) -> DrawResult:
        """
        Draw multiple cards from the deck.
        
        Args:
            count: Number of cards to draw
            orientation: Optional orientation to set for all drawn cards.
                        If None, cards keep their current orientation.
        
        Returns:
            DrawResult containing the drawn cards and deck state
        """
        drawn_cards = []
        actual_count = min(count, len(self._cards))
        
        for _ in range(actual_count):
            card = self.draw_card(orientation)
            if card:
                drawn_cards.append(card)
        
        return DrawResult(
            cards=drawn_cards,
            remaining_count=len(self._cards),
            drawn_count=len(drawn_cards)
        )
    
    def peek_card(self, index: int = 0) -> Optional[Card]:
        """
        Peek at a card without removing it from the deck.
        
        Args:
            index: Index of the card to peek at (0 = top of deck)
        
        Returns:
            The card at the specified index, or None if index is invalid
        """
        if 0 <= index < len(self._cards):
            return self._cards[index]
        return None
    
    def peek_cards(self, count: int) -> List[Card]:
        """
        Peek at multiple cards without removing them from the deck.
        
        Args:
            count: Number of cards to peek at
        
        Returns:
            List of cards from the top of the deck
        """
        return self._cards[:min(count, len(self._cards))]
    
    def reset(self) -> None:
        """Reset the deck to its original state with all 78 cards."""
        self._cards = [Card(card.metadata, card.orientation) for card in self._original_cards]
    
    def add_card(self, card: Card) -> None:
        """
        Add a card back to the deck.
        
        Args:
            card: The card to add to the deck
        """
        self._cards.append(card)
    
    def remove_card(self, card_id: str) -> Optional[Card]:
        """
        Remove a specific card from the deck by ID.
        
        Args:
            card_id: The ID of the card to remove
        
        Returns:
            The removed card, or None if not found
        """
        for i, card in enumerate(self._cards):
            if card.id == card_id:
                return self._cards.pop(i)
        return None
    
    def find_card(self, card_id: str) -> Optional[Card]:
        """
        Find a card in the deck by ID.
        
        Args:
            card_id: The ID of the card to find
        
        Returns:
            The card if found, or None
        """
        for card in self._cards:
            if card.id == card_id:
                return card
        return None
    
    def get_cards_by_suit(self, suit: Suit) -> List[Card]:
        """
        Get all cards of a specific suit from the deck.
        
        Args:
            suit: The suit to filter by
        
        Returns:
            List of cards matching the suit
        """
        return [card for card in self._cards if card.suit == suit]
    
    def get_cards_by_arcana(self, arcana: ArcanaType) -> List[Card]:
        """
        Get all cards of a specific arcana type from the deck.
        
        Args:
            arcana: The arcana type to filter by
        
        Returns:
            List of cards matching the arcana type
        """
        return [card for card in self._cards if card.arcana == arcana]
    
    def get_major_arcana(self) -> List[Card]:
        """Get all Major Arcana cards from the deck."""
        return self.get_cards_by_arcana(ArcanaType.MAJOR)
    
    def get_minor_arcana(self) -> List[Card]:
        """Get all Minor Arcana cards from the deck."""
        return self.get_cards_by_arcana(ArcanaType.MINOR)
    
    def get_court_cards(self) -> List[Card]:
        """Get all court cards (Page, Knight, Queen, King) from the deck."""
        return [card for card in self._cards if card.is_court_card()]
    
    def get_numbered_cards(self) -> List[Card]:
        """Get all numbered Minor Arcana cards from the deck."""
        return [card for card in self._cards if card.is_numbered_card()]
    
    def get_card_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the current deck state.
        
        Returns:
            Dictionary containing deck statistics
        """
        major_count = len(self.get_major_arcana())
        minor_count = len(self.get_minor_arcana())
        court_count = len(self.get_court_cards())
        numbered_count = len(self.get_numbered_cards())
        
        suit_counts = {}
        for suit in Suit:
            suit_counts[suit.value] = len(self.get_cards_by_suit(suit))
        
        return {
            'total_cards': len(self._cards),
            'major_arcana': major_count,
            'minor_arcana': minor_count,
            'court_cards': court_count,
            'numbered_cards': numbered_count,
            'suit_counts': suit_counts,
            'is_complete': self.is_complete,
            'is_empty': self.is_empty
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the deck to a dictionary representation.
        
        Returns:
            Dictionary containing deck information and cards
        """
        return {
            'total_cards': len(self._cards),
            'remaining_cards': len(self._cards),
            'is_complete': self.is_complete,
            'is_empty': self.is_empty,
            'statistics': self.get_card_statistics(),
            'cards': [card.to_dict() for card in self._cards]
        }
    
    def __str__(self) -> str:
        """String representation of the deck."""
        return f"Deck({len(self._cards)} cards remaining)"
    
    def __repr__(self) -> str:
        """Detailed string representation of the deck."""
        return f"Deck(total={len(self._original_cards)}, remaining={len(self._cards)}, complete={self.is_complete})"
    
    def __len__(self) -> int:
        """Get the number of cards in the deck."""
        return len(self._cards)
    
    def __iter__(self):
        """Make the deck iterable."""
        return iter(self._cards)
    
    def __contains__(self, card_id: str) -> bool:
        """Check if a card with the given ID is in the deck."""
        return self.find_card(card_id) is not None