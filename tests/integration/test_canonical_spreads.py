"""
Integration tests for canonical tarot spreads.

This module tests the complete influence engine with canonical spreads,
ensuring proper behavior across different spread types and configurations.
"""

import pytest
import sys
import os
import json
from typing import Dict, List, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.influence.advanced_engine import TarotInfluenceEngine, InfluenceResult


class TestCanonicalSpreads:
    """Integration tests for canonical tarot spreads."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = TarotInfluenceEngine()
        
        # Load complete test card database
        self.test_cards = [
            # Major Arcana
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
                'id': 'high_priestess',
                'name': 'The High Priestess',
                'arcana': 'major',
                'element': 'water',
                'polarity_baseline': 0.3,
                'intensity_baseline': 0.6,
                'keywords': ['intuition', 'mystery', 'subconscious'],
                'upright_text': 'The High Priestess represents intuition and inner wisdom.',
                'reversed_text': 'Reversed, The High Priestess suggests ignoring intuition.',
                'themes': {'intuition': 0.9, 'mystery': 0.8}
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
                'id': 'tower',
                'name': 'The Tower',
                'arcana': 'major',
                'element': 'fire',
                'polarity_baseline': -0.5,
                'intensity_baseline': 0.9,
                'keywords': ['sudden change', 'revelation', 'disaster'],
                'upright_text': 'The Tower represents sudden change and revelation.',
                'reversed_text': 'Reversed, The Tower suggests avoiding necessary change.',
                'themes': {'transformation': 0.8, 'breakthrough': 0.7}
            },
            {
                'id': 'star',
                'name': 'The Star',
                'arcana': 'major',
                'element': 'air',
                'polarity_baseline': 0.8,
                'intensity_baseline': 0.7,
                'keywords': ['hope', 'inspiration', 'guidance'],
                'upright_text': 'The Star represents hope and inspiration.',
                'reversed_text': 'Reversed, The Star suggests hopelessness.',
                'themes': {'hope': 0.9, 'inspiration': 0.8}
            },
            {
                'id': 'world',
                'name': 'The World',
                'arcana': 'major',
                'element': 'earth',
                'polarity_baseline': 0.8,
                'intensity_baseline': 0.8,
                'keywords': ['completion', 'achievement', 'fulfillment'],
                'upright_text': 'The World represents completion and achievement.',
                'reversed_text': 'Reversed, The World suggests incompletion.',
                'themes': {'completion': 0.9, 'achievement': 0.8}
            },
            # Minor Arcana - Wands
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
                'id': 'three_wands',
                'name': 'Three of Wands',
                'arcana': 'minor',
                'suit': 'wands',
                'number': 3,
                'element': 'fire',
                'polarity_baseline': 0.7,
                'intensity_baseline': 0.7,
                'keywords': ['expansion', 'foresight', 'leadership'],
                'upright_text': 'The Three of Wands represents expansion and foresight.',
                'reversed_text': 'Reversed, the Three of Wands suggests lack of progress.',
                'themes': {'expansion': 0.8, 'foresight': 0.7}
            },
            # Minor Arcana - Cups
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
            },
            {
                'id': 'two_cups',
                'name': 'Two of Cups',
                'arcana': 'minor',
                'suit': 'cups',
                'number': 2,
                'element': 'water',
                'polarity_baseline': 0.7,
                'intensity_baseline': 0.6,
                'keywords': ['partnership', 'unity', 'love'],
                'upright_text': 'The Two of Cups represents partnership and unity.',
                'reversed_text': 'Reversed, the Two of Cups suggests disharmony.',
                'themes': {'partnership': 0.9, 'unity': 0.8}
            },
            {
                'id': 'ten_cups',
                'name': 'Ten of Cups',
                'arcana': 'minor',
                'suit': 'cups',
                'number': 10,
                'element': 'water',
                'polarity_baseline': 0.9,
                'intensity_baseline': 0.7,
                'keywords': ['divine love', 'blissful relationships', 'harmony'],
                'upright_text': 'The Ten of Cups represents divine love and blissful relationships.',
                'reversed_text': 'Reversed, the Ten of Cups suggests disharmony.',
                'themes': {'divine_love': 0.9, 'harmony': 0.8}
            },
            # Minor Arcana - Swords
            {
                'id': 'ace_swords',
                'name': 'Ace of Swords',
                'arcana': 'minor',
                'suit': 'swords',
                'number': 1,
                'element': 'air',
                'polarity_baseline': 0.6,
                'intensity_baseline': 0.8,
                'keywords': ['new ideas', 'mental clarity', 'breakthrough'],
                'upright_text': 'The Ace of Swords represents new ideas and mental clarity.',
                'reversed_text': 'Reversed, the Ace of Swords suggests confusion.',
                'themes': {'new_ideas': 0.9, 'mental_clarity': 0.8}
            },
            {
                'id': 'two_swords',
                'name': 'Two of Swords',
                'arcana': 'minor',
                'suit': 'swords',
                'number': 2,
                'element': 'air',
                'polarity_baseline': -0.1,
                'intensity_baseline': 0.6,
                'keywords': ['difficult choices', 'indecision', 'stalemate'],
                'upright_text': 'The Two of Swords represents difficult choices and indecision.',
                'reversed_text': 'Reversed, the Two of Swords suggests making decisions.',
                'themes': {'difficult_choices': 0.8, 'indecision': 0.7}
            },
            # Minor Arcana - Pentacles
            {
                'id': 'ace_pentacles',
                'name': 'Ace of Pentacles',
                'arcana': 'minor',
                'suit': 'pentacles',
                'number': 1,
                'element': 'earth',
                'polarity_baseline': 0.8,
                'intensity_baseline': 0.7,
                'keywords': ['new opportunities', 'prosperity', 'manifestation'],
                'upright_text': 'The Ace of Pentacles represents new opportunities and prosperity.',
                'reversed_text': 'Reversed, the Ace of Pentacles suggests missed opportunities.',
                'themes': {'new_opportunities': 0.9, 'prosperity': 0.8}
            },
            {
                'id': 'two_pentacles',
                'name': 'Two of Pentacles',
                'arcana': 'minor',
                'suit': 'pentacles',
                'number': 2,
                'element': 'earth',
                'polarity_baseline': 0.3,
                'intensity_baseline': 0.6,
                'keywords': ['balance', 'priorities', 'time management'],
                'upright_text': 'The Two of Pentacles represents balance and priorities.',
                'reversed_text': 'Reversed, the Two of Pentacles suggests imbalance.',
                'themes': {'balance': 0.8, 'priorities': 0.7}
            }
        ]
        
        self.engine.load_card_database(self.test_cards)
    
    def test_single_card_spread(self):
        """Test single card spread with no influences."""
        reading_input = {
            'reading_id': 'single_001',
            'spread_type': 'single',
            'positions': [
                {
                    'position_id': 'center',
                    'card_id': 'sun',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                }
            ],
            'user_context': 'What does today hold for me?'
        }
        
        result = self.engine.compute_influences(reading_input)
        
        # Validate result structure
        assert isinstance(result, InfluenceResult)
        assert result.reading_id == 'single_001'
        assert len(result.cards) == 1
        assert len(result.advice) > 0
        assert len(result.follow_up_questions) > 0
        
        # Validate single card
        card = result.cards[0]
        assert card.card_id == 'sun'
        assert card.orientation == 'upright'
        assert len(card.influence_factors) == 0  # No influences for single card
        assert card.polarity_score == 0.9  # Baseline polarity
        assert card.intensity_score == 0.8  # Baseline intensity
        
        # Validate themes
        assert 'joy' in card.themes
        assert 'success' in card.themes
        assert 0.0 <= card.themes['joy'] <= 1.0
        
        # Validate influenced text
        assert len(card.influenced_text) > 0
        assert len(card.journal_prompt) > 0
    
    def test_three_card_spread(self):
        """Test three-card spread with multiple influences."""
        reading_input = {
            'reading_id': 'three_001',
            'spread_type': 'three_card',
            'positions': [
                {
                    'position_id': 'past',
                    'card_id': 'tower',
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
                },
                {
                    'position_id': 'future',
                    'card_id': 'star',
                    'orientation': 'upright',
                    'x_coordinate': 2.0,
                    'y_coordinate': 0.0
                }
            ],
            'user_context': 'How will my career transition unfold?'
        }
        
        result = self.engine.compute_influences(reading_input)
        
        # Validate result structure
        assert len(result.cards) == 3
        assert result.summary is not None
        assert len(result.advice) > 0
        assert len(result.follow_up_questions) > 0
        
        # Validate each card
        for card in result.cards:
            assert card.card_id in ['tower', 'sun', 'star']
            assert -2.0 <= card.polarity_score <= 2.0
            assert 0.0 <= card.intensity_score <= 1.0
            assert len(card.influence_factors) > 0  # Should have influences
            assert len(card.influenced_text) > 0
            assert len(card.journal_prompt) > 0
            
            # Validate influence factors
            for factor in card.influence_factors:
                assert factor.source_position is not None
                assert factor.source_card_id is not None
                assert factor.explain is not None
                assert len(factor.explain) > 0
        
        # Check specific influences
        sun_card = next(c for c in result.cards if c.card_id == 'sun')
        tower_influences = [f for f in sun_card.influence_factors if f.source_card_id == 'tower']
        star_influences = [f for f in sun_card.influence_factors if f.source_card_id == 'star']
        
        assert len(tower_influences) > 0, "Sun should be influenced by Tower"
        assert len(star_influences) > 0, "Sun should be influenced by Star"
    
    def test_celtic_cross_spread(self):
        """Test Celtic Cross spread with complex interactions."""
        reading_input = {
            'reading_id': 'celtic_001',
            'spread_type': 'celtic_cross',
            'positions': [
                {
                    'position_id': 'center',
                    'card_id': 'magician',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'cross',
                    'card_id': 'high_priestess',
                    'orientation': 'reversed',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'past',
                    'card_id': 'ace_wands',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 1.0
                },
                {
                    'position_id': 'future',
                    'card_id': 'ten_cups',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 1.0
                },
                {
                    'position_id': 'above',
                    'card_id': 'world',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 2.0
                },
                {
                    'position_id': 'below',
                    'card_id': 'fool',
                    'orientation': 'reversed',
                    'x_coordinate': 1.0,
                    'y_coordinate': 2.0
                },
                {
                    'position_id': 'self',
                    'card_id': 'two_cups',
                    'orientation': 'upright',
                    'x_coordinate': 2.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'environment',
                    'card_id': 'ace_swords',
                    'orientation': 'upright',
                    'x_coordinate': 2.0,
                    'y_coordinate': 1.0
                },
                {
                    'position_id': 'hopes',
                    'card_id': 'star',
                    'orientation': 'upright',
                    'x_coordinate': 2.0,
                    'y_coordinate': 2.0
                },
                {
                    'position_id': 'outcome',
                    'card_id': 'ace_pentacles',
                    'orientation': 'upright',
                    'x_coordinate': 2.0,
                    'y_coordinate': 3.0
                }
            ],
            'user_context': 'What do I need to know about my current situation?'
        }
        
        result = self.engine.compute_influences(reading_input)
        
        # Validate result structure
        assert len(result.cards) == 10
        assert result.summary is not None
        assert len(result.advice) > 0
        assert len(result.follow_up_questions) > 0
        
        # Validate each card
        for card in result.cards:
            assert -2.0 <= card.polarity_score <= 2.0
            assert 0.0 <= card.intensity_score <= 1.0
            assert len(card.influenced_text) > 0
            assert len(card.journal_prompt) > 0
            
            # Validate influence factors
            for factor in card.influence_factors:
                assert factor.source_position is not None
                assert factor.source_card_id is not None
                assert factor.explain is not None
        
        # Check center card (Magician) has multiple influences
        magician_card = next(c for c in result.cards if c.card_id == 'magician')
        assert len(magician_card.influence_factors) > 0, "Center card should have influences"
        
        # Check reversed card (High Priestess) has reversal effects
        priestess_card = next(c for c in result.cards if c.card_id == 'high_priestess')
        reversal_factors = [f for f in priestess_card.influence_factors if 'reversed' in f.explain.lower()]
        assert len(reversal_factors) > 0, "Reversed card should have reversal effects"
    
    def test_relationship_spread(self):
        """Test relationship spread with emotional themes."""
        reading_input = {
            'reading_id': 'relationship_001',
            'spread_type': 'relationship',
            'positions': [
                {
                    'position_id': 'you',
                    'card_id': 'ace_cups',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'partner',
                    'card_id': 'two_cups',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'relationship',
                    'card_id': 'ten_cups',
                    'orientation': 'upright',
                    'x_coordinate': 0.5,
                    'y_coordinate': 1.0
                },
                {
                    'position_id': 'challenge',
                    'card_id': 'two_swords',
                    'orientation': 'reversed',
                    'x_coordinate': 0.0,
                    'y_coordinate': 2.0
                },
                {
                    'position_id': 'advice',
                    'card_id': 'star',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 2.0
                }
            ],
            'user_context': 'What does my relationship need right now?'
        }
        
        result = self.engine.compute_influences(reading_input)
        
        # Validate result structure
        assert len(result.cards) == 5
        assert result.summary is not None
        assert len(result.advice) > 0
        assert len(result.follow_up_questions) > 0
        
        # Check suit predominance (multiple Cups cards)
        cups_cards = [c for c in result.cards if c.card_id in ['ace_cups', 'two_cups', 'ten_cups']]
        assert len(cups_cards) == 3, "Should have 3 Cups cards"
        
        # Check that Cups cards have suit predominance effects
        for card in cups_cards:
            suit_factors = [f for f in card.influence_factors if 'suit' in f.explain.lower()]
            assert len(suit_factors) > 0, f"{card.card_id} should have suit predominance effects"
        
        # Check elemental interactions (Water vs Air)
        ace_cups_card = next(c for c in result.cards if c.card_id == 'ace_cups')
        elemental_factors = [f for f in ace_cups_card.influence_factors if 'element' in f.explain.lower()]
        assert len(elemental_factors) > 0, "Should have elemental interactions"
    
    def test_year_ahead_spread(self):
        """Test year-ahead spread with monthly progression."""
        reading_input = {
            'reading_id': 'year_001',
            'spread_type': 'year_ahead',
            'positions': [
                {
                    'position_id': 'january',
                    'card_id': 'ace_pentacles',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'february',
                    'card_id': 'two_pentacles',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'march',
                    'card_id': 'ace_wands',
                    'orientation': 'upright',
                    'x_coordinate': 2.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'april',
                    'card_id': 'two_wands',
                    'orientation': 'reversed',
                    'x_coordinate': 3.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'may',
                    'card_id': 'three_wands',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 1.0
                },
                {
                    'position_id': 'june',
                    'card_id': 'ace_cups',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 1.0
                },
                {
                    'position_id': 'july',
                    'card_id': 'two_cups',
                    'orientation': 'upright',
                    'x_coordinate': 2.0,
                    'y_coordinate': 1.0
                },
                {
                    'position_id': 'august',
                    'card_id': 'ten_cups',
                    'orientation': 'reversed',
                    'x_coordinate': 3.0,
                    'y_coordinate': 1.0
                },
                {
                    'position_id': 'september',
                    'card_id': 'ace_swords',
                    'orientation': 'upright',
                    'x_coordinate': 0.0,
                    'y_coordinate': 2.0
                },
                {
                    'position_id': 'october',
                    'card_id': 'two_swords',
                    'orientation': 'reversed',
                    'x_coordinate': 1.0,
                    'y_coordinate': 2.0
                },
                {
                    'position_id': 'november',
                    'card_id': 'star',
                    'orientation': 'upright',
                    'x_coordinate': 2.0,
                    'y_coordinate': 2.0
                },
                {
                    'position_id': 'december',
                    'card_id': 'world',
                    'orientation': 'upright',
                    'x_coordinate': 3.0,
                    'y_coordinate': 2.0
                }
            ],
            'user_context': 'What will this year bring for me?'
        }
        
        result = self.engine.compute_influences(reading_input)
        
        # Validate result structure
        assert len(result.cards) == 12
        assert result.summary is not None
        assert len(result.advice) > 0
        assert len(result.follow_up_questions) > 0
        
        # Check numerical sequences (1-2-3 in Wands)
        wands_cards = [c for c in result.cards if c.card_id in ['ace_wands', 'two_wands', 'three_wands']]
        assert len(wands_cards) == 3, "Should have 3 Wands cards"
        
        # Check that Wands cards have sequence effects
        for card in wands_cards:
            sequence_factors = [f for f in card.influence_factors if 'sequence' in f.explain.lower()]
            assert len(sequence_factors) > 0, f"{card.card_id} should have sequence effects"
        
        # Check suit predominance for each suit
        suits = ['pentacles', 'wands', 'cups', 'swords']
        for suit in suits:
            suit_cards = [c for c in result.cards if c.card_id.startswith(suit.replace('s', '')) or suit in c.card_id]
            if len(suit_cards) >= 2:
                for card in suit_cards:
                    suit_factors = [f for f in card.influence_factors if 'suit' in f.explain.lower()]
                    assert len(suit_factors) > 0, f"{card.card_id} should have suit effects"
    
    def test_mixed_major_minor_influences(self):
        """Test complex interactions between Major and Minor Arcana."""
        reading_input = {
            'reading_id': 'mixed_001',
            'spread_type': 'three_card',
            'positions': [
                {
                    'position_id': 'past',
                    'card_id': 'tower',
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
                },
                {
                    'position_id': 'future',
                    'card_id': 'sun',
                    'orientation': 'upright',
                    'x_coordinate': 2.0,
                    'y_coordinate': 0.0
                }
            ],
            'user_context': 'How will my transformation unfold?'
        }
        
        result = self.engine.compute_influences(reading_input)
        
        # Check Major Arcana dominance
        ace_wands_card = next(c for c in result.cards if c.card_id == 'ace_wands')
        major_influences = [f for f in ace_wands_card.influence_factors 
                          if f.source_card_id in ['tower', 'sun']]
        assert len(major_influences) > 0, "Minor Arcana should be influenced by Major Arcana"
        
        # Check elemental interactions (all Fire elements)
        fire_cards = [c for c in result.cards if c.card_id in ['tower', 'ace_wands', 'sun']]
        assert len(fire_cards) == 3, "Should have 3 Fire element cards"
        
        # Check that Fire cards have elemental reinforcement
        for card in fire_cards:
            elemental_factors = [f for f in card.influence_factors if 'fire' in f.explain.lower()]
            assert len(elemental_factors) > 0, f"{card.card_id} should have elemental effects"
    
    def test_reversed_cards_propagation(self):
        """Test reversal propagation effects."""
        reading_input = {
            'reading_id': 'reversed_001',
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
                    'card_id': 'magician',
                    'orientation': 'upright',
                    'x_coordinate': 1.0,
                    'y_coordinate': 0.0
                },
                {
                    'position_id': 'future',
                    'card_id': 'sun',
                    'orientation': 'reversed',
                    'x_coordinate': 2.0,
                    'y_coordinate': 0.0
                }
            ],
            'user_context': 'What challenges am I facing?'
        }
        
        result = self.engine.compute_influences(reading_input)
        
        # Check reversal effects
        reversed_cards = [c for c in result.cards if c.orientation == 'reversed']
        assert len(reversed_cards) == 2, "Should have 2 reversed cards"
        
        for card in reversed_cards:
            reversal_factors = [f for f in card.influence_factors if 'reversed' in f.explain.lower()]
            assert len(reversal_factors) > 0, f"{card.card_id} should have reversal effects"
        
        # Check that reversed cards affect neighboring cards
        magician_card = next(c for c in result.cards if c.card_id == 'magician')
        reversal_influences = [f for f in magician_card.influence_factors 
                             if f.source_card_id in ['fool', 'sun']]
        assert len(reversal_influences) > 0, "Magician should be influenced by reversed cards"
    
    def test_json_schema_validation(self):
        """Test that output conforms to JSON schema."""
        reading_input = {
            'reading_id': 'schema_001',
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
        
        # Convert to dict for JSON validation
        result_dict = {
            'reading_id': result.reading_id,
            'summary': result.summary,
            'cards': [
                {
                    'position': card.position,
                    'card_id': card.card_id,
                    'card_name': card.card_name,
                    'orientation': card.orientation,
                    'base_text': card.base_text,
                    'influenced_text': card.influenced_text,
                    'polarity_score': card.polarity_score,
                    'intensity_score': card.intensity_score,
                    'themes': card.themes,
                    'influence_factors': [
                        {
                            'source_position': factor.source_position,
                            'source_card_id': factor.source_card_id,
                            'effect': factor.effect,
                            'explain': factor.explain,
                            'confidence': factor.confidence.value
                        }
                        for factor in card.influence_factors
                    ],
                    'journal_prompt': card.journal_prompt
                }
                for card in result.cards
            ],
            'advice': result.advice,
            'follow_up_questions': result.follow_up_questions
        }
        
        # Validate JSON serialization
        json_str = json.dumps(result_dict)
        parsed_result = json.loads(json_str)
        
        assert parsed_result['reading_id'] == 'schema_001'
        assert len(parsed_result['cards']) == 3
        assert len(parsed_result['advice']) > 0
        assert len(parsed_result['follow_up_questions']) > 0
        
        # Validate each card structure
        for card in parsed_result['cards']:
            assert 'position' in card
            assert 'card_id' in card
            assert 'card_name' in card
            assert 'orientation' in card
            assert 'base_text' in card
            assert 'influenced_text' in card
            assert 'polarity_score' in card
            assert 'intensity_score' in card
            assert 'themes' in card
            assert 'influence_factors' in card
            assert 'journal_prompt' in card
            
            # Validate influence factors
            for factor in card['influence_factors']:
                assert 'source_position' in factor
                assert 'source_card_id' in factor
                assert 'effect' in factor
                assert 'explain' in factor
                assert 'confidence' in factor