"""
Card Influence Engine - Rule-based system for computing card interactions.
"""

from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import math


@dataclass
class InfluenceVector:
    """Represents the influence a card has on others."""
    polarity: float  # -2 to +2
    intensity: float  # 0 to 1
    themes: Dict[str, float]  # Theme weights


@dataclass
class CardPosition:
    """Represents a card in a specific position within a spread."""
    card_id: str
    card_name: str
    orientation: str  # 'upright' or 'reversed'
    position_name: str
    x: float
    y: float
    base_polarity: float
    base_intensity: float
    base_themes: Dict[str, float]


@dataclass
class InfluenceFactor:
    """Represents how one card influences another."""
    source_card_id: str
    effect: float
    explain: str


@dataclass
class InfluencedCard:
    """A card with computed influences applied."""
    card_id: str
    card_name: str
    orientation: str
    position_name: str
    base_text: str
    influenced_text: str  # To be filled by AI
    polarity_score: float
    intensity_score: float
    influence_factors: List[InfluenceFactor]
    journal_prompt: str  # To be filled by AI


class CardInfluenceEngine:
    """Rule-based engine for computing card influences in spreads."""
    
    def __init__(self):
        self.adjacency_weights = {
            'direct': 1.0,      # Directly adjacent
            'diagonal': 0.7,    # Diagonally adjacent
            'same_row': 0.5,    # Same row/column
            'distant': 0.2      # Far away
        }
        
        self.major_arcana_multiplier = 1.5
        self.same_suit_amplification = 0.2
        self.reversal_penalty = 0.3
    
    def compute_influences(self, card_positions: List[CardPosition]) -> List[InfluencedCard]:
        """
        Compute influences for all cards in a spread.
        
        Args:
            card_positions: List of cards with their positions and metadata
            
        Returns:
            List of influenced cards with computed effects
        """
        influenced_cards = []
        
        for card in card_positions:
            influence_factors = []
            total_polarity_effect = 0.0
            total_intensity_effect = 0.0
            theme_effects = {}
            
            # Compute influences from all other cards
            for other_card in card_positions:
                if other_card.card_id == card.card_id:
                    continue
                    
                influence_factor = self._compute_card_influence(card, other_card)
                if influence_factor:
                    influence_factors.append(influence_factor)
                    total_polarity_effect += influence_factor.effect
                    
                    # Apply theme effects
                    for theme, weight in other_card.base_themes.items():
                        if theme not in theme_effects:
                            theme_effects[theme] = 0.0
                        theme_effects[theme] += weight * abs(influence_factor.effect)
            
            # Apply reversal effects
            if card.orientation == 'reversed':
                total_polarity_effect *= -1
                total_intensity_effect *= (1 - self.reversal_penalty)
            
            # Compute final scores
            final_polarity = self._clamp_polarity(card.base_polarity + total_polarity_effect)
            final_intensity = self._clamp_intensity(card.base_intensity + total_intensity_effect)
            
            # Create influenced card
            influenced_card = InfluencedCard(
                card_id=card.card_id,
                card_name=card.card_name,
                orientation=card.orientation,
                position_name=card.position_name,
                base_text="",  # Will be filled from card database
                influenced_text="",  # Will be filled by AI
                polarity_score=final_polarity,
                intensity_score=final_intensity,
                influence_factors=influence_factors,
                journal_prompt=""  # Will be filled by AI
            )
            
            influenced_cards.append(influenced_card)
        
        return influenced_cards
    
    def _compute_card_influence(self, target_card: CardPosition, source_card: CardPosition) -> InfluenceFactor:
        """Compute how one card influences another."""
        
        # Calculate distance and adjacency
        distance = self._calculate_distance(target_card, source_card)
        adjacency_type = self._get_adjacency_type(distance)
        base_weight = self.adjacency_weights.get(adjacency_type, 0.1)
        
        # Apply major arcana multiplier
        if self._is_major_arcana(source_card.card_id):
            base_weight *= self.major_arcana_multiplier
        
        # Apply same suit amplification
        if self._is_same_suit(target_card.card_id, source_card.card_id):
            base_weight *= (1 + self.same_suit_amplification)
        
        # Apply numeric progression bonus
        numeric_bonus = self._get_numeric_progression_bonus(target_card.card_id, source_card.card_id)
        base_weight *= (1 + numeric_bonus)
        
        # Calculate polarity effect
        polarity_effect = source_card.base_polarity * base_weight
        
        # Apply reversal effects
        if source_card.orientation == 'reversed':
            polarity_effect *= -0.5  # Reversed cards have reduced, inverted influence
        
        # Generate explanation
        explain = self._generate_influence_explanation(
            source_card, target_card, polarity_effect, adjacency_type
        )
        
        return InfluenceFactor(
            source_card_id=source_card.card_id,
            effect=polarity_effect,
            explain=explain
        )
    
    def _calculate_distance(self, card1: CardPosition, card2: CardPosition) -> float:
        """Calculate Euclidean distance between two cards."""
        dx = card1.x - card2.x
        dy = card1.y - card2.y
        return math.sqrt(dx * dx + dy * dy)
    
    def _get_adjacency_type(self, distance: float) -> str:
        """Determine adjacency type based on distance."""
        if distance <= 1.5:
            return 'direct'
        elif distance <= 2.5:
            return 'diagonal'
        elif distance <= 4.0:
            return 'same_row'
        else:
            return 'distant'
    
    def _is_major_arcana(self, card_id: str) -> bool:
        """Check if a card is from the Major Arcana."""
        major_arcana_ids = {
            'fool', 'magician', 'high_priestess', 'empress', 'emperor',
            'hierophant', 'lovers', 'chariot', 'strength', 'hermit',
            'wheel_fortune', 'justice', 'hanged_man', 'death', 'temperance',
            'devil', 'tower', 'star', 'moon', 'sun', 'judgement', 'world'
        }
        return card_id in major_arcana_ids
    
    def _is_same_suit(self, card1_id: str, card2_id: str) -> bool:
        """Check if two cards are from the same suit."""
        suits = ['wands', 'cups', 'swords', 'pentacles']
        suit1 = None
        suit2 = None
        
        for suit in suits:
            if suit in card1_id:
                suit1 = suit
            if suit in card2_id:
                suit2 = suit
        
        return suit1 is not None and suit1 == suit2
    
    def _get_numeric_progression_bonus(self, card1_id: str, card2_id: str) -> float:
        """Calculate bonus for numeric progressions (e.g., 1-2-3)."""
        # Extract numbers from card IDs
        numbers1 = self._extract_numbers(card1_id)
        numbers2 = self._extract_numbers(card2_id)
        
        if not numbers1 or not numbers2:
            return 0.0
        
        # Check for sequential progression
        if abs(numbers1[0] - numbers2[0]) == 1:
            return 0.1
        
        # Check for same number (different suits)
        if numbers1[0] == numbers2[0]:
            return 0.05
        
        return 0.0
    
    def _extract_numbers(self, card_id: str) -> List[int]:
        """Extract numeric values from card ID."""
        numbers = []
        
        # Major arcana numbers
        major_numbers = {
            'fool': 0, 'magician': 1, 'high_priestess': 2, 'empress': 3,
            'emperor': 4, 'hierophant': 5, 'lovers': 6, 'chariot': 7,
            'strength': 8, 'hermit': 9, 'wheel_fortune': 10, 'justice': 11,
            'hanged_man': 12, 'death': 13, 'temperance': 14, 'devil': 15,
            'tower': 16, 'star': 17, 'moon': 18, 'sun': 19,
            'judgement': 20, 'world': 21
        }
        
        if card_id in major_numbers:
            numbers.append(major_numbers[card_id])
        else:
            # Minor arcana - extract number from name
            import re
            match = re.search(r'(\d+)', card_id)
            if match:
                numbers.append(int(match.group(1)))
        
        return numbers
    
    def _generate_influence_explanation(self, source_card: CardPosition, target_card: CardPosition, 
                                      effect: float, adjacency_type: str) -> str:
        """Generate human-readable explanation of influence."""
        
        effect_strength = "strongly" if abs(effect) > 0.3 else "moderately" if abs(effect) > 0.1 else "slightly"
        effect_direction = "enhances" if effect > 0 else "diminishes" if effect < 0 else "balances"
        
        adjacency_desc = {
            'direct': "directly adjacent to",
            'diagonal': "diagonally near",
            'same_row': "in the same area as",
            'distant': "distant from"
        }.get(adjacency_type, "related to")
        
        return f"{source_card.card_name} ({effect_strength} {effect_direction} {target_card.card_name} being {adjacency_desc})"
    
    def _clamp_polarity(self, value: float) -> float:
        """Clamp polarity value to valid range."""
        return max(-2.0, min(2.0, value))
    
    def _clamp_intensity(self, value: float) -> float:
        """Clamp intensity value to valid range."""
        return max(0.0, min(1.0, value))


# Specific influence rules for major arcana
class MajorArcanaRules:
    """Special rules for Major Arcana card influences."""
    
    @staticmethod
    def get_special_influence(card_id: str) -> Dict[str, float]:
        """Get special influence effects for major arcana cards."""
        
        special_effects = {
            'sun': {'illumination': 0.4, 'positivity': 0.3},
            'moon': {'illusion': 0.3, 'intuition': 0.2},
            'star': {'hope': 0.4, 'guidance': 0.3},
            'tower': {'disruption': 0.5, 'breakthrough': 0.3},
            'death': {'transformation': 0.4, 'endings': 0.3},
            'empress': {'fertility': 0.4, 'creativity': 0.3},
            'emperor': {'structure': 0.4, 'authority': 0.3},
            'magician': {'manifestation': 0.4, 'willpower': 0.3},
            'high_priestess': {'intuition': 0.4, 'mystery': 0.3},
            'fool': {'new_beginnings': 0.4, 'spontaneity': 0.3}
        }
        
        return special_effects.get(card_id, {})
    
    @staticmethod
    def get_element_interactions() -> Dict[Tuple[str, str], float]:
        """Get element interaction multipliers."""
        return {
            ('fire', 'water'): 0.5,    # Fire and water oppose
            ('water', 'fire'): 0.5,
            ('earth', 'air'): 0.5,     # Earth and air oppose
            ('air', 'earth'): 0.5,
            ('fire', 'earth'): 1.2,    # Fire and earth complement
            ('earth', 'fire'): 1.2,
            ('water', 'air'): 1.2,    # Water and air complement
            ('air', 'water'): 1.2,
            ('fire', 'fire'): 1.3,    # Same elements amplify
            ('water', 'water'): 1.3,
            ('earth', 'earth'): 1.3,
            ('air', 'air'): 1.3
        }