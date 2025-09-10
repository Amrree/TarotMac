"""
Spread Layout Definitions

This module defines the structure and positions of various tarot spreads.
It includes predefined layouts for common spreads and provides a framework
for creating custom spreads.
"""

from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


class SpreadType(Enum):
    """Enumeration of supported spread types."""
    SINGLE_CARD = "single_card"
    THREE_CARD = "three_card"
    CELTIC_CROSS = "celtic_cross"
    RELATIONSHIP = "relationship"
    YEAR_AHEAD = "year_ahead"
    HORSESHOE = "horseshoe"
    CROSS = "cross"
    PYRAMID = "pyramid"


class PositionMeaning(Enum):
    """Enumeration of common position meanings."""
    # General meanings
    PAST = "past"
    PRESENT = "present"
    FUTURE = "future"
    
    # Three-card spreads
    SITUATION = "situation"
    ACTION = "action"
    OUTCOME = "outcome"
    
    # Celtic Cross meanings
    CURRENT_SITUATION = "current_situation"
    CHALLENGE = "challenge"
    DISTANT_PAST = "distant_past"
    RECENT_PAST = "recent_past"
    POSSIBLE_OUTCOME = "possible_outcome"
    NEAR_FUTURE = "near_future"
    YOUR_APPROACH = "your_approach"
    EXTERNAL_INFLUENCES = "external_influences"
    HOPES_FEARS = "hopes_fears"
    FINAL_OUTCOME = "final_outcome"
    
    # Relationship meanings
    YOU = "you"
    PARTNER = "partner"
    RELATIONSHIP = "relationship"
    ADVICE = "advice"
    
    # Year-ahead meanings
    JANUARY = "january"
    FEBRUARY = "february"
    MARCH = "march"
    APRIL = "april"
    MAY = "may"
    JUNE = "june"
    JULY = "july"
    AUGUST = "august"
    SEPTEMBER = "september"
    OCTOBER = "october"
    NOVEMBER = "november"
    DECEMBER = "december"


@dataclass
class SpreadPosition:
    """Represents a single position in a tarot spread."""
    
    position_id: str
    name: str
    meaning: PositionMeaning
    description: str
    coordinates: Tuple[float, float]  # (x, y) for visual layout
    is_optional: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert position to dictionary for serialization."""
        return {
            "position_id": self.position_id,
            "name": self.name,
            "meaning": self.meaning.value,
            "description": self.description,
            "coordinates": self.coordinates,
            "is_optional": self.is_optional
        }


class SpreadLayout:
    """Defines the structure and positions of a tarot spread."""
    
    def __init__(self, 
                 spread_type: SpreadType,
                 name: str,
                 description: str,
                 positions: List[SpreadPosition],
                 min_cards: Optional[int] = None,
                 max_cards: Optional[int] = None):
        """
        Initialize a spread layout.
        
        Args:
            spread_type: Type of spread
            name: Human-readable name
            description: Description of the spread's purpose
            positions: List of positions in the spread
            min_cards: Minimum number of cards required (defaults to len(positions))
            max_cards: Maximum number of cards allowed (defaults to len(positions))
        """
        self.spread_type = spread_type
        self.name = name
        self.description = description
        self.positions = positions
        self.min_cards = min_cards if min_cards is not None else len(positions)
        self.max_cards = max_cards if max_cards is not None else len(positions)
        
        # Validate positions
        self._validate_positions()
    
    def _validate_positions(self):
        """Validate that positions are properly defined."""
        if not self.positions:
            raise ValueError("Spread must have at least one position")
        
        position_ids = [pos.position_id for pos in self.positions]
        if len(position_ids) != len(set(position_ids)):
            raise ValueError("Position IDs must be unique")
        
        if self.min_cards > self.max_cards:
            raise ValueError("min_cards cannot be greater than max_cards")
        
        if self.max_cards > len(self.positions):
            raise ValueError("max_cards cannot be greater than number of positions")
    
    def get_position_by_id(self, position_id: str) -> Optional[SpreadPosition]:
        """Get a position by its ID."""
        for position in self.positions:
            if position.position_id == position_id:
                return position
        return None
    
    def get_required_positions(self) -> List[SpreadPosition]:
        """Get positions that are required (not optional)."""
        return [pos for pos in self.positions if not pos.is_optional]
    
    def get_optional_positions(self) -> List[SpreadPosition]:
        """Get positions that are optional."""
        return [pos for pos in self.positions if pos.is_optional]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert layout to dictionary for serialization."""
        return {
            "spread_type": self.spread_type.value,
            "name": self.name,
            "description": self.description,
            "positions": [pos.to_dict() for pos in self.positions],
            "min_cards": self.min_cards,
            "max_cards": self.max_cards
        }
    
    def __repr__(self):
        return f"SpreadLayout(type={self.spread_type.value}, name='{self.name}', positions={len(self.positions)})"


# Predefined spread layouts
def create_single_card_layout() -> SpreadLayout:
    """Create a single card spread layout."""
    positions = [
        SpreadPosition(
            position_id="card_1",
            name="The Answer",
            meaning=PositionMeaning.PRESENT,
            description="The card that answers your question or represents your current situation",
            coordinates=(0.5, 0.5)
        )
    ]
    
    return SpreadLayout(
        spread_type=SpreadType.SINGLE_CARD,
        name="Single Card",
        description="A simple one-card reading for quick insights or daily guidance",
        positions=positions
    )


def create_three_card_layout() -> SpreadLayout:
    """Create a three-card spread layout."""
    positions = [
        SpreadPosition(
            position_id="past",
            name="Past",
            meaning=PositionMeaning.PAST,
            description="What has led to your current situation",
            coordinates=(0.2, 0.5)
        ),
        SpreadPosition(
            position_id="present",
            name="Present",
            meaning=PositionMeaning.PRESENT,
            description="Your current situation or state of mind",
            coordinates=(0.5, 0.5)
        ),
        SpreadPosition(
            position_id="future",
            name="Future",
            meaning=PositionMeaning.FUTURE,
            description="What is likely to happen or what you should focus on",
            coordinates=(0.8, 0.5)
        )
    ]
    
    return SpreadLayout(
        spread_type=SpreadType.THREE_CARD,
        name="Three Card Spread",
        description="A classic past-present-future reading for understanding the flow of events",
        positions=positions
    )


def create_celtic_cross_layout() -> SpreadLayout:
    """Create a Celtic Cross spread layout."""
    positions = [
        SpreadPosition(
            position_id="current_situation",
            name="Current Situation",
            meaning=PositionMeaning.CURRENT_SITUATION,
            description="The heart of the matter - your current situation",
            coordinates=(0.3, 0.4)
        ),
        SpreadPosition(
            position_id="challenge",
            name="Challenge",
            meaning=PositionMeaning.CHALLENGE,
            description="The challenge or opportunity crossing your path",
            coordinates=(0.3, 0.6)
        ),
        SpreadPosition(
            position_id="distant_past",
            name="Distant Past",
            meaning=PositionMeaning.DISTANT_PAST,
            description="The foundation or root cause of your situation",
            coordinates=(0.1, 0.3)
        ),
        SpreadPosition(
            position_id="recent_past",
            name="Recent Past",
            meaning=PositionMeaning.RECENT_PAST,
            description="Recent events that have influenced your situation",
            coordinates=(0.1, 0.5)
        ),
        SpreadPosition(
            position_id="possible_outcome",
            name="Possible Outcome",
            meaning=PositionMeaning.POSSIBLE_OUTCOME,
            description="What could happen if you continue on your current path",
            coordinates=(0.1, 0.7)
        ),
        SpreadPosition(
            position_id="near_future",
            name="Near Future",
            meaning=PositionMeaning.NEAR_FUTURE,
            description="What is likely to happen in the near future",
            coordinates=(0.5, 0.3)
        ),
        SpreadPosition(
            position_id="your_approach",
            name="Your Approach",
            meaning=PositionMeaning.YOUR_APPROACH,
            description="Your attitude and approach to the situation",
            coordinates=(0.5, 0.5)
        ),
        SpreadPosition(
            position_id="external_influences",
            name="External Influences",
            meaning=PositionMeaning.EXTERNAL_INFLUENCES,
            description="People or circumstances affecting your situation",
            coordinates=(0.5, 0.7)
        ),
        SpreadPosition(
            position_id="hopes_fears",
            name="Hopes & Fears",
            meaning=PositionMeaning.HOPES_FEARS,
            description="Your hopes, fears, or expectations about the situation",
            coordinates=(0.7, 0.3)
        ),
        SpreadPosition(
            position_id="final_outcome",
            name="Final Outcome",
            meaning=PositionMeaning.FINAL_OUTCOME,
            description="The likely final outcome or resolution",
            coordinates=(0.7, 0.5)
        )
    ]
    
    return SpreadLayout(
        spread_type=SpreadType.CELTIC_CROSS,
        name="Celtic Cross",
        description="A comprehensive ten-card spread for deep insight into complex situations",
        positions=positions
    )


def create_relationship_layout() -> SpreadLayout:
    """Create a relationship spread layout."""
    positions = [
        SpreadPosition(
            position_id="you",
            name="You",
            meaning=PositionMeaning.YOU,
            description="Your feelings, thoughts, and approach to the relationship",
            coordinates=(0.25, 0.5)
        ),
        SpreadPosition(
            position_id="partner",
            name="Partner",
            meaning=PositionMeaning.PARTNER,
            description="Your partner's feelings, thoughts, and approach to the relationship",
            coordinates=(0.75, 0.5)
        ),
        SpreadPosition(
            position_id="relationship",
            name="Relationship",
            meaning=PositionMeaning.RELATIONSHIP,
            description="The current state and dynamics of the relationship",
            coordinates=(0.5, 0.3)
        ),
        SpreadPosition(
            position_id="advice",
            name="Advice",
            meaning=PositionMeaning.ADVICE,
            description="Guidance for improving or understanding the relationship",
            coordinates=(0.5, 0.7)
        )
    ]
    
    return SpreadLayout(
        spread_type=SpreadType.RELATIONSHIP,
        name="Relationship Spread",
        description="A four-card spread for understanding relationship dynamics and guidance",
        positions=positions
    )


def create_year_ahead_layout() -> SpreadLayout:
    """Create a year-ahead spread layout."""
    positions = [
        SpreadPosition(
            position_id="january",
            name="January",
            meaning=PositionMeaning.JANUARY,
            description="Themes and energy for January",
            coordinates=(0.1, 0.1)
        ),
        SpreadPosition(
            position_id="february",
            name="February",
            meaning=PositionMeaning.FEBRUARY,
            description="Themes and energy for February",
            coordinates=(0.3, 0.1)
        ),
        SpreadPosition(
            position_id="march",
            name="March",
            meaning=PositionMeaning.MARCH,
            description="Themes and energy for March",
            coordinates=(0.5, 0.1)
        ),
        SpreadPosition(
            position_id="april",
            name="April",
            meaning=PositionMeaning.APRIL,
            description="Themes and energy for April",
            coordinates=(0.7, 0.1)
        ),
        SpreadPosition(
            position_id="may",
            name="May",
            meaning=PositionMeaning.MAY,
            description="Themes and energy for May",
            coordinates=(0.9, 0.1)
        ),
        SpreadPosition(
            position_id="june",
            name="June",
            meaning=PositionMeaning.JUNE,
            description="Themes and energy for June",
            coordinates=(0.9, 0.3)
        ),
        SpreadPosition(
            position_id="july",
            name="July",
            meaning=PositionMeaning.JULY,
            description="Themes and energy for July",
            coordinates=(0.9, 0.5)
        ),
        SpreadPosition(
            position_id="august",
            name="August",
            meaning=PositionMeaning.AUGUST,
            description="Themes and energy for August",
            coordinates=(0.9, 0.7)
        ),
        SpreadPosition(
            position_id="september",
            name="September",
            meaning=PositionMeaning.SEPTEMBER,
            description="Themes and energy for September",
            coordinates=(0.9, 0.9)
        ),
        SpreadPosition(
            position_id="october",
            name="October",
            meaning=PositionMeaning.OCTOBER,
            description="Themes and energy for October",
            coordinates=(0.7, 0.9)
        ),
        SpreadPosition(
            position_id="november",
            name="November",
            meaning=PositionMeaning.NOVEMBER,
            description="Themes and energy for November",
            coordinates=(0.5, 0.9)
        ),
        SpreadPosition(
            position_id="december",
            name="December",
            meaning=PositionMeaning.DECEMBER,
            description="Themes and energy for December",
            coordinates=(0.3, 0.9)
        )
    ]
    
    return SpreadLayout(
        spread_type=SpreadType.YEAR_AHEAD,
        name="Year Ahead",
        description="A twelve-card spread for monthly guidance throughout the year",
        positions=positions
    )


# Registry of available spreads
SPREAD_REGISTRY = {
    SpreadType.SINGLE_CARD: create_single_card_layout,
    SpreadType.THREE_CARD: create_three_card_layout,
    SpreadType.CELTIC_CROSS: create_celtic_cross_layout,
    SpreadType.RELATIONSHIP: create_relationship_layout,
    SpreadType.YEAR_AHEAD: create_year_ahead_layout,
}


def get_spread_layout(spread_type: SpreadType) -> SpreadLayout:
    """Get a spread layout by type."""
    if spread_type not in SPREAD_REGISTRY:
        raise ValueError(f"Unknown spread type: {spread_type}")
    
    return SPREAD_REGISTRY[spread_type]()


def get_available_spreads() -> List[SpreadType]:
    """Get list of available spread types."""
    return list(SPREAD_REGISTRY.keys())