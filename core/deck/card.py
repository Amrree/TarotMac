"""
Tarot Card representation for the Deck Module.

This module defines the Card class that represents individual tarot cards
with their metadata, meanings, and orientation support.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class ArcanaType(Enum):
    """Enumeration for Major and Minor Arcana types."""
    MAJOR = "major"
    MINOR = "minor"


class Suit(Enum):
    """Enumeration for Minor Arcana suits."""
    WANDS = "wands"
    CUPS = "cups"
    SWORDS = "swords"
    PENTACLES = "pentacles"


class Orientation(Enum):
    """Enumeration for card orientation."""
    UPRIGHT = "upright"
    REVERSED = "reversed"


@dataclass
class CardMetadata:
    """Metadata for a tarot card."""
    name: str
    arcana: ArcanaType
    suit: Optional[Suit] = None
    number: Optional[int] = None
    rank: Optional[str] = None  # For court cards: page, knight, queen, king
    element: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    upright_text: str = ""
    reversed_text: str = ""
    themes: Dict[str, float] = field(default_factory=dict)
    polarity_baseline: float = 0.0
    intensity_baseline: float = 0.5


class Card:
    """
    Represents a single tarot card with its metadata and current state.
    
    A Card object contains all the information needed to represent a tarot card
    including its name, arcana type, suit, meanings, and current orientation.
    """
    
    def __init__(self, metadata: CardMetadata, orientation: Orientation = Orientation.UPRIGHT):
        """
        Initialize a Card with metadata and orientation.
        
        Args:
            metadata: CardMetadata object containing card information
            orientation: Current orientation of the card (upright or reversed)
        """
        self.metadata = metadata
        self.orientation = orientation
        self._id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate a unique ID for the card."""
        if self.metadata.arcana == ArcanaType.MAJOR:
            return self.metadata.name.lower().replace(' ', '_').replace('the_', '')
        else:
            suit_name = self.metadata.suit.value if self.metadata.suit else "unknown"
            if self.metadata.number:
                return f"{self.metadata.number}_{suit_name}"
            elif self.metadata.rank:
                return f"{self.metadata.rank}_{suit_name}"
            else:
                return f"unknown_{suit_name}"
    
    @property
    def id(self) -> str:
        """Get the unique identifier for this card."""
        return self._id
    
    @property
    def name(self) -> str:
        """Get the card name."""
        return self.metadata.name
    
    @property
    def arcana(self) -> ArcanaType:
        """Get the arcana type (Major or Minor)."""
        return self.metadata.arcana
    
    @property
    def suit(self) -> Optional[Suit]:
        """Get the suit (for Minor Arcana cards)."""
        return self.metadata.suit
    
    @property
    def number(self) -> Optional[int]:
        """Get the number (for numbered Minor Arcana cards)."""
        return self.metadata.number
    
    @property
    def rank(self) -> Optional[str]:
        """Get the rank (for court cards)."""
        return self.metadata.rank
    
    @property
    def element(self) -> Optional[str]:
        """Get the elemental association."""
        return self.metadata.element
    
    @property
    def keywords(self) -> List[str]:
        """Get the keywords associated with this card."""
        return self.metadata.keywords.copy()
    
    @property
    def themes(self) -> Dict[str, float]:
        """Get the thematic weights for this card."""
        return self.metadata.themes.copy()
    
    @property
    def polarity_baseline(self) -> float:
        """Get the baseline polarity score."""
        return self.metadata.polarity_baseline
    
    @property
    def intensity_baseline(self) -> float:
        """Get the baseline intensity score."""
        return self.metadata.intensity_baseline
    
    def get_meaning(self) -> str:
        """
        Get the meaning text for the current orientation.
        
        Returns:
            The upright or reversed meaning text based on current orientation
        """
        if self.orientation == Orientation.UPRIGHT:
            return self.metadata.upright_text
        else:
            return self.metadata.reversed_text
    
    def get_upright_meaning(self) -> str:
        """Get the upright meaning text."""
        return self.metadata.upright_text
    
    def get_reversed_meaning(self) -> str:
        """Get the reversed meaning text."""
        return self.metadata.reversed_text
    
    def flip(self) -> None:
        """Flip the card to the opposite orientation."""
        if self.orientation == Orientation.UPRIGHT:
            self.orientation = Orientation.REVERSED
        else:
            self.orientation = Orientation.UPRIGHT
    
    def set_orientation(self, orientation: Orientation) -> None:
        """
        Set the card orientation.
        
        Args:
            orientation: The new orientation for the card
        """
        self.orientation = orientation
    
    def is_major(self) -> bool:
        """Check if this is a Major Arcana card."""
        return self.metadata.arcana == ArcanaType.MAJOR
    
    def is_minor(self) -> bool:
        """Check if this is a Minor Arcana card."""
        return self.metadata.arcana == ArcanaType.MINOR
    
    def is_court_card(self) -> bool:
        """Check if this is a court card (Page, Knight, Queen, King)."""
        return self.metadata.rank is not None
    
    def is_numbered_card(self) -> bool:
        """Check if this is a numbered Minor Arcana card."""
        return self.metadata.number is not None
    
    def get_display_name(self) -> str:
        """
        Get a display-friendly name for the card.
        
        Returns:
            Formatted name suitable for display
        """
        if self.metadata.arcana == ArcanaType.MAJOR:
            return self.metadata.name
        else:
            if self.metadata.number:
                return f"{self.metadata.number} of {self.metadata.suit.value.title()}"
            elif self.metadata.rank:
                return f"{self.metadata.rank.title()} of {self.metadata.suit.value.title()}"
            else:
                return self.metadata.name
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the card to a dictionary representation.
        
        Returns:
            Dictionary containing all card information
        """
        return {
            'id': self.id,
            'name': self.name,
            'arcana': self.arcana.value,
            'suit': self.suit.value if self.suit else None,
            'number': self.number,
            'rank': self.rank,
            'element': self.element,
            'keywords': self.keywords,
            'themes': self.themes,
            'polarity_baseline': self.polarity_baseline,
            'intensity_baseline': self.intensity_baseline,
            'orientation': self.orientation.value,
            'upright_text': self.get_upright_meaning(),
            'reversed_text': self.get_reversed_meaning(),
            'current_meaning': self.get_meaning()
        }
    
    def __str__(self) -> str:
        """String representation of the card."""
        orientation_str = "Upright" if self.orientation == Orientation.UPRIGHT else "Reversed"
        return f"{self.get_display_name()} ({orientation_str})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the card."""
        return f"Card(id='{self.id}', name='{self.name}', arcana='{self.arcana.value}', orientation='{self.orientation.value}')"
    
    def __eq__(self, other) -> bool:
        """Check if two cards are equal (same ID and orientation)."""
        if not isinstance(other, Card):
            return False
        return self.id == other.id and self.orientation == other.orientation
    
    def __hash__(self) -> int:
        """Hash the card for use in sets and dictionaries."""
        return hash((self.id, self.orientation.value))