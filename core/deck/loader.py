"""
Deck data loader for the Deck Module.

This module provides functionality to load tarot card data from various sources
including JSON files, and create Deck instances with proper card metadata.
"""

import json
import os
from typing import List, Dict, Any, Optional
from .deck import Deck
from .card import CardMetadata, ArcanaType, Suit


class DeckLoader:
    """
    Loads tarot card data from various sources and creates Deck instances.
    
    The DeckLoader class provides methods to load card data from JSON files
    and create properly configured Deck objects.
    """
    
    @staticmethod
    def load_from_json(file_path: str) -> List[Dict[str, Any]]:
        """
        Load card data from a JSON file.
        
        Args:
            file_path: Path to the JSON file containing card data
        
        Returns:
            List of dictionaries containing card information
        
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
            ValueError: If the file doesn't contain valid card data
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Card data file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in file {file_path}: {e}")
        
        # Handle different JSON structures
        if isinstance(data, list):
            # Direct list of cards
            card_data = data
        elif isinstance(data, dict):
            # Check for common keys
            if 'cards' in data:
                card_data = data['cards']
            elif 'deck' in data:
                card_data = data['deck']
            else:
                # Assume the dict itself contains card data
                card_data = [data]
        else:
            raise ValueError(f"Invalid data structure in {file_path}. Expected list or dict.")
        
        # Validate card data
        DeckLoader._validate_card_data(card_data)
        
        return card_data
    
    @staticmethod
    def _validate_card_data(card_data: List[Dict[str, Any]]) -> None:
        """
        Validate that card data contains required fields.
        
        Args:
            card_data: List of card dictionaries to validate
        
        Raises:
            ValueError: If required fields are missing or invalid
        """
        required_fields = ['name', 'arcana']
        
        for i, card in enumerate(card_data):
            if not isinstance(card, dict):
                raise ValueError(f"Card {i} is not a dictionary")
            
            # Check required fields
            for field in required_fields:
                if field not in card:
                    raise ValueError(f"Card {i} missing required field: {field}")
            
            # Validate arcana type
            arcana = card['arcana']
            if arcana not in ['major', 'minor']:
                raise ValueError(f"Card {i} has invalid arcana type: {arcana}")
            
            # Validate minor arcana fields
            if arcana == 'minor':
                if 'suit' not in card:
                    raise ValueError(f"Minor arcana card {i} missing suit field")
                
                suit = card['suit']
                if suit not in ['wands', 'cups', 'swords', 'pentacles']:
                    raise ValueError(f"Card {i} has invalid suit: {suit}")
                
                # Check for number or rank
                if 'number' not in card and 'rank' not in card:
                    raise ValueError(f"Minor arcana card {i} missing number or rank")
                
                if 'number' in card and 'rank' in card:
                    raise ValueError(f"Minor arcana card {i} has both number and rank")
    
    @staticmethod
    def create_deck_from_json(file_path: str, seed: Optional[int] = None) -> Deck:
        """
        Create a Deck instance from a JSON file.
        
        Args:
            file_path: Path to the JSON file containing card data
            seed: Optional random seed for reproducible shuffling
        
        Returns:
            Deck instance with cards loaded from the file
        """
        card_data = DeckLoader.load_from_json(file_path)
        return Deck(card_data, seed)
    
    @staticmethod
    def create_deck_from_data(card_data: List[Dict[str, Any]], seed: Optional[int] = None) -> Deck:
        """
        Create a Deck instance from card data.
        
        Args:
            card_data: List of dictionaries containing card information
            seed: Optional random seed for reproducible shuffling
        
        Returns:
            Deck instance with cards from the provided data
        """
        DeckLoader._validate_card_data(card_data)
        return Deck(card_data, seed)
    
    @staticmethod
    def get_canonical_deck_path() -> str:
        """
        Get the path to the canonical deck data file.
        
        Returns:
            Path to the canonical deck JSON file
        """
        # Get the directory containing this module
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up to the project root and find the db directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        canonical_path = os.path.join(project_root, 'db', 'canonical_deck.json')
        
        # If not found, try relative to current working directory
        if not os.path.exists(canonical_path):
            canonical_path = os.path.join(os.getcwd(), 'db', 'canonical_deck.json')
        
        return canonical_path
    
    @staticmethod
    def load_canonical_deck(seed: Optional[int] = None) -> Deck:
        """
        Load the canonical 78-card tarot deck.
        
        Args:
            seed: Optional random seed for reproducible shuffling
        
        Returns:
            Deck instance with the canonical tarot deck
        """
        canonical_path = DeckLoader.get_canonical_deck_path()
        return DeckLoader.create_deck_from_json(canonical_path, seed)
    
    @staticmethod
    def save_deck_to_json(deck: Deck, file_path: str) -> None:
        """
        Save a deck's card data to a JSON file.
        
        Args:
            deck: Deck instance to save
            file_path: Path where to save the JSON file
        """
        # Get the original card data (before any draws)
        original_cards = deck._original_cards
        
        card_data = []
        for card in original_cards:
            card_dict = {
                'id': card.id,
                'name': card.name,
                'arcana': card.arcana.value,
                'suit': card.suit.value if card.suit else None,
                'number': card.number,
                'rank': card.rank,
                'element': card.element,
                'keywords': card.keywords,
                'upright_text': card.get_upright_meaning(),
                'reversed_text': card.get_reversed_meaning(),
                'themes': card.themes,
                'polarity_baseline': card.polarity_baseline,
                'intensity_baseline': card.intensity_baseline
            }
            card_data.append(card_dict)
        
        # Create the output structure
        output_data = {
            'deck_name': 'Canonical Tarot Deck',
            'total_cards': len(card_data),
            'description': 'Complete 78-card tarot deck with Major and Minor Arcana',
            'cards': card_data
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def get_deck_info(file_path: str) -> Dict[str, Any]:
        """
        Get information about a deck file without loading all cards.
        
        Args:
            file_path: Path to the deck JSON file
        
        Returns:
            Dictionary containing deck metadata
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Deck file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract deck information
        if isinstance(data, dict):
            # Check for different JSON structures
            if 'deck_info' in data:
                deck_info = data['deck_info']
                deck_name = deck_info.get('name', 'Unknown Deck')
                description = deck_info.get('description', '')
            else:
                deck_name = data.get('deck_name', 'Unknown Deck')
                description = data.get('description', '')
            
            if 'cards' in data:
                cards = data['cards']
                total_cards = len(cards)
            else:
                cards = []
                total_cards = data.get('total_cards', 0)
        else:
            deck_name = 'Unknown Deck'
            description = ''
            total_cards = len(data)
            cards = data
        
        # Count card types
        major_count = 0
        minor_count = 0
        suit_counts = {'wands': 0, 'cups': 0, 'swords': 0, 'pentacles': 0}
        
        for card in cards:
            if card.get('arcana') == 'major':
                major_count += 1
            elif card.get('arcana') == 'minor':
                minor_count += 1
                suit = card.get('suit')
                if suit in suit_counts:
                    suit_counts[suit] += 1
        
        return {
            'file_path': file_path,
            'deck_name': deck_name,
            'description': description,
            'total_cards': total_cards,
            'major_arcana': major_count,
            'minor_arcana': minor_count,
            'suit_counts': suit_counts,
            'is_complete': total_cards == 78
        }