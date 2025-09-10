"""
Unit tests for the advanced tarot influence engine.

This module tests each rule class individually with known inputs and expected outputs,
ensuring deterministic behavior and proper influence calculations.
"""

import pytest
import sys
import os
from typing import Dict, List, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.influence.advanced_engine import (
    TarotInfluenceEngine, CardMetadata, CardPosition, InfluenceFactor,
    InfluencedCard, InfluenceResult, ConfidenceLevel
)


class TestTarotInfluenceEngine:
    """Test cases for the Tarot Influence Engine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = TarotInfluenceEngine()
        
        # Create test card database
        self.test_cards = [
            {
                'id': 'fool',
                'name': 'The Fool',
                'arcana': 'major',
                'element': 'air',
                'polarity_baseline': 0.5,
                'intensity_baseline': 0.7,
                'keywords': ['new beginnings', 'innocence', 'spontaneity'],
                'upright_text': 'The Fool represents new beginnings and innocence.',
                'reversed_text': 'Reversed, The Fool warns of recklessness.',
                'themes': {'new_beginnings': 0.9, 'innocence': 0.8}
            },
            {
                'id': 'magician',
                'name': 'The Magician',
                'arcana': 'major',
                'element': 'air',
                'polarity_baseline': 0.8,
                'intensity_baseline': 0.9,
                'keywords': ['manifestation', 'willpower', 'skill'],
                'upright_text': 'The Magician represents manifestation through willpower.',
                'reversed_text': 'Reversed, The Magician suggests manipulation.',
                'themes': {'manifestation': 0.9, 'willpower': 0.8}
            },
            {
                'id': 'sun',
                'name': 'The Sun',
                'arcana': 'major',
                'element': 'fire',
                'polarity_baseline': 0.9,
                'intensity_baseline': 0.8,
                'keywords': ['joy', 'success', 'vitality'],
                'upright_text': 'The Sun represents joy, success, and vitality.',
                'reversed_text': 'Reversed, The Sun suggests temporary setbacks.',
                'themes': {'joy': 0.9, 'success': 0.8}
            },
            {
                'id': 'ace_wands',
                'name': 'Ace of Wands',
                'arcana': 'minor',
                'suit': 'wands',
                'number': 1,
                'element': 'fire',
                'polarity_baseline': 0.8,
                'intensity_baseline': 0.8,
                'keywords': ['inspiration', 'new opportunities', 'creativity'],
                'upright_text': 'The Ace of Wands represents new inspiration and creative opportunities.',
                'reversed_text': 'Reversed, the Ace of Wands suggests blocked creativity.',
                'themes': {'inspiration': 0.9, 'new_opportunities': 0.8}
            },
            {
                'id': 'two_wands',
                'name': 'Two of Wands',
                'arcana': 'minor',
                'suit': 'wands',
                'number': 2,
                'element': 'fire',
                'polarity_baseline': 0.6,
                'intensity_baseline': 0.7,
                'keywords': ['planning', 'future planning', 'personal power'],
                'upright_text': 'The Two of Wands represents planning for the future.',
                'reversed_text': 'Reversed, the Two of Wands suggests poor planning.',
                'themes': {'planning': 0.8, 'future_planning': 0.7}
            },
            {
                'id': 'ace_cups',
                'name': 'Ace of Cups',
                'arcana': 'minor',
                'suit': 'cups',
                'number': 1,
                'element': 'water',
                'polarity_baseline': 0.8,
                'intensity_baseline': 0.7,
                'keywords': ['new love', 'spiritual awakening', 'intuition'],
                'upright_text': 'The Ace of Cups represents new love and spiritual awakening.',
                'reversed_text': 'Reversed, the Ace of Cups suggests blocked emotions.',
                'themes': {'new_love': 0.9, 'spiritual_awakening': 0.8}
            }
        ]
        
        self.engine.load_card_database(self.test_cards)
    
    def test_major_dominance_rule(self):
        """Test Major Arcana dominance rule."""
        reading_input = {
            'reading_id': 'test_001',
            'spread_type': 'three_card',
            'positions': [
                {
                    'position_id': 'past',
                    'card_id': 'fool',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'present',
                    'card_id': 'ace_wands',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                }
            ]
        }
        
        result = self.engine.compute_influences(reading_input)
        
        # Check that Major Arcana (Fool) influences Minor Arcana (Ace of Wands)
        ace_wands_card = next(c for c in result.cards if c.card_id == 'ace_wands')
        
        # Should have influence factors from Major Arcana
        major_influences = [f for f in ace_wands_card.influence_factors 
                          if f.source_card_id == 'fool']
        
        assert len(major_influences) > 0, "Major Arcana should influence Minor Arcana"
        assert major_influences[0].confidence == ConfidenceLevel.HIGH, "Major dominance should be high confidence"
    
    def test_adjacency_weighting_rule(self):
        """Test adjacency weighting rule."""
        reading_input = {
            'reading_id': 'test_002',
            'spread_type': 'three_card',
            'positions': [
                {
                    'position_id': 'past',
                    'card_id': 'ace_wands',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'present',
                    'card_id': 'two_wands',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                }
            ]
        }
        
        result = self.engine.compute_influences(reading_input)
        
        # Check adjacency influence
        two_wands_card = next(c for c in result.cards if c.card_id == 'two_wands')
        
        adjacency_influences = [f for f in two_wands_card.influence_factors 
                              if 'adjacency' in f.explain.lower()]
        
        assert len(adjacency_influences) > 0, "Adjacent cards should influence each other"
        assert adjacency_influences[0].confidence in [ConfidenceLevel.HIGH, ConfidenceLevel.MEDIUM], "Adjacency should have reasonable confidence"
    
    def test_elemental_dignities_rule(self):
        """Test elemental dignities rule."""
        reading_input = {
            'reading_id': 'test_003',
            'spread_type': 'three_card',
            'positions': [
                {
                    'position_id': 'past',
                    'card_id': 'ace_wands',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'present',
                    'card_id': 'sun',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                }
            ]
        }
        
        result = self.engine.compute_influences(reading_input)
        
        # Both cards are Fire element - should reinforce
        sun_card = next(c for c in result.cards if c.card_id == 'sun')
        
        elemental_influences = [f for f in sun_card.influence_factors 
                              if 'fire' in f.explain.lower() and 'reinforcing' in f.explain.lower()]
        
        assert len(elemental_influences) > 0, "Same element cards should reinforce each other"
        assert elemental_influences[0].effect > 0, "Same element reinforcement should be positive"
    
    def test_numerical_sequence_rule(self):
        """Test numerical sequence rule."""
        reading_input = {
            'reading_id': 'test_004',
            'spread_type': 'three_card',
            'positions': [
                {
                    'position_id': 'past',
                    'card_id': 'ace_wands',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'present',
                    'card_id': 'two_wands',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                }
            ]
        }
        
        result = self.engine.compute_influences(reading_input)
        
        # Check numerical sequence (1 -> 2)
        two_wands_card = next(c for c in result.cards if c.card_id == 'two_wands')
        
        sequence_influences = [f for f in two_wands_card.influence_factors 
                             if 'sequence' in f.explain.lower()]
        
        assert len(sequence_influences) > 0, "Numerical sequences should be detected"
        assert sequence_influences[0].effect > 0, "Ascending sequence should be positive"
    
    def test_suit_predominance_rule(self):
        """Test suit predominance rule."""
        reading_input = {
            'reading_id': 'test_005',
            'spread_type': 'three_card',
            'positions': [
                {
                    'position_id': 'past',
                    'card_id': 'ace_wands',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'present',
                    'card_id': 'two_wands',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                }
            ]
        }
        
        result = self.engine.compute_influences(reading_input)
        
        # Both cards are Wands - should trigger suit predominance
        ace_wands_card = next(c for c in result.cards if c.card_id == 'ace_wands')
        
        suit_influences = [f for f in ace_wands_card.influence_factors 
                          if 'suit' in f.explain.lower()]
        
        assert len(suit_influences) > 0, "Suit predominance should be detected"
        assert suit_influences[0].effect > 0, "Suit predominance should be positive"
    
    def test_reversal_propagation_rule(self):
        """Test reversal propagation rule."""
        reading_input = {
            'reading_id': 'test_006',
            'spread_type': 'three_card',
            'positions': [
                {
                    'position_id': 'past',
                    'card_id': 'fool',
                    'orientation': 'reversed',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'present',
                    'card_id': 'ace_wands',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                }
            ]
        }
        
        result = self.engine.compute_influences(reading_input)
        
        # Check reversal propagation
        fool_card = next(c for c in result.cards if c.card_id == 'fool')
        
        reversal_influences = [f for f in fool_card.influence_factors 
                              if 'reversed' in f.explain.lower()]
        
        assert len(reversal_influences) > 0, "Reversed cards should have reversal effects"
        assert reversal_influences[0].effect < 0, "Reversal should reduce stability"
    
    def test_deterministic_behavior(self):
        """Test that the engine produces deterministic results."""
        reading_input = {
            'reading_id': 'test_007',
            'spread_type': 'three_card',
            'positions': [
                {
                    'position_id': 'past',
                    'card_id': 'fool',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'present',
                    'card_id': 'magician',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'future',
                    'card_id': 'sun',
                    'orientation': 'upright',
                    'x_coordinate': 2.0,
                    'y_coordinate': 0.0
                }
            ]
        }
        
        # Run the same input multiple times
        result1 = self.engine.compute_influences(reading_input)
        result2 = self.engine.compute_influences(reading_input)
        
        # Results should be identical
        assert result1.reading_id == result2.reading_id
        assert len(result1.cards) == len(result2.cards)
        
        for card1, card2 in zip(result1.cards, result2.cards):
            assert card1.polarity_score == card2.polarity_score
            assert card1.intensity_score == card2.intensity_score
            assert len(card1.influence_factors) == len(card2.influence_factors)
    
    def test_polarity_score_bounds(self):
        """Test that polarity scores are within valid bounds."""
        reading_input = {
            'reading_id': 'test_008',
            'spread_type': 'three_card',
            'positions': [
                {
                    'position_id': 'past',
                    'card_id': 'fool',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'present',
                    'card_id': 'magician',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'future',
                    'card_id': 'sun',
                    'orientation': 'upright',
                    'x_coordinate': 2.0,
                    'y_coordinate': 0.0
                }
            ]
        }
        
        result = self.engine.compute_influences(reading_input)
        
        for card in result.cards:
            assert -2.0 <= card.polarity_score <= 2.0, f"Polarity score {card.polarity_score} out of bounds"
            assert 0.0 <= card.intensity_score <= 1.0, f"Intensity score {card.intensity_score} out of bounds"
    
    def test_theme_weights_bounds(self):
        """Test that theme weights are within valid bounds."""
        reading_input = {
            'reading_id': 'test_009',
            'spread_type': 'three_card',
            'positions': [
                {
                    'position_id': 'past',
                    'card_id': 'fool',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'present',
                    'card_id': 'magician',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                }
            ]
        }
        
        result = self.engine.compute_influences(reading_input)
        
        for card in result.cards:
            for theme, weight in card.themes.items():
                assert 0.0 <= weight <= 1.0, f"Theme weight {weight} out of bounds for {theme}"
    
    def test_influence_factor_traceability(self):
        """Test that influence factors are traceable and explainable."""
        reading_input = {
            'reading_id': 'test_010',
            'spread_type': 'three_card',
            'positions': [
                {
                    'position_id': 'past',
                    'card_id': 'fool',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'present',
                    'card_id': 'magician',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                }
            ]
        }
        
        result = self.engine.compute_influences(reading_input)
        
        for card in result.cards:
            for factor in card.influence_factors:
                assert factor.source_position is not None, "Source position must be specified"
                assert factor.source_card_id is not None, "Source card ID must be specified"
                assert factor.explain is not None, "Explanation must be provided"
                assert len(factor.explain) > 0, "Explanation must not be empty"
                assert factor.confidence in [ConfidenceLevel.HIGH, ConfidenceLevel.MEDIUM, ConfidenceLevel.LOW], "Confidence must be valid"
    
    def test_single_card_reading(self):
        """Test single card reading with no influences."""
        reading_input = {
            'reading_id': 'test_011',
            'spread_type': 'single',
            'positions': [
                {
                    'position_id': 'center',
                    'card_id': 'fool',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                }
            ]
        }
        
        result = self.engine.compute_influences(reading_input)
        
        assert len(result.cards) == 1
        assert len(result.cards[0].influence_factors) == 0, "Single card should have no influence factors"
        assert result.cards[0].polarity_score == 0.5, "Single card should have baseline polarity"
        assert result.cards[0].intensity_score == 0.7, "Single card should have baseline intensity"
    
    def test_opposing_elements(self):
        """Test opposing elements rule."""
        reading_input = {
            'reading_id': 'test_012',
            'spread_type': 'three_card',
            'positions': [
                {
                    'position_id': 'past',
                    'card_id': 'ace_wands',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'present',
                    'card_id': 'ace_cups',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                }
            ]
        }
        
        result = self.engine.compute_influences(reading_input)
        
        # Fire (Wands) vs Water (Cups) - should create tension
        ace_cups_card = next(c for c in result.cards if c.card_id == 'ace_cups')
        
        opposing_influences = [f for f in ace_cups_card.influence_factors 
                             if 'opposing' in f.explain.lower() or 'tension' in f.explain.lower()]
        
        assert len(opposing_influences) > 0, "Opposing elements should create tension"
        assert opposing_influences[0].effect < 0, "Opposing elements should have negative effect"
    
    def test_complementary_elements(self):
        """Test complementary elements rule."""
        # Create a test with complementary elements (Fire + Earth)
        # Note: We need to add an Earth element card for this test
        earth_card = {
            'id': 'ace_pentacles',
            'name': 'Ace of Pentacles',
            'arcana': 'minor',
            'suit': 'pentacles',
            'number': 1,
            'element': 'earth',
            'polarity_baseline': 0.7,
            'intensity_baseline': 0.6,
            'keywords': ['new opportunities', 'prosperity', 'manifestation'],
            'upright_text': 'The Ace of Pentacles represents new opportunities and prosperity.',
            'reversed_text': 'Reversed, the Ace of Pentacles suggests missed opportunities.',
            'themes': {'new_opportunities': 0.9, 'prosperity': 0.8}
        }
        
        self.engine.load_card_database([earth_card])
        
        reading_input = {
            'reading_id': 'test_013',
            'spread_type': 'three_card',
            'positions': [
                {
                    'position_id': 'past',
                    'card_id': 'ace_wands',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'present',
                    'card_id': 'ace_pentacles',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                }
            ]
        }
        
        result = self.engine.compute_influences(reading_input)
        
        # Fire (Wands) + Earth (Pentacles) - should be complementary
        ace_pentacles_card = next(c for c in result.cards if c.card_id == 'ace_pentacles')
        
        complementary_influences = [f for f in ace_pentacles_card.influence_factors 
                                  if 'complementary' in f.explain.lower()]
        
        assert len(complementary_influences) > 0, "Complementary elements should be detected"
        assert complementary_influences[0].effect > 0, "Complementary elements should have positive effect"
    
    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Test missing required fields
        with pytest.raises(ValueError):
            self.engine.compute_influences({'reading_id': 'test'})
        
        # Test invalid card ID
        with pytest.raises(ValueError):
            self.engine.compute_influences({
                'reading_id': 'test',
                'spread_type': 'single',
                'positions': [{'position_id': 'center', 'card_id': 'invalid_card', 'orientation': 'upright'}]
            })
        
        # Test empty positions
        with pytest.raises(ValueError):
            self.engine.compute_influences({
                'reading_id': 'test',
                'spread_type': 'single',
                'positions': []
            })
    
    def test_configuration_override(self):
        """Test that configuration can be overridden."""
        # Create engine with custom configuration
        custom_config = {
            'major_dominance': {
                'enabled': True,
                'multiplier': 2.0,  # Higher than default
                'override_threshold': 0.5
            },
            'adjacency_weighting': {
                'enabled': True,
                'distance_decay': 0.7,
                'max_distance': 3.0
            }
        }
        
        custom_engine = TarotInfluenceEngine(custom_config)
        custom_engine.load_card_database(self.test_cards)
        
        reading_input = {
            'reading_id': 'test_014',
            'spread_type': 'three_card',
            'positions': [
                {
                    'position_id': 'past',
                    'card_id': 'fool',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'present',
                    'card_id': 'ace_wands',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                }
            ]
        }
        
        result = custom_engine.compute_influences(reading_input)
        
        # Check that custom configuration is applied
        ace_wands_card = next(c for c in result.cards if c.card_id == 'ace_wands')
        
        major_influences = [f for f in ace_wands_card.influence_factors 
                          if f.source_card_id == 'fool']
        
        assert len(major_influences) > 0, "Major dominance should still work with custom config"
        # The effect should be stronger due to higher multiplier
        assert major_influences[0].effect > 0, "Major dominance effect should be positive"