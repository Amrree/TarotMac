"""
Advanced Tarot Influence Engine - Deterministic system for computing card influences.

This module implements a comprehensive influence engine that applies established
tarot combination methods through algorithmic rules, producing structured,
explainable interpretations with traceable influence factors.
"""

import json
import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ConfidenceLevel(Enum):
    """Confidence levels for influence factors."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class CardMetadata:
    """Metadata for a tarot card."""
    card_id: str
    name: str
    arcana: str  # "major" or "minor"
    suit: Optional[str] = None  # "wands", "cups", "swords", "pentacles"
    number: Optional[int] = None
    rank: Optional[str] = None  # "page", "knight", "queen", "king"
    element: str = "fire"  # "fire", "water", "air", "earth"
    baseline_polarity: float = 0.0  # -1.0 to +1.0
    baseline_intensity: float = 0.5  # 0.0 to 1.0
    keywords: List[str] = field(default_factory=list)
    base_upright_text: str = ""
    base_reversed_text: str = ""
    themes: Dict[str, float] = field(default_factory=dict)


@dataclass
class CardPosition:
    """A card positioned within a spread."""
    position_id: str
    card_id: str
    orientation: str  # "upright" or "reversed"
    x_coordinate: float = 0.0
    y_coordinate: float = 0.0


@dataclass
class InfluenceFactor:
    """Represents how one card influences another."""
    source_position: str
    source_card_id: str
    effect: float
    explain: str
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM


@dataclass
class InfluencedCard:
    """A card with computed influences applied."""
    position: str
    card_id: str
    card_name: str
    orientation: str
    base_text: str
    influenced_text: str
    polarity_score: float
    intensity_score: float
    themes: Dict[str, float]
    influence_factors: List[InfluenceFactor]
    journal_prompt: str


@dataclass
class InfluenceResult:
    """Complete result of influence computation."""
    reading_id: str
    summary: str
    cards: List[InfluencedCard]
    advice: List[str]
    follow_up_questions: List[str]


class TarotInfluenceEngine:
    """Deterministic engine for computing tarot card influences."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the influence engine with configuration."""
        self.config = config or self._get_default_config()
        self.card_database: Dict[str, CardMetadata] = {}
        self.spread_definitions: Dict[str, Dict[str, Any]] = {}
        
        # Load default configurations
        self._load_spread_definitions()
        
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for the engine."""
        return {
            "major_dominance": {
                "enabled": True,
                "multiplier": 1.5,
                "override_threshold": 0.7
            },
            "adjacency_weighting": {
                "enabled": True,
                "distance_decay": 0.8,
                "max_distance": 4.0
            },
            "elemental_dignities": {
                "enabled": True,
                "same_element_boost": 0.2,
                "complementary_boost": 0.1,
                "opposing_reduction": 0.15
            },
            "numerical_sequences": {
                "enabled": True,
                "ascending_boost": 0.15,
                "descending_boost": 0.15,
                "same_number_boost": 0.2
            },
            "suit_predominance": {
                "enabled": True,
                "three_card_boost": 0.25,
                "four_card_boost": 0.35,
                "opposing_reduction": 0.15
            },
            "reversal_propagation": {
                "enabled": True,
                "stability_reduction": 0.3,
                "major_multiplier": 1.5
            }
        }
    
    def _load_spread_definitions(self):
        """Load spread definitions from configuration."""
        # Load from engine_spec.json if available
        try:
            with open('/workspace/engine_spec.json', 'r') as f:
                spec = json.load(f)
                self.spread_definitions = spec.get('spread_definitions', {})
        except FileNotFoundError:
            # Use default spread definitions
            self.spread_definitions = {
                "single": {
                    "positions": [{"id": "center", "x": 0.0, "y": 0.0}]
                },
                "three_card": {
                    "positions": [
                        {"id": "past", "x": 0.0, "y": 0.0},
                        {"id": "present", "x": 1.0, "y": 0.0},
                        {"id": "future", "x": 2.0, "y": 0.0}
                    ]
                }
            }
    
    def load_card_database(self, card_data: List[Dict[str, Any]]):
        """Load card database from provided data."""
        for card_info in card_data:
            card = CardMetadata(
                card_id=card_info['id'],
                name=card_info['name'],
                arcana=card_info['arcana'],
                suit=card_info.get('suit'),
                number=card_info.get('number'),
                rank=card_info.get('rank'),
                element=card_info.get('element', 'fire'),
                baseline_polarity=card_info.get('polarity_baseline', 0.0),
                baseline_intensity=card_info.get('intensity_baseline', 0.5),
                keywords=card_info.get('keywords', []),
                base_upright_text=card_info.get('upright_text', ''),
                base_reversed_text=card_info.get('reversed_text', ''),
                themes=card_info.get('themes', {})
            )
            self.card_database[card.card_id] = card
    
    def compute_influences(self, reading_input: Dict[str, Any]) -> InfluenceResult:
        """
        Compute influences for a complete reading.
        
        Args:
            reading_input: Input reading data with positions and context
            
        Returns:
            Complete influence result with all computed influences
        """
        reading_id = reading_input['reading_id']
        spread_type = reading_input['spread_type']
        positions = reading_input['positions']
        user_context = reading_input.get('user_context', '')
        
        # Validate input
        self._validate_input(reading_input)
        
        # Get card metadata for all positions
        card_positions = []
        for pos in positions:
            if pos['card_id'] not in self.card_database:
                raise ValueError(f"Card {pos['card_id']} not found in database")
            
            card_meta = self.card_database[pos['card_id']]
            card_positions.append({
                'position': pos,
                'metadata': card_meta
            })
        
        # Compute influences for each card
        influenced_cards = []
        for card_data in card_positions:
            influenced_card = self._compute_card_influences(
                card_data, card_positions, reading_id
            )
            influenced_cards.append(influenced_card)
        
        # Generate summary and advice
        summary = self._generate_summary(influenced_cards, user_context)
        advice = self._generate_advice(influenced_cards)
        follow_up_questions = self._generate_follow_up_questions(influenced_cards)
        
        return InfluenceResult(
            reading_id=reading_id,
            summary=summary,
            cards=influenced_cards,
            advice=advice,
            follow_up_questions=follow_up_questions
        )
    
    def _validate_input(self, reading_input: Dict[str, Any]):
        """Validate input reading data."""
        required_fields = ['reading_id', 'spread_type', 'positions']
        for field in required_fields:
            if field not in reading_input:
                raise ValueError(f"Missing required field: {field}")
        
        if not reading_input['positions']:
            raise ValueError("No positions provided")
        
        for pos in reading_input['positions']:
            required_pos_fields = ['position_id', 'card_id', 'orientation']
            for field in required_pos_fields:
                if field not in pos:
                    raise ValueError(f"Missing required position field: {field}")
    
    def _compute_card_influences(self, card_data: Dict[str, Any], 
                               all_cards: List[Dict[str, Any]], 
                               reading_id: str) -> InfluencedCard:
        """Compute influences for a single card."""
        position = card_data['position']
        metadata = card_data['metadata']
        
        # Initialize influence tracking
        influence_factors = []
        polarity_effects = []
        intensity_effects = []
        theme_effects = {}
        
        # Apply each rule in order
        if self.config['major_dominance']['enabled']:
            self._apply_major_dominance(card_data, all_cards, influence_factors)
        
        if self.config['adjacency_weighting']['enabled']:
            self._apply_adjacency_weighting(card_data, all_cards, influence_factors)
        
        if self.config['elemental_dignities']['enabled']:
            self._apply_elemental_dignities(card_data, all_cards, influence_factors)
        
        if self.config['numerical_sequences']['enabled']:
            self._apply_numerical_sequences(card_data, all_cards, influence_factors)
        
        if self.config['suit_predominance']['enabled']:
            self._apply_suit_predominance(card_data, all_cards, influence_factors)
        
        if self.config['reversal_propagation']['enabled']:
            self._apply_reversal_propagation(card_data, all_cards, influence_factors)
        
        # Calculate final scores
        final_polarity = self._calculate_final_polarity(metadata, influence_factors)
        final_intensity = self._calculate_final_intensity(metadata, influence_factors)
        final_themes = self._calculate_final_themes(metadata, influence_factors)
        
        # Generate influenced text
        influenced_text = self._generate_influenced_text(metadata, influence_factors)
        
        # Generate journal prompt
        journal_prompt = self._generate_journal_prompt(metadata, influence_factors)
        
        return InfluencedCard(
            position=position['position_id'],
            card_id=metadata.card_id,
            card_name=metadata.name,
            orientation=position['orientation'],
            base_text=self._get_base_text(metadata, position['orientation']),
            influenced_text=influenced_text,
            polarity_score=final_polarity,
            intensity_score=final_intensity,
            themes=final_themes,
            influence_factors=influence_factors,
            journal_prompt=journal_prompt
        )
    
    def _apply_major_dominance(self, card_data: Dict[str, Any], 
                              all_cards: List[Dict[str, Any]], 
                              influence_factors: List[InfluenceFactor]):
        """Apply Major Arcana dominance rules."""
        position = card_data['position']
        metadata = card_data['metadata']
        
        if metadata.arcana != "major":
            return
        
        config = self.config['major_dominance']
        multiplier = config['multiplier']
        
        for other_card in all_cards:
            if other_card['position']['position_id'] == position['position_id']:
                continue
            
            other_meta = other_card['metadata']
            distance = self._calculate_distance(position, other_card['position'])
            
            if distance <= config.get('max_distance', 4.0):
                effect = multiplier * other_meta.baseline_polarity * 0.1
                
                influence_factors.append(InfluenceFactor(
                    source_position=other_card['position']['position_id'],
                    source_card_id=other_meta.card_id,
                    effect=effect,
                    explain=f"{metadata.name} (Major Arcana) exerts dominant influence on {other_meta.name}",
                    confidence=ConfidenceLevel.HIGH
                ))
    
    def _apply_adjacency_weighting(self, card_data: Dict[str, Any], 
                                 all_cards: List[Dict[str, Any]], 
                                 influence_factors: List[InfluenceFactor]):
        """Apply adjacency weighting rules."""
        position = card_data['position']
        metadata = card_data['metadata']
        
        for other_card in all_cards:
            if other_card['position']['position_id'] == position['position_id']:
                continue
            
            other_meta = other_card['metadata']
            distance = self._calculate_distance(position, other_card['position'])
            
            if distance <= self.config['adjacency_weighting']['max_distance']:
                weight = self._calculate_adjacency_weight(distance)
                effect = weight * other_meta.baseline_polarity
                
                influence_factors.append(InfluenceFactor(
                    source_position=other_card['position']['position_id'],
                    source_card_id=other_meta.card_id,
                    effect=effect,
                    explain=f"{other_meta.name} influences {metadata.name} through adjacency (distance: {distance:.2f})",
                    confidence=ConfidenceLevel.HIGH if weight > 0.7 else ConfidenceLevel.MEDIUM
                ))
    
    def _apply_elemental_dignities(self, card_data: Dict[str, Any], 
                                 all_cards: List[Dict[str, Any]], 
                                 influence_factors: List[InfluenceFactor]):
        """Apply elemental dignity rules."""
        position = card_data['position']
        metadata = card_data['metadata']
        
        for other_card in all_cards:
            if other_card['position']['position_id'] == position['position_id']:
                continue
            
            other_meta = other_card['metadata']
            
            if metadata.element == other_meta.element:
                # Same element reinforcement
                effect = self.config['elemental_dignities']['same_element_boost']
                influence_factors.append(InfluenceFactor(
                    source_position=other_card['position']['position_id'],
                    source_card_id=other_meta.card_id,
                    effect=effect,
                    explain=f"{metadata.name} and {other_meta.name} share {metadata.element} element, reinforcing themes",
                    confidence=ConfidenceLevel.HIGH
                ))
            elif self._are_complementary_elements(metadata.element, other_meta.element):
                # Complementary elements
                effect = self.config['elemental_dignities']['complementary_boost']
                influence_factors.append(InfluenceFactor(
                    source_position=other_card['position']['position_id'],
                    source_card_id=other_meta.card_id,
                    effect=effect,
                    explain=f"{metadata.element} and {other_meta.element} are complementary elements",
                    confidence=ConfidenceLevel.MEDIUM
                ))
            elif self._are_opposing_elements(metadata.element, other_meta.element):
                # Opposing elements
                effect = -self.config['elemental_dignities']['opposing_reduction']
                influence_factors.append(InfluenceFactor(
                    source_position=other_card['position']['position_id'],
                    source_card_id=other_meta.card_id,
                    effect=effect,
                    explain=f"{metadata.element} and {other_meta.element} are opposing elements, creating tension",
                    confidence=ConfidenceLevel.MEDIUM
                ))
    
    def _apply_numerical_sequences(self, card_data: Dict[str, Any], 
                                all_cards: List[Dict[str, Any]], 
                                influence_factors: List[InfluenceFactor]):
        """Apply numerical sequence rules."""
        position = card_data['position']
        metadata = card_data['metadata']
        
        if metadata.number is None:
            return
        
        # Find other cards with numbers
        numbered_cards = []
        for other_card in all_cards:
            other_meta = other_card['metadata']
            if other_meta.number is not None:
                numbered_cards.append((other_meta.number, other_meta.card_id))
        
        # Check for sequences
        for other_number, other_card_id in numbered_cards:
            if other_card_id == metadata.card_id:
                continue
            
            if abs(metadata.number - other_number) == 1:
                # Adjacent numbers
                if metadata.number < other_number:
                    effect = self.config['numerical_sequences']['ascending_boost']
                    explain = f"Numerical sequence: {metadata.number} → {other_number} (ascending)"
                else:
                    effect = self.config['numerical_sequences']['descending_boost']
                    explain = f"Numerical sequence: {metadata.number} → {other_number} (descending)"
                
                influence_factors.append(InfluenceFactor(
                    source_position="sequence",
                    source_card_id=other_card_id,
                    effect=effect,
                    explain=explain,
                    confidence=ConfidenceLevel.MEDIUM
                ))
            elif metadata.number == other_number:
                # Same number
                effect = self.config['numerical_sequences']['same_number_boost']
                influence_factors.append(InfluenceFactor(
                    source_position="sequence",
                    source_card_id=other_card_id,
                    effect=effect,
                    explain=f"Same number ({metadata.number}) across different suits",
                    confidence=ConfidenceLevel.MEDIUM
                ))
    
    def _apply_suit_predominance(self, card_data: Dict[str, Any], 
                               all_cards: List[Dict[str, Any]], 
                               influence_factors: List[InfluenceFactor]):
        """Apply suit predominance rules."""
        position = card_data['position']
        metadata = card_data['metadata']
        
        if metadata.suit is None:
            return
        
        # Count cards by suit
        suit_counts = {}
        for other_card in all_cards:
            other_meta = other_card['metadata']
            if other_meta.suit:
                suit_counts[other_meta.suit] = suit_counts.get(other_meta.suit, 0) + 1
        
        # Apply suit predominance
        if suit_counts.get(metadata.suit, 0) >= 3:
            if suit_counts[metadata.suit] == 3:
                effect = self.config['suit_predominance']['three_card_boost']
            else:
                effect = self.config['suit_predominance']['four_card_boost']
            
            influence_factors.append(InfluenceFactor(
                source_position="suit_predominance",
                source_card_id="suit_group",
                effect=effect,
                explain=f"Suit predominance: {suit_counts[metadata.suit]} {metadata.suit} cards",
                confidence=ConfidenceLevel.HIGH
            ))
    
    def _apply_reversal_propagation(self, card_data: Dict[str, Any], 
                                  all_cards: List[Dict[str, Any]], 
                                  influence_factors: List[InfluenceFactor]):
        """Apply reversal propagation rules."""
        position = card_data['position']
        metadata = card_data['metadata']
        
        if position['orientation'] != 'reversed':
            return
        
        config = self.config['reversal_propagation']
        reduction = config['stability_reduction']
        
        if metadata.arcana == 'major':
            reduction *= config['major_multiplier']
        
        influence_factors.append(InfluenceFactor(
            source_position=position['position_id'],
            source_card_id=metadata.card_id,
            effect=-reduction,
            explain=f"Reversed {metadata.name} reduces stability themes in the reading",
            confidence=ConfidenceLevel.HIGH
        ))
    
    def _calculate_distance(self, pos1: Dict[str, Any], pos2: Dict[str, Any]) -> float:
        """Calculate Euclidean distance between two positions."""
        dx = pos1['x_coordinate'] - pos2['x_coordinate']
        dy = pos1['y_coordinate'] - pos2['y_coordinate']
        return math.sqrt(dx * dx + dy * dy)
    
    def _calculate_adjacency_weight(self, distance: float) -> float:
        """Calculate adjacency weight based on distance."""
        if distance <= 1.0:
            return 1.0  # Direct adjacency
        elif distance <= 1.5:
            return 0.7  # Diagonal adjacency
        elif distance <= 2.5:
            return 0.5  # Same row/column
        elif distance <= 4.0:
            return 0.3  # Nearby
        else:
            return 0.1  # Distant
    
    def _are_complementary_elements(self, elem1: str, elem2: str) -> bool:
        """Check if two elements are complementary."""
        complementary_pairs = [
            ('fire', 'earth'),
            ('earth', 'fire'),
            ('water', 'air'),
            ('air', 'water')
        ]
        return (elem1, elem2) in complementary_pairs
    
    def _are_opposing_elements(self, elem1: str, elem2: str) -> bool:
        """Check if two elements are opposing."""
        opposing_pairs = [
            ('fire', 'water'),
            ('water', 'fire'),
            ('earth', 'air'),
            ('air', 'earth')
        ]
        return (elem1, elem2) in opposing_pairs
    
    def _calculate_final_polarity(self, metadata: CardMetadata, 
                                influence_factors: List[InfluenceFactor]) -> float:
        """Calculate final polarity score."""
        base_polarity = metadata.baseline_polarity
        
        # Apply influence effects
        for factor in influence_factors:
            base_polarity += factor.effect
        
        # Clamp to valid range
        return max(-2.0, min(2.0, base_polarity))
    
    def _calculate_final_intensity(self, metadata: CardMetadata, 
                                influence_factors: List[InfluenceFactor]) -> float:
        """Calculate final intensity score."""
        base_intensity = metadata.baseline_intensity
        
        # Apply influence effects
        for factor in influence_factors:
            base_intensity += abs(factor.effect) * 0.1
        
        # Clamp to valid range
        return max(0.0, min(1.0, base_intensity))
    
    def _calculate_final_themes(self, metadata: CardMetadata, 
                             influence_factors: List[InfluenceFactor]) -> Dict[str, float]:
        """Calculate final theme weights."""
        themes = metadata.themes.copy()
        
        # Apply theme effects from influences
        for factor in influence_factors:
            if factor.effect > 0:
                # Positive influence boosts themes
                for theme in themes:
                    themes[theme] += factor.effect * 0.1
            else:
                # Negative influence reduces themes
                for theme in themes:
                    themes[theme] += factor.effect * 0.05
        
        # Clamp theme weights
        for theme in themes:
            themes[theme] = max(0.0, min(1.0, themes[theme]))
        
        return themes
    
    def _get_base_text(self, metadata: CardMetadata, orientation: str) -> str:
        """Get base text for card based on orientation."""
        if orientation == 'reversed':
            return metadata.base_reversed_text
        else:
            return metadata.base_upright_text
    
    def _generate_influenced_text(self, metadata: CardMetadata, 
                                influence_factors: List[InfluenceFactor]) -> str:
        """Generate influenced text from base text and influence factors."""
        base_text = metadata.base_upright_text if metadata.baseline_polarity >= 0 else metadata.base_reversed_text
        
        if not influence_factors:
            return base_text
        
        # Generate influence description
        influences = []
        for factor in influence_factors:
            if abs(factor.effect) > 0.1:
                if factor.effect > 0:
                    influences.append(f"enhanced by {factor.source_card_id}")
                else:
                    influences.append(f"tempered by {factor.source_card_id}")
        
        if influences:
            return f"{base_text} This meaning is {', '.join(influences)}."
        else:
            return base_text
    
    def _generate_journal_prompt(self, metadata: CardMetadata, 
                               influence_factors: List[InfluenceFactor]) -> str:
        """Generate journal prompt based on card and influences."""
        base_prompts = {
            'major': f"Reflect on the deeper meaning of {metadata.name} in your current situation.",
            'minor': f"Consider how {metadata.name} relates to your daily experiences."
        }
        
        base_prompt = base_prompts.get(metadata.arcana, f"Explore the significance of {metadata.name}.")
        
        if influence_factors:
            influence_text = "Pay attention to how other cards in your reading modify this card's meaning."
            return f"{base_prompt} {influence_text}"
        else:
            return base_prompt
    
    def _generate_summary(self, cards: List[InfluencedCard], 
                         user_context: str) -> str:
        """Generate overall reading summary."""
        if len(cards) == 1:
            return f"This reading centers on {cards[0].card_name}, suggesting {cards[0].influenced_text[:100]}..."
        else:
            card_names = [card.card_name for card in cards]
            return f"This reading involves {', '.join(card_names)}, creating a complex narrative of influences and interactions."
    
    def _generate_advice(self, cards: List[InfluencedCard]) -> List[str]:
        """Generate practical advice based on the reading."""
        advice = []
        
        for card in cards:
            if card.polarity_score > 0.5:
                advice.append(f"Embrace the positive energy of {card.card_name}")
            elif card.polarity_score < -0.5:
                advice.append(f"Address the challenges indicated by {card.card_name}")
            else:
                advice.append(f"Consider the balanced message of {card.card_name}")
        
        return advice[:3]  # Limit to 3 pieces of advice
    
    def _generate_follow_up_questions(self, cards: List[InfluencedCard]) -> List[str]:
        """Generate follow-up questions based on the reading."""
        questions = []
        
        for card in cards:
            questions.append(f"What does {card.card_name} mean to you in your current situation?")
            questions.append(f"How do you feel about the message of {card.card_name}?")
        
        return questions[:3]  # Limit to 3 questions