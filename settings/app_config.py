"""
Application configuration module.
"""

import json
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class AppConfig:
    """Mock app configuration for testing."""
    
    def __init__(self):
        """Initialize app configuration."""
        self.app_name = "Tarot"
        self.version = "1.0.0"
        self.database_path = "tarot.db"
        self.log_level = "INFO"
        self.theme = "dark"
        self.auto_save = True
        self.backup_enabled = True
        self.backup_interval = 7  # days
    
    def load(self):
        """Load configuration from storage."""
        # Mock implementation
        pass
    
    def save(self):
        """Save configuration to storage."""
        # Mock implementation
        pass
    
    def reset_to_defaults(self):
        """Reset to default configuration."""
        self.__init__()