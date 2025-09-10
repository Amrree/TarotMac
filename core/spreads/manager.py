"""
Spread Manager

This module provides the main interface for creating and managing tarot spreads.
It integrates with the deck module for card drawing and the influence engine
for card interpretation.
"""

from typing import List, Dict, Any, Optional, Tuple
import random
from datetime import datetime

from .layout import SpreadLayout, SpreadType, get_spread_layout, get_available_spreads
from .reading import SpreadReading, PositionedCard
from ..deck.deck import Deck
from ..deck.card import Card, Orientation
from ..influence.advanced_engine import TarotInfluenceEngine, CardPosition


class SpreadManager:
    """Manages tarot spread operations and integration with other modules."""
    
    def __init__(self, deck: Optional[Deck] = None, influence_engine: Optional[TarotInfluenceEngine] = None):
        """
        Initialize the spread manager.
        
        Args:
            deck: Deck instance for card drawing (optional)
            influence_engine: Influence engine for card interpretation (optional)
        """
        self.deck = deck
        self.influence_engine = influence_engine
        self._available_spreads = get_available_spreads()
    
    def get_available_spreads(self) -> List[SpreadType]:
        """Get list of available spread types."""
        return self._available_spreads.copy()
    
    def create_spread_layout(self, spread_type: SpreadType) -> SpreadLayout:
        """Create a spread layout of the specified type."""
        return get_spread_layout(spread_type)
    
    def create_reading(self, 
                      spread_type: SpreadType, 
                      question: Optional[str] = None,
                      shuffle_seed: Optional[int] = None) -> SpreadReading:
        """
        Create a new spread reading with the specified layout.
        
        Args:
            spread_type: Type of spread to create
            question: Optional question for the reading
            shuffle_seed: Optional seed for deterministic shuffling
            
        Returns:
            SpreadReading instance ready for card placement
        """
        layout = self.create_spread_layout(spread_type)
        reading = SpreadReading(layout=layout, question=question)
        
        # Note: Deck seed is set during creation, not after
        # For deterministic shuffling, create a new deck with the seed
        if shuffle_seed is not None and self.deck is not None:
            # We'll use the seed when drawing cards instead
            pass
        
        return reading
    
    def draw_cards_for_reading(self, 
                              reading: SpreadReading,
                              allow_reversed: bool = True,
                              shuffle_before_drawing: bool = True,
                              shuffle_seed: Optional[int] = None) -> SpreadReading:
        """
        Draw cards from the deck and place them in the reading.
        
        Args:
            reading: The reading to populate with cards
            allow_reversed: Whether to allow reversed cards
            shuffle_before_drawing: Whether to shuffle deck before drawing
            shuffle_seed: Optional seed for deterministic shuffling
            
        Returns:
            The reading with cards placed in positions
        """
        if self.deck is None:
            raise ValueError("No deck available for drawing cards")
        
        if reading.is_complete():
            raise ValueError("Reading is already complete")
        
        # Reset deck to full state
        self.deck.reset()
        
        # Shuffle if requested
        if shuffle_before_drawing:
            if shuffle_seed is not None:
                # Set the random seed for shuffling
                random.seed(shuffle_seed)
            self.deck.shuffle()
        
        # Get positions that need cards
        missing_positions = reading.get_missing_positions()
        
        # Draw cards for each missing position
        for position in missing_positions:
            if self.deck.is_empty:
                raise ValueError("Not enough cards in deck for reading")
            
            # Draw a card
            card = self.deck.draw_card()
            
            # Set orientation (randomly if allowing reversed)
            if allow_reversed and random.choice([True, False]):
                card.set_orientation(Orientation.REVERSED)
            else:
                card.set_orientation(Orientation.UPRIGHT)
            
            # Add card to reading
            reading.add_card(card, position)
        
        return reading
    
    def interpret_reading(self, reading: SpreadReading) -> Dict[str, Any]:
        """
        Interpret a reading using the influence engine.
        
        Args:
            reading: The reading to interpret
            
        Returns:
            Dictionary containing interpretations and influence factors
        """
        if self.influence_engine is None:
            # Return basic interpretation without influence engine
            return self._basic_interpretation(reading)
        
        # Convert reading to influence engine format
        card_positions = []
        for pc in reading.positioned_cards:
            card_pos = CardPosition(
                position_id=pc.position.position_id,
                card_id=pc.card.id,
                orientation=pc.card.orientation.value,
                x_coordinate=pc.position.coordinates[0],
                y_coordinate=pc.position.coordinates[1]
            )
            card_positions.append(card_pos)
        
        # Get influence results
        # Convert card positions to the format expected by the influence engine
        reading_input = {
            "reading_id": reading.reading_id,
            "spread_type": reading.layout.spread_type.value,
            "positions": [
                {
                    "position_id": cp.position_id,
                    "card_id": cp.card_id,
                    "orientation": cp.orientation,
                    "coordinates": [cp.x_coordinate, cp.y_coordinate]
                }
                for cp in card_positions
            ]
        }
        influence_result = self.influence_engine.compute_influences(reading_input)
        
        # Format results for reading
        interpretations = {}
        for influenced_card in influence_result.influenced_cards:
            position_id = influenced_card.position_id
            interpretations[position_id] = {
                "card_name": influenced_card.card.name,
                "orientation": influenced_card.card.orientation.value,
                "influenced_text": influenced_card.influenced_text,
                "confidence": influenced_card.confidence,
                "influence_factors": [
                    {
                        "source": factor.source,
                        "explanation": factor.explanation,
                        "polarity_effect": factor.polarity_effect,
                        "intensity_effect": factor.intensity_effect,
                        "theme_effects": factor.theme_effects
                    }
                    for factor in influenced_card.influence_factors
                ]
            }
        
        return {
            "reading_summary": reading.get_reading_summary(),
            "interpretations": interpretations,
            "overall_summary": influence_result.summary,
            "advice": influence_result.advice,
            "confidence": influence_result.confidence
        }
    
    def _basic_interpretation(self, reading: SpreadReading) -> Dict[str, Any]:
        """Provide basic interpretation without influence engine."""
        interpretations = {}
        
        for pc in reading.positioned_cards:
            interpretations[pc.position.position_id] = {
                "card_name": pc.card.name,
                "orientation": pc.card.orientation.value,
                "basic_meaning": pc.card.get_meaning(),
                "position_meaning": pc.position.description,
                "keywords": pc.card.keywords
            }
        
        return {
            "reading_summary": reading.get_reading_summary(),
            "interpretations": interpretations,
            "overall_summary": "Basic interpretation without influence engine",
            "advice": "Consider using influence engine for deeper insights",
            "confidence": "medium"
        }
    
    def get_reading_statistics(self, reading: SpreadReading) -> Dict[str, Any]:
        """Get statistics about a reading."""
        cards = reading.get_all_cards()
        
        # Count by arcana
        major_count = sum(1 for card in cards if card.arcana == "major")
        minor_count = sum(1 for card in cards if card.arcana == "minor")
        
        # Count by orientation
        upright_count = sum(1 for card in cards if card.orientation == Orientation.UPRIGHT)
        reversed_count = sum(1 for card in cards if card.orientation == Orientation.REVERSED)
        
        # Count by suit (minor arcana only)
        suit_counts = {}
        for card in cards:
            if card.arcana == "minor" and card.suit:
                suit_counts[card.suit] = suit_counts.get(card.suit, 0) + 1
        
        # Count by element
        element_counts = {}
        for card in cards:
            if card.element:
                element_counts[card.element] = element_counts.get(card.element, 0) + 1
        
        return {
            "total_cards": len(cards),
            "major_arcana": major_count,
            "minor_arcana": minor_count,
            "upright_cards": upright_count,
            "reversed_cards": reversed_count,
            "suit_distribution": suit_counts,
            "element_distribution": element_counts,
            "completion_status": "complete" if reading.is_complete() else "incomplete"
        }
    
    def validate_reading(self, reading: SpreadReading) -> Tuple[bool, List[str]]:
        """
        Validate a reading for completeness and correctness.
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        # Check completeness
        if not reading.is_complete():
            missing = reading.get_missing_positions()
            issues.append(f"Reading incomplete: missing {len(missing)} required positions")
        
        # Check card count
        if len(reading.positioned_cards) > reading.layout.max_cards:
            issues.append(f"Too many cards: {len(reading.positioned_cards)} > {reading.layout.max_cards}")
        
        if len(reading.positioned_cards) < reading.layout.min_cards:
            issues.append(f"Too few cards: {len(reading.positioned_cards)} < {reading.layout.min_cards}")
        
        # Check for duplicate cards
        card_ids = [pc.card.id for pc in reading.positioned_cards]
        if len(card_ids) != len(set(card_ids)):
            issues.append("Duplicate cards found in reading")
        
        # Check deck state if available
        if self.deck is not None:
            if self.deck.is_empty:
                issues.append("Deck is empty")
        
        return len(issues) == 0, issues
    
    def export_reading(self, reading: SpreadReading, format: str = "json") -> str:
        """
        Export a reading in the specified format.
        
        Args:
            reading: The reading to export
            format: Export format ("json", "text", "summary")
            
        Returns:
            Exported reading as string
        """
        if format == "json":
            import json
            return json.dumps(reading.to_dict(), indent=2)
        
        elif format == "text":
            lines = [
                f"Reading: {reading.layout.name}",
                f"Question: {reading.question or 'No specific question'}",
                f"Date: {reading.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
                f"Cards: {len(reading.positioned_cards)}",
                ""
            ]
            
            for pc in reading.positioned_cards:
                lines.extend([
                    f"{pc.position.name} ({pc.position.meaning.value}):",
                    f"  {pc.card.get_display_name()}",
                    f"  {pc.card.get_meaning()}",
                    ""
                ])
            
            return "\n".join(lines)
        
        elif format == "summary":
            summary = reading.get_reading_summary()
            return f"Reading {summary['reading_id'][:8]}: {summary['layout']['name']} - {summary['card_count']} cards"
        
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def __repr__(self):
        return f"SpreadManager(deck={'available' if self.deck else 'none'}, influence={'available' if self.influence_engine else 'none'})"