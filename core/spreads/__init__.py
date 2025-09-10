"""
Spreads Module for TarotMac

This module provides spread layout definitions, drawing logic, and interpretation
framework for tarot card spreads. It integrates with the deck module for card
drawing and the influence engine for card interpretation.

Classes:
    SpreadLayout: Defines the structure and positions of a tarot spread
    SpreadPosition: Represents a single position in a spread
    SpreadReading: Manages a complete spread reading with cards and interpretations
    SpreadManager: Handles spread operations and integration with other modules

Enums:
    SpreadType: Enumeration of supported spread types
    PositionMeaning: Enumeration of position meanings
"""

from .layout import SpreadLayout, SpreadPosition, SpreadType, PositionMeaning
from .reading import SpreadReading
from .manager import SpreadManager

__all__ = [
    'SpreadLayout',
    'SpreadPosition', 
    'SpreadReading',
    'SpreadManager',
    'SpreadType',
    'PositionMeaning'
]