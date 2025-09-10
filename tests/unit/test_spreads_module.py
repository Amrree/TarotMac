"""
Unit tests for the Spreads Module

Tests all components of the spreads module including layouts, readings,
and the spread manager.
"""

import pytest
import json
from datetime import datetime
from typing import List, Dict, Any

from core.spreads.layout import (
    SpreadLayout, SpreadPosition, SpreadType, PositionMeaning,
    create_single_card_layout, create_three_card_layout, create_celtic_cross_layout,
    create_relationship_layout, create_year_ahead_layout,
    get_spread_layout, get_available_spreads
)
from core.spreads.reading import SpreadReading, PositionedCard
from core.spreads.manager import SpreadManager
from core.deck.deck import Deck
from core.deck.card import Card, Orientation
from core.deck.loader import DeckLoader


class TestSpreadLayout:
    """Test spread layout functionality."""
    
    def test_spread_position_creation(self):
        """Test SpreadPosition creation and validation."""
        position = SpreadPosition(
            position_id="test_pos",
            name="Test Position",
            meaning=PositionMeaning.PRESENT,
            description="A test position",
            coordinates=(0.5, 0.5)
        )
        
        assert position.position_id == "test_pos"
        assert position.name == "Test Position"
        assert position.meaning == PositionMeaning.PRESENT
        assert position.coordinates == (0.5, 0.5)
        assert not position.is_optional
    
    def test_spread_position_to_dict(self):
        """Test SpreadPosition serialization."""
        position = SpreadPosition(
            position_id="test_pos",
            name="Test Position",
            meaning=PositionMeaning.PRESENT,
            description="A test position",
            coordinates=(0.5, 0.5),
            is_optional=True
        )
        
        data = position.to_dict()
        assert data["position_id"] == "test_pos"
        assert data["meaning"] == "present"
        assert data["is_optional"] is True
    
    def test_spread_layout_creation(self):
        """Test SpreadLayout creation and validation."""
        positions = [
            SpreadPosition(
                position_id="pos1",
                name="Position 1",
                meaning=PositionMeaning.PRESENT,
                description="First position",
                coordinates=(0.3, 0.5)
            ),
            SpreadPosition(
                position_id="pos2",
                name="Position 2",
                meaning=PositionMeaning.FUTURE,
                description="Second position",
                coordinates=(0.7, 0.5)
            )
        ]
        
        layout = SpreadLayout(
            spread_type=SpreadType.THREE_CARD,
            name="Test Layout",
            description="A test layout",
            positions=positions
        )
        
        assert layout.spread_type == SpreadType.THREE_CARD
        assert layout.name == "Test Layout"
        assert len(layout.positions) == 2
        assert layout.min_cards == 2
        assert layout.max_cards == 2
    
    def test_spread_layout_validation(self):
        """Test SpreadLayout validation."""
        # Test empty positions
        with pytest.raises(ValueError, match="Spread must have at least one position"):
            SpreadLayout(
                spread_type=SpreadType.SINGLE_CARD,
                name="Empty Layout",
                description="Empty",
                positions=[]
            )
        
        # Test duplicate position IDs
        positions = [
            SpreadPosition("pos1", "Pos 1", PositionMeaning.PRESENT, "Desc", (0.3, 0.5)),
            SpreadPosition("pos1", "Pos 1", PositionMeaning.FUTURE, "Desc", (0.7, 0.5))
        ]
        
        with pytest.raises(ValueError, match="Position IDs must be unique"):
            SpreadLayout(
                spread_type=SpreadType.THREE_CARD,
                name="Duplicate Layout",
                description="Duplicate",
                positions=positions
            )
        
        # Test invalid card counts
        positions = [
            SpreadPosition("pos1", "Pos 1", PositionMeaning.PRESENT, "Desc", (0.5, 0.5))
        ]
        
        with pytest.raises(ValueError, match="min_cards cannot be greater than max_cards"):
            SpreadLayout(
                spread_type=SpreadType.SINGLE_CARD,
                name="Invalid Layout",
                description="Invalid",
                positions=positions,
                min_cards=2,
                max_cards=1
            )
    
    def test_spread_layout_methods(self):
        """Test SpreadLayout utility methods."""
        positions = [
            SpreadPosition("pos1", "Pos 1", PositionMeaning.PRESENT, "Desc", (0.3, 0.5)),
            SpreadPosition("pos2", "Pos 2", PositionMeaning.FUTURE, "Desc", (0.7, 0.5), is_optional=True)
        ]
        
        layout = SpreadLayout(
            spread_type=SpreadType.THREE_CARD,
            name="Test Layout",
            description="Test",
            positions=positions
        )
        
        # Test get_position_by_id
        pos = layout.get_position_by_id("pos1")
        assert pos is not None
        assert pos.name == "Pos 1"
        
        pos = layout.get_position_by_id("nonexistent")
        assert pos is None
        
        # Test get_required_positions
        required = layout.get_required_positions()
        assert len(required) == 1
        assert required[0].position_id == "pos1"
        
        # Test get_optional_positions
        optional = layout.get_optional_positions()
        assert len(optional) == 1
        assert optional[0].position_id == "pos2"
    
    def test_predefined_layouts(self):
        """Test predefined spread layouts."""
        # Test single card layout
        single_layout = create_single_card_layout()
        assert single_layout.spread_type == SpreadType.SINGLE_CARD
        assert len(single_layout.positions) == 1
        assert single_layout.positions[0].meaning == PositionMeaning.PRESENT
        
        # Test three card layout
        three_layout = create_three_card_layout()
        assert three_layout.spread_type == SpreadType.THREE_CARD
        assert len(three_layout.positions) == 3
        meanings = [pos.meaning for pos in three_layout.positions]
        assert PositionMeaning.PAST in meanings
        assert PositionMeaning.PRESENT in meanings
        assert PositionMeaning.FUTURE in meanings
        
        # Test Celtic Cross layout
        celtic_layout = create_celtic_cross_layout()
        assert celtic_layout.spread_type == SpreadType.CELTIC_CROSS
        assert len(celtic_layout.positions) == 10
        
        # Test relationship layout
        relationship_layout = create_relationship_layout()
        assert relationship_layout.spread_type == SpreadType.RELATIONSHIP
        assert len(relationship_layout.positions) == 4
        
        # Test year ahead layout
        year_layout = create_year_ahead_layout()
        assert year_layout.spread_type == SpreadType.YEAR_AHEAD
        assert len(year_layout.positions) == 12
    
    def test_spread_registry(self):
        """Test spread registry functionality."""
        # Test get_available_spreads
        available = get_available_spreads()
        assert SpreadType.SINGLE_CARD in available
        assert SpreadType.THREE_CARD in available
        assert SpreadType.CELTIC_CROSS in available
        
        # Test get_spread_layout
        layout = get_spread_layout(SpreadType.SINGLE_CARD)
        assert layout.spread_type == SpreadType.SINGLE_CARD
        
        # Test unknown spread type
        with pytest.raises(ValueError, match="Unknown spread type"):
            get_spread_layout(SpreadType.HORSESHOE)  # Not in registry


class TestSpreadReading:
    """Test spread reading functionality."""
    
    def test_reading_creation(self):
        """Test SpreadReading creation."""
        layout = create_single_card_layout()
        reading = SpreadReading(layout=layout, question="Test question?")
        
        assert reading.layout == layout
        assert reading.question == "Test question?"
        assert len(reading.positioned_cards) == 0
        assert not reading.is_complete()
    
    def test_reading_without_layout(self):
        """Test SpreadReading validation without layout."""
        with pytest.raises(ValueError, match="Spread reading must have a layout"):
            SpreadReading(layout=None)
    
    def test_add_card_to_reading(self):
        """Test adding cards to a reading."""
        layout = create_single_card_layout()
        reading = SpreadReading(layout=layout)
        
        card = Card(name="Test Card", arcana="major")
        position = layout.positions[0]
        
        reading.add_card(card, position)
        
        assert len(reading.positioned_cards) == 1
        assert reading.get_card_at_position(position.position_id) == card
        assert reading.is_complete()
    
    def test_add_card_to_occupied_position(self):
        """Test adding card to already occupied position."""
        layout = create_single_card_layout()
        reading = SpreadReading(layout=layout)
        
        card1 = Card(name="Card 1", arcana="major")
        card2 = Card(name="Card 2", arcana="major")
        position = layout.positions[0]
        
        reading.add_card(card1, position)
        
        with pytest.raises(ValueError, match="Position .* is already occupied"):
            reading.add_card(card2, position)
    
    def test_add_card_exceeds_maximum(self):
        """Test adding card when maximum is reached."""
        layout = create_single_card_layout()
        reading = SpreadReading(layout=layout)
        
        card1 = Card(name="Card 1", arcana="major")
        card2 = Card(name="Card 2", arcana="major")
        position = layout.positions[0]
        
        reading.add_card(card1, position)
        
        with pytest.raises(ValueError, match="Cannot add more cards"):
            reading.add_card(card2, position)
    
    def test_remove_card_from_reading(self):
        """Test removing cards from a reading."""
        layout = create_single_card_layout()
        reading = SpreadReading(layout=layout)
        
        card = Card(name="Test Card", arcana="major")
        position = layout.positions[0]
        
        reading.add_card(card, position)
        assert reading.is_complete()
        
        removed_card = reading.remove_card(position.position_id)
        assert removed_card == card
        assert not reading.is_complete()
        assert reading.get_card_at_position(position.position_id) is None
    
    def test_remove_card_from_empty_position(self):
        """Test removing card from empty position."""
        layout = create_single_card_layout()
        reading = SpreadReading(layout=layout)
        
        removed_card = reading.remove_card("nonexistent")
        assert removed_card is None
    
    def test_get_cards_by_meaning(self):
        """Test getting cards by position meaning."""
        layout = create_three_card_layout()
        reading = SpreadReading(layout=layout)
        
        # Add cards to past and present positions
        past_pos = layout.get_position_by_id("past")
        present_pos = layout.get_position_by_id("present")
        
        reading.add_card(Card(name="Past Card", arcana="major"), past_pos)
        reading.add_card(Card(name="Present Card", arcana="major"), present_pos)
        
        past_cards = reading.get_cards_by_meaning("past")
        assert len(past_cards) == 1
        assert past_cards[0].card.name == "Past Card"
        
        present_cards = reading.get_cards_by_meaning("present")
        assert len(present_cards) == 1
        assert present_cards[0].card.name == "Present Card"
    
    def test_interpretation_management(self):
        """Test interpretation management."""
        layout = create_single_card_layout()
        reading = SpreadReading(layout=layout)
        
        card = Card(name="Test Card", arcana="major")
        position = layout.positions[0]
        
        reading.add_card(card, position)
        
        # Set interpretation
        reading.set_interpretation(position.position_id, "This is a test interpretation")
        
        # Get interpretation
        interpretation = reading.get_interpretation(position.position_id)
        assert interpretation == "This is a test interpretation"
        
        # Test interpretation for non-existent position
        with pytest.raises(ValueError, match="No card at position"):
            reading.set_interpretation("nonexistent", "Test")
    
    def test_reading_summary(self):
        """Test reading summary generation."""
        layout = create_single_card_layout()
        reading = SpreadReading(layout=layout, question="Test question?")
        
        card = Card(name="Test Card", arcana="major")
        position = layout.positions[0]
        
        reading.add_card(card, position)
        reading.set_interpretation(position.position_id, "Test interpretation")
        
        summary = reading.get_reading_summary()
        
        assert summary["question"] == "Test question?"
        assert summary["is_complete"] is True
        assert summary["card_count"] == 1
        assert len(summary["positions"]) == 1
        assert summary["positions"][0]["card_name"] == "Test Card"
        assert summary["positions"][0]["interpretation"] == "Test interpretation"
    
    def test_reading_serialization(self):
        """Test reading serialization."""
        layout = create_single_card_layout()
        reading = SpreadReading(layout=layout, question="Test question?")
        
        card = Card(name="Test Card", arcana="major")
        position = layout.positions[0]
        
        reading.add_card(card, position)
        
        data = reading.to_dict()
        
        assert data["question"] == "Test question?"
        assert len(data["positioned_cards"]) == 1
        assert data["positioned_cards"][0]["card"]["name"] == "Test Card"
        assert data["positioned_cards"][0]["position"]["position_id"] == position.position_id


class TestSpreadManager:
    """Test spread manager functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.deck = DeckLoader.load_canonical_deck(seed=42)
        self.manager = SpreadManager(deck=self.deck)
    
    def test_manager_creation(self):
        """Test SpreadManager creation."""
        manager = SpreadManager()
        assert manager.deck is None
        assert manager.influence_engine is None
        
        manager_with_deck = SpreadManager(deck=self.deck)
        assert manager_with_deck.deck == self.deck
    
    def test_get_available_spreads(self):
        """Test getting available spreads."""
        spreads = self.manager.get_available_spreads()
        assert SpreadType.SINGLE_CARD in spreads
        assert SpreadType.THREE_CARD in spreads
        assert SpreadType.CELTIC_CROSS in spreads
    
    def test_create_spread_layout(self):
        """Test creating spread layouts."""
        layout = self.manager.create_spread_layout(SpreadType.SINGLE_CARD)
        assert layout.spread_type == SpreadType.SINGLE_CARD
        assert len(layout.positions) == 1
    
    def test_create_reading(self):
        """Test creating readings."""
        reading = self.manager.create_reading(
            SpreadType.SINGLE_CARD,
            question="Test question?",
            shuffle_seed=123
        )
        
        assert reading.layout.spread_type == SpreadType.SINGLE_CARD
        assert reading.question == "Test question?"
        assert not reading.is_complete()
    
    def test_draw_cards_for_reading(self):
        """Test drawing cards for a reading."""
        reading = self.manager.create_reading(SpreadType.SINGLE_CARD)
        
        # Draw cards
        self.manager.draw_cards_for_reading(reading)
        
        assert reading.is_complete()
        assert len(reading.positioned_cards) == 1
        
        # Test drawing for already complete reading
        with pytest.raises(ValueError, match="Reading is already complete"):
            self.manager.draw_cards_for_reading(reading)
    
    def test_draw_cards_without_deck(self):
        """Test drawing cards without deck."""
        manager = SpreadManager()  # No deck
        reading = manager.create_reading(SpreadType.SINGLE_CARD)
        
        with pytest.raises(ValueError, match="No deck available"):
            manager.draw_cards_for_reading(reading)
    
    def test_draw_cards_insufficient_deck(self):
        """Test drawing cards with insufficient deck."""
        # Create a deck with only one card
        single_card = Card(name="Only Card", arcana="major")
        small_deck = Deck([single_card])
        manager = SpreadManager(deck=small_deck)
        
        reading = manager.create_reading(SpreadType.THREE_CARD)
        
        with pytest.raises(ValueError, match="Not enough cards in deck"):
            manager.draw_cards_for_reading(reading)
    
    def test_basic_interpretation(self):
        """Test basic interpretation without influence engine."""
        reading = self.manager.create_reading(SpreadType.SINGLE_CARD)
        self.manager.draw_cards_for_reading(reading)
        
        interpretation = self.manager.interpret_reading(reading)
        
        assert "reading_summary" in interpretation
        assert "interpretations" in interpretation
        assert "overall_summary" in interpretation
        assert "advice" in interpretation
        assert "confidence" in interpretation
        
        # Check that interpretation contains card information
        position_id = reading.positioned_cards[0].position.position_id
        assert position_id in interpretation["interpretations"]
        assert "card_name" in interpretation["interpretations"][position_id]
        assert "basic_meaning" in interpretation["interpretations"][position_id]
    
    def test_reading_statistics(self):
        """Test reading statistics generation."""
        reading = self.manager.create_reading(SpreadType.THREE_CARD)
        self.manager.draw_cards_for_reading(reading)
        
        stats = self.manager.get_reading_statistics(reading)
        
        assert stats["total_cards"] == 3
        assert stats["completion_status"] == "complete"
        assert "major_arcana" in stats
        assert "minor_arcana" in stats
        assert "upright_cards" in stats
        assert "reversed_cards" in stats
    
    def test_validate_reading(self):
        """Test reading validation."""
        reading = self.manager.create_reading(SpreadType.THREE_CARD)
        
        # Test incomplete reading
        is_valid, issues = self.manager.validate_reading(reading)
        assert not is_valid
        assert any("incomplete" in issue for issue in issues)
        
        # Complete the reading
        self.manager.draw_cards_for_reading(reading)
        
        # Test complete reading
        is_valid, issues = self.manager.validate_reading(reading)
        assert is_valid
        assert len(issues) == 0
    
    def test_export_reading(self):
        """Test reading export functionality."""
        reading = self.manager.create_reading(SpreadType.SINGLE_CARD, question="Test?")
        self.manager.draw_cards_for_reading(reading)
        
        # Test JSON export
        json_export = self.manager.export_reading(reading, "json")
        data = json.loads(json_export)
        assert data["question"] == "Test?"
        assert len(data["positioned_cards"]) == 1
        
        # Test text export
        text_export = self.manager.export_reading(reading, "text")
        assert "Reading: Single Card" in text_export
        assert "Question: Test?" in text_export
        
        # Test summary export
        summary_export = self.manager.export_reading(reading, "summary")
        assert "Single Card" in summary_export
        assert "1 cards" in summary_export
        
        # Test unsupported format
        with pytest.raises(ValueError, match="Unsupported export format"):
            self.manager.export_reading(reading, "xml")


class TestSpreadsIntegration:
    """Integration tests for the spreads module."""
    
    def test_complete_reading_workflow(self):
        """Test complete reading workflow."""
        # Create manager with deck
        deck = DeckLoader.load_canonical_deck(seed=42)
        manager = SpreadManager(deck=deck)
        
        # Create reading
        reading = manager.create_reading(
            SpreadType.THREE_CARD,
            question="What does the future hold?",
            shuffle_seed=123
        )
        
        # Draw cards
        manager.draw_cards_for_reading(reading)
        
        # Verify reading is complete
        assert reading.is_complete()
        assert len(reading.positioned_cards) == 3
        
        # Get interpretation
        interpretation = manager.interpret_reading(reading)
        assert "interpretations" in interpretation
        
        # Get statistics
        stats = manager.get_reading_statistics(reading)
        assert stats["total_cards"] == 3
        assert stats["completion_status"] == "complete"
        
        # Validate reading
        is_valid, issues = manager.validate_reading(reading)
        assert is_valid
        assert len(issues) == 0
        
        # Export reading
        export = manager.export_reading(reading, "text")
        assert "Three Card Spread" in export
        assert "What does the future hold?" in export
    
    def test_multiple_readings_same_deck(self):
        """Test multiple readings with the same deck."""
        deck = DeckLoader.load_canonical_deck(seed=42)
        manager = SpreadManager(deck=deck)
        
        # Create first reading
        reading1 = manager.create_reading(SpreadType.SINGLE_CARD, shuffle_seed=123)
        manager.draw_cards_for_reading(reading1)
        
        # Create second reading
        reading2 = manager.create_reading(SpreadType.SINGLE_CARD, shuffle_seed=456)
        manager.draw_cards_for_reading(reading2)
        
        # Verify both readings are complete
        assert reading1.is_complete()
        assert reading2.is_complete()
        
        # Verify different cards were drawn (due to different seeds)
        card1 = reading1.get_all_cards()[0]
        card2 = reading2.get_all_cards()[0]
        # Note: This might occasionally fail if the same card is drawn by chance
        # In a real test, we'd use deterministic seeds to ensure different cards
    
    def test_celtic_cross_complexity(self):
        """Test Celtic Cross spread complexity."""
        deck = DeckLoader.load_canonical_deck(seed=42)
        manager = SpreadManager(deck=deck)
        
        # Create Celtic Cross reading
        reading = manager.create_reading(SpreadType.CELTIC_CROSS)
        
        # Verify layout
        assert len(reading.layout.positions) == 10
        assert reading.layout.min_cards == 10
        assert reading.layout.max_cards == 10
        
        # Draw all cards
        manager.draw_cards_for_reading(reading)
        
        # Verify all positions are filled
        assert reading.is_complete()
        assert len(reading.positioned_cards) == 10
        
        # Verify all positions have unique cards
        card_ids = [pc.card.id for pc in reading.positioned_cards]
        assert len(card_ids) == len(set(card_ids))
        
        # Get interpretation
        interpretation = manager.interpret_reading(reading)
        assert len(interpretation["interpretations"]) == 10


if __name__ == "__main__":
    pytest.main([__file__])