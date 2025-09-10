"""
Readings manager for integrating GUI with core tarot modules.
"""

import logging
from typing import List, Optional, Dict, Any

# Import core modules
from core.deck.loader import DeckLoader
from core.spreads.manager import SpreadManager
from core.spreads.layout import SpreadType
from core.influence.advanced_engine import TarotInfluenceEngine

logger = logging.getLogger(__name__)


class ReadingsManager:
    """Manages tarot readings and integrates GUI with core modules."""
    
    def __init__(self):
        """Initialize the readings manager."""
        try:
            self.deck = DeckLoader.load_canonical_deck()
        except Exception as e:
            logger.error(f"Failed to load canonical deck: {e}")
            # Create a minimal deck for testing
            self.deck = None
        
        if self.deck:
            self.spread_manager = SpreadManager(self.deck)
        else:
            self.spread_manager = None
        
        self.influence_engine = TarotInfluenceEngine()
        
        # Current reading state
        self.current_reading = None
        self.current_spread_type = None
    
    def createReading(self, spread_type: str) -> bool:
        """Create a new reading with the specified spread type."""
        try:
            if not self.spread_manager:
                logger.error("Spread manager not available")
                return False
            
            # Map string to SpreadType enum
            spread_type_enum = self._getSpreadTypeEnum(spread_type)
            if not spread_type_enum:
                logger.error(f"Invalid spread type: {spread_type}")
                return False
            
            # Create reading
            self.current_reading = self.spread_manager.create_reading(spread_type_enum)
            self.current_spread_type = spread_type
            
            logger.info(f"Created {spread_type} reading")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create reading: {e}")
            return False
    
    def drawCards(self, shuffle_seed: Optional[int] = None) -> bool:
        """Draw cards for the current reading."""
        try:
            if not self.current_reading:
                logger.error("No current reading to draw cards for")
                return False
            
            if not self.spread_manager:
                logger.error("Spread manager not available")
                return False
            
            # Draw cards
            success = self.spread_manager.draw_cards_for_reading(
                self.current_reading, 
                shuffle_seed=shuffle_seed
            )
            
            if success:
                logger.info(f"Drew cards for {self.current_spread_type} reading")
                return True
            else:
                logger.error("Failed to draw cards")
                return False
                
        except Exception as e:
            logger.error(f"Error drawing cards: {e}")
            return False
    
    def getCurrentReading(self):
        """Get the current reading."""
        return self.current_reading
    
    def getCurrentSpreadType(self) -> Optional[str]:
        """Get the current spread type."""
        return self.current_spread_type
    
    def getReadingCards(self) -> List[Dict[str, Any]]:
        """Get cards from the current reading."""
        if not self.current_reading:
            return []
        
        cards_data = []
        for card_position in self.current_reading.positioned_cards:
            card_data = {
                'id': card_position.card.id,
                'name': card_position.card.name,
                'orientation': card_position.card.orientation.value,
                'position_id': card_position.position.position_id,
                'x_coordinate': card_position.position.coordinates[0],
                'y_coordinate': card_position.position.coordinates[1],
                'meaning': card_position.card.get_meaning()
            }
            cards_data.append(card_data)
        
        return cards_data
    
    def getReadingInterpretation(self) -> str:
        """Get interpretation for the current reading."""
        if not self.current_reading:
            return "No reading available"
        
        if not self.spread_manager:
            return "Spread manager not available"
        
        try:
            # Get basic interpretation
            interpretation = self.spread_manager.interpret_reading(self.current_reading)
            
            # Convert dict to string if needed
            if isinstance(interpretation, dict):
                # Extract the overall summary or create a summary
                if 'overall_summary' in interpretation:
                    return interpretation['overall_summary']
                elif 'interpretations' in interpretation:
                    # Create a summary from individual card interpretations
                    summaries = []
                    for pos_id, card_interpretation in interpretation['interpretations'].items():
                        if isinstance(card_interpretation, dict) and 'basic_meaning' in card_interpretation:
                            summaries.append(card_interpretation['basic_meaning'])
                    return " ".join(summaries) if summaries else "Interpretation generated"
                else:
                    return str(interpretation)
            else:
                return str(interpretation)
            
        except Exception as e:
            logger.error(f"Error getting interpretation: {e}")
            return f"Error generating interpretation: {e}"
    
    def clearReading(self):
        """Clear the current reading."""
        self.current_reading = None
        self.current_spread_type = None
        logger.info("Cleared current reading")
    
    def _getSpreadTypeEnum(self, spread_type: str) -> Optional[SpreadType]:
        """Convert string to SpreadType enum."""
        spread_type_map = {
            'single': SpreadType.SINGLE_CARD,
            'three': SpreadType.THREE_CARD,
            'celtic_cross': SpreadType.CELTIC_CROSS,
            'relationship': SpreadType.RELATIONSHIP,
            'year_ahead': SpreadType.YEAR_AHEAD
        }
        return spread_type_map.get(spread_type.lower())
    
    def getAvailableSpreadTypes(self) -> List[str]:
        """Get list of available spread types."""
        return ['single', 'three', 'celtic_cross', 'relationship', 'year_ahead']
    
    def getDeckStatus(self) -> Dict[str, Any]:
        """Get current deck status."""
        if not self.deck:
            return {
                'total_cards': 0,
                'remaining_cards': 0,
                'is_empty': True
            }
        
        return {
            'total_cards': self.deck.total_count,
            'remaining_cards': self.deck.count,
            'is_empty': self.deck.is_empty
        }