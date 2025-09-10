"""
Settings manager for integrating GUI with settings module.
"""

import logging
from typing import Dict, Any, Optional

# Import settings module
from settings.app_config import AppConfig
from settings.user_preferences import UserPreferences

logger = logging.getLogger(__name__)


class SettingsManager:
    """Manages application settings and user preferences."""
    
    def __init__(self):
        """Initialize the settings manager."""
        self.app_config = AppConfig()
        self.user_preferences = UserPreferences()
        
        # Load settings
        self.loadSettings()
    
    def loadSettings(self):
        """Load settings from storage."""
        try:
            self.app_config.load()
            self.user_preferences.load()
            logger.info("Settings loaded successfully")
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
    
    def saveSettings(self):
        """Save settings to storage."""
        try:
            self.app_config.save()
            self.user_preferences.save()
            logger.info("Settings saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False
    
    def getAppConfig(self) -> Dict[str, Any]:
        """Get application configuration."""
        return {
            'app_name': self.app_config.app_name,
            'version': self.app_config.version,
            'database_path': self.app_config.database_path,
            'log_level': self.app_config.log_level,
            'theme': self.app_config.theme,
            'auto_save': self.app_config.auto_save,
            'backup_enabled': self.app_config.backup_enabled,
            'backup_interval': self.app_config.backup_interval
        }
    
    def getUserPreferences(self) -> Dict[str, Any]:
        """Get user preferences."""
        return {
            'default_spread': self.user_preferences.default_spread,
            'card_orientation': self.user_preferences.card_orientation,
            'interpretation_style': self.user_preferences.interpretation_style,
            'ai_model': self.user_preferences.ai_model,
            'chat_history_limit': self.user_preferences.chat_history_limit,
            'export_format': self.user_preferences.export_format,
            'encryption_enabled': self.user_preferences.encryption_enabled
        }
    
    def updateAppConfig(self, config: Dict[str, Any]):
        """Update application configuration."""
        try:
            for key, value in config.items():
                if hasattr(self.app_config, key):
                    setattr(self.app_config, key, value)
            
            logger.info("App config updated")
            return True
        except Exception as e:
            logger.error(f"Error updating app config: {e}")
            return False
    
    def updateUserPreferences(self, preferences: Dict[str, Any]):
        """Update user preferences."""
        try:
            for key, value in preferences.items():
                if hasattr(self.user_preferences, key):
                    setattr(self.user_preferences, key, value)
            
            logger.info("User preferences updated")
            return True
        except Exception as e:
            logger.error(f"Error updating user preferences: {e}")
            return False
    
    def resetToDefaults(self):
        """Reset all settings to defaults."""
        try:
            self.app_config.reset_to_defaults()
            self.user_preferences.reset_to_defaults()
            logger.info("Settings reset to defaults")
            return True
        except Exception as e:
            logger.error(f"Error resetting settings: {e}")
            return False
    
    def exportSettings(self, file_path: str) -> bool:
        """Export settings to a file."""
        try:
            settings = {
                'app_config': self.getAppConfig(),
                'user_preferences': self.getUserPreferences()
            }
            
            import json
            with open(file_path, 'w') as f:
                json.dump(settings, f, indent=2)
            
            logger.info(f"Settings exported to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting settings: {e}")
            return False
    
    def importSettings(self, file_path: str) -> bool:
        """Import settings from a file."""
        try:
            import json
            with open(file_path, 'r') as f:
                settings = json.load(f)
            
            if 'app_config' in settings:
                self.updateAppConfig(settings['app_config'])
            
            if 'user_preferences' in settings:
                self.updateUserPreferences(settings['user_preferences'])
            
            logger.info(f"Settings imported from {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error importing settings: {e}")
            return False