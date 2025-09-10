"""
Model Configuration Management for TarotMac AI Module

This module provides model selection, configuration management,
and integration with Ollama for different LLM models.
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ModelSize(Enum):
    """Enumeration of model sizes."""
    TINY = "tiny"      # < 1B parameters
    SMALL = "small"    # 1-3B parameters
    MEDIUM = "medium"  # 3-7B parameters
    LARGE = "large"    # 7-13B parameters
    XLARGE = "xlarge"  # 13B+ parameters


class ModelPurpose(Enum):
    """Enumeration of model purposes."""
    GENERAL = "general"
    TAROT = "tarot"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"


@dataclass
class ModelConfig:
    """Configuration for a specific model."""
    
    name: str
    display_name: str
    size: ModelSize
    purpose: ModelPurpose
    description: str
    parameters: int
    context_length: int
    recommended_temperature: float = 0.7
    recommended_top_p: float = 0.9
    max_tokens: int = 2000
    is_available: bool = False
    download_size_gb: float = 0.0
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "size": self.size.value,
            "purpose": self.purpose.value,
            "description": self.description,
            "parameters": self.parameters,
            "context_length": self.context_length,
            "recommended_temperature": self.recommended_temperature,
            "recommended_top_p": self.recommended_top_p,
            "max_tokens": self.max_tokens,
            "is_available": self.is_available,
            "download_size_gb": self.download_size_gb,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelConfig':
        """Create config from dictionary."""
        return cls(
            name=data["name"],
            display_name=data["display_name"],
            size=ModelSize(data["size"]),
            purpose=ModelPurpose(data["purpose"]),
            description=data["description"],
            parameters=data["parameters"],
            context_length=data["context_length"],
            recommended_temperature=data.get("recommended_temperature", 0.7),
            recommended_top_p=data.get("recommended_top_p", 0.9),
            max_tokens=data.get("max_tokens", 2000),
            is_available=data.get("is_available", False),
            download_size_gb=data.get("download_size_gb", 0.0),
            tags=data.get("tags", [])
        )


class ModelConfigManager:
    """Manages model configurations and selection."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the model configuration manager.
        
        Args:
            config_file: Path to configuration file (optional)
        """
        self.config_file = config_file or os.path.join(os.path.dirname(__file__), "model_configs.json")
        self.models: Dict[str, ModelConfig] = {}
        self.current_model: Optional[str] = None
        self.custom_configs: Dict[str, ModelConfig] = {}
        
        self._load_default_configs()
        self._load_config_file()
    
    def _load_default_configs(self) -> None:
        """Load default model configurations."""
        default_models = [
            ModelConfig(
                name="llama3.2:3b",
                display_name="Llama 3.2 3B",
                size=ModelSize.SMALL,
                purpose=ModelPurpose.GENERAL,
                description="Fast, efficient model good for general conversations and tarot readings",
                parameters=3000000000,
                context_length=128000,
                recommended_temperature=0.7,
                recommended_top_p=0.9,
                max_tokens=2000,
                download_size_gb=2.0,
                tags=["fast", "efficient", "general"]
            ),
            ModelConfig(
                name="llama3.2:1b",
                display_name="Llama 3.2 1B",
                size=ModelSize.TINY,
                purpose=ModelPurpose.GENERAL,
                description="Ultra-fast model for quick responses, good for simple tarot interpretations",
                parameters=1000000000,
                context_length=128000,
                recommended_temperature=0.6,
                recommended_top_p=0.8,
                max_tokens=1500,
                download_size_gb=0.7,
                tags=["ultra-fast", "lightweight", "simple"]
            ),
            ModelConfig(
                name="llama3.1:8b",
                display_name="Llama 3.1 8B",
                size=ModelSize.MEDIUM,
                purpose=ModelPurpose.GENERAL,
                description="Balanced model with good reasoning capabilities for detailed tarot readings",
                parameters=8000000000,
                context_length=128000,
                recommended_temperature=0.8,
                recommended_top_p=0.9,
                max_tokens=3000,
                download_size_gb=4.7,
                tags=["balanced", "reasoning", "detailed"]
            ),
            ModelConfig(
                name="mistral:7b",
                display_name="Mistral 7B",
                size=ModelSize.MEDIUM,
                purpose=ModelPurpose.ANALYTICAL,
                description="Analytical model excellent for complex tarot interpretations and advice",
                parameters=7000000000,
                context_length=32000,
                recommended_temperature=0.7,
                recommended_top_p=0.9,
                max_tokens=2500,
                download_size_gb=4.1,
                tags=["analytical", "complex", "advice"]
            ),
            ModelConfig(
                name="gemma2:9b",
                display_name="Gemma 2 9B",
                size=ModelSize.MEDIUM,
                purpose=ModelPurpose.CREATIVE,
                description="Creative model good for imaginative tarot interpretations and storytelling",
                parameters=9000000000,
                context_length=8192,
                recommended_temperature=0.8,
                recommended_top_p=0.95,
                max_tokens=2000,
                download_size_gb=5.4,
                tags=["creative", "imaginative", "storytelling"]
            )
        ]
        
        for model in default_models:
            self.models[model.name] = model
    
    def _load_config_file(self) -> None:
        """Load configurations from file."""
        if not os.path.exists(self.config_file):
            return
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load custom configs
            for model_data in data.get("custom_models", []):
                model = ModelConfig.from_dict(model_data)
                self.custom_configs[model.name] = model
            
            # Load current model setting
            self.current_model = data.get("current_model")
            
        except Exception as e:
            logger.error(f"Error loading model config file: {e}")
    
    def _save_config_file(self) -> None:
        """Save configurations to file."""
        try:
            data = {
                "current_model": self.current_model,
                "custom_models": [model.to_dict() for model in self.custom_configs.values()]
            }
            
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving model config file: {e}")
    
    def get_available_models(self) -> List[ModelConfig]:
        """Get list of available models."""
        return [model for model in self.models.values() if model.is_available]
    
    def get_models_by_size(self, size: ModelSize) -> List[ModelConfig]:
        """Get models filtered by size."""
        return [model for model in self.models.values() if model.size == size]
    
    def get_models_by_purpose(self, purpose: ModelPurpose) -> List[ModelConfig]:
        """Get models filtered by purpose."""
        return [model for model in self.models.values() if model.purpose == purpose]
    
    def get_recommended_models(self, purpose: Optional[ModelPurpose] = None,
                             max_size_gb: Optional[float] = None) -> List[ModelConfig]:
        """Get recommended models based on criteria."""
        models = list(self.models.values())
        
        if purpose:
            models = [m for m in models if m.purpose == purpose]
        
        if max_size_gb:
            models = [m for m in models if m.download_size_gb <= max_size_gb]
        
        # Sort by parameters (smaller first for efficiency)
        models.sort(key=lambda m: m.parameters)
        
        return models
    
    def get_model(self, name: str) -> Optional[ModelConfig]:
        """Get a specific model configuration."""
        return self.models.get(name) or self.custom_configs.get(name)
    
    def set_current_model(self, name: str) -> bool:
        """Set the current model."""
        if name in self.models or name in self.custom_configs:
            self.current_model = name
            self._save_config_file()
            return True
        return False
    
    def get_current_model(self) -> Optional[ModelConfig]:
        """Get the current model configuration."""
        if self.current_model:
            return self.get_model(self.current_model)
        return None
    
    def add_custom_model(self, config: ModelConfig) -> bool:
        """Add a custom model configuration."""
        try:
            self.custom_configs[config.name] = config
            self._save_config_file()
            return True
        except Exception as e:
            logger.error(f"Error adding custom model: {e}")
            return False
    
    def remove_custom_model(self, name: str) -> bool:
        """Remove a custom model configuration."""
        if name in self.custom_configs:
            del self.custom_configs[name]
            self._save_config_file()
            return True
        return False
    
    def update_model_availability(self, name: str, is_available: bool) -> bool:
        """Update model availability status."""
        model = self.get_model(name)
        if model:
            model.is_available = is_available
            return True
        return False
    
    def get_model_recommendations(self, use_case: str) -> List[ModelConfig]:
        """Get model recommendations for specific use cases."""
        recommendations = []
        
        if use_case == "quick_reading":
            # Fast, lightweight models
            recommendations = self.get_models_by_size(ModelSize.TINY) + self.get_models_by_size(ModelSize.SMALL)
        elif use_case == "detailed_analysis":
            # Medium to large models with good reasoning
            recommendations = self.get_models_by_size(ModelSize.MEDIUM) + self.get_models_by_size(ModelSize.LARGE)
        elif use_case == "creative_interpretation":
            # Creative models
            recommendations = self.get_models_by_purpose(ModelPurpose.CREATIVE)
        elif use_case == "analytical_advice":
            # Analytical models
            recommendations = self.get_models_by_purpose(ModelPurpose.ANALYTICAL)
        else:
            # General purpose
            recommendations = self.get_models_by_purpose(ModelPurpose.GENERAL)
        
        # Filter by availability and sort by parameters
        recommendations = [m for m in recommendations if m.is_available]
        recommendations.sort(key=lambda m: m.parameters)
        
        return recommendations
    
    def get_model_stats(self) -> Dict[str, Any]:
        """Get statistics about available models."""
        total_models = len(self.models) + len(self.custom_configs)
        available_models = sum(1 for m in self.models.values() if m.is_available)
        available_models += sum(1 for m in self.custom_configs.values() if m.is_available)
        
        size_counts = {}
        for model in self.models.values():
            size_counts[model.size.value] = size_counts.get(model.size.value, 0) + 1
        
        purpose_counts = {}
        for model in self.models.values():
            purpose_counts[model.purpose.value] = purpose_counts.get(model.purpose.value, 0) + 1
        
        return {
            "total_models": total_models,
            "available_models": available_models,
            "custom_models": len(self.custom_configs),
            "current_model": self.current_model,
            "size_distribution": size_counts,
            "purpose_distribution": purpose_counts
        }
    
    def export_config(self) -> Dict[str, Any]:
        """Export current configuration."""
        return {
            "current_model": self.current_model,
            "models": {name: model.to_dict() for name, model in self.models.items()},
            "custom_models": {name: model.to_dict() for name, model in self.custom_configs.items()}
        }
    
    def import_config(self, config_data: Dict[str, Any]) -> bool:
        """Import configuration from data."""
        try:
            # Import custom models
            for model_data in config_data.get("custom_models", {}).values():
                model = ModelConfig.from_dict(model_data)
                self.custom_configs[model.name] = model
            
            # Set current model
            if "current_model" in config_data:
                self.current_model = config_data["current_model"]
            
            self._save_config_file()
            return True
            
        except Exception as e:
            logger.error(f"Error importing config: {e}")
            return False