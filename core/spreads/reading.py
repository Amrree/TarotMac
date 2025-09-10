"""
Spread Reading Management

This module manages individual tarot spread readings, including card placement,
interpretation, and integration with the influence engine.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import uuid

from .layout import SpreadLayout, SpreadPosition
from ..deck.card import Card, Orientation


@dataclass
class PositionedCard:
    """A card placed in a specific position within a spread."""
    
    card: Card
    position: SpreadPosition
    drawn_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "card": self.card.to_dict(),
            "position": self.position.to_dict(),
            "drawn_at": self.drawn_at.isoformat()
        }


@dataclass
class SpreadReading:
    """Manages a complete tarot spread reading."""
    
    reading_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    layout: SpreadLayout = None
    positioned_cards: List[PositionedCard] = field(default_factory=list)
    question: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    interpretations: Dict[str, str] = field(default_factory=dict)
    notes: str = ""
    
    def __post_init__(self):
        """Validate the reading after initialization."""
        if self.layout is None:
            raise ValueError("Spread reading must have a layout")
        
        # Only validate positioned cards if there are any
        if self.positioned_cards:
            self._validate_positioned_cards()
    
    def _validate_positioned_cards(self):
        """Validate that positioned cards are properly placed."""
        if len(self.positioned_cards) > self.layout.max_cards:
            raise ValueError(f"Too many cards: {len(self.positioned_cards)} > {self.layout.max_cards}")
        
        if len(self.positioned_cards) < self.layout.min_cards:
            raise ValueError(f"Too few cards: {len(self.positioned_cards)} < {self.layout.min_cards}")
        
        # Check for duplicate positions
        position_ids = [pc.position.position_id for pc in self.positioned_cards]
        if len(position_ids) != len(set(position_ids)):
            raise ValueError("Duplicate positions found in reading")
        
        # Check for invalid positions
        valid_position_ids = {pos.position_id for pos in self.layout.positions}
        for pc in self.positioned_cards:
            if pc.position.position_id not in valid_position_ids:
                raise ValueError(f"Invalid position: {pc.position.position_id}")
    
    def add_card(self, card: Card, position: SpreadPosition) -> None:
        """Add a card to a specific position."""
        # Check if position is already occupied
        for pc in self.positioned_cards:
            if pc.position.position_id == position.position_id:
                raise ValueError(f"Position {position.position_id} is already occupied")
        
        # Check if we can add more cards
        if len(self.positioned_cards) >= self.layout.max_cards:
            raise ValueError(f"Cannot add more cards: maximum {self.layout.max_cards} allowed")
        
        positioned_card = PositionedCard(card=card, position=position)
        self.positioned_cards.append(positioned_card)
    
    def remove_card(self, position_id: str) -> Optional[Card]:
        """Remove a card from a specific position."""
        for i, pc in enumerate(self.positioned_cards):
            if pc.position.position_id == position_id:
                removed_card = self.positioned_cards.pop(i).card
                return removed_card
        return None
    
    def get_card_at_position(self, position_id: str) -> Optional[Card]:
        """Get the card at a specific position."""
        for pc in self.positioned_cards:
            if pc.position.position_id == position_id:
                return pc.card
        return None
    
    def get_positioned_card(self, position_id: str) -> Optional[PositionedCard]:
        """Get the positioned card at a specific position."""
        for pc in self.positioned_cards:
            if pc.position.position_id == position_id:
                return pc
        return None
    
    def get_cards_by_meaning(self, meaning: str) -> List[PositionedCard]:
        """Get all cards with a specific position meaning."""
        return [pc for pc in self.positioned_cards 
                if pc.position.meaning.value == meaning]
    
    def get_all_cards(self) -> List[Card]:
        """Get all cards in the reading."""
        return [pc.card for pc in self.positioned_cards]
    
    def is_complete(self) -> bool:
        """Check if the reading is complete (has all required cards)."""
        required_positions = self.layout.get_required_positions()
        occupied_positions = {pc.position.position_id for pc in self.positioned_cards}
        
        for pos in required_positions:
            if pos.position_id not in occupied_positions:
                return False
        
        return True
    
    def get_missing_positions(self) -> List[SpreadPosition]:
        """Get positions that still need cards."""
        occupied_positions = {pc.position.position_id for pc in self.positioned_cards}
        return [pos for pos in self.layout.positions 
                if pos.position_id not in occupied_positions]
    
    def get_available_positions(self) -> List[SpreadPosition]:
        """Get positions that are available for new cards."""
        occupied_positions = {pc.position.position_id for pc in self.positioned_cards}
        return [pos for pos in self.layout.positions 
                if pos.position_id not in occupied_positions]
    
    def set_interpretation(self, position_id: str, interpretation: str) -> None:
        """Set interpretation for a specific position."""
        # Verify position exists
        if not any(pc.position.position_id == position_id for pc in self.positioned_cards):
            raise ValueError(f"No card at position {position_id}")
        
        self.interpretations[position_id] = interpretation
    
    def get_interpretation(self, position_id: str) -> Optional[str]:
        """Get interpretation for a specific position."""
        return self.interpretations.get(position_id)
    
    def get_reading_summary(self) -> Dict[str, Any]:
        """Get a summary of the reading."""
        return {
            "reading_id": self.reading_id,
            "layout": self.layout.to_dict(),
            "question": self.question,
            "created_at": self.created_at.isoformat(),
            "is_complete": self.is_complete(),
            "card_count": len(self.positioned_cards),
            "positions": [
                {
                    "position_id": pc.position.position_id,
                    "position_name": pc.position.name,
                    "meaning": pc.position.meaning.value,
                    "card_name": pc.card.name,
                    "orientation": pc.card.orientation.value,
                    "interpretation": self.interpretations.get(pc.position.position_id)
                }
                for pc in self.positioned_cards
            ]
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert reading to dictionary for serialization."""
        return {
            "reading_id": self.reading_id,
            "layout": self.layout.to_dict(),
            "positioned_cards": [pc.to_dict() for pc in self.positioned_cards],
            "question": self.question,
            "created_at": self.created_at.isoformat(),
            "interpretations": self.interpretations,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SpreadReading':
        """Create a reading from dictionary data."""
        # This would need to be implemented with proper deserialization
        # For now, we'll raise NotImplementedError
        raise NotImplementedError("Deserialization from dict not yet implemented")
    
    def __repr__(self):
        return f"SpreadReading(id={self.reading_id[:8]}, layout={self.layout.name}, cards={len(self.positioned_cards)})"