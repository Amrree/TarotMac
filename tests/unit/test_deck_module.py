"""
Unit tests for the Deck Module.

This module tests the Card, Deck, and DeckLoader classes to ensure
proper functionality, data integrity, and error handling.
"""

import pytest
import sys
import os
import json
import tempfile
from typing import List, Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.deck import (
    Card, CardMetadata, ArcanaType, Suit, Orientation,
    Deck, DrawResult, DeckLoader
)


class TestCard:
    """Test cases for the Card class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.major_metadata = CardMetadata(
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
        
        self.minor_metadata = CardMetadata(
            name="Ace of Wands",
            arcana=ArcanaType.MINOR,
            suit=Suit.WANDS,
            number=1,
            element="fire",
            keywords=["inspiration", "new opportunities", "creativity"],
            upright_text="The Ace of Wands represents new inspiration and creative opportunities.",
            reversed_text="Reversed, the Ace of Wands suggests blocked creativity.",
            themes={"inspiration": 0.9, "new_opportunities": 0.8},
            polarity_baseline=0.8,
            intensity_baseline=0.8
        )
        
        self.court_metadata = CardMetadata(
            name="Queen of Cups",
            arcana=ArcanaType.MINOR,
            suit=Suit.CUPS,
            rank="queen",
            element="water",
            keywords=["emotional maturity", "intuition", "compassion"],
            upright_text="The Queen of Cups represents emotional maturity and intuition.",
            reversed_text="Reversed, the Queen of Cups suggests emotional instability.",
            themes={"emotional_maturity": 0.9, "intuition": 0.8},
            polarity_baseline=0.7,
            intensity_baseline=0.6
        )
    
    def test_card_creation_major(self):
        """Test creating a Major Arcana card."""
        card = Card(self.major_metadata)
        
        assert card.name == "The Fool"
        assert card.arcana == ArcanaType.MAJOR
        assert card.suit is None
        assert card.number is None
        assert card.rank is None
        assert card.element == "air"
        assert card.orientation == Orientation.UPRIGHT
        assert card.id == "fool"
        assert card.is_major()
        assert not card.is_minor()
        assert not card.is_court_card()
        assert not card.is_numbered_card()
    
    def test_card_creation_minor(self):
        """Test creating a Minor Arcana card."""
        card = Card(self.minor_metadata)
        
        assert card.name == "Ace of Wands"
        assert card.arcana == ArcanaType.MINOR
        assert card.suit == Suit.WANDS
        assert card.number == 1
        assert card.rank is None
        assert card.element == "fire"
        assert card.orientation == Orientation.UPRIGHT
        assert card.id == "1_wands"
        assert not card.is_major()
        assert card.is_minor()
        assert not card.is_court_card()
        assert card.is_numbered_card()
    
    def test_card_creation_court(self):
        """Test creating a court card."""
        card = Card(self.court_metadata)
        
        assert card.name == "Queen of Cups"
        assert card.arcana == ArcanaType.MINOR
        assert card.suit == Suit.CUPS
        assert card.number is None
        assert card.rank == "queen"
        assert card.element == "water"
        assert card.orientation == Orientation.UPRIGHT
        assert card.id == "queen_cups"
        assert not card.is_major()
        assert card.is_minor()
        assert card.is_court_card()
        assert not card.is_numbered_card()
    
    def test_card_orientation(self):
        """Test card orientation functionality."""
        card = Card(self.major_metadata)
        
        # Test initial orientation
        assert card.orientation == Orientation.UPRIGHT
        assert card.get_meaning() == card.get_upright_meaning()
        
        # Test flipping
        card.flip()
        assert card.orientation == Orientation.REVERSED
        assert card.get_meaning() == card.get_reversed_meaning()
        
        # Test setting orientation
        card.set_orientation(Orientation.UPRIGHT)
        assert card.orientation == Orientation.UPRIGHT
        assert card.get_meaning() == card.get_upright_meaning()
    
    def test_card_display_name(self):
        """Test card display name generation."""
        major_card = Card(self.major_metadata)
        minor_card = Card(self.minor_metadata)
        court_card = Card(self.court_metadata)
        
        assert major_card.get_display_name() == "The Fool"
        assert minor_card.get_display_name() == "1 of Wands"
        assert court_card.get_display_name() == "Queen of Cups"
    
    def test_card_to_dict(self):
        """Test card to dictionary conversion."""
        card = Card(self.major_metadata, Orientation.REVERSED)
        card_dict = card.to_dict()
        
        assert card_dict['id'] == "fool"
        assert card_dict['name'] == "The Fool"
        assert card_dict['arcana'] == "major"
        assert card_dict['suit'] is None
        assert card_dict['orientation'] == "reversed"
        assert card_dict['current_meaning'] == card.get_reversed_meaning()
        assert 'keywords' in card_dict
        assert 'themes' in card_dict
        assert 'polarity_baseline' in card_dict
        assert 'intensity_baseline' in card_dict
    
    def test_card_equality(self):
        """Test card equality comparison."""
        card1 = Card(self.major_metadata, Orientation.UPRIGHT)
        card2 = Card(self.major_metadata, Orientation.UPRIGHT)
        card3 = Card(self.major_metadata, Orientation.REVERSED)
        card4 = Card(self.minor_metadata, Orientation.UPRIGHT)
        
        assert card1 == card2
        assert card1 != card3  # Different orientation
        assert card1 != card4  # Different metadata
        assert card1 != "not a card"  # Different type
    
    def test_card_string_representation(self):
        """Test card string representations."""
        card = Card(self.major_metadata, Orientation.REVERSED)
        
        str_repr = str(card)
        assert "The Fool" in str_repr
        assert "Reversed" in str_repr
        
        repr_str = repr(card)
        assert "Card" in repr_str
        assert "fool" in repr_str
        assert "reversed" in repr_str


class TestDeck:
    """Test cases for the Deck class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.test_cards = [
            {
                'id': 'fool',
                'name': 'The Fool',
                'arcana': 'major',
                'element': 'air',
                'keywords': ['new beginnings', 'innocence'],
                'upright_text': 'The Fool represents new beginnings.',
                'reversed_text': 'Reversed, The Fool warns of recklessness.',
                'themes': {'new_beginnings': 0.9},
                'polarity_baseline': 0.5,
                'intensity_baseline': 0.7
            },
            {
                'id': 'magician',
                'name': 'The Magician',
                'arcana': 'major',
                'element': 'air',
                'keywords': ['manifestation', 'willpower'],
                'upright_text': 'The Magician represents manifestation.',
                'reversed_text': 'Reversed, The Magician suggests manipulation.',
                'themes': {'manifestation': 0.9},
                'polarity_baseline': 0.8,
                'intensity_baseline': 0.9
            },
            {
                'id': 'ace_wands',
                'name': 'Ace of Wands',
                'arcana': 'minor',
                'suit': 'wands',
                'number': 1,
                'element': 'fire',
                'keywords': ['inspiration', 'new opportunities'],
                'upright_text': 'The Ace of Wands represents new inspiration.',
                'reversed_text': 'Reversed, the Ace of Wands suggests blocked creativity.',
                'themes': {'inspiration': 0.9},
                'polarity_baseline': 0.8,
                'intensity_baseline': 0.8
            },
            {
                'id': 'two_wands',
                'name': 'Two of Wands',
                'arcana': 'minor',
                'suit': 'wands',
                'number': 2,
                'element': 'fire',
                'keywords': ['planning', 'future planning'],
                'upright_text': 'The Two of Wands represents planning for the future.',
                'reversed_text': 'Reversed, the Two of Wands suggests poor planning.',
                'themes': {'planning': 0.8},
                'polarity_baseline': 0.6,
                'intensity_baseline': 0.7
            }
        ]
    
    def test_deck_creation(self):
        """Test deck creation from card data."""
        deck = Deck(self.test_cards)
        
        assert deck.count == 4
        assert deck.total_count == 4
        assert not deck.is_empty
        assert deck.is_complete == False  # Not 78 cards
        assert len(deck) == 4
    
    def test_deck_shuffling(self):
        """Test deck shuffling functionality."""
        deck = Deck(self.test_cards, seed=42)
        
        # Get initial order
        initial_order = [card.id for card in deck._cards]
        
        # Shuffle and check order changed
        deck.shuffle()
        shuffled_order = [card.id for card in deck._cards]
        
        # With seed, should be deterministic
        assert initial_order != shuffled_order
        
        # Test multiple shuffles
        deck.shuffle()
        deck.shuffle()
        assert len(deck._cards) == 4  # Still has all cards
    
    def test_deck_draw_single(self):
        """Test drawing a single card."""
        deck = Deck(self.test_cards)
        
        # Draw one card
        card = deck.draw_card()
        
        assert card is not None
        assert card.id in [c['id'] for c in self.test_cards]
        assert deck.count == 3
        assert len(deck) == 3
        
        # Draw from empty deck
        deck = Deck([])
        card = deck.draw_card()
        assert card is None
    
    def test_deck_draw_with_orientation(self):
        """Test drawing cards with specific orientation."""
        deck = Deck(self.test_cards)
        
        # Draw with reversed orientation
        card = deck.draw_card(Orientation.REVERSED)
        
        assert card is not None
        assert card.orientation == Orientation.REVERSED
        assert card.get_meaning() == card.get_reversed_meaning()
    
    def test_deck_draw_multiple(self):
        """Test drawing multiple cards."""
        deck = Deck(self.test_cards)
        
        # Draw multiple cards
        result = deck.draw_cards(2)
        
        assert isinstance(result, DrawResult)
        assert len(result.cards) == 2
        assert result.drawn_count == 2
        assert result.remaining_count == 2
        assert deck.count == 2
        
        # Draw more than available
        result = deck.draw_cards(5)
        assert len(result.cards) == 2  # Only 2 remaining
        assert result.drawn_count == 2
        assert result.remaining_count == 0
        assert deck.is_empty
    
    def test_deck_peek(self):
        """Test peeking at cards without drawing."""
        deck = Deck(self.test_cards)
        
        # Peek at first card
        card = deck.peek_card(0)
        assert card is not None
        assert deck.count == 4  # Count unchanged
        
        # Peek at multiple cards
        cards = deck.peek_cards(2)
        assert len(cards) == 2
        assert deck.count == 4  # Count unchanged
        
        # Peek at invalid index
        card = deck.peek_card(10)
        assert card is None
    
    def test_deck_reset(self):
        """Test deck reset functionality."""
        deck = Deck(self.test_cards)
        
        # Draw some cards
        deck.draw_cards(2)
        assert deck.count == 2
        
        # Reset deck
        deck.reset()
        assert deck.count == 4
        assert deck.total_count == 4
    
    def test_deck_card_management(self):
        """Test adding and removing cards."""
        deck = Deck(self.test_cards)
        
        # Create a new card
        new_metadata = CardMetadata(
            name="Test Card",
            arcana=ArcanaType.MAJOR,
            keywords=["test"],
            upright_text="Test upright meaning.",
            reversed_text="Test reversed meaning."
        )
        new_card = Card(new_metadata)
        
        # Add card
        deck.add_card(new_card)
        assert deck.count == 5
        
        # Remove card by ID
        removed_card = deck.remove_card("test_card")
        assert removed_card is not None
        assert removed_card.id == "test_card"
        assert deck.count == 4
        
        # Remove non-existent card
        removed_card = deck.remove_card("nonexistent")
        assert removed_card is None
    
    def test_deck_find_card(self):
        """Test finding cards in the deck."""
        deck = Deck(self.test_cards)
        
        # Find existing card
        card = deck.find_card("fool")
        assert card is not None
        assert card.id == "fool"
        
        # Find non-existent card
        card = deck.find_card("nonexistent")
        assert card is None
    
    def test_deck_filtering(self):
        """Test filtering cards by various criteria."""
        deck = Deck(self.test_cards)
        
        # Filter by arcana
        major_cards = deck.get_cards_by_arcana(ArcanaType.MAJOR)
        assert len(major_cards) == 2
        assert all(card.is_major() for card in major_cards)
        
        minor_cards = deck.get_cards_by_arcana(ArcanaType.MINOR)
        assert len(minor_cards) == 2
        assert all(card.is_minor() for card in minor_cards)
        
        # Filter by suit
        wands_cards = deck.get_cards_by_suit(Suit.WANDS)
        assert len(wands_cards) == 2
        assert all(card.suit == Suit.WANDS for card in wands_cards)
        
        # Get major and minor arcana
        major_arcana = deck.get_major_arcana()
        minor_arcana = deck.get_minor_arcana()
        assert len(major_arcana) == 2
        assert len(minor_arcana) == 2
        
        # Get numbered cards
        numbered_cards = deck.get_numbered_cards()
        assert len(numbered_cards) == 2
        assert all(card.is_numbered_card() for card in numbered_cards)
    
    def test_deck_statistics(self):
        """Test deck statistics generation."""
        deck = Deck(self.test_cards)
        stats = deck.get_card_statistics()
        
        assert stats['total_cards'] == 4
        assert stats['major_arcana'] == 2
        assert stats['minor_arcana'] == 2
        assert stats['court_cards'] == 0
        assert stats['numbered_cards'] == 2
        assert stats['suit_counts']['wands'] == 2
        assert stats['suit_counts']['cups'] == 0
        assert stats['suit_counts']['swords'] == 0
        assert stats['suit_counts']['pentacles'] == 0
        assert not stats['is_complete']
        assert not stats['is_empty']
    
    def test_deck_to_dict(self):
        """Test deck to dictionary conversion."""
        deck = Deck(self.test_cards)
        deck_dict = deck.to_dict()
        
        assert deck_dict['total_cards'] == 4
        assert deck_dict['remaining_cards'] == 4
        assert not deck_dict['is_complete']
        assert not deck_dict['is_empty']
        assert 'statistics' in deck_dict
        assert 'cards' in deck_dict
        assert len(deck_dict['cards']) == 4
    
    def test_deck_iteration(self):
        """Test deck iteration functionality."""
        deck = Deck(self.test_cards)
        
        card_ids = [card.id for card in deck]
        expected_ids = [c['id'] for c in self.test_cards]
        
        assert set(card_ids) == set(expected_ids)
    
    def test_deck_contains(self):
        """Test deck membership testing."""
        deck = Deck(self.test_cards)
        
        assert "fool" in deck
        assert "magician" in deck
        assert "ace_wands" in deck
        assert "nonexistent" not in deck


class TestDeckLoader:
    """Test cases for the DeckLoader class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.valid_card_data = [
            {
                'id': 'fool',
                'name': 'The Fool',
                'arcana': 'major',
                'element': 'air',
                'keywords': ['new beginnings'],
                'upright_text': 'The Fool represents new beginnings.',
                'reversed_text': 'Reversed, The Fool warns of recklessness.',
                'themes': {'new_beginnings': 0.9},
                'polarity_baseline': 0.5,
                'intensity_baseline': 0.7
            },
            {
                'id': 'ace_wands',
                'name': 'Ace of Wands',
                'arcana': 'minor',
                'suit': 'wands',
                'number': 1,
                'element': 'fire',
                'keywords': ['inspiration'],
                'upright_text': 'The Ace of Wands represents new inspiration.',
                'reversed_text': 'Reversed, the Ace of Wands suggests blocked creativity.',
                'themes': {'inspiration': 0.9},
                'polarity_baseline': 0.8,
                'intensity_baseline': 0.8
            }
        ]
    
    def test_load_from_json_list(self):
        """Test loading card data from JSON list."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.valid_card_data, f)
            temp_file = f.name
        
        try:
            loaded_data = DeckLoader.load_from_json(temp_file)
            assert len(loaded_data) == 2
            assert loaded_data[0]['name'] == 'The Fool'
            assert loaded_data[1]['name'] == 'Ace of Wands'
        finally:
            os.unlink(temp_file)
    
    def test_load_from_json_dict(self):
        """Test loading card data from JSON dict."""
        json_data = {
            'deck_name': 'Test Deck',
            'cards': self.valid_card_data
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(json_data, f)
            temp_file = f.name
        
        try:
            loaded_data = DeckLoader.load_from_json(temp_file)
            assert len(loaded_data) == 2
            assert loaded_data[0]['name'] == 'The Fool'
        finally:
            os.unlink(temp_file)
    
    def test_load_from_nonexistent_file(self):
        """Test loading from non-existent file."""
        with pytest.raises(FileNotFoundError):
            DeckLoader.load_from_json("nonexistent.json")
    
    def test_load_from_invalid_json(self):
        """Test loading from invalid JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            temp_file = f.name
        
        try:
            with pytest.raises(json.JSONDecodeError):
                DeckLoader.load_from_json(temp_file)
        finally:
            os.unlink(temp_file)
    
    def test_validate_card_data_valid(self):
        """Test validation of valid card data."""
        # Should not raise any exception
        DeckLoader._validate_card_data(self.valid_card_data)
    
    def test_validate_card_data_missing_name(self):
        """Test validation with missing name field."""
        invalid_data = [{'arcana': 'major'}]  # Missing name
        
        with pytest.raises(ValueError, match="missing required field: name"):
            DeckLoader._validate_card_data(invalid_data)
    
    def test_validate_card_data_missing_arcana(self):
        """Test validation with missing arcana field."""
        invalid_data = [{'name': 'Test Card'}]  # Missing arcana
        
        with pytest.raises(ValueError, match="missing required field: arcana"):
            DeckLoader._validate_card_data(invalid_data)
    
    def test_validate_card_data_invalid_arcana(self):
        """Test validation with invalid arcana value."""
        invalid_data = [{'name': 'Test Card', 'arcana': 'invalid'}]
        
        with pytest.raises(ValueError, match="invalid arcana type"):
            DeckLoader._validate_card_data(invalid_data)
    
    def test_validate_card_data_minor_missing_suit(self):
        """Test validation of minor arcana missing suit."""
        invalid_data = [{'name': 'Test Card', 'arcana': 'minor'}]
        
        with pytest.raises(ValueError, match="missing suit field"):
            DeckLoader._validate_card_data(invalid_data)
    
    def test_validate_card_data_minor_invalid_suit(self):
        """Test validation of minor arcana with invalid suit."""
        invalid_data = [{'name': 'Test Card', 'arcana': 'minor', 'suit': 'invalid'}]
        
        with pytest.raises(ValueError, match="invalid suit"):
            DeckLoader._validate_card_data(invalid_data)
    
    def test_validate_card_data_minor_missing_number_rank(self):
        """Test validation of minor arcana missing number or rank."""
        invalid_data = [{'name': 'Test Card', 'arcana': 'minor', 'suit': 'wands'}]
        
        with pytest.raises(ValueError, match="missing number or rank"):
            DeckLoader._validate_card_data(invalid_data)
    
    def test_create_deck_from_json(self):
        """Test creating deck from JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.valid_card_data, f)
            temp_file = f.name
        
        try:
            deck = DeckLoader.create_deck_from_json(temp_file, seed=42)
            assert isinstance(deck, Deck)
            assert deck.count == 2
            assert deck.total_count == 2
        finally:
            os.unlink(temp_file)
    
    def test_create_deck_from_data(self):
        """Test creating deck from card data."""
        deck = DeckLoader.create_deck_from_data(self.valid_card_data, seed=42)
        
        assert isinstance(deck, Deck)
        assert deck.count == 2
        assert deck.total_count == 2
    
    def test_save_deck_to_json(self):
        """Test saving deck to JSON file."""
        deck = Deck(self.valid_card_data)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            DeckLoader.save_deck_to_json(deck, temp_file)
            
            # Verify the saved file
            with open(temp_file, 'r') as f:
                saved_data = json.load(f)
            
            assert 'deck_name' in saved_data
            assert 'total_cards' in saved_data
            assert 'cards' in saved_data
            assert len(saved_data['cards']) == 2
        finally:
            os.unlink(temp_file)
    
    def test_get_deck_info(self):
        """Test getting deck information."""
        json_data = {
            'deck_name': 'Test Deck',
            'description': 'A test deck',
            'total_cards': 2,
            'cards': self.valid_card_data
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(json_data, f)
            temp_file = f.name
        
        try:
            info = DeckLoader.get_deck_info(temp_file)
            
            assert info['file_path'] == temp_file
            assert info['deck_name'] == 'Test Deck'
            assert info['description'] == 'A test deck'
            assert info['total_cards'] == 2
            assert info['major_arcana'] == 1
            assert info['minor_arcana'] == 1
            assert info['suit_counts']['wands'] == 1
            assert not info['is_complete']
        finally:
            os.unlink(temp_file)
    
    def test_get_canonical_deck_path(self):
        """Test getting canonical deck path."""
        path = DeckLoader.get_canonical_deck_path()
        assert path.endswith('canonical_deck.json')
        assert os.path.exists(path)  # Should exist from previous work
    
    def test_load_canonical_deck(self):
        """Test loading the canonical deck."""
        deck = DeckLoader.load_canonical_deck(seed=42)
        
        assert isinstance(deck, Deck)
        assert deck.count == 78  # Full tarot deck
        assert deck.total_count == 78
        assert deck.is_complete
        
        # Check it has the expected structure
        stats = deck.get_card_statistics()
        assert stats['major_arcana'] == 22
        assert stats['minor_arcana'] == 56
        assert stats['court_cards'] == 16  # 4 suits × 4 court cards
        assert stats['numbered_cards'] == 40  # 4 suits × 10 numbered cards