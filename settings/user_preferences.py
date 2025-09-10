"""
User preferences module.
"""

import json
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class UserPreferences:
    """Mock user preferences for testing."""
    
    def __init__(self):
        """Initialize user preferences."""
        self.default_spread = "single"
        self.card_orientation = "upright"
        self.interpretation_style = "detailed"
        self.ai_model = "llama3.2"
        self.chat_history_limit = 100
        self.export_format = "json"
        self.encryption_enabled = False
    
    def load(self):
        """Load preferences from storage."""
        # Mock implementation
        pass
    
    def save(self):
        """Save preferences to storage."""
        # Mock implementation
        pass
    
    def reset_to_defaults(self):
        """Reset to default preferences."""
        self.__init__()