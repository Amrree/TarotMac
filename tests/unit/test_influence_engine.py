"""
Unit tests for the card influence engine.
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.influence.engine import (
    CardInfluenceEngine, CardPosition, InfluenceFactor, InfluencedCard
)


class TestCardInfluenceEngine:
    """Test cases for the card influence engine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = CardInfluenceEngine()
        
        # Create test card positions
        self.fool = CardPosition(
            card_id="fool",
            card_name="The Fool",
            orientation="upright",
            position_name="center",
            x=0.0, y=0.0,
            base_polarity=0.5,
            base_intensity=0.7,
            base_themes={"new_beginnings": 0.9, "innocence": 0.8}
        )
        
        self.magician = CardPosition(
            card_id="magician",
            card_name="The Magician",
            orientation="upright",
            position_name="left",
            x=-1.0, y=0.0,
            base_polarity=0.8,
            base_intensity=0.9,
            base_themes={"manifestation": 0.9, "willpower": 0.8}
        )
        
        self.sun = CardPosition(
            card_id="sun",
            card_name="The Sun",
            orientation="upright",
            position_name="right",
            x=1.0, y=0.0,
            base_polarity=0.9,
            base_intensity=0.8,
            base_themes={"joy": 0.9, "success": 0.8}
        )
    
    def test_adjacency_calculation(self):
        """Test adjacency type calculation."""
        # Direct adjacency
        distance = 1.0
        assert self.engine._get_adjacency_type(distance) == "direct"
        
        # Diagonal adjacency
        distance = 2.0
        assert self.engine._get_adjacency_type(distance) == "diagonal"
        
        # Same row
        distance = 3.0
        assert self.engine._get_adjacency_type(distance) == "same_row"
        
        # Distant
        distance = 5.0
        assert self.engine._get_adjacency_type(distance) == "distant"
    
    def test_major_arcana_detection(self):
        """Test major arcana detection."""
        assert self.engine._is_major_arcana("fool") == True
        assert self.engine._is_major_arcana("magician") == True
        assert self.engine._is_major_arcana("ace_wands") == False
        assert self.engine._is_major_arcana("king_cups") == False
    
    def test_same_suit_detection(self):
        """Test same suit detection."""
        assert self.engine._is_same_suit("ace_wands", "two_wands") == True
        assert self.engine._is_same_suit("ace_wands", "ace_cups") == False
        assert self.engine._is_same_suit("king_wands", "page_wands") == True
        assert self.engine._is_same_suit("fool", "magician") == False  # Major arcana
    
    def test_numeric_progression_bonus(self):
        """Test numeric progression bonus calculation."""
        # Sequential progression
        bonus = self.engine._get_numeric_progression_bonus("ace_wands", "two_wands")
        assert bonus == 0.1
        
        # Same number
        bonus = self.engine._get_numeric_progression_bonus("ace_wands", "ace_cups")
        assert bonus == 0.05
        
        # No progression
        bonus = self.engine._get_numeric_progression_bonus("ace_wands", "three_wands")
        assert bonus == 0.0
    
    def test_card_influence_calculation(self):
        """Test individual card influence calculation."""
        influence = self.engine._compute_card_influence(self.fool, self.magician)
        
        assert influence is not None
        assert influence.source_card_id == "magician"
        assert isinstance(influence.effect, float)
        assert isinstance(influence.explain, str)
        assert len(influence.explain) > 0
    
    def test_reversed_card_influence(self):
        """Test influence from reversed cards."""
        reversed_fool = CardPosition(
            card_id="fool",
            card_name="The Fool",
            orientation="reversed",
            position_name="center",
            x=0.0, y=0.0,
            base_polarity=0.5,
            base_intensity=0.7,
            base_themes={"new_beginnings": 0.9, "innocence": 0.8}
        )
        
        influence = self.engine._compute_card_influence(self.magician, reversed_fool)
        
        # Reversed cards should have reduced, inverted influence
        assert influence.effect < 0  # Should be negative due to inversion
    
    def test_major_arcana_multiplier(self):
        """Test major arcana influence multiplier."""
        influence = self.engine._compute_card_influence(self.fool, self.magician)
        
        # Major arcana should have stronger influence
        # This is a basic test - the exact multiplier depends on implementation
        assert abs(influence.effect) > 0
    
    def test_complete_influence_computation(self):
        """Test complete influence computation for a spread."""
        cards = [self.fool, self.magician, self.sun]
        influenced_cards = self.engine.compute_influences(cards)
        
        assert len(influenced_cards) == 3
        
        for influenced_card in influenced_cards:
            assert isinstance(influenced_card, InfluencedCard)
            assert influenced_card.card_id in ["fool", "magician", "sun"]
            assert isinstance(influenced_card.polarity_score, float)
            assert isinstance(influenced_card.intensity_score, float)
            assert isinstance(influenced_card.influence_factors, list)
            
            # Check polarity and intensity are within valid ranges
            assert -2.0 <= influenced_card.polarity_score <= 2.0
            assert 0.0 <= influenced_card.intensity_score <= 1.0
    
    def test_polarity_clamping(self):
        """Test polarity value clamping."""
        assert self.engine._clamp_polarity(3.0) == 2.0
        assert self.engine._clamp_polarity(-3.0) == -2.0
        assert self.engine._clamp_polarity(1.5) == 1.5
        assert self.engine._clamp_polarity(0.0) == 0.0
    
    def test_intensity_clamping(self):
        """Test intensity value clamping."""
        assert self.engine._clamp_intensity(1.5) == 1.0
        assert self.engine._clamp_intensity(-0.5) == 0.0
        assert self.engine._clamp_intensity(0.7) == 0.7
        assert self.engine._clamp_intensity(0.0) == 0.0
    
    def test_distance_calculation(self):
        """Test distance calculation between cards."""
        distance = self.engine._calculate_distance(self.fool, self.magician)
        assert distance == 1.0  # Distance between (0,0) and (-1,0)
        
        distance = self.engine._calculate_distance(self.fool, self.sun)
        assert distance == 1.0  # Distance between (0,0) and (1,0)
        
        # Diagonal distance
        diagonal_card = CardPosition(
            card_id="test", card_name="Test", orientation="upright",
            position_name="diagonal", x=1.0, y=1.0,
            base_polarity=0.0, base_intensity=0.0, base_themes={}
        )
        distance = self.engine._calculate_distance(self.fool, diagonal_card)
        assert abs(distance - 1.414) < 0.01  # sqrt(2)
    
    def test_influence_explanation_generation(self):
        """Test influence explanation generation."""
        influence = self.engine._compute_card_influence(self.fool, self.sun)
        
        assert isinstance(influence.explain, str)
        assert len(influence.explain) > 0
        assert "The Sun" in influence.explain
        assert "The Fool" in influence.explain
    
    def test_empty_spread(self):
        """Test influence computation with empty spread."""
        influenced_cards = self.engine.compute_influences([])
        assert len(influenced_cards) == 0
    
    def test_single_card_spread(self):
        """Test influence computation with single card."""
        cards = [self.fool]
        influenced_cards = self.engine.compute_influences(cards)
        
        assert len(influenced_cards) == 1
        assert influenced_cards[0].card_id == "fool"
        assert len(influenced_cards[0].influence_factors) == 0  # No other cards to influence